import requests
import zipfile
import os
import shutil
import subprocess

def get_chrome_version():
    try:
        result = subprocess.run(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            capture_output=True,
            text=True
        )
        version = result.stdout.split()[-1]
        return version
    except:
        return "144.0.7559.133"

def download_chromedriver():
    chrome_version = get_chrome_version()
    major_version = chrome_version.split('.')[0]
    
    print(f"Chrome version detected: {chrome_version}")
    print(f"Downloading ChromeDriver for version {chrome_version}...")
    
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"
    
    print(f"Download URL: {url}")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to download. Trying latest stable...")
        url = "https://storage.googleapis.com/chrome-for-testing-public/144.0.7559.133/win64/chromedriver-win64.zip"
        response = requests.get(url)
    
    if response.status_code == 200:
        zip_path = "chromedriver-win64.zip"
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded successfully!")
        
        if os.path.exists('chromedriver'):
            shutil.rmtree('chromedriver')
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')
        
        os.remove(zip_path)
        
        driver_path = os.path.join(os.getcwd(), 'chromedriver-win64', 'chromedriver.exe')
        print(f"\nChromeDriver installed at: {driver_path}")
        print(f"File exists: {os.path.exists(driver_path)}")
        return driver_path
    else:
        print(f"Failed to download ChromeDriver. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    download_chromedriver()
