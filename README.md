# Autonomous Robots Floor

## Project Description
Inspired by Amazon's Smart Fulfillment Centers, AR Floor employs algorithms to guide robots in efficiently retrieving items and delivering them to workstations.

## Example Videos
- [Video 1](https://www.youtube.com/watch?v=Jh27vjAhE-c)
- [Video 2](https://www.youtube.com/watch?v=LDhJ5I89H_I)

## Tech Stack
- **Backend:** Python
- **Testing:** pytest
- **Dependency Management:** Poetry
- **CI/CD:** GitHub Actions

## A* Algorithm Implementation
AR Floor uses the A* (A-star) algorithm for its pathfinding logic. This algorithm optimally calculates the shortest path from point A to B while taking into account various constraints like obstacles. It is highly efficient and ensures that the robots navigate through the floor in the best way possible.

## How to Run the Project

### Clone the Repository
```
git clone https://github.com/MarcGroc/AR-floor
```

### Navigate to Project Directory
```
cd AR-Floor
```
### Install Poetry if you haven't
```
pip install poetry
```
### Install Dependencies
```
poetry install
```
### Activate Virtual Environment
```poetry shell```
### Run the Application
```
python src/run.py
```

#### If You're using Pycharm mark ```src/``` directory as a source directory.