import os
from pathlib import Path
import sys

# Essayer d'importer dotenv, sinon afficher un message d'erreur
try:
    from dotenv import load_dotenv
    # Charger les variables d'environnement depuis le fichier .env
    # Chercher le fichier .env dans le répertoire parent (racine du projet)
    env_path = Path(__file__).resolve().parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    print("AVERTISSEMENT: Le module python-dotenv n'est pas installé.")
    print("Pour une meilleure gestion des variables d'environnement, installez-le avec:")
    print("pip install python-dotenv")

def get_api_key():
    """Récupère la clé API OpenWeather depuis les variables d'environnement"""
    api_key = os.environ.get("OPENWEATHER_API_KEY", "")
    
    if not api_key:
        print("\n" + "="*80)
        print("ATTENTION: La clé API OpenWeather n'est pas définie!")
        print("Veuillez créer un fichier .env à la racine du projet avec votre clé API.")
        print("Exemple: OPENWEATHER_API_KEY=votre_clé_api_ici")
        print("="*80 + "\n")
    
    return api_key