# RabTech CLI Diagnostics Tool

A Python command-line tool that checks basic developer environment information and analyzes diagnostic events.

## Features

- Checks Python version and executable path
- Checks disk usage and available space
- Checks important environment variables
- Supports human-readable output
- Supports JSON output
- Analyzes diagnostic events
- Detects errors and warnings
- Detects HTTP 5xx status codes
- Calculates average latency
- Includes unit tests
- Includes an object-oriented inventory management engine
- Supports JSON and CSV data persistence
- Uses custom exception handling

## Project Structure

```text
rabtech-cli-diagnostics/
├── samples/
│   └── diagnostic-events (3).json
├── src/
│   └── diagnostics/
│       ├── __init__.py
│       ├── checks.py
│       ├── cli.py
│       ├── event_analyzer.py
│       ├── inventory.py
│       └── storage.py
├── tests/
│   ├── test_diagnostics.py
│   ├── test_event_analyzer.py
│   └── test_inventory.py
├── .gitignore
├── pyproject.toml
└── README.md