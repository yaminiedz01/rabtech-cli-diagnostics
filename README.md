# RabTech CLI Diagnostics Tool

A Python command-line tool that checks basic developer environment information.

## Features

- Checks Python version and executable path
- Checks disk usage and available space
- Checks important environment variables
- Supports human-readable output
- Supports JSON output
- Includes unit tests

## Project Structure

```text
rabtech-cli-diagnostics/
├── samples/
├── src/
│   └── diagnostics/
│       ├── __init__.py
│       ├── checks.py
│       └── cli.py
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md