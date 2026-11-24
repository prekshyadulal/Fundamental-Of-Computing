# read.py

def read_inventory(filename="hardware.txt"):
    """Read products from the file and return a list of dictionaries"""
    products = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    if len(parts) >= 6:
                        product = {
                            'id': parts[0].strip(),
                            'name': parts[1].strip(),
                            'brand': parts[2].strip(),
                            'quantity': float(parts[3].strip()),
                            'unit': parts[4].strip(),
                            'rate': float(parts[5].strip())
                        }
                        products.append(product)
    except FileNotFoundError:
        print("Error: hardware.txt file not found!")
        return []
    return products


def save_inventory(products, filename="hardware.txt"):
    """Save the current product list back to the file"""
    with open(filename, 'w') as file:
        for p in products:
            line = f"{p['id']}, {p['name']}, {p['brand']}, {p['quantity']}, {p['unit']}, {p['rate']}\n"
            file.write(line)
