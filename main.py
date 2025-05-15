from typing import Optional
import requests
from fastapi import FastAPI

app = FastAPI()

GEN_API_URL = "https://greenaillmapi.onrender.com/GenerateChallenge"

@app.get("/create")
def create_challenges(count=1):
    get_location_and_info(count)
    for i in range(count):
        place = LOCATIONS[i]
        loc = POSTCODES[place[0]]
        url = f"{GEN_API_URL}?location={loc}&information={place[1]}"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {"message": "Challenge generated successfully", "data": response.json()}
        else:
            return {"error": "Failed to generate challenge", "status_code": response.status_code,
                    "response": response.text}

def get_location_and_info(count):
    # TODO: Implement logic to get location and information based on AI system
    # For now, we will use a static list of locations and information
    pass

LOCATIONS=[(5011, "Leefbaarheid = 2/5, Luchtkwaliteit = 2/5, Geluidsoverlast = 4/5, struiken = weinig, bomen = veel"), (5012, "Leefbaarheid = 3/5, Luchtkwaliteit = 3/5, Geluidsoverlast = 2/5, struiken = veel, bomen = weinig"), (5013, "Leefbaarheid = 4/5, Luchtkwaliteit = 4/5, Geluidsoverlast = 1/5, struiken = gemiddeld, bomen = gemiddeld")]


# Gedeeltelijk Ai generated... Controleer of de buurten correct zijn.
POSTCODES = {
    5011: "Postcode 5011, De Schans, Tilburg",
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