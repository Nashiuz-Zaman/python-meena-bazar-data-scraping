from playwright.sync_api import sync_playwright
import sys
import csv
import os
import time
from utils import scroll_until_done


def collect_product_urls(url: str, csv_name: str):
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv_data")
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, csv_name)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        )

        page = context.new_page()

        # 1. Initial navigation to establish the domain context
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle")

        # 2. Inject LocalStorage to bypass location selection
        print("Injecting delivery location context...")
        page.evaluate(
            """() => {
            localStorage.setItem('area_id', '234');
            localStorage.setItem('area_thana_district', 'Eastern Housing, Mirpur, Dhaka');
            localStorage.setItem('subunit_id', '1100');
            localStorage.setItem('cart', '[]');
            localStorage.setItem('cart_obj', JSON.stringify({"CartId":"","SubUnitId":"1100","AreaId":"10"}));
        }"""
        )

        # 3. Reload to apply changes and trigger product loading
        page.reload(wait_until="networkidle")
        time.sleep(2)  # Short buffer for Angular to boot

        print("Page reloaded with location. Starting infinite scroll...")
        scroll_until_done(page)

        time.sleep(2)

        # Extraction logic
        selector = "app-thumb a"
        product_urls = page.locator(selector).evaluate_all(
            "elements => elements.map(el => el.href)"
        )

        # 2. Clean: Remove duplicates, empty strings, and the base URL
        current_url = page.url
        clean_urls = [
            unique_url
            for unique_url in dict.fromkeys(product_urls)  # deduplicate
            if unique_url and unique_url.strip() != "" and unique_url != current_url
        ]

        # 3. Prepare data with API_URL column
        data_rows = []
        for url in clean_urls:
            # Extract the last two parts from the product URL
            parts = url.rstrip("/").split("/")
            product_name = parts[-2]
            product_id = parts[-1]

            api_url = f"https://mbonlineapi.com/api/front/products/{product_id}/{product_name}?SubUnitId=1100&AreaId=234"

            data_rows.append({"URL": url, "API_URL": api_url})

        # 4. Write both columns to CSV
        with open(csv_path, mode="w", newline="", encoding="utf-8") as write_file:
            fieldnames = ["URL", "API_URL"]
            writer = csv.DictWriter(write_file, fieldnames=fieldnames)

            writer.writeheader()  # write the header row
            for i, row in enumerate(data_rows, start=1):
                writer.writerow(row)
                # CLI progress
                print(f"\rProducts done: {i}/{len(data_rows)}", end="")
                sys.stdout.flush()  # force print

        print()
        print(f"Successfully saved {len(clean_urls)} URLs ✅")
        browser.close()
