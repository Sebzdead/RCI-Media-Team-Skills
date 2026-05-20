# Footage Sourcing Specialist Skill (`footage-sourcer`)

This folder contains the `footage-sourcer` workspace-scoped skill for the Antigravity AI coding assistant. This capability bundle helps video editors and researchers find, verify, and log historical, theoretical, and current events video footage and assets.

---

## 📂 Skill Topology

```
.agent/skills/footage-sourcer/
├── SKILL.md            # Skill Brain: System Prompt & Command Bindings
├── README.md           # This documentation
├── scripts/
│   └── log_credits.py  # Automation: Manifest appending script
└── resources/
    └── source_rules.json # Knowledge Base: Licensing profiles & rules
```

---

## ⚙️ Installation & Sharing

Because this is an **on-demand, workspace-scoped capability bundle**, it is tracked by Git. Sharing it with teammates is completely native:

1. **Commit and Push**: Ensure this entire folder is committed and pushed to your shared repository.
2. **Clone / Pull**: Teammates only need to clone the repository or pull the latest changes.
3. **Auto-Match**: When teammates open the workspace in their Antigravity client, the engine will automatically parse the YAML header in `SKILL.md` and register the skill. No manual activation or install scripts are needed!

---

## 🚀 How to Use

### 1. Invoking via Antigravity Chat
Teammates can trigger the skill by using the `/footage-sourcer` slash command or asking for footage research in the chat panel:

> **Example Query:**
> `/footage-sourcer I need historical clips of the 1919 Seattle General Strike`

**The agent will automatically:**
1. Formulate a list of **5–10 candidate queries** across target repositories (e.g. Library of Congress, Wikimedia Commons).
2. Query and filter for **open-licensed media** (Public Domain, CC0, CC BY) that can be used immediately.
3. Call the local `log_credits.py` script to write matching assets to the local `credits_manifest.txt` file at the root.
4. Output primary sourced matches and the candidate query matrix.

---

### 2. Manual Log Appending
If editors find footage manually, they can append it to the central credit manifest using the automation script directly from the terminal:

```bash
python3 .agent/skills/footage-sourcer/scripts/log_credits.py "[Source Name]" "[Direct Resource URL]" "[Licensing Profile]"
```

**Example:**
```bash
python3 .agent/skills/footage-sourcer/scripts/log_credits.py "Library of Congress" "https://loc.gov/item/12345/" "Public Domain"
```
This adds a timestamped entry to the root `credits_manifest.txt`.
