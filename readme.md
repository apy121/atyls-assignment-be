# Dental Stall Scraper

This is a FastAPI-based project designed to scrape dental stall product data and store it in a structured format.

## Project Structure
```
dental_stall_scraper/
│── images/                # Directory for storing scraped images
│── models/                # Directory containing database models
│   │── product.py         # Pydantic model for product data
│── services/              # Directory for service-related logic
│── venv/                  # Virtual environment directory
│── .env                   # Environment variables file
│── main.py                # Entry point for FastAPI application
│── products.json          # JSON file to store scraped product data
│── requirements.txt       # Dependencies list
```

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/apy121/atyls-assignment-be.git
cd dental_stall_scraper
```

### 2. Create and Activate a Virtual Environment
#### On macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```
#### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 5. Run the FastAPI Application
```sh
uvicorn main:app --reload
```

### 6. Access the API Documentation
Once the server is running, open your browser and go to:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


## Running Tests
To run tests (if any are included), use:
```sh
pytest
```

## Get Scrap Data CURL
To run tests (if any are included), use:
```sh
curl --location 'http://127.0.0.1:8000/scrape/' \
--header 'X-API-Key: default_secret_token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'page_limit=5'
```

## Contributing
Feel free to submit issues or pull requests for improvements.

## License
This project is licensed under the MIT License.

