import yaml
import time
from playwright.sync_api import sync_playwright
from controller.scraper_controller import ScraperController  # Adjust the import path

class IndeedScraper:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.url = config['INDEED_URL']
        self.user_agent = config['user_agent']
        self.isHeadless = config['isHeadless']
        self.input_fields = config.get('input_fields', {})
        self.clickable_fields = config.get('button_fields', {})
        self.controller = None

    def run(self):
        with sync_playwright() as p:
            browser, page = self.setup_crawler(p)

            time.sleep(2)

            browser.close()

    def setup_crawler(self, playwright):
        # Launch the browser
        browser = playwright.chromium.launch(headless=self.isHeadless)
        # Create a new page
        page = browser.new_page()
        # Set default navigation timeout
        page.set_default_navigation_timeout(0)
        # Set extra HTTP headers
        page.set_extra_http_headers({"User-Agent": self.user_agent})
        # Navigate to the URL
        page.goto(self.url)


        self.setup_scraper_controller(page)


        self.enter_data()


        self.click_submit_button()

        return browser, page

    def setup_scraper_controller(self, page):
        self.controller = ScraperController(page)

    def enter_data(self):
        for field_type in ['keyword', 'location']:
            self.enter_data_for_fields(field_type)

    def enter_data_for_fields(self, field_type):
        field_data = self.input_fields.get(field_type, {})
        selector = field_data.get('selector', '')
        data = field_data.get('data', '')
        if selector and data:
            print(f"Entering data '{data}' into {field_type} field with selector '{selector}'")
            self.controller.enter_data(selector, data)
        else:
            print(f"Selector or data not found for {field_type} field in config.yaml")

    def click_submit_button(self):
        # Click on the submit button
        selector = self.clickable_fields.get('submit_button', {}).get('selector', '')
        if selector:
            print(f"Clicking on submit button with selector '{selector}'")
            self.controller.click(selector)
        else:
            print("Selector not found for submit button in config.yaml")

if __name__ == "__main__":
    config_path = "config.yaml"
    scraper = IndeedScraper(config_path)
    scraper.run()
