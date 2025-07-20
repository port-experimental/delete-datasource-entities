import requests
import os
from collections import defaultdict

# ======== Configuration ========
CLIENT_ID = os.getenv("PORT_CLIENT_ID")
CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")
DATASOURCE_NAME = "<data source name>"
DRY_RUN = False  # Set to False to actually delete
PORT_API_BASE = "https://api.port.io/v1"
# ===============================

def get_access_token(client_id, client_secret):
    url = f"{PORT_API_BASE}/auth/access_token"
    payload = {
        "clientId": client_id,
        "clientSecret": client_secret
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    token = response.json().get("accessToken")
    if not token:
        raise ValueError("Access token not found in response.")
    return token

def search_entities(datasource_name, token):
    url = f"{PORT_API_BASE}/entities/search?include=identifier&include=blueprint"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "combinator": "and",
        "rules": [
            {
                "property": "$datasource",
                "operator": "contains",
                "value": datasource_name
            }
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("entities", [])

def group_by_blueprint(entities):
    grouped = defaultdict(list)
    for entity in entities:
        blueprint = entity.get("blueprint")
        identifier = entity.get("identifier")
        if blueprint and identifier:
            grouped[blueprint].append(identifier)
    return grouped

def bulk_delete(blueprint, identifiers, token):
    url = f"{PORT_API_BASE}/blueprints/{blueprint}/bulk/entities"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "entities": identifiers
    }
    response = requests.delete(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    print("Authenticating with Port...")
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    print("Access token acquired.\n")

    print(f"Searching for entities with datasource containing '{DATASOURCE_NAME}'...")
    entities = search_entities(DATASOURCE_NAME, token)
    print(f"Found {len(entities)} entities.\n")
    grouped_entities = group_by_blueprint(entities)

    for blueprint, ids in grouped_entities.items():
        print(f"Blueprint: {blueprint}")
        print(f"Number of entities to be deleted: {len(ids)}")
        print(f"Entities ids: {ids}\n")

        if not DRY_RUN:
            print("Deleting...")
            result = bulk_delete(blueprint, ids, token)
            print(f"Delete result: {result}\n")
        else:
            print("Dry run enabled — no deletion performed.\n")

if __name__ == "__main__":
    main()
