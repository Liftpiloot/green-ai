# Green AI API

De **Green AI API** is een RESTful API ontworpen voor gebruik binnen de Green AI-applicatie. Deze API biedt een eenvoudige manier om op locatie gebaseerde **challenges** te genereren en om te detecteren of een **vuilnisbak vol is** met behulp van AI-modellen.

## Functionaliteiten

### 🔹 Challenge-generatie

Challenges kunnen op twee manieren worden aangemaakt:

- **Automatisch**: via het AI-model met de endpoint `POST /create`
- **Handmatig**: via de gebruiker met de endpoint `POST /GenerateChallenge(location, information)`

De gegenereerde challenges zijn afhankelijk van gegevens over de locatie, en worden gegenereerd met behulp van **Gemini AI** en kaarten van **Atlas Natuurlijk Kapitaal**.

### 🔹 Vuilnisbakdetectie

- Endpoint: `POST /trashcan_is_full(image)`
- Deze endpoint ontvangt een afbeelding van een vuilnisbak en bepaalt met behulp van een getraind **YOLO-model** of de vuilnisbak vol is.

## Technische details

- **Challenge-generatie** maakt gebruik van:
  - **Gemini AI** (via API key)
  - **Kaartinformatie** van Atlas Natuurlijk Kapitaal
- **Vuilnisbakstatus** wordt bepaald met:
  - Een **getraind YOLO AI-model** op basis van vuilnisbakafbeeldingen

De volledige documentatie van het AI-model en de data is beschikbaar in het bijgeleverde **Jupyter-notebook**.

## Installatie en gebruik

1. Maak een `.env` bestand aan in de hoofdmap met daarin je Gemini API key:

   ```env
   GeminiAPI=your_api_key

2. Installeer de benodigde Python-pakketten:

   ```bash
   pip install -r requirements.txt
   ```
   
3. Start de API-server met:

   ```bash
    python main.py
    ```
   
De API is nu beschikbaar op `http://localhost:8000`.

## Gebruik in de Green AI-app
De Green-AI app gebruikt deze API om:
- Challenges te genereren op basis van de huidige locatie van de gebruiker.
- De status van vuilnisbakken te controleren door een foto te maken en deze te uploaden.

### Setup in de app
1. Host deze API-server op een publieke server
2. Configureer de URL van de API in de source code van de Green AI-app. onder /lib/constants/api_constants.dart