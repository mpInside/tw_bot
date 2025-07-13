import os
from datetime import datetime
import time
import traceback
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from logger import setup_logger

logger = setup_logger('tradingview')

@contextmanager
def create_driver(options):
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        yield driver
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def get_tradingview_screenshot(ticker: str) -> str:
    """
    Get a screenshot from TradingView for a given ticker.
    Returns the path to the saved screenshot.
    """
    try:
        # Create screenshots directory if it doesn't exist
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshots_dir}/{ticker}_{timestamp}.png"

        logger.info("Initializing Chrome driver...")
        # Configure Chrome options
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        with create_driver(options) as driver:
            logger.info("Chrome driver initialized successfully")

            # Navigate to TradingView
            url = f"https://www.tradingview.com/chart/?symbol={ticker}&interval=1H"
            logger.info(f"Navigating to {url}")
            driver.get(url)

            logger.info("Waiting for chart to load...")
            # Wait for the chart to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chart-container"))
            )

            logger.info("Chart loaded, waiting additional time...")
            # Additional wait to ensure chart is fully loaded
            time.sleep(5)

            logger.info("Taking screenshot...")
            # Take screenshot
            driver.save_screenshot(filename)
            logger.info(f"Screenshot saved to {filename}")
            return filename

    except Exception as e:
        logger.error(f"Error getting screenshot: {str(e)}")
        logger.error("Full traceback:")
        logger.error(traceback.format_exc())
        return None 