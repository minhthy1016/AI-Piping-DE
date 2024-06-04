# Beanie and Mongomock with MongoDB

This project demonstrates how to use Beanie and Mongomock to access MongoDB, handling Lead and Persona data.

## Setup

### Prerequisites

- Python 3.x
- MongoDB server running locally or on a remote server
- Libraries: Beanie, FastAPI, Uvicorn, and Mongomock

```bash
pip install -r requirements.txt
```
## Beanie Model Definitions
Define data models for Lead and Persona using Beanie in file ```server\model\data.py``` 
This will modify data schema of table Lead and table Persona in your local MongoDB. 

## MongoDB Configuration
- Local MongoDB: Ensure MongoDB is running locally.
- MongoDB Atlas: If using MongoDB Atlas, ensure you have the connection string.
Run app :

```bash
python main.py
```
The output persona data will be stored to a JSON file.


