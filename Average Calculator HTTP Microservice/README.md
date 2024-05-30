# Average Calculator HTTP Microservice

This microservice calculates the average of numbers fetched from a test server and maintains a sliding window of a specified size.

### How to Run

1. Ensure you have Python installed on your system.
2. Run the microservice using the command `python Average Calculator.py`.

### Usage

- Send a GET request to `http://localhost:9876/numbers/{numberid}` where `{numberid}` can be 'p' for prime, 'f' for Fibonacci, 'e' for even, or 'r' for random numbers.
- The microservice will fetch numbers of the specified type from the test server, calculate the average, and return the result along with the previous and current state of the sliding window.

### Note

- Make sure to configure your access credentials in the `Average Calculator.py` file.
