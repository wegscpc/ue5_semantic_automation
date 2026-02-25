🛠️ UE5 AI-Driven Asset Manager & Quality Auditor

## Overview
This project arose from the need to optimize the workflow in Unreal Engine 5, eliminating human error and technical debt in large-scale projects. It combines automation with Python, Quality Assurance standards, and Generative AI to maintain a clean, optimized, and professional Content Browser.

## 🚀 Key Features

- Semantic Auto-Naming: Uses pattern logic and integration with LLMs (via API/Local) to rename assets based on their class and context, following industry standards (SM_, T_, M_).

- QA Sanity Check: Automatic asset auditing to detect common errors before packaging:
    - Textures that are not a power of 2.
    - Materials with unused nodes.
    - Assets without assigned collisions.

- AI Metadata Generation: Automatically generates tags and descriptions for the Unreal search engine, facilitating asset location for large teams.

- Editor Utility Widget: An intuitive interface built in UE5 for artists to run tools without writing a single line of code.

## 🛠️ Tech Stack
- Engine: Unreal Engine 5.x
- Language: Python (Unreal API), C#
- AI Integration: OpenAI API / Local LLMs (via Windsurf/Roo Code for development orchestration).
- Version Control: Git & GitHub Actions for CI/CD of engine tools.

## 📈 Impact on SDLC
As a Senior Quality Engineer, my focus is on reducing the time spent on repetitive tasks:
    - 80% reduction in manual folder organization time.
    - Early detection of unoptimized assets, reducing errors in the final build.
    - Full project standardization to facilitate collaboration between departments (Art, Development, QA).

## 📖 How to Use
- Clone the repository to your /Plugins or /Content/Python folder.
- Open Unreal Engine 5.
- Right-click on any asset or folder and select "AI Asset Organizer" from the Scripted Asset Actions menu.

## About the Author
Walter Gomis - "M" Shaped Engineer | Technical Artist | QA Strategist. 
Specializing in bridging the gap between technical quality and artistic vision through intelligent automation.