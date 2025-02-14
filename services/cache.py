class Cache:
    def __init__(self):
        self.cached_products = {}

    def update_cache(self, products):
        for product in products:
            if product is not None:  # Check if product is not None
                self.cached_products[product.product_title] = product.product_price

    def is_cached(self, product):
        return product.product_title in self.cached_products and product.product_price == self.cached_products[product.product_title]