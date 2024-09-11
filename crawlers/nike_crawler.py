from bs4 import BeautifulSoup
import re
from utils.request_helper import make_request


def crawl_nike(shoe_model, shoe_size, gender, condition):
    gender_keyword = "mens" if gender.lower() == "men" else "womens"
    url = f"https://www.nike.com/w?q={gender_keyword}%20{shoe_model.replace(' ', '%20')}+{shoe_size}"

    # Inform the user that Nike typically only sells new products
    if condition.lower() != "new":
        print(
            "Nike's official website typically only sells new products. The condition parameter may not affect the search.")

    response = make_request(url)
    if response is None:
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    product_containers = soup.find_all('div', class_='product-card__body')

    min_price = float('inf')
    min_url = None

    for container in product_containers:
        price_div = container.find('div', class_='product-price')
        if price_div:
            price_text = re.sub(r'[^\d.]', '', price_div.get_text())
            price = float(price_text) if price_text else None
            product_url = container.find('a', class_='product-card__link-overlay')['href']
            if not product_url.startswith("https://www.nike.com"):
                product_url = "https://www.nike.com" + product_url
            if price and price < min_price:
                min_price = price
                min_url = product_url

    return min_price, min_url
