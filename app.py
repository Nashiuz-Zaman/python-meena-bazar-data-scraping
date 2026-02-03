import sys
from product_urls import collect_product_urls
from product_data import get_product_data, clean_data
from utils import get_valid_csv_name


def show_menu():
    print("\nWhat do you want to do?")
    print("1. Collect Product URLs")
    print("2. Get Products Data")
    print("3. Clean Data")
    print("4. Exit")


def handle_collect_product_urls():
    url = input("Enter category URL: ").strip()
    if not url:
        print("❌ URL cannot be empty. Returning to menu.")
        return

    csv_name = get_valid_csv_name("Enter CSV filename (e.g., meat_urls.csv): ")
    if not csv_name:
        return

    try:
        collect_product_urls(url, csv_name)
        print(f"✅ URLs successfully saved to {csv_name}")
    except Exception as e:
        print(f"❌ Failed to collect URLs: {e}")

    input("\nPress Enter to return to the menu...")


def handle_get_products_data():
    csv_name = get_valid_csv_name("Enter CSV filename (e.g., meat_urls.csv): ")
    if not csv_name:
        return

    try:
        get_product_data(csv_name)
    except Exception as e:
        print(f"❌ Failed to get data: {e}")

    input("\nPress Enter to return to the menu...")


def handle_clean_data():
    csv_name = get_valid_csv_name(
        "Enter product data CSV filename (e.g., meat_product_data.csv): "
    )
    if not csv_name:
        return

    try:
        clean_data(csv_name)
        print("✅ Data cleaned successfully.")
    except Exception as e:
        print(f"❌ Failed to clean data: {e}")

    input("\nPress Enter to return to the menu...")


def main():
    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            handle_collect_product_urls()
        elif choice == "2":
            handle_get_products_data()
        elif choice == "3":
            handle_clean_data()
        elif choice == "4":
            print("👋 Bye!")
            sys.exit()
        else:
            print("❌ Invalid choice, try again.")


if __name__ == "__main__":
    main()
