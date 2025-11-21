## Artwork Archive – PySide6 Desktop Application

Artwork Archive is a lightweight desktop application for artists and collectors
who want to store, organize, and browse their artwork database. The app provides
a clean table-based view of all entries, fast filtering, and a simple form for
adding new works. It supports saving data to a local SQLite database and lets users
attach image thumbnails for each artwork.

## Technical Overview

The application is built with PySide6 and uses QTableView with a QSortFilterProxyModel
to handle sorting and live filtering across all columns. Data is stored locally
in a SQLite database, automatically created on first launch. The UI includes dynamically
updated table rows, input forms for CRUD operations, and basic file selection for
thumbnail images. The project structure is intentionally minimal to highlight GUI
logic, data flow, and overall architecture.

## Testing & QA Scope

This project is also used as part of my QA portfolio, showcasing manual testing
skills. The repository includes structured test documentation: user stories, functional
test cases, exploratory testing notes, and bug reports created during development.
The goal is to demonstrate practical testing techniques on a real, working application
— covering GUI behavior, CRUD operations, data validation, filtering logic, and
interactions with the database.
