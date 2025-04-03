import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from weather_agent import WeatherAgent

# Initialiser l'agent météo
weather_agent = WeatherAgent()

# Définition des outils disponibles
TOOLS = {
    "get_weather": {
        "description": "Obtenir les informations météorologiques pour une ville marocaine",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nom de la ville marocaine"
                }
            },
            "required": ["city"]
        }
    },
    "list_cities": {
        "description": "Obtenir la liste des villes marocaines disponibles",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

# Implémentation des outils
def execute_get_weather(params):
    city = params.get("city", "")
    if not city:
        return {"error": "Nom de ville requis"}
    
    try:
        weather_data = weather_agent.get_weather(city)
        return weather_data
    except Exception as e:
        return {"error": f"Erreur lors de la récupération des données météo: {str(e)}"}

def execute_list_cities(params):
    try:
        cities = weather_agent.get_available_cities()
        return {"cities": cities}
    except Exception as e:
        return {"error": f"Erreur lors de la récupération de la liste des villes: {str(e)}"}

TOOL_EXECUTORS = {
    "get_weather": execute_get_weather,
    "list_cities": execute_list_cities
}

class MCPHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Connection', 'close')  # Fermer la connexion après la réponse
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
        self.wfile.write(b'')
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/sse':
            self._handle_sse()
        else:
            self._set_headers()
            self.wfile.write(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": "Méthode GET non prise en charge. Utilisez POST pour les requêtes JSON-RPC."
                },
                "id": None
            }).encode())
    
    def _handle_sse(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Envoyer un message initial
        self.wfile.write(b'data: {"jsonrpc":"2.0","method":"ready","params":{}}\n\n')
        self.wfile.flush()
        
        # Garder la connexion ouverte avec des pings périodiques
        try:
            for _ in range(10):  # Réduit à 10 secondes max
                time.sleep(1)
                self.wfile.write(b': ping\n\n')  # Commentaire SSE pour garder la connexion active
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
    
    def do_POST(self):
        print("Requête POST reçue")
        content_length = int(self.headers.get('Content-Length', 0))
        print(f"Content-Length: {content_length}")
        
        if content_length == 0:
            self._set_headers()
            self.wfile.write(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Corps de requête vide"
                },
                "id": None
            }).encode())
            return
        
        try:
            post_data = self.rfile.read(content_length)
            print(f"Données reçues: {post_data.decode('utf-8')}")
            request = json.loads(post_data.decode('utf-8'))
            
            if not isinstance(request, dict):
                raise ValueError("La requête doit être un objet JSON")
            
            method = request.get("method")
            print(f"Méthode appelée: {method}")
            
            if method == "initialize":
                response = self._handle_initialize(request)
            elif method == "getTools":
                response = self._handle_get_tools(request)
            elif method == "executeTool":
                response = self._handle_execute_tool(request)
            else:
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Méthode non prise en charge: {method}"
                    },
                    "id": request.get("id")
                }
            
            self._set_headers()
            print(f"Réponse: {json.dumps(response)}")
            self.wfile.write(json.dumps(response).encode())
        
        except json.JSONDecodeError:
            print("Erreur: JSON invalide")
            self._set_headers()
            self.wfile.write(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Erreur d'analyse JSON"
                },
                "id": None
            }).encode())
        except Exception as e:
            print(f"Erreur: {str(e)}")
            self._set_headers()
            self.wfile.write(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Erreur interne: {str(e)}"
                },
                "id": None
            }).encode())
    
    def _handle_initialize(self, request):
        print("Initialisation de la connexion")
        return {
            "jsonrpc": "2.0",
            "result": {
                "name": "morocco-weather-mcp-server",
                "version": "1.0.0",
                "vendor": "example",
                "capabilities": {
                    "tools": True
                }
            },
            "id": request.get("id")
        }
    
    def _handle_get_tools(self, request):
        print("Récupération des outils disponibles")
        return {
            "jsonrpc": "2.0",
            "result": {
                "tools": TOOLS
            },
            "id": request.get("id")
        }
    
    def _handle_execute_tool(self, request):
        params = request.get("params", {})
        tool_name = params.get("name")
        tool_params = params.get("parameters", {})
        
        print(f"Exécution de l'outil: {tool_name}")
        print(f"Paramètres: {tool_params}")
        
        if not tool_name:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Nom d'outil manquant"
                },
                "id": request.get("id")
            }
        
        if tool_name not in TOOL_EXECUTORS:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": f"Outil inconnu: {tool_name}"
                },
                "id": request.get("id")
            }
        
        try:
            result = TOOL_EXECUTORS[tool_name](tool_params)
            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request.get("id")
            }
        except Exception as e:
            print(f"Erreur lors de l'exécution de l'outil: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Erreur d'exécution: {str(e)}"
                },
                "id": request.get("id")
            }

def run_server(host='0.0.0.0', port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, MCPHandler)
    print(f"Serveur MCP Météo démarré sur http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print(f"Outils disponibles: {', '.join(TOOLS.keys())}")
    print("Appuyez sur Ctrl+C pour arrêter le serveur")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
        httpd.server_close()
        print("Serveur arrêté")

if __name__ == "__main__":
    run_server()