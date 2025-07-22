# delete-datasource-entities

This Python script helps you **delete all entities from all blueprints** in [Port](https://www.getport.io) that were ingested from a specific **data source** (e.g., `jira`, a decommissioned Kubernetes cluster, etc).

It:

* Authenticates using your Port client ID and secret.
* Searches for all entities that contain the given `$datasource` value.
* Groups them by blueprint.
* Supports **bulk deletion** using Port's Bulk Delete API.
* Offers a **dry run** mode to preview what would be deleted, safely.
* Provides a CLI interface for flexibility and automation.

---

## 📌 Overview

When using Port to manage infrastructure or third-party tools, it's common to ingest data from systems that may later be decommissioned.

This script provides a safe and automated way to clean up **all entities across all blueprints** that were created by a given data source.

---

## 🧠 When Should You Use This?

A common use case is when an integration is decommissioned but its entities remain in Port. For example:

* A **Kubernetes cluster** was deleted, but its services and workloads still exist in Port.
* A **Jira / GitHub** integration was disconnected, but entities are still in the catalog.

This tool ensures those orphaned entities are removed cleanly and efficiently.

---

## 🚀 How to Use

1. **Clone the repo or copy the script** into your environment.
2. **Install dependencies**:

   ```bash
   pip install requests
   ```
3. **Set your credentials**:

   * Option 1: Use environment variables:

     ```bash
     export PORT_CLIENT_ID=your-client-id
     export PORT_CLIENT_SECRET=your-client-secret
     ```
   * Option 2: Pass them as arguments.
4. **Run the script**:

   ```bash
   python main.py \
     --integration-id my-eks-prod \
     --client-id $PORT_CLIENT_ID \
     --client-secret $PORT_CLIENT_SECRET \
     --dry-run
   ```

---

## ⚙️ Command-Line Arguments

| Argument               | Description                                                                  |
| ---------------------- | ---------------------------------------------------------------------------- |
| `--client-id`          | Your Port client ID (can fall back to `PORT_CLIENT_ID` env variable)         |
| `--client-secret`      | Your Port client secret (can fall back to `PORT_CLIENT_SECRET` env variable) |
| `--integration-id`     | **Required.** The integration `$datasource` value to search for              |
| `--dry-run`            | If set, only previews what would be deleted (safe mode)                      |
| `--delete-integration` | If set, deletes the integration itself after entity cleanup                  |

---

## 🛡️ Safety & Notes

* Only entities that include the given `$datasource` value are selected for deletion.
* The script groups entities by blueprint and deletes them using the **bulk deletion** endpoint.
* Use `--dry-run` first to safely inspect what would be deleted.

---

## 🧹 Example Output (Dry Run)

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
