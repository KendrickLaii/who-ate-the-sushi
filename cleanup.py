import os
import shutil

files_to_remove = [
    'poster_scraper.py',
    'scrape_posters.py',
    'test_ocr.py',
    'add_promotional_items.py',
    'INSTALL_TESSERACT.md',
    'README_POSTERS.md',
    'test_sushiro.py',
    'inspect_network.py',
]

folders_to_remove = [
    'posters',
    'chromedriver-win64',
]

print("Cleaning up unnecessary files...\n")

for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
        print(f"✓ Removed: {file}")
    else:
        print(f"  Skip: {file} (not found)")

for folder in folders_to_remove:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"✓ Removed folder: {folder}")
    else:
        print(f"  Skip: {folder}/ (not found)")

print("\n✓ Cleanup complete!")
print("\nRemaining files:")
print("  - main_selenium.py (main scraper)")
print("  - scraper_selenium.py (scraper logic)")
print("  - database.py (database handler)")
print("  - add_custom_item.py (manual item entry)")
print("  - download_chromedriver.py (driver installer)")
print("  - requirements.txt (dependencies)")
print("  - scraped_data.json (your data)")
print("  - .env (configuration)")
