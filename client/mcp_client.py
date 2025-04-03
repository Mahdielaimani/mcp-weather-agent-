import requests
import json
import time

class MCPClient:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url
        self.initialized = False
        self.max_retries = 3
        self.retry_delay = 2
    
    def initialize(self):
        """Initialise la connexion avec le serveur MCP"""
        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"Tentative de connexion {attempt}/{self.max_retries}...")
                
                # Requête HTTP directe sans vérification préalable
                payload = {
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "params": {},
                    "id": 1
                }
                
                # Utiliser une session avec un timeout très long
                session = requests.Session()
                response = session.post(
                    self.server_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30  # 30 secondes
                )
                
                # Vérifier le code de statut
                if response.status_code != 200:
                    raise Exception(f"Erreur HTTP: {response.status_code}")
                
                # Analyser la réponse JSON
                result = response.json()
                
                if "result" in result:
                    self.initialized = True
                    return result["result"]
                else:
                    error_msg = result.get("error", {}).get("message", "Erreur inconnue")
                    raise Exception(f"Erreur d'initialisation: {error_msg}")
                    
            except Exception as e:
                if attempt < self.max_retries:
                    print(f"Échec de la connexion: {str(e)}")
                    print(f"Nouvelle tentative dans {self.retry_delay} secondes...")
                    time.sleep(self.retry_delay)
                else:
                    raise Exception(f"Erreur de connexion au serveur MCP après {self.max_retries} tentatives: {str(e)}")
    
    def get_tools(self):
        """Récupère la liste des outils disponibles"""
        if not self.initialized:
            self.initialize()
        
        payload = {
            "jsonrpc": "2.0",
            "method": "getTools",
            "params": {},
            "id": 2
        }
        
        response = requests.post(
            self.server_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"Erreur HTTP: {response.status_code}")
        
        result = response.json()
        
        if "result" in result and "tools" in result["result"]:
            return result["result"]["tools"]
        else:
            error_msg = result.get("error", {}).get("message", "Erreur inconnue")
            raise Exception(f"Erreur lors de la récupération des outils: {error_msg}")
    
    def execute_tool(self, tool_name, parameters=None):
        """Exécute un outil sur le serveur MCP"""
        if not self.initialized:
            self.initialize()
        
        if parameters is None:
            parameters = {}
        
        payload = {
            "jsonrpc": "2.0",
            "method": "executeTool",
            "params": {
                "name": tool_name,
                "parameters": parameters
            },
            "id": 3
        }
        
        response = requests.post(
            self.server_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"Erreur HTTP: {response.status_code}")
        
        result = response.json()
        
        if "result" in result:
            return result["result"]
        else:
            error_msg = result.get("error", {}).get("message", "Erreur inconnue")
            raise Exception(f"Erreur lors de l'exécution de l'outil {tool_name}: {error_msg}")