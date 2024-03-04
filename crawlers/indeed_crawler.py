import os
import yaml
import time
import threading
from playwright.sync_api import sync_playwright

#I DONT KNOW WHY IT WOKRS BUT IT WOKRS
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.controller_sraper import ScraperController

DISMISS_BUTTON = "#mosaic-desktopserpjapopup > div.css-g6agtu.eu4oa1w0 > button"

class IndeedScraper:
    def __init__(self, config_path, depth=5):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.url = config['INDEED_URL']
        self.user_agent = config['user_agent']
        self.isHeadless = config['isHeadless']
        self.input_fields = config.get('input_fields', {})
        self.clickable_fields = config.get('button_fields', {})
        self.controller = None
        self.depth = depth

    def run(self):
        with sync_playwright() as p:
            browser, page = self.setup_crawler(p)

            time.sleep(1)


            for page_idx in range(1, self.depth):
                self.scroll_and_check_element(page)

                time.sleep(1)
                self.store_page_as_html(page, f"page{page_idx}.html")
                self.click_next_button()

            browser.close()



    def scroll_and_check_element(self, page):
        start_time = time.time()
        timeout = 5
        while not self.is_element_visible(page, DISMISS_BUTTON):
            if time.time() - start_time > timeout:
                print("Element did not appear within the timeout period.")
                break
            time.sleep(0.5)

        self.scroll_to_element(page, 'pagination-page-next')

    def is_element_visible(self, page, selector):
        return page.is_visible(selector)

    def handle_popup(self, selector):
        self.controller.click(selector)


    def setup_crawler(self, playwright):
        browser = playwright.chromium.launch(headless=self.isHeadless)
        page = browser.new_page()
        page.set_default_timeout(60000)
        page.set_extra_http_headers({"User-Agent": self.user_agent})
        page.goto(self.url)

        self.setup_scraper_controller(page)

        time.sleep(1)

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
        selector = self.clickable_fields.get('submit_button', {}).get('selector', '')
        if selector:
            print(f"Clicking on submit button with selector '{selector}'")
            self.controller.click(selector)
        else:
            print("Selector not found for submit button in config.yaml")

    def click_next_button(self):
        selector = self.clickable_fields.get('next_button', {}).get('selector', '')
        if selector:
            print(f"Clicking on next button with selector '{selector}'")
            self.controller.click(selector, custom_query="data-testid='myButton'")
        else:
            print("Selector not found for next button in config.yaml")


    def scroll_to_bottom_smooth(self, page):
        page.evaluate('(async () => { await new Promise(resolve => { let totalHeight = 0; let distance = 100; let timer = setInterval(() => { let scrollHeight = document.body.scrollHeight; window.scrollBy(0, distance); totalHeight += distance; if(totalHeight >= scrollHeight){ clearInterval(timer); resolve(); } }, 50); }); })()')

    def scroll_to_element(self, page, test_id):
            script = f'''
                (async () => {{
                    const targetElement = document.querySelector('[data-testid="{test_id}"]');
                    if (!targetElement) {{
                        console.error('Target element not found with data-testid:', '{test_id}');
                        return;
                    }}

                    await new Promise(resolve => {{
                        let distance = 100;
                        let timer = setInterval(() => {{
                            let rect = targetElement.getBoundingClientRect();
                            if (rect.top >= 0 && rect.bottom <= window.innerHeight) {{
                                clearInterval(timer);
                                resolve();
                            }} else {{
                                window.scrollBy(0, distance);
                            }}
                        }}, 50);
                    }});
                }})();
            '''
            page.evaluate(script)



    def store_page_as_html(self, page, file_name):
        html_content = page.content()
        file_path = os.path.join("html", file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"Page HTML stored as {file_path}")

if __name__ == "__main__":
    config_path = "config.yaml"
    scraper = IndeedScraper(config_path)
    scraper.run()
