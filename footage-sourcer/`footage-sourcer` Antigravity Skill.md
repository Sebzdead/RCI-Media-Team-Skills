## 1. Project Topology & Architecture

The `footage-sourcer` skill will be constructed as an **on-demand, workspace-scoped capability bundle**. This guarantees it is tracked inside your project's Git repository, enabling all researchers and editors to share the setup.

### Target Directory Layout

Plaintext

```
<workspace-root>/
└── .agent/
    └── skills/
        └── footage-sourcer/
            ├── SKILL.md            <-- Brain: YAML Frontmatter, Core Prompt, Anchor Anchors
            ├── scripts/
            │   └── log_credits.py  <-- Tool: Automation script for credit manifests
            └── resources/
                └── source_rules.json <-- Knowledge Context: Source constraints & licenses
```

## 2. Component Blueprints

### Component A: The Skill Brain (`SKILL.md`)

The `SKILL.md` file defines the semantic triggers and equips the Antigravity agent with specialized reasoning loops to locate your pillars.

The file **MUST** be written with the following structural layout:

Markdown

```
---
name: footage-sourcer
description: Discovered when users request video b-roll, historical newsreels, images, current event streams, or footage sourcing leads across political economy and history topics.
---

# Footage Sourcing Specialist Directive

## Context & Constraints
You are an advanced digital asset researcher for our video production team. Your core directive is to translate semantic text descriptions of video scenes or historical events into direct, accurate resource URLs, accompanied by real-time license evaluation.

## Core Sourcing Grounding Matrix
When evaluating requests, query across our target channels:
- Pillar A (History): archive.org, loc.gov, marxists.org, europeanfilmgateway.eu
- Pillar B (Theory): pexels.com, pixabay.com, unsplash.com
- Pillar C (Current Events): laborvideo.org, democracynow.org, dvidshub.net, local union profiles

## Execution Workflow Protocol
1. Isolate the target historical era or structural topic from the user prompt.
2. Formulate target search patterns using your native `Google Search` capability (e.g., combining terms with `site:archive.org` or `site:loc.gov`).
3. Traverse and evaluate returned paths with `url_context` to verify page contents match the target request.
4. Calculate copyright risk using guidelines in `resources/source_rules.json`.
5. Run the automation helper script (`scripts/log_credits.py`) to systematically log every discovery for the editing team.

## Output Structure Requirement
Format all responses cleanly as follows:

### 🎯 Primary Sourced Matches
* **Source Platform / Repository**: [Platform Name]
  * **Verified Scene Description**: [Summary of the exact video/image file contents]
  * **Direct Resource URL**: [Active verified hyperlink]
  * **Licensing Profile**: [Public Domain / CC0 / CC BY / Fair Use Required]
  * **Editor Asset Action**: [e.g., "Transcode from WebM to ProRes 422 LT at 24fps"]

### 🔍 Secondary Search Anchors
Provide 2-3 precise search strings for copy-paste queries on internal networks.
```

### Component B: The Automation Script (`scripts/log_credits.py`)

This script acts as the agent's executable "hands". Instead of just spitting out text, the skill uses this Python file to build an accumulation manifest file (`credits_manifest.txt`) on the shared storage layer.

Python

```
#!/usr/bin/env python3
import sys
import os
import datetime

def append_to_manifest(source_name, url, license_type):
    """
    Appends discovered footage data directly to an ongoing manifest 
    for the video editors to drop into YouTube descriptions.
    """
    manifest_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../credits_manifest.txt"))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_line = f"[{timestamp}] SOURCE: {source_name} | URL: {url} | LICENSE: {license_type}\n"
    
    try:
        with open(manifest_path, "a", encoding="utf-8") as f:
            f.write(log_line)
        print(f"SUCCESS: Logged {source_name} to local manifest tracking file.")
    except Exception as e:
        print(f"ERROR: Failed writing to log file: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 log_credits.py [Source] [URL] [License]", file=sys.stderr)
        sys.exit(1)
    append_to_manifest(sys.argv[1], sys.argv[2], sys.argv[3])
```

### Component C: The Knowledge Base Context File (`resources/source_rules.json`)

This structured JSON file anchors the agent’s legal reasoning, ensuring it handles licensing uniformly without hallucinating rules.

JSON

```
{
  "licensing_rules": {
    "Public Domain": {
      "allowed": true,
      "attribution_required": false,
      "editor_note": "Safe to modify and cut freely."
    },
    "CC0": {
      "allowed": true,
      "attribution_required": false,
      "editor_note": "Universal creative commons zero drop-in."
    },
    "CC BY": {
      "allowed": true,
      "attribution_required": true,
      "editor_note": "Requires adding the creator's link exactly to the manifest log."
    },
    "CC BY-NC": {
      "allowed": false,
      "attribution_required": true,
      "editor_note": "WARNING: Avoid if alternative exists. Patreon/Donation funding can be flagged as commercial usage."
    },
    "All Rights Reserved": {
      "allowed": "conditional",
      "attribution_required": true,
      "editor_note": "Evaluate strictly under Fair Use criteria. Use short critique/analysis segments only."
    }
  }
}
```

## 3. Tool Binding Instructions (How to connect scripts to the skill)

To make sure the Antigravity agent knows it can run your automated script, you must explicitly document the interface boundary at the bottom of your `SKILL.md` file using the following command standard:

Markdown

```
## Automated Code Tool Bindings
When you identify a successful asset link and present it to the user, you must immediately call the execution environment to append the credit tracking line. 
Invoke this exact code execution payload via the shell:
`python3 .agent/skills/footage-sourcer/scripts/log_credits.py "[Source Name]" "[Direct Resource URL]" "[Licensing Profile]"`
```

## 4. Setting Up & Bootstrapping the Agent (Verification Routine)

Instruct your Antigravity agent to implement this configuration step-by-step using these initialization stages:

1. **Bootstrap Phase:** Drop this comprehensive implementation text into a file named `sourcing_spec.md` at your project root.
    
2. **Execution Phase:** In your Antigravity chat panel or via your terminal prompt, state:
    
    > _"Read sourcing_spec.md and build the complete .agent/skills/footage-sourcer/ capability directory. Write the SKILL.md, python script, and metadata json files exactly as requested."_
    
3. **Activation Check:** Once the agent creates the files, make a small change in your repository to sync the workspace directory. The Antigravity engine will read the YAML frontmatter header and cache the metadata for just-in-time matching.
    
4. **Validation Test Run:** Enter an active query to verify the loop functions flawlessly:
    
    > _"Find me video footage of industrial strike lines during the 1934 Minneapolis Teamsters Strike."_
    

The agent will capture the search intent, activate the custom skill framework, employ its browser search capabilities to locate matching resource targets, write the data to your log manifest file, and output the target workspace solution package directly to your team.