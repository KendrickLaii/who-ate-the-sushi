import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TARGET_URL = os.getenv('TARGET_URL', 'https://example.com')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///scraped_data.db')
    REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', '1'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    TIMEOUT = int(os.getenv('TIMEOUT', '30'))
    
    @classmethod
    def validate(cls):
        if not cls.TARGET_URL:
            raise ValueError("TARGET_URL must be set")
        if cls.REQUEST_DELAY < 0:
            raise ValueError("REQUEST_DELAY must be non-negative")
        if cls.MAX_RETRIES < 1:
            raise ValueError("MAX_RETRIES must be at least 1")
        if cls.TIMEOUT < 1:
            raise ValueError("TIMEOUT must be at least 1")
