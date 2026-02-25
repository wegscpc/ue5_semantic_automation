Project: "UE5 Semantic Asset Organizer & AI Material Generator"

This would be an Editor Utility Widget (or a Python script for the engine) that helps artists avoid wasting time on repetitive organization and basic creation tasks.

1. What would the tool do?

Automatic Classification with AI: The script scans the /Content folder and, using a local LLM (via API or plugin), analyzes asset names to automatically move them to folders following industry standards (e.g., M_ for materials, T_ for textures, SM_ for meshes).

"Master Materials" Generator via Prompt: An interface where the artist types: "I need a wet stone material with moss." The script uses an AI API to generate the parameters of a pre-existing Master Material in UE5, automatically assigning textures and roughness/metallic values.

Texture Optimizer (LODs): A command that detects over-resolution textures and uses QA logic (your strength) to resize or compress them according to the expected viewing distance, optimizing game performance.

2. Repository Structure (What the recruiter will see)

To make this project on your GitHub unassailable, organize it like this:

/src: Python scripts for Unreal and .uasset files for the plugin/widget.

/docs: A short technical design document explaining how the tool reduces asset management time by X%.

README.md:

* Problem: "Artists waste 20% of their time organizing files and configuring base materials."

* Solution: "Semantic automation using Python and AI."

* Demo: A GIF or short video showing the tool in action within UE5


This code is an excellent starting point because it uses the Unreal Engine API to interact with the engine, demonstrating your ability to program workflow tools: PRD\organize_assets.py

How to take this to the next level on your GitHub?

To make this script meet the Technical Artist + AI profile we discussed, I suggest adding these layers to your repository:

- LLM Integration (Pseudocode): Add a module that, if the asset doesn't have a clear name (e.g., "Asset_123"), sends metadata to an LLM API (like OpenAI or a local model you already handle) to suggest a name based on the visual or descriptive context of the object.

- QA Validation: As Senior Quality Automation, you can include a "Sanity Check" function that verifies if textures have power-of-2 dimensions (e.g., 1024x1024), flagging an error if they don't meet optimization standards.

- User Interface (UI): Create an Editor Utility Widget in UE5 that calls this Python script, allowing artists to use it with a single click.