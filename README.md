# made with luv special for yandex 💛

# Project Setup

This project is a test automation suite for the Petstore API.

## Installation

1. Clone the repository:
   ```sh
   git clone github.com/beccapana/yandex_tests
   cd yandex_tests
   ```
   or use GitHub Desktop like me:)
   
3. Create a virtual environment (optional):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

- The API endpoint is defined in `config.py`:
  ```python
  ENDPOINT = "https://petstore.swagger.io/v2"
  ```
- Pairwise data files are located in `test_cases/`:
  - `NewPetPos.xlsx` (positive test cases)
  - `NewPetNeg.xlsx` (negative test cases)

## Running Tests

To run all tests, use:
```sh
pytest tests_petstore.py
```