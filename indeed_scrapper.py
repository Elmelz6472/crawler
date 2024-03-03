import yaml
import time
from playwright.sync_api import sync_playwright
from controller.scraper_controller import ScraperController  # Adjust the import path


class IndeedScraper:
    def __init__(self, config_path):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        self.url = config["INDEED_URL"]
        self.user_agent = config["user_agent"]
        self.isHeadless = config["isHeadless"]
        self.input_fields = config.get('input_fields', {})
        self.clickable_fields = config.get('button_fields', {})
        self.controller = None


    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.isHeadless)
            page = browser.new_page()
            page.set_default_navigation_timeout(0)
            page.set_extra_http_headers({"User-Agent": self.user_agent})
            page.goto(self.url)

            # Create an instance of ScraperController
            self.controller = ScraperController(page)

            # Enter data for different input fields
            time.sleep(1)
            self.enter_data_for_fields('keyword')
            self.enter_data_for_fields('location')

            self.controller.click(self.clickable_fields.get('submit_button', {}).get('selector', ''))

            time.sleep(2)

            browser.close()


    def enter_data_for_fields(self, field_type):
        field_data = self.input_fields.get(field_type, {})
        selector = field_data.get('selector', '')
        data = field_data.get('data', '')
        if selector and data:
            print(f"Entering data '{data}' into {field_type} field with selector '{selector}'")
            self.controller.enter_data(selector, data)
        else:
            print(f"Selector or data not found for {field_type} field in config.yaml")





if __name__ == "__main__":
    config_path = "config.yaml"
    scraper = IndeedScraper(config_path)
    scraper.run()
