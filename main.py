# main.py
from display import clear_screen, display_menu, display_products
from read import read_inventory
from transactions import purchase_products, restock_products, view_invoices

def main():
    """Main program"""
    products = read_inventory()

    while True:
        clear_screen()
        display_menu()

        choice = input("Enter choice (1-5): ").strip()

        if choice == '1':
            display_products(products)
            input("\nPress Enter to continue...")

        elif choice == '2':
            display_products(products)
            purchase_products(products)
            input("\nPress Enter to continue...")

        elif choice == '3':
            display_products(products)
            restock_products(products)
            input("\nPress Enter to continue...")

        elif choice == '4':
            view_invoices()
            input("\nPress Enter to continue...")

        elif choice == '5':
            print("\nThank you for using BuildMart System!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
