import os
import logging
from database import JSONDatabase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def add_custom_item():
    """
    Interactive script to manually add promotional items.
    """
    
    print("\n=== Add Promotional Item ===\n")
    
    title = input("Item name (Chinese): ").strip()
    if not title:
        print("Title is required!")
        return
    
    price = input("Price (e.g., HK$12): ").strip()
    if not price.startswith('HK$'):
        price = f"HK${price}"
    
    description = input("Description (optional): ").strip() or None
    
    item = {
        'title': title,
        'price': price,
        'description': description,
        'category': 'Promotional',
        'source': 'manual',
        'url': 'https://sushirohk.com.hk',
        'image_url': None,
        'item_id': None
    }
    
    print("\n--- Item to add ---")
    print(f"Title: {item['title']}")
    print(f"Price: {item['price']}")
    print(f"Description: {item['description']}")
    print(f"Category: {item['category']}")
    
    confirm = input("\nAdd this item? (y/n): ").strip().lower()
    
    if confirm == 'y':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db = JSONDatabase(os.path.join(script_dir, 'scraped_data.json'))
        saved = db.save_data([item])
        
        if saved > 0:
            logger.info(f"✓ Item added successfully!")
            logger.info(f"Total records in database: {db.count_records()}")
        else:
            logger.warning("Item already exists (duplicate)")
        
        db.close()
    else:
        print("Cancelled")
    
    add_more = input("\nAdd another item? (y/n): ").strip().lower()
    if add_more == 'y':
        add_custom_item()


if __name__ == "__main__":
    add_custom_item()
