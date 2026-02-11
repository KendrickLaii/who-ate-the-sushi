import os
import logging
from dotenv import load_dotenv
from scraper_selenium import SeleniumScraper
from database import JSONDatabase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    
    target_url = os.getenv('TARGET_URL', 'https://example.com')
    json_file = os.getenv('JSON_FILE', 'scraped_data.json')
    request_delay = float(os.getenv('REQUEST_DELAY', '2'))
    
    logger.info("Starting Selenium web scraper...")
    logger.info(f"Target URL: {target_url}")
    logger.info(f"JSON file: {json_file}")
    
    scraper = SeleniumScraper(
        base_url=target_url,
        delay=request_delay,
        headless=True
    )
    
    db = JSONDatabase(json_file)
    
    try:
        logger.info("Beginning scrape operation...")
        data = scraper.scrape_all_categories()
        
        if data:
            logger.info(f"Scraped {len(data)} items")
            saved = db.save_data(data)
            logger.info(f"Successfully saved {saved} new records")
            
            total_records = db.count_records()
            logger.info(f"Total records in database: {total_records}")
            
            logger.info("\n=== Sample of scraped data ===")
            for i, item in enumerate(data[:5], 1):
                logger.info(f"\nItem {i}:")
                logger.info(f"  Category: {item.get('category')}")
                logger.info(f"  Title: {item.get('title')}")
                logger.info(f"  Price: {item.get('price')}")
                desc = item.get('description') or ''
                logger.info(f"  Description: {desc[:50] if desc else 'N/A'}...")
        else:
            logger.warning("No data scraped")
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
    finally:
        scraper.close()
        db.close()
        logger.info("Scraper finished")


if __name__ == "__main__":
    main()
