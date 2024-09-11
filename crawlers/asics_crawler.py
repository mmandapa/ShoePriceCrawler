from bs4 import BeautifulSoup
import re
from utils.request_helper import make_request

def crawl_asics(shoe_model, shoe_size, gender, condition):
    gender_keyword = "mens" if gender.lower() == "men" else "womens"
    url = f"https://www.asics.com/us/en-us/search/?q={gender_keyword}%20{shoe_model.replace(' ', '%20')}+{shoe_size}"

    if condition.lower() != "new":
        print("Asics's official website typically only sells new products. The condition parameter may not affect the search.")

    response = make_request(url)
    if response is None:
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    product_containers = soup.find_all('div', class_='product-tile')

    min_price = float('inf')
    min_url = None

    for container in product_containers:
        price_span = container.find('span', class_='product-price')
        if price_span:
            price_text = re.sub(r'[^\d.]', '', price_span.get_text())
            price = float(price_text) if price_text else None
            product_url = "https://www.asics.com" + container.find('a', class_='product-tile__main-image-link')['href']
            if price and price < min_price:
                min_price = price
                min_url = product_url

    return min_price, min_url
