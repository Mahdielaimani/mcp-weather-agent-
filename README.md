# Morocco Weather Application with MCP

Une application météo complète pour les villes marocaines utilisant l'architecture Model Context Protocol (MCP). Ce projet démontre comment construire une application client-serveur qui exploite le protocole MCP pour fournir des informations météorologiques via une interface standardisée.

## Qu'est-ce que MCP?

Le Model Context Protocol (MCP) est un protocole standardisé pour la communication entre les modèles d'IA et les outils ou services externes. Il permet:

- **Communication standardisée**: Interface cohérente pour que les modèles interagissent avec des outils externes
- **Découverte d'outils**: Découverte dynamique des outils disponibles et de leurs capacités
- **Échange de données structuré**: Format de communication basé sur JSON-RPC bien défini
- **Extensibilité**: Ajout facile de nouveaux outils sans modifier l'implémentation du client

## Fonctionnalités

- **Données météo en temps réel**: Obtenez les conditions météorologiques actuelles pour les villes marocaines
- **Liste des villes**: Parcourez les villes marocaines disponibles
- **Interface CLI interactive**: Interface en ligne de commande conviviale
- **Gestion sécurisée des clés API**: Stockage des clés API basé sur des variables d'environnement
- **Gestion des erreurs**: Gestion robuste des erreurs et retour d'information à l'utilisateur
- **Architecture extensible**: Facilité d'ajout de nouveaux outils et fonctionnalités


## Prérequis

- Python 3.7 ou supérieur
- Connexion Internet pour l'accès à l'API
- Clé API OpenWeatherMap (niveau gratuit disponible)
- Connaissance de base des interfaces en ligne de commande

## Installation

### Étape 1: Cloner le dépôt

```bash
git clone https://github.com/yourusername/weather-mcp.git
cd weather-mcp



###: Installer les dépendances
pip install -r requirements.txt