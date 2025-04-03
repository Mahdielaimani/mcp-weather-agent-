import requests
import json
from config import get_api_key

class WeatherAgent:
    def __init__(self):
        self.api_key = get_api_key()
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        # Liste des principales villes marocaines
        self.moroccan_cities = [
            "Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", "Agadir",
            "Meknès", "Oujda", "Kenitra", "Tétouan", "Safi", "El Jadida",
            "Nador", "Mohammedia", "Béni Mellal", "Taza", "Khemisset",
            "Taourirt", "Berkane", "Larache", "Khouribga", "Ouarzazate",
            "Settat", "Essaouira", "Ksar El Kebir", "Tiflet", "Berrechid",
            "Khénifra", "Taroudant", "Chefchaouen"
        ]
    
    def get_available_cities(self):
        """Retourne la liste des villes marocaines disponibles"""
        return self.moroccan_cities
    
    def is_valid_moroccan_city(self, city):
        """Vérifie si la ville est une ville marocaine valide"""
        return city.lower() in [c.lower() for c in self.moroccan_cities]
    
    def get_weather(self, city):
        """Récupère les données météo pour une ville marocaine"""
        if not self.api_key:
            raise ValueError("Clé API OpenWeather non configurée. Veuillez configurer la variable d'environnement OPENWEATHER_API_KEY.")
            
        if not self.is_valid_moroccan_city(city):
            raise ValueError(f"'{city}' n'est pas une ville marocaine valide. Utilisez list_cities pour voir les villes disponibles.")
        
        params = {
            'q': f"{city},ma",  # Ajouter le code pays 'ma' pour le Maroc
            'appid': self.api_key,
            'units': 'metric',   # Pour obtenir la température en Celsius
            'lang': 'fr'         # Pour obtenir les descriptions en français
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)  # Ajout d'un timeout de 10 secondes
            response.raise_for_status()  # Lever une exception pour les erreurs HTTP
            
            data = response.json()
            
            # Formater les données météo
            weather_info = {
                'city': city,
                'country': 'Maroc',
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather_condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'timestamp': data['dt']
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la requête API: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Erreur lors du traitement des données météo: {str(e)}")