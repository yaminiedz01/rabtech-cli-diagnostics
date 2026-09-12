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
│       └── event_analyzer.py
├── tests/
│   ├── test_diagnostics.py
│   └── test_event_analyzer.py
├── .gitignore
├── pyproject.toml
└── README.md