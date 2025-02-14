import json

class Database:
    def store_products(self, products):
        with open('products.json', 'w') as f:
            json.dump([p.dict() for p in products], f)