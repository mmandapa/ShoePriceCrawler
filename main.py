from utils.input_validation import validate_model, validate_shoe_size, validate_gender, validate_condition, KNOWN_MODELS

from crawlers.ebay_crawler import crawl_ebay
from crawlers.ross_crawler import crawl_ross
from crawlers.nike_crawler import crawl_nike
from crawlers.adidas_crawler import crawl_adidas
from crawlers.asics_crawler import crawl_asics


def main():
    while True:
        brand = input("Which brand are you looking for (Nike, Adidas, Asics)? ").lower()
        if brand in KNOWN_MODELS:
            break
        else:
            print("Invalid brand. Please choose 'Nike', 'Adidas', or 'Asics'.")

    while True:
        shoe_model = input(f"Enter the {brand.capitalize()} shoe model ({', '.join(KNOWN_MODELS[brand])}): ")
        if validate_model(brand, shoe_model):
            break
        else:
            print(f"Invalid {brand.capitalize()} model. Please choose from: {', '.join(KNOWN_MODELS[brand])}")

    while True:
        gender = input("Enter the gender (Men/Women): ")
        if validate_gender(gender):
            break
        else:
            print("Invalid gender. Please enter 'Men' or 'Women'.")

    while True:
        shoe_size = input("Enter your shoe size (between 1 and 13): ")
        if validate_shoe_size(shoe_size):
            break
        else:
            print("Invalid shoe size. Please enter a valid size between 1 and 13.")

    while True:
        condition = input("Enter the condition of the shoe (Options: New, Used, Refurbished): ").lower()
        if validate_condition(condition):
            break
        else:
            print("Invalid condition. Please choose from 'New', 'Used', or 'Refurbished'.")

    print(f"Searching for the best price for the {shoe_model} in {condition.capitalize()} condition...")

    crawlers = {
        "ebay": crawl_ebay,
        "ross": crawl_ross,
        "nike": crawl_nike,
        "adidas": crawl_adidas,
        "asics": crawl_asics
    }

    min_price = float('inf')
    min_url = None

    for site in ["ebay", "ross", brand]:
        price, url = crawlers[site](shoe_model, shoe_size, gender, condition)
        if price is not None and url is not None and price < min_price:
            min_price = price
            min_url = url

    if min_price < float('inf') and min_url:
        print(f"The best price found is ${min_price:.2f}. You can buy it here: [Best Shoes for You]({min_url})")
    else:
        print("Sorry, no matching products were found.")


if __name__ == "__main__":
    main()
