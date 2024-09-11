from bs4 import BeautifulSoup
import re
from utils.request_helper import make_request


def crawl_ebay(shoe_model, shoe_size, gender, condition):
    gender_keyword = f"{gender}'s" if gender.lower() == "men" else "womens"
    condition_keyword = f"&LH_ItemCondition={condition_mapping(condition)}"
    url = f"https://www.ebay.com/sch/i.html?_nkw={gender_keyword}+{shoe_model.replace(' ', '+')}+{shoe_size}{condition_keyword}"

    response = make_request(url)
    if response is None:
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    product_containers = soup.find_all('li', class_='s-item')

    min_price = float('inf')
    min_url = None

    for container in product_containers:
        price_span = container.find('span', class_='s-item__price')
        if price_span:
            price_text = re.sub(r'[^\d.]', '', price_span.get_text())
            if re.match(r'^\d+(\.\d{1,2})?$', price_text):
                price = float(price_text)
                product_url = container.find('a', class_='s-item__link')['href']
                if price < min_price:
                    min_price = price
                    min_url = product_url

    return min_price, min_url


def condition_mapping(condition):
    """Maps the condition to eBay's specific query parameters."""
    condition = condition.lower()
    return {
        "new": "1000",
        "used": "3000",
        "refurbished": "2000"
    }.get(condition, "1000")  # Default to "new" if the condition is not recognized
