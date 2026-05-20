# Agent Orchestrator

An automated framework for managing, planning, and executing social media content for AI-driven character personas.

## Overview
This project provides a modular system to bridge the gap between creative content planning and social media execution. It uses an LLM-based planner to generate character-specific content and an orchestration engine to manage the lifecycle and posting of those plans.

## Core Components
- **Content Planning:** Automated generation of character-driven content plans using LLMs.
- **Plan Management:** A persistent `PlanStore` that tracks the status (pending, executed, failed) of content plans.
- **Orchestration:** A central engine that coordinates between the plan store and social media clients.
- **Social Clients:** A pluggable architecture supporting multiple platforms (e.g., Instagram) and a mock client for safe testing.
- **TUI Interface:** A terminal-based dashboard for real-time monitoring and manual intervention.

## Architecture
The system is organized into distinct domains:
- `src/content/`: Logic for plan generation, validation, and storage.
- `src/orchestration/`: The core execution loop and state management.
- `src/social/`: Platform-specific implementations for content delivery.
- `src/ui/`: Interactive terminal interface.
- `characters/`: Data directory containing character profiles and their respective content plans.

## Getting Started

### Prerequisites
- Python 3.x
- API access to an LLM provider (e.g., OpenRouter/OpenAI).

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your API keys and credentials:
   ```bash
   cp .env.example .env
   ```

### Usage
- **Interactive Mode:** Use the TUI to manage and execute plans manually:
  ```bash
  python tui.py [character_name]
  ```
- **Automated Mode:** Run the orchestrator to process pending plans:
  ```bash
  python main.py [character_name]
  ```

## Contributing
Contributions are welcome! Please ensure that new social clients implement the `BaseSocialClient` interface and that all new logic is covered by tests in the `tests/` directory.
