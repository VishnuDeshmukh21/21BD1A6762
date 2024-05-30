# Top Products HTTP Microservice

This microservice retrieves top products from multiple e-commerce companies and provides them through a REST API.

### How to Run

1. Ensure you have Python installed on your system.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the microservice using the command `python Top Products.py`.

### Usage

- Send a GET request to `http://localhost:9876/categories/{categoryname}/products` to retrieve top products within a specified category.
- You can specify additional query parameters like `top`, `minPrice`, `maxPrice`, `sortBy`, and `sortOrder` for customization.

### Note

- Make sure to configure your access credentials in the `Top Products.py` file.
