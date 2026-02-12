import os
import logging
from dotenv import load_dotenv
from scraper import WebScraper
from database import JSONDatabase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    
    target_url = os.getenv('TARGET_URL', 'https://example.com')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.getenv('JSON_FILE', os.path.join(script_dir, 'scraped_data.json'))
    request_delay = float(os.getenv('REQUEST_DELAY', '1'))
    max_retries = int(os.getenv('MAX_RETRIES', '3'))
    timeout = int(os.getenv('TIMEOUT', '30'))
    
    logger.info("Starting web scraper...")
    logger.info(f"Target URL: {target_url}")
    logger.info(f"JSON file: {json_file}")
    
    scraper = WebScraper(
        base_url=target_url,
        delay=request_delay,
        max_retries=max_retries,
        timeout=timeout
    )
    
    db = JSONDatabase(json_file)
    
    try:
        logger.info("Beginning scrape operation...")
        data = scraper.scrape()
        
        if data:
            logger.info(f"Scraped {len(data)} items")
            saved = db.save_data(data)
            logger.info(f"Successfully saved {saved} new records")
            
            total_records = db.count_records()
            logger.info(f"Total records in database: {total_records}")
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
