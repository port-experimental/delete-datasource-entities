import requests
import os
import argparse
from collections import defaultdict

PORT_API_BASE = "https://api.port.io/v1"
BATCH_SIZE = 100

def get_access_token(client_id, client_secret):
    url = f"{PORT_API_BASE}/auth/access_token"
    payload = {"clientId": client_id, "clientSecret": client_secret}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    token = response.json().get("accessToken")
    if not token:
        raise ValueError("Access token not found in response.")
    return token

def search_entities(datasource_name, token):
    url = f"{PORT_API_BASE}/entities/search?include=identifier&include=blueprint"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {
        "combinator": "and",
        "rules": [
            {"property": "$datasource", "operator": "contains", "value": datasource_name}
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

def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def bulk_delete(blueprint, identifiers, token):
    url = f"{PORT_API_BASE}/blueprints/{blueprint}/bulk/entities"
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"entities": identifiers}
    response = requests.delete(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def delete_integration(integration_id, token):
    url = f"{PORT_API_BASE}/integration/{integration_id}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Delete Port entities by integration ID.")
    parser.add_argument("--client-id", default=os.getenv("PORT_CLIENT_ID"), help="Port Client ID")
    parser.add_argument("--client-secret", default=os.getenv("PORT_CLIENT_SECRET"), help="Port Client Secret")
    parser.add_argument("--integration-id", required=True, help="Integration ID (data source identifier)")
    parser.add_argument("--dry-run", action="store_true", help="Do not actually delete entities")
    parser.add_argument("--delete-integration", action="store_true", help="Delete integration after deleting entities")

    args = parser.parse_args()

    print("Authenticating with Port...")
    token = get_access_token(args.client_id, args.client_secret)
    print("Access token acquired.\n")

    print(f"Searching for entities with datasource containing '{args.integration_id}'...")
    entities = search_entities(args.integration_id, token)
    print(f"Found {len(entities)} entities.\n")

    grouped_entities = group_by_blueprint(entities)

    for blueprint, ids in grouped_entities.items():
        print(f"Blueprint: {blueprint}")
        print(f"Number of entities to be deleted: {len(ids)}")
        print(f"Entities ids: {ids}\n")

        if args.dry_run:
            print("Dry run enabled — no deletion performed.\n")
        else:
            for batch in chunked(ids, BATCH_SIZE):
                print(f"Deleting batch of {len(batch)} entities from blueprint '{blueprint}'...")
                bulk_result = bulk_delete(blueprint, batch, token)
                print(f"Result: {bulk_result}")

    if args.delete_integration:
        print(f"Attempting to delete integration: {args.integration_id}")
        integration_deletion_result = delete_integration(args.integration_id, token)
        print(f"Result: {integration_deletion_result}")

if __name__ == "__main__":
    main()
