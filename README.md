# Finance-Tracker CLI


## Introduction
A lightweight, high-performance Command Line Interface (CLI) application designed for individuals who want to track their spending without the clutter of modern banking apps. This tool provides dynamic financial insights, category-based tracking, and robust search capabilities.

Directory structure:

```text
.
├── cli.py              # Main entry point and User Interface loop
├── debug.py            # Utility script for testing and database inspection
├── finance_tracker.db  # SQLite database (generated on first run)
├── helpers.py          # General utility functions (formatting, dates)
├── __init__.py
└── models
    ├── __init__.py     # Package exports and shared imports
    ├── database.py     # SQLAlchemy engine and session configuration
    ├── logic.py        # Core logic (Burn Rate, Search, Aggregates)
    └── models.py       # SQLAlchemy ORM classes (User, Expense)
```



## Generating Your Environment

Clone this repository then:

```console
pipenv install
pipenv shell
```

---

## Running the CLI
```console
cd lib
python cli.py
```




## License
This project is open-source and available under the MIT License.



