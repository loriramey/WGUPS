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

## User Interface
The program provides a menu-driven interface with the following options:
1. View the status of a single package by ID and time.
2. View the status of all packages by time + total truck mileage.
3. View the all package status + total truck mileage at end of day.
4. Exit the program.

## Screenshots
Screenshots of the program output will be stored in the `screenshots/` folder as required by the project.

# Sources and References
- Garg, P. (2024). Basics of hash tables. _Hackerearth_. [https://www.hackerearth.com/practice/data-structures/hash-tables/basics-of-hash-tables/tutorial/](https://www.hackerearth.com/practice/data-structures/hash-tables/basics-of-hash-tables/tutorial/)
- Python Software Foundation. (n.d.). Datetime. _Python Documentation._ [https://docs.python.org/3/library/datetime.html#module-datetime](https://docs.python.org/3/library/datetime.html#module-datetime)
- Western Governors University. (n.d.) _C 950 Data structures and algorithms II._ ZyBooks.  https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/6/section/1
- W3 Schools. (n.d.) Python DSA Hash Tables. _W3 Schools._ https://www.w3schools.com/dsa/dsa_theory_hashtables.php
- W3 Schools. (n.d.).Python DSA Greedy Algorithms. _W3 Schools._ [https://www.w3schools.com/dsa/dsa_ref_greedy.php](https://www.w3schools.com/dsa/dsa_ref_greedy.php)
- W3 Schools. (n.d.) Python Tuples. _W3 Schools_  [https://www.w3schools.com/python/python_tuples.asp](https://www.w3schools.com/python/python_tuples.asp)


# Technical Details
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
**Author:** Lori Ramey
