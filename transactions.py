# transactions.py
import os
from datetime import datetime
from read import save_inventory


def find_product(products, product_id):
    """Search product list by id, return the dictionary or None"""
    for p in products:
        if p['id'] == product_id:
            return p
    return None


def purchase_products(products):
    """Handle a sale to a customer, can buy more than one product"""
    customer = input("Enter customer name: ").strip()
    if customer == "":
        print("Customer name cannot be empty!")
        return

    cart = []
    while True:
        product_id = input("Enter product ID to buy (or 0 to finish): ").strip()
        if product_id == '0':
            break

        product = find_product(products, product_id)
        if product is None:
            print("Product not found! Try again.")
            continue

        try:
            qty = float(input(f"Enter quantity of {product['name']} ({product['unit']}): "))
        except ValueError:
            print("Invalid quantity, please enter a number!")
            continue

        if qty <= 0:
            print("Quantity must be greater than 0!")
            continue

        if qty > product['quantity']:
            print(f"Not enough stock available! Only {product['quantity']} {product['unit']} left.")
            continue

        cart.append({'product': product, 'qty': qty})
        print(f"{product['name']} added to cart.")

    if len(cart) == 0:
        print("No items purchased.")
        return

    total = 0
    invoice_lines = []
    for item in cart:
        product = item['product']
        qty = item['qty']
        amount = qty * product['rate']
        discount = 0

        if product['unit'].lower() == 'kg' and qty >= 50:
            discount = amount * 0.05
        elif product['unit'].lower() == 'pcs' and qty >= 100:
            discount = amount * 0.05

        final_amount = amount - discount
        total += final_amount
        product['quantity'] -= qty
        invoice_lines.append((product, qty, amount, discount, final_amount))

    save_inventory(products)
    invoice_file = generate_invoice("SALE", customer, invoice_lines, total)
    print(f"\nSale completed successfully. Invoice saved as {invoice_file}")


def restock_products(products):
    """Handle restocking from a supplier, can restock more than one product"""
    supplier = input("Enter supplier name: ").strip()
    if supplier == "":
        print("Supplier name cannot be empty!")
        return

    cart = []
    while True:
        product_id = input("Enter product ID to restock (or 0 to finish): ").strip()
        if product_id == '0':
            break

        product = find_product(products , product_id)
        if product is None:
            print("Product not found! Try again.")
            continue

        try:
            qty = float(input(f"Enter quantity to restock for {product['name']}: "))
        except ValueError:
            print("Invalid quantity, please enter a number!")
            continue

        if qty <= 0:
            print("Quantity must be greater than 0!")
            continue

        cart.append({'product': product, 'qty': qty})
        print(f"{product['name']} added to restock list.")

    if len(cart) == 0:
        print("No products restocked.")
        return

    total = 0
    invoice_lines = []
    for item in cart:
        product = item['product']
        qty = item['qty']
        amount = qty * product['rate']
        total += amount
        product['quantity'] += qty
        invoice_lines.append((product, qty, amount, 0, amount))

    save_inventory(products)
    invoice_file = generate_invoice("RESTOCK", supplier, invoice_lines, total)
    print(f"\nRestock completed successfully. Invoice saved as {invoice_file}")


def generate_invoice(invoice_type, name, invoice_lines, total):
    """Write a text invoice file for a sale or restock transaction"""
    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    now = datetime.now()
    invoice_id = now.strftime("%Y%m%d%H%M%S")
    filename = f"invoices/{invoice_type}_{invoice_id}.txt"

    label = "Customer" if invoice_type == "SALE" else "Supplier"

    with open(filename, 'w') as file:
        file.write("=" * 45 + "\n")
        file.write("      BUILDMART HARDWARE STORE\n")
        file.write(f"      {invoice_type} INVOICE\n")
        file.write("=" * 45 + "\n")
        file.write(f"{label} Name : {name}\n")
        file.write(f"Date          : {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("-" * 45 + "\n")

        for product, qty, amount, discount, final_amount in invoice_lines:
            file.write(f"Product   : {product['name']} ({product['brand']})\n")
            file.write(f"Quantity  : {qty} {product['unit']}\n")
            file.write(f"Rate      : Rs.{product['rate']:.2f}\n")
            file.write(f"Amount    : Rs.{amount:.2f}\n")
            if discount > 0:
                file.write(f"Discount  : Rs.{discount:.2f} (5%)\n")
            file.write(f"Sub Total : Rs.{final_amount:.2f}\n")
            file.write("-" * 45 + "\n")

        file.write(f"TOTAL AMOUNT : Rs.{total:.2f}\n")
        file.write("=" * 45 + "\n")

    return filename


def view_invoices():
    """List saved invoices and let the user open one"""
    if not os.path.exists("invoices") or len(os.listdir("invoices")) == 0:
        print("\nNo invoices found.")
        return

    files = sorted(os.listdir("invoices"))
    print(f"\nTotal Invoices: {len(files)}")
    for f in files:
        print(f" - {f}")

    choice = input("\nEnter invoice file name to view (press Enter to skip): ").strip()
    if choice == "":
        return

    path = os.path.join("invoices", choice)
    if os.path.exists(path):
        with open(path, 'r') as file:
            print("\n" + file.read())
    else:

        print("Invoice not found.")
