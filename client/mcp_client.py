import requests
import json

class MCPClient:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url
        self.initialized = False
    
    def initialize(self):
        """Initialise la connexion avec le serveur MCP"""
        try:
            response = self._send_request("initialize", {})
            if "result" in response:
                self.initialized = True
                return response["result"]
            else:
                raise Exception(f"Erreur d'initialisation: {response.get('error', {}).get('message', 'Erreur inconnue')}")
        except Exception as e:
            raise Exception(f"Erreur de connexion au serveur MCP: {str(e)}")
    
    def get_tools(self):
        """Récupère la liste des outils disponibles"""
        if not self.initialized:
            self.initialize()
        
        response = self._send_request("getTools", {})
        if "result" in response and "tools" in response["result"]:
            return response["result"]["tools"]
        else:
            raise Exception(f"Erreur lors de la récupération des outils: {response.get('error', {}).get('message', 'Erreur inconnue')}")
    
    def execute_tool(self, tool_name, parameters=None):
        """Exécute un outil sur le serveur MCP"""
        if not self.initialized:
            self.initialize()
        
        if parameters is None:
            parameters = {}
        
        response = self._send_request("executeTool", {
            "name": tool_name,
            "parameters": parameters
        })
        
        if "result" in response:
            return response["result"]
        else:
            error_msg = response.get('error', {}).get('message', 'Erreur inconnue')
            raise Exception(f"Erreur lors de l'exécution de l'outil {tool_name}: {error_msg}")
    
    def _send_request(self, method, params, request_id=1):
        """Envoie une requête JSON-RPC au serveur MCP"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id
        }
        
        try:
            response = requests.post(
                self.server_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur de requête HTTP: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Réponse invalide du serveur (JSON invalide)")