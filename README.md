# Task Manager with MySQL Database + Automated Tests

This project is Task Manager application connected to a MySQL database.  
Users can add tasks, view active tasks, update their status, and delete them.  
The project also includes a full pytest test suite to verify that database operations work correctly.

## Features

### Application Features (main.py)

**Add a new task**  
Inserts a new record into the 'ukoly' database table with the default status "Nezahájeno".  
**Display tasks**  
Shows tasks whose status is "Nezahájeno" or "Probíhá".  
Completed tasks ("Hotovo") are hidden.  
**Update a task**
Allows changing the task status to:

- "Probíhá" (In progress)
- "Hotovo" (Completed)

**Delete a task**  
Removes a task from the database by ID.

**Database connection handling**  
Includes functions for connecting and disconnecting from MySQL.

**Automatic table creation**  
A helper function creates the 'ukoly' table if it does not already exist.

## Test Suite (test_main.py)

The test file includes pytest tests covering the database logic:  
✔ test_pridat_ukol_pozitivni – inserting a valid task  
✔ test_pridat_ukol_negativni – inserting invalid data (should raise an error)  
✔ test_aktualizovat_ukol_pozitivni – updating an existing task  
✔ test_aktualizovat_ukol_negativni – updating a non-existent task  
✔ test_odstranit_ukol_pozitivni – deleting a task  
✔ test_odstranit_ukol_negativni – deleting a non-existent task

Each test uses its own temporary test table, which is automatically cleaned up after the test execution.

## Requirements

- Python 3.10+
- MySQL server
- Required Python packages:  
  `mysql-connector-python`  
  `pytest`

## Installation

1. Clone the project  
   `git clone <repository-url>`  
   `cd <project-folder>`
2. Create and activate a virtual environment

- Linux / macOS:  
  `python3 -m venv venv`  
  `source venv/bin/activate`
- Windows:  
  `python -m venv venv`  
  `venv\Scripts\activate`

3. Install dependencies  
   `pip install -r requirements.txt`
4. Configure database connection

```
user="root",
password="password",
database="sys"
```

Use credentials matching your local MySQL setup.

## Running the Application

Start the main program:  
`python main.py`  
You will see an interactive menu:

```
1. Přidat nový úkol
2. Zobrazit úkoly
3. Aktualizovat úkol
4. Odstranit úkol
5. Konec programu
```

## Running the Tests

The tests use a separate database (e.g., testDB).  
Make sure it exists or update the credentials accordingly.  
Run all tests with:  
`pytest -v`

## Database Structure

The application uses a table called 'ukoly':  
| Column | Type | Description |  
|---------|--------------|--------------------|  
|id | INT, PK, AI | Task ID |  
|nazev | VARCHAR(20) | Task name |
|popis | VARCHAR(50) | Task description |
|stav | VARCHAR(20) | Task status |

Statuses used:

- "Nezahájeno" (Not started)
- "Probíhá" (In progress)
- "Hotovo" (Completed)

## ✔ Summary

This project demonstrates:

- Working with MySQL databases in Python
- Building a command-line CRUD application
- Writing unit tests for database operations using pytest
- Using fixtures to set up and tear down test environments
