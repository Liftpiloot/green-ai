import tempfile

import joblib
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, UploadFile, File
import os
from google import genai
import google.genai.errors
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rum the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from ultralytics import YOLO

model = YOLO("yolo/best.pt")

@app.post("/trashcan_is_full")
async def inspect(image: UploadFile = File(...)):
    contents = await image.read()
    image = Image.open(io.BytesIO(contents))
    results = model(image)
    detections = results[0].boxes
    names = results[0].names

    found_valid = False
    only_irrelevant = True
    objects = []

    for box in detections:
        cls_id = int(box.cls)
        cls_name = names[cls_id]
        conf = float(box.conf)

        objects.append({"class": cls_name, "confidence": conf})

        if cls_name in ["Full Trashcan", "Ground Trash"] and conf >= 0.65:
            found_valid = True
            only_irrelevant = False
        elif cls_name in ["Empty Trashcan", "Plant"]:
            continue
        else:
            only_irrelevant = False  # Onbekende of andere relevante klasse

    if found_valid:
        return {
            "approved": True,
            "message": "Bedankt voor het doorsturen van het afval. Wij gaan er zo snel mogelijk mee aan de slag.",
            "objects": objects
        }
    elif only_irrelevant:
        return {
            "approved": False,
            "message": "Geen volle vuilnisbak gevonden, probeer het nogmaals.",
            "objects": objects
        }
    else:
        return {
            "approved": False,
            "message": "Afbeelding niet herkend. Probeer het opnieuw met een duidelijkere foto.",
            "objects": objects
        }

from dotenv import load_dotenv
load_dotenv()
AI_API_KEY = os.getenv("GeminiAPI")

#@app.post("/trashcan_is_full")
#async def trashcan_is_full(image: UploadFile = File(...)):
 #   if not AI_API_KEY:
  #      return {"error": "AI API key not found"}
   # client = genai.Client(api_key=AI_API_KEY)
    #contents = await image.read()

    # Write to a temporary file (Gemini needs a file path)
    #with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
     #   tmp.write(contents)
      #  tmp_path = tmp.name

    #uploaded_file = client.files.upload(file=tmp_path)

    #caption = "Check if the image contains a full trashcan. If it does, return 'yes', otherwise return 'no'. Do not add any other words. return no if the trashcan is not full. Only return yes if the trashcan is visibly full."
    #response = client.models.generate_content(
     #   model="gemini-2.0-flash", contents=[uploaded_file, caption])
    # Clean up the temporary file
    #os.remove(tmp_path)
    # return true if response contains yes
    #if "yes" in response.text.lower():
     #   return {"message": "Trashcan is full", "data": response.text}
    #elif "no" in response.text.lower():
     #   return {"message": "Trashcan is not full", "data": response.text}
    #else:
     #   return {"message": "Could not determine if the trashcan is full", "data": response.text}





@app.get("/GenerateChallenge")
async def generate_challenge(location: str = None, information: str = None):
    if not AI_API_KEY:
        return {"error": "AI API key not found"}
    content = (
        f"Genereer een korte en concrete uitdaging om de omgeving te verbeteren (maximaal 20 woorden) voor gebruikers in de buurt van {location}, waar {information}. Houd het leuk en motiverend. Voorbeelden zijn: plant een boom, plant een haag of een bloem, enzovoort. Wees heel precies, de gebruiker moet exact weten wat te doen. Noem bij een boom het type boom, bij een bloem het type bloem. Gebruik geen andere woorden dan de uitdaging zelf. De locaties zijn openbare ruimtes. Geef ook de reden aan en welke meetwaarde hierdoor verbetert."
        f"Geef het antwoord als volgt terug:\n"
        f"Titel: <titel>\n"
        f"Uitdaging: <uitdaging>"
    )
    client = genai.Client(api_key=AI_API_KEY)
    print("content: " + content)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=content)
        # send challenge to greenAi API
        return {"message": "Challenge generated successfully", "data": response.text}
    except:
        print("Error generating challenge:")
        return {"error": "Gemini failed to generate challenge, please try again later."}

@app.get("/create")
async def create_challenges(count: int=1):
    print("Creating challenges for count:", count)
    locations = get_location_and_info(count)
    print("Locations:", locations)
    challenges = []
    for i in range(count):
        if count > len(locations):
            return {"error": "Count exceeds available locations"}
        place = locations[i]
        challenge = await generate_challenge(location=place[0], information=f"Percentage bomen: {place[1]:.1f}%, struiken: {place[2]:.1f}%, gras: {place[3]:.1f}%, Mogelijke verbetering in milieugezondheidsrisico {place[4]:.1f}.")
        # TODO send challenge to greenAi API
        if "error" not in challenge:
            challenges.append([challenge, place[4]])
    return {"message": "Challenges created successfully", "data": challenges}

