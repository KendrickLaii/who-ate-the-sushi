"""
Generate data.js from scraped_data.json and serve the frontend.
Usage: python frontend/serve.py
"""
import json
import os
import re
import http.server
import socketserver
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(PROJECT_ROOT, 'scraped_data.json')
DATA_JS_PATH = os.path.join(SCRIPT_DIR, 'data.js')
PORT = 3000


def generate_data_js():
    """Generate data.js from scraped_data.json"""
    if not os.path.exists(JSON_PATH):
        print(f"Warning: {JSON_PATH} not found. Using empty menu.")
        with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
            f.write('const SUSHIRO_MENU = [];\n')
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

    with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
        f.write('// Auto-generated from scraped_data.json\n')
        f.write('const SUSHIRO_MENU = ')
        f.write(json.dumps(cleaned, indent=2, ensure_ascii=False))
        f.write(';\n')

    print(f"Generated data.js with {len(cleaned)} items")

    categories = {}
    for item in cleaned:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1
    print("\nCategories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} items")


def serve():
    """Start a local HTTP server"""
    os.chdir(SCRIPT_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\nServing at {url}")
        print("Press Ctrl+C to stop\n")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        httpd.serve_forever()


if __name__ == '__main__':
    generate_data_js()
    serve()
