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
        self._playwright = None

    def get_authenticated_page(self):
        self._playwright = sync_playwright().start()
        browser = self._playwright.chromium.launch_persistent_context(
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
        page.wait_for_selector('input[name="username"]')
        page.fill('input[name="username"]', self.username)
        page.fill('input[name="password"]', self.password)
        page.click('button[type="submit"]')
        
        # Wait for user to handle 2FA or security challenges
        print("Please complete any 2FA or security challenges in the browser.")
        page.wait_for_selector('svg[aria-label="Home"]', timeout=120000)

    def post_content(self, page, content_text):
        # Logic to navigate to create post and input text
        page.goto("https://www.instagram.com/create/style/")
        # Add specific selectors for your UI automation here
        page.wait_for_selector('textarea')
        page.fill('textarea', content_text)
        page.click('button:has-text("Share")')

    def close(self):
        """Call this to clean up resources."""
        if self._playwright:
            self._playwright.stop()
