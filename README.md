# OMNISCIENCE Program

## Objective
To design, build, and operate a persistent, multi-layered Swarm intelligence platform capable of autonomously discovering online retailers, crawling their product catalogs, identifying functionally identical products, and exposing real-time arbitrage opportunities.

## Architecture
The OMNISCIENCE platform is composed of a series of specialized agents and data infrastructure components. The system is designed as a pipeline to discover, process, and analyze product data from across the web.

### Core Components
*   **Publisher Agent:** A Flask-based web application that will serve as the front-end dashboard for viewing arbitrage opportunities.
*   **Database Agent:** The central data repository, built on SQLAlchemy to be database-agnostic. It is currently configured to use SQLite for development.
*   **Message Queue Agent:** An in-memory queue system to manage the flow of data (URLs) between the different swarm agents. It provides a `crawl_queue` and an `extraction_queue`.
*   **Discovery Swarm:** A set of logic responsible for finding new e-commerce websites.
*   **Crawler Swarm (Planned):** Will be responsible for crawling retailer websites to find product pages.
*   **Extractor Swarm (Planned):** Will be responsible for extracting structured data (name, price, UPC) from product pages.
*   **Analyzer Agent (Planned):** Will be responsible for querying the database to find arbitrage opportunities.

### Execution Model: Human-in-the-Loop Orchestration
Due to the current execution environment, the agents' logic (e.g., `discovery_swarm/agent.py`) is separated from the execution of specialized tools (e.g., `google_search`).

Therefore, the system operates using a **turn-based orchestration model**, with the AI agent **Jules** acting as the central orchestrator.

A typical workflow is executed as follows:
1.  **Jules (Orchestrator):** Initiates a task, such as discovering new retailers.
2.  **Jules (Orchestrator):** Calls a specialized tool, for example, `google_search("online stores")`.
3.  **Jules (Orchestrator):** Takes the output from the tool and passes it to a logic script for processing. This may involve saving the tool output to a temporary file that a processing script can read.
4.  **Jules (Orchestrator):** Continues this cycle of calling tools and executing logic functions until the workflow is complete and the results (e.g., verified retailer domains) are published to the message queue.

This model allows for robust development and testing of the individual components while working within the constraints of the environment.

## Current Status
The following components have been implemented:
*   Initial framework for the **Publisher Agent**.
*   **Database Agent** setup with a `Product` model.
*   **Message Queue Agent** with an in-memory implementation.
*   The core logic library for the **Discovery Swarm**.
