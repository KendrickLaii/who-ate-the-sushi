import json
import os
from datetime import datetime
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class JSONDatabase:
    def __init__(self, json_file: str = 'scraped_data.json'):
        self.json_file = json_file
        self.data = self._load_data()
        logger.info(f"JSON database initialized: {json_file}")

    def _load_data(self) -> List[Dict]:
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data)} existing records")
                    return data
            except json.JSONDecodeError as e:
                logger.error(f"Error reading JSON file: {e}")
                return []
            except Exception as e:
                logger.error(f"Error loading data: {e}")
                return []
        return []

    def _save_to_file(self):
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Data saved to {self.json_file}")
        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            raise

    def save_data(self, data: List[Dict]) -> int:
        saved_count = 0
        skipped_count = 0
        
        existing_items = {(item.get('title'), item.get('price')) for item in self.data}
        
        for item in data:
            url = item.get('url')
            item_key = (item.get('title'), item.get('price'))
            
            if item_key in existing_items:
                logger.debug(f"Skipping duplicate: {item.get('title')}")
                skipped_count += 1
                continue
            
            record = {
                'id': len(self.data) + 1,
                'title': item.get('title'),
                'description': item.get('description'),
                'price': item.get('price'),
                'image_url': item.get('image_url'),
                'url': url,
                'item_id': item.get('item_id'),
                'category': item.get('category'),
                'scraped_at': datetime.utcnow().isoformat()
            }
            
            self.data.append(record)
            existing_items.add(item_key)
            saved_count += 1
        
        if saved_count > 0:
            self._save_to_file()
        
        logger.info(f"Saved {saved_count} records, skipped {skipped_count} duplicates")
        return saved_count

    def get_all_data(self) -> List[Dict]:
        return self.data

    def get_data_by_id(self, record_id: int) -> Optional[Dict]:
        for record in self.data:
            if record.get('id') == record_id:
                return record
        return None

    def count_records(self) -> int:
        return len(self.data)

    def clear_all_data(self):
        self.data = []
        self._save_to_file()
        logger.info("All data cleared from database")

    def close(self):
        logger.info("JSON database closed")