def get_location_and_info(count):
    locations = []
    if count > len(POSTCODES):
        print(f"Requested count {count} exceeds available postcodes {len(POSTCODES)}. Adjusting to maximum available.")
        count = len(POSTCODES)
    else:
        print(f"Using count: {count} for available postcodes.")
    for pc4 in list(POSTCODES.keys())[:count]:
        row = DF[DF['pc4'] == pc4]
        if row.empty:
            print(f"No data for pc4: {pc4}, skipping.")
            continue
        improvement = calculate_improvement(pc4)
        loc = POSTCODES[pc4]
        info = DF[DF['pc4'] == pc4].iloc[0]
        locations.append([loc, info['PercentageTrees'], info['PercentageBushes'], info['PercentageGrass'], improvement])
    return locations


DF = pd.read_csv('merged_df.csv')
SVM_MGR_MODEL = joblib.load('svm_mgr_model.joblib')

def calculate_improvement(pc4):
    print(f"Calculating improvement for pc4: {pc4}")
    row = DF[DF['pc4'] == pc4]
    if row.empty:
        print(f"No data found for pc4: {pc4}")
        return None  # or 0, or handle as needed
    print(f"Row data: {row}")
    mgr_mean = row['mgr_mean'].values[0]
    percentage_green = row['PercentageTrees'].values[0]
    percentage_bushes = row['PercentageBushes'].values[0]
    percentage_grass = row['PercentageGrass'].values[0]

    # increase the percentages by factor of 10 percent
    new_percentage_green = min(percentage_green * 1.1, 100)
    new_percentage_bushes = min(percentage_bushes * 1.1, 100)
    new_percentage_grass = min(percentage_grass * 1.1, 100)

    # calculate the new mgr_mean based on the new percentages
    input_features = row.copy()
    input_features = input_features.drop(columns=['mgr_mean', 'pc4'])
    input_features['PercentageTrees'] = new_percentage_green
    input_features['PercentageBushes'] = new_percentage_bushes
    input_features['PercentageGrass'] = new_percentage_grass
    new_mgr = SVM_MGR_MODEL.predict(input_features.values)[0]
    print(f"New MGR: {new_mgr}, Original MGR Mean: {mgr_mean}")
    improvement = mgr_mean - new_mgr  # Positive if risk decreases
    return improvement


# Gedeeltelijk Ai generated... Controleer of de buurten correct zijn.
POSTCODES = {
    5011: "Postcode 5011, Noord, Tilburg",
    5012: "Postcode 5012, Quirijnstok, Tilburg",
    5013: "Postcode 5013, Oude stad/Lovense kanaalzone, Tilburg",
    5014: "Postcode 5014, Groeseind-Hoefstraat, Tilburg",
    5015: "Postcode 5015, Industrieterrein-Oost, Tilburg",
    5016: "Postcode 5016, Tilburg",
    5017: "Postcode 5017, Oud-Zuid/Centrum, Tilburg",
    5018: "Postcode 5018, Jeruzalem, Tilburg",
    5019: "Postcode 5019, Tilburg",
    5020: "Postcode 5020, Tilburg",
    5021: "Postcode 5021, Oerle, Tilburg",
    5022: "Postcode 5022, Groenewoud, Tilburg",
    5023: "Postcode 5023, Tilburg",
    5024: "Postcode 5024, Tilburg",
    5025: "Postcode 5025, Korvel, Tilburg",
    5026: "Postcode 5026, De Katsbogten, Tilburg",
    5027: "Postcode 5027, Tilburg",
    5028: "Postcode 5028, Hilvarenbeek",
    5029: "Postcode 5029, Tilburg",
    5030: "Postcode 5030, Tilburg",
    5031: "Postcode 5031, Tilburg",
    5032: "Postcode 5032, Tilburg",
    5033: "Postcode 5033, Tilburg",
    5034: "Postcode 5034, Tilburg",
    5035: "Postcode 5035, Tilburg",
    5036: "Postcode 5036, Tilburg",
    5037: "Postcode 5037, Tilburg",
    5038: "Postcode 5038, Hagelkruis, Tilburg",
    5039: "Postcode 5039, Tilburg",
    5040: "Postcode 5040, Tilburg",
    5041: "Postcode 5041, Tilburg",
    5042: "Postcode 5042, Tilburg",
    5043: "Postcode 5043, Tilburg",
    5044: "Postcode 5044, Tilburg",
    5045: "Postcode 5045, Tilburg",
    5046: "Postcode 5046, Tilburg",
    5047: "Postcode 5047, Bedrijventerrein Vossenberg, Tilburg",
    5048: "Postcode 5048, Tilburg",
    5049: "Postcode 5049, Tilburg",
}