from fastapi import FastAPI, HTTPException, Depends,Form
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


from services.cache import Cache
from services.database import Database
from services.notifier import Notifier
from services.scraper import Scraper

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN", "default_secret_token")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend's domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.post("/scrape/")
async def scrape_products(page_limit: int = Form(5), proxy: str = None, api_key: str = Depends(get_api_key)):
    scraper = Scraper(proxy)
    cache = Cache()
    db = Database()
    notifier = Notifier()

    try:
        print(page_limit)
        products, updated_count = await scraper.scrape(page_limit)
        cache.update_cache(products)
        db.store_products([p for p in products if p is not None and not cache.is_cached(p)])
        notifier.notify(updated_count)
        return {
            "status": "success",
            "updated_products": updated_count,
            "products": [p.dict() for p in products if p is not None]  # Exclude None products
        }
    finally:
        await scraper.close()  # Ensure session is closed