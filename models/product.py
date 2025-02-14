from pydantic import BaseModel

class Product(BaseModel):
    product_title: str
    product_price: float  # This would be the sale price
    discount_percentage: float  # Changed to float for more precision
    weight: str
    average_rating: float
    total_ratings: int
    path_to_image: str