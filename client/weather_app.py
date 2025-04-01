import os
import sys
import time
from mcp_client import MCPClient

class WeatherApp:
    def __init__(self, server_url="http://localhost:8000"):
        self.client = MCPClient(server_url)
        self.cities = []
    
    def initialize(self):
        """Initialise l'application et récupère la liste des villes"""
        try:
            print("Connexion au serveur météo...")
            self.client.initialize()
            print("Récupération de la liste des villes marocaines...")
            cities_data = self.client.execute_tool("list_cities")
            self.cities = cities_data.get("cities", [])
            if not self.cities:
                print("Avertissement: Aucune ville n'a été récupérée.")
            return True
        except Exception as e:
            print(f"Erreur d'initialisation: {str(e)}")
            return False
    
    def get_weather(self, city):
        """Récupère et affiche les informations météo pour une ville"""
        try:
            weather_data = self.client.execute_tool("get_weather", {"city": city})
            return weather_data
        except Exception as e:
            print(f"Erreur: {str(e)}")
            return None
    
    def display_weather(self, weather_data):
        """Affiche les informations météo de manière formatée"""
        if not weather_data:
            return
        
        if "error" in weather_data:
            print(f"Erreur: {weather_data['error']}")
            return
        
        # Effacer l'écran
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Afficher les informations météo
        print("\n" + "="*50)
        print(f"  MÉTÉO POUR {weather_data['city'].upper()}, {weather_data['country']}")
        print("="*50)
        print(f"Condition:     {weather_data['weather_condition']} ({weather_data['description']})")
        print(f"Température:   {weather_data['temperature']}°C (Ressenti: {weather_data['feels_like']}°C)")
        print(f"Humidité:      {weather_data['humidity']}%")
        print(f"Pression:      {weather_data['pressure']} hPa")
        print(f"Vent:          {weather_data['wind_speed']} m/s")
        print(f"Nuages:        {weather_data['clouds']}%")
        
        # Convertir le timestamp en heure locale
        local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(weather_data['timestamp']))
        print(f"Mise à jour:   {local_time}")
        print("="*50 + "\n")
    
    def display_cities(self):
        """Affiche la liste des villes disponibles"""
        if not self.cities:
            print("Aucune ville disponible.")
            return
        
        print("\nVilles marocaines disponibles:")
        print("="*50)
        
        # Afficher les villes en colonnes
        col_width = 15
        num_cols = 3
        
        for i in range(0, len(self.cities), num_cols):
            row = self.cities[i:i+num_cols]
            print("".join(city.ljust(col_width) for city in row))
        
        print("="*50 + "\n")
    
    def run(self):
        """Exécute l'application météo interactive"""
        if not self.initialize():
            print("Impossible d'initialiser l'application. Veuillez vérifier la connexion au serveur.")
            return
        
        while True:
            print("\n=== APPLICATION MÉTÉO MAROC ===")
            print("1. Afficher la météo pour une ville")
            print("2. Afficher la liste des villes disponibles")
            print("3. Quitter")
            
            choice = input("\nVotre choix (1-3): ")
            
            if choice == "1":
                city = input("Entrez le nom de la ville: ")
                weather_data = self.get_weather(city)
                self.display_weather(weather_data)
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == "2":
                self.display_cities()
                input("Appuyez sur Entrée pour continuer...")
            
            elif choice == "3":
                print("Au revoir!")
                break
            
            else:
                print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    # Permettre de spécifier l'URL du serveur en argument
    server_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    app = WeatherApp(server_url)
    app.run()