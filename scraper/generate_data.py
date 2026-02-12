"""
Generate TypeScript menu data file from scraped_data.json for the Vue frontend.
Run this script after scraping to update the frontend menu.
Usage: python scraper/generate_data.py
"""
import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(SCRIPT_DIR, 'scraped_data.json')
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'src', 'data', 'menu.ts')


def generate_menu_ts():
    if not os.path.exists(JSON_PATH):
        print(f"Error: {JSON_PATH} not found.")
        print("Run the scraper first: python scraper/main_selenium.py")
        return

    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned = []
    for item in data:
        price_str = item.get('price', 'HK$0') or 'HK$0'
        price_num = 0
        match = re.search(r'[\d.]+', price_str.replace(',', ''))
        if match:
            price_num = float(match.group())

        entry = {
            'id': item.get('id', len(cleaned) + 1),
            'title': item.get('title', 'Unknown'),
            'description': item.get('description', '') or '',
            'price': price_num,
            'priceLabel': price_str,
            'imageUrl': item.get('image_url', '') or '',
            'category': item.get('category', 'Other') or 'Other',
        }
        cleaned.append(entry)

    # Generate TypeScript file
    lines = [
        "import type { MenuItem } from '../types'",
        "",
        "// Auto-generated from scraped_data.json",
        f"// Generated with {len(cleaned)} items",
        "// To regenerate: python scraper/generate_data.py",
        "export const SUSHIRO_MENU: MenuItem[] = ",
    ]

    ts_content = '\n'.join(lines)
    ts_content += json.dumps(cleaned, indent=2, ensure_ascii=False)
    ts_content += '\n'

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(ts_content)

    print(f"Generated {OUTPUT_PATH} with {len(cleaned)} items")

    # Print summary
    categories = {}
    for item in cleaned:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1

    print("\nCategories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} items")


if __name__ == '__main__':
    generate_menu_ts()
