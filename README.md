# WGUPS Routing Program

## Project Overview
This project implements a routing program for the Western Governors University Parcel Service (WGUPS). The goal is to efficiently plan delivery routes for packages, ensuring all deliveries are completed on time while keeping the total mileage under 140 miles for three trucks.

The program uses a **Nearest Neighbor Algorithm** combined with a custom hash table to optimize delivery routes and manage package data. It is designed to handle the specific requirements of the Salt Lake City Downtown delivery route but is adaptable for use in other cities.

## Key Features
- **Hash Table Implementation:** A custom hash table stores and manages package data.
- **Routing Algorithm:** A Nearest Neighbor algorithm calculates the most efficient delivery routes for each truck.
- **Simulation:** Tracks truck locations, package statuses, and delivery times.
- **User Interface:** Allows users to query package statuses and total mileage traveled by all trucks at specific times.

## Project Requirements
- **Programming Language:** Python 3.x
- **Development Environment:** PyCharm IDE with a virtual environment
- **Libraries Allowed:** Only Python's standard library (e.g., `csv`, `datetime`)
- **Data Provided:**
  - Package data (CSV file)
  - Distance matrix (CSV file)
  - Map of Salt Lake City Downtown

## Python Version Compatibility
This project is tested and designed for Python 3.9.x. Please ensure your environment supports Python 3.9 to avoid compatibility issues.

## File Structure
```
PythonProject/
├── .venv/                 # Virtual environment
├── app_wgups/             # Folder for program modules
│   ├── __init__.py        # Makes this a package
│   ├── hash_table.py      # Hash table implementation
│   ├── packages.py        # Package class
│   ├── routing.py         # Nearest Neighbor algorithm
│   ├── trucks.py          # Truck class
│   └── ui.py              # User interface functions
├── data/                  # Folder for input data files
│   ├── distances.csv
│   ├── packages.csv
├── screenshots/           # Screenshots for the project report
├── tests/                 # Folder for test cases
│   ├── __init__.py
│   └── main.py            # Test cases
├── README.md              # Project documentation
└── main.py                # Entry point of the program
```

## How to Run
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd WGUPSapp
   ```
3. Set up the virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install any necessary dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```
5. Run the program:
   ```bash
   python main.py
   ```

## User Interface
The program provides a menu-driven interface with the following options:
1. View the status of all packages at a specific time.
2. View the status of a single package by ID.
3. View the total mileage traveled by all trucks.
4. Exit the program.

## Screenshots
Screenshots of the program output will be stored in the `screenshots/` folder as required by the project.

## Technical Details
### Algorithm
- The **Nearest Neighbor Algorithm** selects the next closest delivery location from the current position, ensuring efficient routing. It runs with a time complexity of **O(n²)** in the worst case.

### Data Structure
- A custom **Hash Table** stores package data, using chaining to handle collisions. The hash table supports:
  - **Insertion**: Adding package data.
  - **Lookup**: Retrieving package data by package ID.

## Assumptions
- Trucks travel at 18 mph.
- Each truck can carry a maximum of 16 packages.
- Loading and unloading times are instantaneous.
- Specific package constraints are adhered to (e.g., special handling requirements, delayed addresses).

## License
This project is for educational purposes and is not intended for commercial use.

---
**Date:** January 2025
