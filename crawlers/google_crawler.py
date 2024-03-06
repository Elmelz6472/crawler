import threading
import yaml
import time
import json
from playwright.sync_api import sync_playwright


GOOGLE_SELECTOR_INPUT = '#APjFqb'
GOOGLE_SELECTOR_FIRST_LINK = '.LC20lb'
MAX_TIMEOUT = 60_000
class GoogleSearch:
    def __init__(self, config_path, max_threads=2):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.url = config['GOOGLE_URL']
        self.is_headless = config['isHeadless']
        self.user_agent = config['user_agent']
        self.max_threads = max_threads
        self.names = []
        self.threads = []
        self.controller = None

    def add_name(self, name):
        self.names.append(name)

    def search(self, names):
            with sync_playwright() as p:
                browser, page = self.setup_crawler(p)
                for name in names:
                    page.fill(GOOGLE_SELECTOR_INPUT, name)
                    page.press(GOOGLE_SELECTOR_INPUT, "Enter")
                    page.wait_for_load_state("networkidle")
                    link = page.query_selector(GOOGLE_SELECTOR_FIRST_LINK)
                    if link:
                        link.click()
                    else:
                        print("No search results found")
                browser.close()

    def setup_crawler(self, playwright):
        browser = playwright.chromium.launch(headless=self.is_headless)
        page = browser.new_page()
        page.set_default_timeout(MAX_TIMEOUT)
        if self.user_agent:
            page.set_extra_http_headers({"User-Agent": self.user_agent})
        page.goto(self.url)
        return browser, page

    def start_searches(self):
        for i in range(0, len(self.names), self.max_threads):
            chunk = self.names[i:i+self.max_threads]
            thread = threading.Thread(target=self.search, args=(chunk,))
            self.threads.append(thread)
            thread.start()

        for thread in self.threads:
            thread.join()



class JSONFileReader:
    def __init__(self, filename):
        self.filename = filename

    def read_names(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            names = [entry["name"] for entry in data]
            return names

    def get_number_of_entries(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return len(data)

    def calculate_percentage(self, percentage):
        total_entries = self.get_number_of_entries()
        return int(percentage * total_entries / 100)

    def __len__(self):
        return self.get_number_of_entries()




if __name__ == "__main__":
    """max_thread is basically a divisor
    4 names with 1 max_thread ->  4 concurrent instances of chrome
    4 names with 4 max_thread -> 1 concurrent instance of chrome
    """
    config_path = "config.yaml"
    filename = "results/companies.json"

    json_reader = JSONFileReader(filename)
    names = json_reader.read_names()


    google_search = GoogleSearch(config_path, max_threads=json_reader.calculate_percentage(50))


    for name in names:
        google_search.add_name(name)


    # Start the searches
    google_search.start_searches()




