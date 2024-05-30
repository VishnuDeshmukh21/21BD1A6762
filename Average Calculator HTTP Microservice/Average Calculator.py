from flask import Flask, request, jsonify
import requests
import time
from requests.exceptions import ConnectTimeout, RequestException

app = Flask(__name__)

# Configuration and Global Variables
ACCESS_CODE = "YourAccessCode"
BASE_URL = "http://20.244.56.144/test"
WINDOW_SIZE = 10
window = []  # Current sliding window
prev_window = []  # Previous state of the sliding window
access_token = None  # Access token for authentication

# Authentication Function
def authenticate():
    """
    Authenticate with the server to obtain an access token.
    """
    url = f"{BASE_URL}/auth"
    payload = {
    "companyName": "Keshav Memorial Institute of Technology",
    "clientID": "96ae1eb7-3426-44b1-951a-1ad027550dd2",
    "clientSecret": "FaTNMITkUABHAPaj",
    "ownerName": "Vishnu Deshmukh",
    "ownerEmail": "vishnudeshmukh1222@gmail.com",
    "rollNo": "21BD1A6762"
}
    response = requests.post(url, json=payload)
    return response.json()

# Fetch numbers from Test Server
def fetch_numbers(type):
    """
    Fetch numbers of a specific type from the server.
    """
    url = f"{BASE_URL}/{type}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    retries = 3  # Number of retries in case of connection timeout
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=0.5)
            if response.status_code == 200:
                return response.json().get("numbers", [])
        except ConnectTimeout:
            print("Connection timed out. Retrying...")
        except RequestException as e:
            print(f"Request failed: {e}")
            break
    return []

# Calculate average
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    """
    return sum(numbers) / len(numbers) if numbers else 0

@app.route('/numbers/<string:numberid>', methods=['GET'])
def get_numbers(numberid):
    """
    API endpoint to get numbers of a specified type and calculate their average.
    """
    global window, prev_window
    
    # Mapping of number types to their corresponding endpoints
    type_mapping = {
        'p': 'primes',
        'f': 'fibo',
        'e': 'even',
        'r': 'rand'
    }
    
    if numberid not in type_mapping:
        return jsonify({"error": "Invalid number ID"}), 400
    
    numbers = fetch_numbers(type_mapping[numberid])
    if not numbers:
        return jsonify({"error": "Failed to fetch numbers"}), 500
    
    prev_window = window.copy()  # Save current state of the window
    
    # Maintain unique numbers and sliding window of size WINDOW_SIZE
    for num in numbers:
        if num not in window:
            if len(window) >= WINDOW_SIZE:
                window.pop(0)  # Remove the oldest number if window is full
            window.append(num)
    
    avg = calculate_average(window)
    
    response = {
        "numbers": numbers,
        "windowPrevState": prev_window,
        "windowCurrState": window,
        "avg": avg
    }
    
    return jsonify(response)

if __name__ == '__main__':
    # Authenticate and get access token
    auth_response = authenticate()
    
    if 'access_token' in auth_response:
        access_token = auth_response['access_token']
        app.run(port=9876)
    else:
        print("Authentication failed. No access token received.")
