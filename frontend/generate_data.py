"""
Generate a JavaScript data file from scraped_data.json for the frontend.
Run this script whenever the scraped data changes.
Usage: python frontend/generate_data.py
"""
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
json_path = os.path.join(project_root, 'scraped_data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Clean and normalize data
cleaned = []
for item in data:
    price_str = item.get('price', 'HK$0')
    # Extract numeric price
    price_num = 0
    if price_str:
        import re
        match = re.search(r'[\d.]+', price_str.replace(',', ''))
        if match:
            price_num = float(match.group())
    
    cleaned.append({
        'id': item.get('id', len(cleaned) + 1),
        'title': item.get('title', 'Unknown'),
        'description': item.get('description', ''),
        'price': price_num,
        'priceLabel': price_str or f'HK${price_num}',
        'imageUrl': item.get('image_url', ''),
        'category': item.get('category', 'Other'),
    })

output_path = os.path.join(script_dir, 'data.js')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('// Auto-generated from scraped_data.json\n')
    f.write('const SUSHIRO_MENU = ')
    f.write(json.dumps(cleaned, indent=2, ensure_ascii=False))
    f.write(';\n')

print(f"Generated {output_path} with {len(cleaned)} items")

# Print summary
categories = {}
for item in cleaned:
    cat = item['category']
    categories[cat] = categories.get(cat, 0) + 1

print("\nCategories:")
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count} items")
