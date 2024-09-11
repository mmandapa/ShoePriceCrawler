from bs4 import BeautifulSoup
import re
from utils.request_helper import make_request

def crawl_ross(shoe_model, shoe_size, gender, condition):
    gender_keyword = "mens" if gender.lower() == "men" else "womens"
    url = f"https://www.rossstores.com/products?search={gender_keyword}+{shoe_model.replace(' ', '%20')}+{shoe_size}"
    response = make_request(url)
    if response is None:
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    product_containers = soup.find_all('div', class_='product-card')

    min_price = float('inf')
    min_url = None

    for container in product_containers:
        # Ross might not support direct condition filtering in the URL,
        # but if condition information is available in the product details, you can filter it here.
        product_condition = container.find('div', class_='product-condition')
        if product_condition and condition.lower() not in product_condition.get_text().lower():
            continue  # Skip this product if the condition doesn't match

        price_div = container.find('div', class_='product-card__price')
        if price_div:
            price_text = re.sub(r'[^\d.]', '', price_div.get_text())
            if re.match(r'^\d+(\.\d{1,2})?$', price_text):
                price = float(price_text)
                product_url = container.find('a', class_='product-card__link')['href']
                if not product_url.startswith("https://www.rossstores.com"):
                    product_url = "https://www.rossstores.com" + product_url
                if price < min_price:
                    min_price = price
                    min_url = product_url

    return min_price, min_url
