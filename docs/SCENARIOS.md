# 🛠️ Creating Custom Scenarios

Diane allows you to define your own worlds, factions, and regions. You can do this interactively via Discord or by uploading a JSON configuration.

## 1. Interactive Creation (Discord)

Use the following commands to build a scenario step-by-step:

1.  `!new_scenario`: Start a fresh draft.
2.  `!capture_draft`: **[NEW]** Captures the current active simulation state into your draft. This is the best way to interact with dynamic events like rebel factions.
3.  `!add_faction <id> <name> [power] [legitimacy] [resources] [traits...]`: Add or update a faction.
4.  `!add_region <id> <name> [owner_id]`: Add or update a territory.
5.  `!assign_region <region_id> <faction_id>`: Associate an existing region with a faction.
6.  `!view_draft`: Check your current setup.
7.  `!start_custom [session_name]`: Launch the simulation using your draft.

## 2. JSON Scenario Upload

You can upload a `.json` file with the `!upload_scenario` command. 

### JSON Format Example:
```json
{
  "factions": [
    {
      "id": "f_empire",
      "name": "The Empire",
      "power": 80.0,
      "legitimacy": 40.0,
      "resources": 100.0,
      "traits": ["Militarist", "Industrialist"]
    },
    {
      "id": "f_republic",
      "name": "New Republic",
      "power": 40.0,
      "legitimacy": 80.0,
      "resources": 60.0,
      "traits": ["Diplomat"]
    }
  ],
  "regions": [
    {
      "id": "r1",
      "name": "Capital",
      "population": 10000,
      "stability": 100.0,
      "owner": "f_empire"
    },
    {
      "id": "r2",
      "name": "Colony",
      "population": 500,
      "stability": 60.0,
      "owner": "f_republic"
    }
  ]
}
```

### Steps:
1.  Create your JSON file.
2.  Drag and drop it into Discord.
3.  Add the comment `!upload_scenario` to the upload.
4.  Once confirmed, type `!start_custom`.

---
*Factions and regions are automatically cross-referenced based on IDs.*
