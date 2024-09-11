import re

KNOWN_MODELS = {
    "nike": ["Air Force 1", "Air Max 90", "Air Jordan 1", "Blazer", "Dunk", "Cortez"],
    "adidas": ["Ultraboost", "NMD", "Superstar", "Stan Smith", "Yeezy"],
    "asics": ["Gel-Kayano", "Gel-Nimbus", "Gel-Lyte", "Gel-Quantum", "GT-2000"]
}

VALID_CONDITIONS = ["new", "used", "refurbished"]

def validate_model(brand, model):
    return model.lower() in [m.lower() for m in KNOWN_MODELS.get(brand, [])]

def validate_shoe_size(size):
    if re.match(r"^\d+(\.\d{1})?$", size):
        size_float = float(size)
        return 1 <= size_float <= 13
    return False

def validate_gender(gender):
    return gender.lower() in ["men", "women"]

def validate_condition(condition):
    return condition.lower() in VALID_CONDITIONS
