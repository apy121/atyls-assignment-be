import aiohttp
from bs4 import BeautifulSoup
import re
from models.product import Product
import os
import asyncio


class Scraper:
    def __init__(self, proxy=None):
        self.proxy = proxy
        self.session = aiohttp.ClientSession()

    async def scrape(self, page_limit):
        print(page_limit,"aa")
        products = []
        for page in range(1, page_limit + 1):
            url = f"https://dentalstall.com/shop/page/{page}/"
            try:
                async with self.session.get(url, proxy=self.proxy) as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        product_urls = self.get_product_urls(soup)
                        products.extend(await self.fetch_detailed_products(product_urls))
                    else:
                        await asyncio.sleep(5)  # Example retry mechanism
                        continue
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
        return products, len(products)

    def get_product_urls(self, soup):
        product_containers = soup.find_all('li', class_='product')
        return [container.find('h2', class_='woo-loop-product__title').a['href'] for container in product_containers if
                container.find('h2', class_='woo-loop-product__title')]

    async def fetch_detailed_products(self, urls):
        tasks = [self.fetch_product_details(url) for url in urls]
        return await asyncio.gather(*tasks)

    async def fetch_product_details(self, url):
        try:
            async with self.session.get(url, proxy=self.proxy) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    return self.parse_detailed_product(soup)
                else:
                    print(f"Failed to fetch product from {url}")
                    return None
        except Exception as e:
            print(f"Error fetching product details from {url}: {e}")
            return None

    def parse_detailed_product(self, soup):
        # Product Title
        title_elem = soup.find('h1', class_='product_title entry-title')
        product_title = title_elem.text.strip() if title_elem else "Unknown Title"

        # Product Price and Discount
        price_elem = soup.find('p', class_='price')
        if price_elem:
            price_text = price_elem.text.strip()
            # Use more specific regex patterns to match each part of the price information
            original_price_match = re.search(r'<del>.*₹([\d,]+)', price_text)
            sale_price_match = re.search(r'(?:<ins>.*₹|₹)([\d,]+)',
                                         price_text)  # Adjusted to match either <ins> or outside it
            discount_match = re.search(r'(-?\d+)%', price_text)  # Capture discount percentage

            original_price = float(original_price_match.group(1).replace(',', '')) if original_price_match else 0
            sale_price = float(sale_price_match.group(1).replace(',', '')) if sale_price_match else original_price
            discount_percentage = float(discount_match.group(1)) if discount_match else 0
        else:
            original_price = sale_price = discount_percentage = 0

        # Product Weight
        weight_elem = soup.find('td', class_='woocommerce-product-attributes-item__value')
        weight = weight_elem.text.strip() if weight_elem else "Unknown Weight"

        # Average Rating and Total Ratings
        rating_elem = soup.find('div', class_='woocommerce-product-rating')
        if rating_elem:
            average_rating_elem = rating_elem.find('span', class_='rating')
            total_ratings_elem = rating_elem.find('span', class_='count')

            if average_rating_elem:
                try:
                    average_rating = float(average_rating_elem.text)
                except ValueError:
                    average_rating = 0.0
            else:
                average_rating = 0.0

            if total_ratings_elem:
                total_ratings_text = total_ratings_elem.text.strip()
                total_ratings_match = re.search(r'\((\d+)', total_ratings_text)
                total_ratings = int(total_ratings_match.group(1)) if total_ratings_match else 0
            else:
                total_ratings = 0
        else:
            average_rating = 0.0
            total_ratings = 0

        # Image Path
        img_elem = soup.find('img', class_='wp-post-image')
        if img_elem and 'src' in img_elem.attrs:
            img_url = img_elem['src']
            img_path = img_url
        else:
            img_path = "no_image.jpg"  # Default no image path

        return Product(
            product_title=product_title,
            product_price=sale_price,
            discount_percentage=discount_percentage,
            weight=weight,
            average_rating=average_rating,
            total_ratings=total_ratings,
            path_to_image=img_path
        )

    async def close(self):
        await self.session.close()