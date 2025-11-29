## Tests

This directory contains comprehensive test coverage for the app, demonstrating various methodologies.

### `01_unit/`

Isolated automated pytest unit testing:

- **Artwork CRUD operations** - testing addArtwork() for happy path
- **Data validation** - testing addArtwork() for edge cases (empty fields, invalid year)
- **Database operations** - testing saveArchive() synchronization
- **Filtering & search** - testing QSortFilterProxyModel() (case-insensitive, special chars)
- **Sorting** - testing if QtSortOrder() works for proxy model (ascending, descending)
- **Thumbnail handling** - Testing image loading, scaling and error handling

### `02_integration/`

Verifying component interactions with pytest:

- **CRUD with database** - End-to-end testing of database operations
- **Data persistence** - State management across sessions
- **Export/Import** - Migrating and backing up databases
- **Regression suite** - Automated regression checks (TODO)

### `03_manual/`

Structured manual testing documentation:

Naming pattern: `tc_[feature]_[number]_[scenario].org`

- **Test cases** - Detailed scenarios for feature areas:
  (add, edit, delete, filter, export, import, undo/redo, PDF export)
- **Test execution** - Execution logs and results (TODO)
- **Bug reports** - Documented issues (TODO)
- **Exploratory testing** - Ad-hoc testing notes (TODO)
- **Regression checklists** - Manual verification procedures (TODO)

### `fixtures/`

Reusable test data and utilities:

- Sample artwork datasets
- Pre-configured databases (empty, populated, corrupted)
- Helper functions for test setup

### `user-stories/`

Acceptance criteria I created for the application

## Running Tests

### Requirements

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Run

```bash
# Run all automated tests
pytest

# Run with verbose output and print statements
pytest -vs 

# Run specific test suite
pytest 01_unit/
pytest 02_integration/

# Run with coverage
# Creates an automatic report in htmlcov folder
pytest --cov=src --cov-report=html

# Run specific test file
pytest 01_unit/test_artwork_crud.py
```
