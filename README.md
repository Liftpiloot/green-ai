# Green Ai APi

De green Ai API is een RESTful API die is ontworpen voor de Green AI applicatie. Deze API biedt een makkelijke manier om challenges te genereren voor de app, op basis van gegevens over de locatie.
De Challenges kunnen op twee manieren worden gemaakt: 
- Automatisch, door het AI model met /create 
- Door de gebruiker met /GenerateChallenge(location,information). 

Ook bevat de applicatie een endpoint om te controleren of een vuilnisbak vol is.
- /trashcan_is_full(image) stuurt een afbeelding van de vuilnisbak naar de API, die vervolgens een antwoord terugstuurt met de status van de vuilnisbak.
Dit is in de huidige versie gedaan met een Gemini API, maar in de toekomst gaan we ons eigen model implementeren, Sem heeft dit model al getraind.

De Api gebruikt Gemini AI om de challenges te genereren, en het eigen AI model, dat is getraind op basis van informatie, te vinden op kaarten van AtlasNatuurlijk kapitaal. De documentatie hiervan is te vinden in het Jupyter notebook.