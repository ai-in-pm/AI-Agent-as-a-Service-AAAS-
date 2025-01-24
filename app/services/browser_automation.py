from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from playwright.sync_api import sync_playwright
import logging
from typing import Optional, Dict, Any, List
import json
import asyncio
from contextlib import asynccontextmanager

class BrowserAutomationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._selenium_driver = None
        self._playwright = None
        self._playwright_browser = None

    async def init_selenium(self):
        """
        Initialize Selenium WebDriver
        """
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run in headless mode
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self._selenium_driver = webdriver.Chrome(options=options)
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Selenium: {str(e)}")
            return False

    async def init_playwright(self):
        """
        Initialize Playwright
        """
        try:
            self._playwright = sync_playwright().start()
            self._playwright_browser = self._playwright.chromium.launch(
                headless=True
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Playwright: {str(e)}")
            return False

    async def selenium_navigate(self, url: str) -> Dict[str, Any]:
        """
        Navigate to a URL using Selenium
        """
        try:
            if not self._selenium_driver:
                await self.init_selenium()
            
            self._selenium_driver.get(url)
            return {
                "status": "success",
                "title": self._selenium_driver.title,
                "current_url": self._selenium_driver.current_url
            }
        except Exception as e:
            self.logger.error(f"Selenium navigation failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def playwright_navigate(self, url: str) -> Dict[str, Any]:
        """
        Navigate to a URL using Playwright
        """
        try:
            if not self._playwright_browser:
                await self.init_playwright()
            
            page = self._playwright_browser.new_page()
            page.goto(url)
            return {
                "status": "success",
                "title": page.title(),
                "current_url": page.url
            }
        except Exception as e:
            self.logger.error(f"Playwright navigation failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def selenium_screenshot(self, selector: Optional[str] = None) -> bytes:
        """
        Take a screenshot using Selenium
        """
        try:
            if not self._selenium_driver:
                await self.init_selenium()
            
            if selector:
                element = self._selenium_driver.find_element(By.CSS_SELECTOR, selector)
                return element.screenshot_as_png
            return self._selenium_driver.get_screenshot_as_png()
        except Exception as e:
            self.logger.error(f"Screenshot failed: {str(e)}")
            return None

    async def playwright_screenshot(self, selector: Optional[str] = None) -> bytes:
        """
        Take a screenshot using Playwright
        """
        try:
            if not self._playwright_browser:
                await self.init_playwright()
            
            page = self._playwright_browser.new_page()
            if selector:
                element = page.locator(selector)
                return element.screenshot()
            return page.screenshot()
        except Exception as e:
            self.logger.error(f"Screenshot failed: {str(e)}")
            return None

    async def extract_data(self, url: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """
        Extract data from a webpage using both Selenium and Playwright
        """
        try:
            if not self._selenium_driver:
                await self.init_selenium()
            
            self._selenium_driver.get(url)
            data = {}
            
            for key, selector in selectors.items():
                try:
                    element = WebDriverWait(self._selenium_driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    data[key] = element.text
                except Exception as e:
                    self.logger.error(f"Failed to extract {key}: {str(e)}")
                    data[key] = None
            
            return {"status": "success", "data": data}
        except Exception as e:
            self.logger.error(f"Data extraction failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def __del__(self):
        """
        Cleanup resources
        """
        if self._selenium_driver:
            try:
                self._selenium_driver.quit()
            except:
                pass
        
        if self._playwright_browser:
            try:
                self._playwright_browser.close()
            except:
                pass
        
        if self._playwright:
            try:
                self._playwright.stop()
            except:
                pass
