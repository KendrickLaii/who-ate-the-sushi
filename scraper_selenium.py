from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging
import os
from typing import List, Dict, Optional
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SeleniumScraper:
    def __init__(
        self,
        base_url: str,
        delay: float = 2.0,
        headless: bool = True
    ):
        self.base_url = base_url
        self.delay = delay
        self.driver = self._setup_driver(headless)

    def _setup_driver(self, headless: bool):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        driver_path = os.path.join(os.getcwd(), 'chromedriver-win64', 'chromedriver.exe')
        
        if not os.path.exists(driver_path):
            logger.error(f"ChromeDriver not found at {driver_path}")
            logger.info("Please run: python download_chromedriver.py")
            raise FileNotFoundError("ChromeDriver not found. Run download_chromedriver.py first.")
        
        logger.info(f"Using ChromeDriver at: {driver_path}")
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Chrome WebDriver initialized successfully")
        return driver

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            logger.info(f"Fetching with Selenium: {url}")
            self.driver.get(url)
            
            time.sleep(self.delay)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except Exception as e:
                logger.warning(f"Wait timeout: {e}")
            
            page_source = self.driver.page_source
            return BeautifulSoup(page_source, 'lxml')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def get_menu_categories(self, soup: BeautifulSoup) -> List[Dict]:
        categories = []
        
        menu_boxes = soup.find_all('div', class_='menu-icon-box')
        
        for box in menu_boxes:
            link = box.find('a', href=True)
            if link:
                category_name = link.get_text(strip=True)
                category_url = urljoin(self.base_url, link['href'])
                
                categories.append({
                    'name': category_name,
                    'url': category_url
                })
        
        logger.info(f"Found {len(categories)} menu categories")
        return categories
    
    def extract_data(self, soup: BeautifulSoup, category_name: str = None) -> List[Dict]:
        data = []
        
        items = soup.find_all('div', class_='menu-wrapper-box')
        
        if not items:
            logger.warning("No menu-wrapper-box items found")
            return data
        
        logger.info(f"Found {len(items)} menu items")
        
        for item in items:
            try:
                img_elem = item.find('img')
                span_elem = item.find('span')
                
                title = None
                price = None
                
                if span_elem:
                    text_content = span_elem.get_text(strip=True)
                    parts = text_content.split('HK$')
                    
                    if len(parts) == 2:
                        title = parts[0].strip()
                        price = f"HK${parts[1].strip()}"
                    else:
                        title = text_content
                
                image_url = None
                if img_elem:
                    image_url = img_elem.get('src') or img_elem.get('data-src')
                    if image_url and not image_url.startswith('http'):
                        image_url = urljoin(self.base_url, image_url)
                
                modal_target = item.find('div', class_='menu-img')
                item_id = None
                if modal_target:
                    item_id = modal_target.get('data-target', '').replace('#', '')
                
                if title:
                    record = {
                        'title': title,
                        'description': None,
                        'price': price,
                        'image_url': image_url,
                        'url': self.base_url,
                        'item_id': item_id,
                        'category': category_name
                    }
                    data.append(record)
            except Exception as e:
                logger.error(f"Error extracting item: {e}")
                continue
        
        logger.info(f"Extracted {len(data)} items")
        return data

    def scrape(self, url: Optional[str] = None, category_name: str = None) -> List[Dict]:
        target_url = url or self.base_url
        soup = self.fetch_page(target_url)
        
        if not soup:
            logger.error(f"Failed to fetch page: {target_url}")
            return []
        
        return self.extract_data(soup, category_name)
    
    def scrape_all_categories(self) -> List[Dict]:
        logger.info("Starting full menu scrape across all categories...")
        
        soup = self.fetch_page(self.base_url)
        if not soup:
            logger.error("Failed to fetch main menu page")
            return []
        
        categories = self.get_menu_categories(soup)
        
        all_data = []
        for i, category in enumerate(categories, 1):
            logger.info(f"\n[{i}/{len(categories)}] Scraping category: {category['name']}")
            category_data = self.scrape(category['url'], category['name'])
            all_data.extend(category_data)
            logger.info(f"  → Found {len(category_data)} items in {category['name']}")
        
        logger.info(f"\nTotal items scraped: {len(all_data)}")
        return all_data

    def scrape_multiple_pages(self, urls: List[str]) -> List[Dict]:
        all_data = []
        for url in urls:
            data = self.scrape(url)
            all_data.extend(data)
        return all_data

    def close(self):
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
