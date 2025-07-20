# delete-datasource-entities

# 🧹 Port Entity Cleanup Tool

This Python script helps you **delete all entities from all blueprints** in [Port](https://www.getport.io) that were ingested from a specific **data source** (e.g., `jira`, a decommissioned Kubernetes cluster, etc).  

It:
- Authenticates using your Port client ID and secret.
- Searches for all entities that contain the given `$datasource` value.
- Groups them by blueprint.
- Supports **bulk deletion** using Port's Bulk Delete API.
- Offers a **dry run** mode to preview what would be deleted, safely.

---

## 📌 Overview

When using Port to manage infrastructure or third-party tools, it's common to ingest data from systems that may later be decommissioned.

This script provides a safe and automated way to clean up **all entities across all blueprints** that were created by a given data source.

---

## 🧠 When Should You Use This?

A common use case is when an integration is decommissioned but its entities remain in Port. For example:
- A **Kubernetes cluster** was deleted, but its services and workloads still exist in Port.
- A **Jira / GitHub** were disconnected, but entities are still in catalog.

This tool ensures those orphaned entities are removed cleanly and efficiently.

---

## 🚀 How to Use

1. **Clone the repo or copy the script** into your environment.
2. **Install dependencies (optional)**:
   ```bash
   pip install requests
   ```
3. **Set your credentials**:
   - Option 1: Use environment variables:
     ```bash
     export PORT_CLIENT_ID=your-client-id
     export PORT_CLIENT_SECRET=your-client-secret
     ```
   - Option 2: Hardcode them in the script (for testing only).
4. **Set `DATASOURCE_NAME`** to match the `$datasource` value to clean up (e.g., `jira-server`, `my-eks-prod`).
5. **Toggle `DRY_RUN`**:
   - `True`: Show what would be deleted (default).
   - `False`: Actually delete the entities from Port.

6. **Run the script**:
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration

You can configure the following variables at the top of the script:

| Variable         | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `PORT_CLIENT_ID` | Your Port client ID (via env or inline).                                   |
| `PORT_CLIENT_SECRET` | Your Port client secret (via env or inline).                          |
| `DATASOURCE_NAME`| The `$datasource` value to filter entities by.                             |
| `DRY_RUN`        | `True` to preview deletions, `False` to delete for real.                   |
| `PORT_API_BASE`  | (Optional) Base URL for Port’s API. Default is `https://api.port.io`.      |

---

## 🛡️ Safety & Notes

- Only entities that include the given `$datasource` value are selected for deletion.
- The script groups entities by blueprint and deletes them using the **bulk deletion** endpoint.
- Use `DRY_RUN = True` first to safely inspect what would be deleted.

---

## 🧩 Example Output (Dry Run)

```
Blueprint: jiraServerIssue  
Number of entities to be deleted: 3  
Entities ids: ['MAT-1', 'MAT-2', 'MAT-3']

Dry run enabled — no deletion performed.
```

---

## 📬 Support

Need help with Port’s APIs or data modeling?  
📚 Visit [Port Docs](https://docs.getport.io) or reach out to your Customer Success or Solutions Engineer.
