import tempfile

from fastapi import FastAPI, UploadFile, File
import os
from google import genai
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
    content = f"Generate a short and actionable challenge for improving the environment (max 20 words) for users near {location}, where {information}. Keep it fun and motivating. examples are, plant a tree, plant a hedge or a flower, etc. Be very exact, the user should know exactly what to do. if talking about a tree, be specific about the type of tree, if talking about a flower, be specific about the type of flower. Do not use any other words than the challenge itself. The locations are public areas. Also state the reason, which metric will it improve"
    client = genai.Client(api_key=AI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=content)
    # send challenge to greenAi API
    return {"message": "Challenge generated successfully", "data": response.text}

@app.get("/create")
async def create_challenges(count: int=1):
    get_location_and_info(count)
    for i in range(count):
        place = LOCATIONS[i]
        loc = POSTCODES[place[0]]
        challenge = await generate_challenge(location=loc, information=place[1])
        # TODO send challenge to greenAi API
        return {"message": "Challenge generated successfully", "data": challenge}

def get_location_and_info(count):
    # TODO: Implement logic to get location and information based on AI system
    # For now, we will use a static list of locations and information
    pass

LOCATIONS=[(5011, "Leefbaarheid = 2/5, Luchtkwaliteit = 2/5, Geluidsoverlast = 4/5, struiken = weinig, bomen = veel"), (5012, "Leefbaarheid = 3/5, Luchtkwaliteit = 3/5, Geluidsoverlast = 2/5, struiken = veel, bomen = weinig"), (5013, "Leefbaarheid = 4/5, Luchtkwaliteit = 4/5, Geluidsoverlast = 1/5, struiken = gemiddeld, bomen = gemiddeld")]


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