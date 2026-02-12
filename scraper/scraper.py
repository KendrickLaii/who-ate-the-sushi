import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(
        self,
        base_url: str,
        delay: float = 1.0,
        max_retries: int = 3,
        timeout: int = 30
    ):
        self.base_url = base_url
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching: {url} (attempt {attempt + 1}/{self.max_retries})")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                time.sleep(self.delay)
                return BeautifulSoup(response.content, 'lxml')
            except requests.RequestException as e:
                logger.error(f"Error fetching {url}: {e}")
                if attempt == self.max_retries - 1:
                    return None
                time.sleep(self.delay * (attempt + 1))
        return None

    def extract_data(self, soup: BeautifulSoup) -> List[Dict]:
        data = []
        
        items = soup.find_all('li', class_='item')
        
        if not items:
            items = soup.find_all('div', class_='menu-item')
        
        if not items:
            items = soup.find_all('div', class_='item')
        
        for item in items:
            try:
                title_elem = item.find('h3') or item.find('h2') or item.find('div', class_='name')
                desc_elem = item.find('p', class_='description') or item.find('div', class_='desc')
                price_elem = item.find('span', class_='price') or item.find('div', class_='price')
                img_elem = item.find('img')
                link_elem = item.find('a', href=True)
                
                record = {
                    'title': title_elem.get_text(strip=True) if title_elem else None,
                    'description': desc_elem.get_text(strip=True) if desc_elem else None,
                    'price': price_elem.get_text(strip=True) if price_elem else None,
                    'image_url': img_elem.get('src') if img_elem else None,
                    'url': urljoin(self.base_url, link_elem['href']) if link_elem else None,
                }
                
                if record['title'] or record['description']:
                    data.append(record)
            except Exception as e:
                logger.error(f"Error extracting item: {e}")
                continue
        
        logger.info(f"Extracted {len(data)} items")
        return data

    def scrape(self, url: Optional[str] = None) -> List[Dict]:
        target_url = url or self.base_url
        soup = self.fetch_page(target_url)
        
        if not soup:
            logger.error(f"Failed to fetch page: {target_url}")
            return []
        
        return self.extract_data(soup)

    def scrape_multiple_pages(self, urls: List[str]) -> List[Dict]:
        all_data = []
        for url in urls:
            data = self.scrape(url)
            all_data.extend(data)
        return all_data

    def close(self):
        self.session.close()
