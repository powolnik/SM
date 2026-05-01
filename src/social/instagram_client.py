import os
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from dotenv import load_dotenv

load_dotenv()

class InstagramClient:
    def __init__(self, user_data_dir="browser_data"):
        self.user_data_dir = user_data_dir
        self.username = os.getenv("IG_USERNAME")
        self.password = os.getenv("IG_PASSWORD")

    def get_authenticated_page(self):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser.pages[0]
        stealth_sync(page)
        
        page.goto("https://www.instagram.com/")
        
        # Check if we are logged in by looking for the Home icon
        if not page.locator('svg[aria-label="Home"]').is_visible(timeout=5000):
            self._perform_login(page)
            
        return browser, page

    def _perform_login(self, page):
        print("Logging in to Instagram...")
        page.goto("https://www.instagram.com/accounts/login/")
        page.fill('input[name="username"]', self.username)
        page.fill('input[name="password"]', self.password)
        page.click('button[type="submit"]')
        
        # Wait for user to handle 2FA or security challenges
        print("Please complete any 2FA or security challenges in the browser.")
        page.wait_for_selector('svg[aria-label="Home"]', timeout=120000)
