# display.py
import os


def clear_screen():
    """Clear the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    """Show main menu"""
    print("\n" + "=" * 50)
    print("      BUILDMART HARDWARE STORE")
    print("=" * 50)
    print("1. View All Products")
    print("2. Purchase Products")
    print("3. Restock Products")
    print("4. Invoices")
    print("5. Exit")
    print("=" * 50)


def display_products(products):
    """Show all products in a table format"""
    if not products:
        print("\nNo products found!")
        return

    print("\n" + "=" * 85)
    print("                              PRODUCT LIST")
    print("=" * 85)
    print("ID     Name                 Brand              Qty         Unit    Rate")
    print("-" * 85)

    for p in products:
        print(f"{p['id']:<6} {p['name'][:20]:20} {p['brand'][:18]:18} "
              f"{p['quantity']:<11.2f} {p['unit']:<7} Rs.{p['rate']:.2f}")

    print("=" * 85)
    print(f"Total Products: {len(products)}")
