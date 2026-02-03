import csv
import requests
import time
from typing import Dict, Any
from utils import process_multiple_images, resolve_csv_paths

# API key → CSV header mapping
API_TO_CSV_MAP = {
    "ItemCategoryName": "itemCategoryName",
    "CategoryDisplayName": "categoryDisplayName",
    "ItemSubCategoryName": "itemSubCategoryName",
    "SubCategoryDisplayName": "subCategoryDisplayName",
    "ItemBrandName": "itemBrandName",
    "BrandDisplayName": "brandDisplayName",
    "ItemSlug": "itemSlug",
    "ItemDisplayName": "itemDisplayName",
    "Unit": "unit",
    "UnitSalesPrice": "unitSalesPrice",
    "UnitDiscount": "unitDiscount",
    "DiscountSalesPrice": "discountSalesPrice",
    "ItemDetails": "itemDetails",
    "ImageUrl": "imageUrl",
    "fullimageURl": "fullImageUrl",
    "multipleImageData": "multipleImageData",
    "UnitConvert": "unitConvert",
}


def get_product_data(csv_name: str):
    input_csv_path, output_csv_path = resolve_csv_paths(
        input_csv_name=csv_name,
        replace_from="_urls.csv",
        replace_to="_product_data.csv",
    )

    print("")
    print("Started fetching data...")
    print("Input CSV :", str(input_csv_path).split("\\")[-1])
    print("Output CSV:", str(output_csv_path).split("\\")[-1])

    rows_to_write = []

    with open(input_csv_path, newline="", encoding="utf-8") as read_file:
        reader = list(csv.DictReader(read_file))
        total = len(reader)

        for i, row in enumerate(reader, start=1):
            api_url = row.get("API_URL")
            if not api_url:
                continue

            try:
                response = requests.get(api_url, timeout=15)
                response.raise_for_status()
                payload = response.json()

                product: Dict[str, Any] = payload.get("data", {}).get("product", {})

                # Extract only the fields we need
                extracted_row = {}
                for api_key, csv_key in API_TO_CSV_MAP.items():
                    value = product.get(api_key)
                    if api_key == "multipleImageData":
                        # Process multipleImageData using utility function
                        value = process_multiple_images(value)
                    extracted_row[csv_key] = value

                rows_to_write.append(extracted_row)

                print(f"\r✅ Products processed: {i}/{total}", end="")
                time.sleep(1)

            except requests.RequestException as e:
                print(f"\n❌ Request failed for {api_url}: {e}")
            except ValueError as e:
                print(f"\n❌ JSON error for {api_url}: {e}")

    print("\nWriting CSV...")

    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=list(API_TO_CSV_MAP.values()))
        writer.writeheader()
        writer.writerows(rows_to_write)

    print(f"Done! Saved {len(rows_to_write)} products.")
