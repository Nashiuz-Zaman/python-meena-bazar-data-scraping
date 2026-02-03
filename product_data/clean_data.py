import csv
import re
from utils import resolve_csv_paths


MEENA_REGEX = re.compile(r"\b(Meena|meena)\b")


def is_url(value: str) -> bool:
    return (
        value.startswith("http://")
        or value.startswith("https://")
        or value.startswith("HTTP://")
        or value.startswith("HTTPS://")
    )


def replace_meena(match: re.Match) -> str:
    return "Bengal" if match.group(0)[0].isupper() else "bengal"


def clean_data(csv_name: str):
    input_csv_path, output_csv_path = resolve_csv_paths(
        input_csv_name=csv_name,
        replace_from="_product_data.csv",
        replace_to="_product_data_cleaned.csv",
    )

    with open(input_csv_path, mode="r", newline="", encoding="utf-8") as infile, open(
        output_csv_path, mode="w", newline="", encoding="utf-8"
    ) as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            cleaned_row = {}

            for key, value in row.items():
                if isinstance(value, str) and value and not is_url(value):
                    value = MEENA_REGEX.sub(replace_meena, value)

                cleaned_row[key] = value

            writer.writerow(cleaned_row)

    print()
    print(f"Cleaned CSV written to: {output_csv_path}")
