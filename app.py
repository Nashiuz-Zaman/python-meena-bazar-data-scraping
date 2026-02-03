import sys
from product_urls.collect_product_urls import collect_product_urls
from product_data.get_product_data import get_product_data


def show_menu():
    print("\nWhat do you want to do?")
    print("1. Collect Product URLs")
    print("2. Get Products Data")
    print("3. Exit")


def handle_collect_product_urls():
    url = input("Enter category URL: ").strip()
    if not url:
        print("❌ URL cannot be empty. Returning to menu.")
        return

    csv_name = input("Enter CSV filename (e.g., meat_urls.csv): ").strip()
    if not csv_name:
        print("❌ CSV filename cannot be empty. Returning to menu.")
        return

    if not csv_name.endswith(".csv"):
        csv_name += ".csv"

    try:
        collect_product_urls(url, csv_name)
        print(f"✅ URLs successfully saved to {csv_name}")
    except Exception as e:
        print(f"❌ Failed to collect URLs: {e}")

    input("\nPress Enter to return to the menu...")


def get_products_data():
    csv_name = input("Enter CSV filename (e.g., meat_urls.csv): ").strip()
    if not csv_name:
        print("❌ CSV filename cannot be empty. Returning to menu.")
        return

    try:
        get_product_data(csv_name)
    except Exception as e:
        print(f"❌ Failed get data: {e}")

    input("\nPress Enter to return to the menu...")


def main():
    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            handle_collect_product_urls()
        elif choice == "2":
            get_products_data()
        elif choice == "3":
            print("👋 Bye!")
            sys.exit()
        else:
            print("❌ Invalid choice, try again.")


if __name__ == "__main__":
    main()
