from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI()

# FatSecret API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = os.getenv("TOKEN_URL")
API_URL = os.getenv("API_URL")

# Function to get OAuth 2.0 access token
def get_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "basic"
    }
    
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

# Route to fetch the OAuth 2.0 access token
@app.get("/get-token")
def fetch_token():
    token = get_access_token()
    if token:
        return {"access_token": token}
    return {"error": "Failed to retrieve access token"}

# Route to search for foods using the FatSecret API
@app.get("/search-foods/")
def search_foods(query: str = Query(..., description="Food name to search")):
    token = get_access_token()
    if not token:
        return {"error": "Authentication failed"}
    
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "method": "foods.search",
        "format": "json",
        "search_expression": query
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve food data"}


