from flask import Flask, request, jsonify
import requests
import hashlib
from requests.exceptions import ConnectTimeout, RequestException

app = Flask(__name__)

# Configuration and Global Variables
BASE_URL = "http://20.244.56.144/test"
PAGE_SIZE = 10
access_token = None

# Authentication Function
def authenticate():
    url = f"{BASE_URL}/auth"
    payload ={
    "companyName": "Keshav Memorial Institute of Technology",
    "clientID": "96ae1eb7-3426-44b1-951a-1ad027550dd2",
    "clientSecret": "FaTNMITkUABHAPaj",
    "ownerName": "Vishnu Deshmukh",
    "ownerEmail": "vishnudeshmukh1222@gmail.com",
    "rollNo": "21BD1A6762"
}
    response = requests.post(url, json=payload)
    return response.json()

# Fetch products from Test Server
def fetch_products(company, category, top, minPrice, maxPrice):
    url = f"{BASE_URL}/companies/{company}/categories/{category}/products"
    params = {
        "top": top,
        "minPrice": minPrice,
        "maxPrice": maxPrice
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    retries = 3
    for _ in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=0.5)
            if response.status_code == 200:
                return response.json()
        except ConnectTimeout:
            print("Connection timed out. Retrying...")
        except RequestException as e:
            print(f"Request failed: {e}")
            break
    return []

# Generate unique product ID
def generate_product_id(product):
    product_string = f"{product['productName']}-{product['price']}-{product['rating']}"
    return hashlib.md5(product_string.encode()).hexdigest()

@app.route('/categories/<string:categoryname>/products', methods=['GET'])
def get_products(categoryname):
    top = int(request.args.get('top', 10))
    page = int(request.args.get('page', 1))
    minPrice = int(request.args.get('minPrice', 0))
    maxPrice = int(request.args.get('maxPrice', float('inf')))
    sort_by = request.args.get('sortBy', 'price')
    sort_order = request.args.get('sortOrder', 'asc')
    
    companies = ["AMZ", "FLP", "SNP", "MYN", "AZO"]
    all_products = []
    
    for company in companies:
        products = fetch_products(company, categoryname, top, minPrice, maxPrice)
        for product in products:
            product['id'] = generate_product_id(product)
            product['company'] = company
        all_products.extend(products)
    
    # Sort products
    reverse_order = (sort_order == 'desc')
    all_products.sort(key=lambda x: x[sort_by], reverse=reverse_order)
    
    # Paginate results
    start_index = (page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    paginated_products = all_products[start_index:end_index]
    
    response = {
        "products": paginated_products,
        "total": len(all_products),
        "page": page,
        "pageSize": PAGE_SIZE
    }
    
    return jsonify(response)

@app.route('/categories/<string:categoryname>/products/<string:productid>', methods=['GET'])
def get_product_details(categoryname, productid):
    companies = ["AMZ", "FLP", "SNP", "MYN", "AZO"]
    for company in companies:
        products = fetch_products(company, categoryname, 100, 0, float('inf'))
        for product in products:
            if generate_product_id(product) == productid:
                return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    # Authenticate and get access token
    auth_response = authenticate()
    
    if 'access_token' in auth_response:
        access_token = auth_response['access_token']
        app.run(port=9876)
    else:
        print("Authentication failed. No access token received.")
