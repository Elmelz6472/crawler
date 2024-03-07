import threading
import yaml
import time
import json
from playwright.sync_api import sync_playwright


GOOGLE_SELECTOR_INPUT = '#APjFqb'
GOOGLE_SELECTOR_FIRST_LINK = '.LC20lb'
MAX_TIMEOUT = 60_000
chrome_profile_directory = '/Users/malikmacbook/Library/Application Support/Google/Chrome/Profile 54'

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
        for name in names:
            with sync_playwright() as p:
                browser, page = self.setup_crawler(p)
                page.fill(GOOGLE_SELECTOR_INPUT, name)
                page.press(GOOGLE_SELECTOR_INPUT, "Enter")
                page.wait_for_load_state("networkidle")
                link = page.query_selector(GOOGLE_SELECTOR_FIRST_LINK)
                if link:
                    link.click()
                    page.wait_for_load_state("networkidle")
                    self.navigate_to_contact_page(page, name)
                else:
                    print("No search results found")
                browser.close()



    def navigate_to_contact_page(self, page, name):
        current_url = page.url
        old_url = current_url
        if current_url.endswith('/'):
            current_url = current_url[:-1]  # Remove trailing slash

        variations = ["contact", "contact.html", "contact-us", "contact-us.html"]
        flag
        for variation in variations:
            try:
                page.goto(current_url + f"/{variation}")
                page.wait_for_load_state('networkidle')

                # Check if the page contains 'error' or '404' in its text content
                if 'error' in page.inner_text('*') or '404' in page.inner_text('*'):
                    raise Exception("Error 404 or 'error' found in page content.")

                print("Navigated to Contact Page:", page.url)
                time.sleep(2)

                print("before write")
                flag=True
                JSONFileHandler.write_info(name, page.url)
                print("finished write")
                break  # Exit loop if successful

            except Exception as e:
                print(f"Error navigating to {variation}: {e}")
                continue  # Try the next variation

        else:
            if not flag: JSONFileHandler.write_info(name, old_url)
            print("Failed to navigate to the contact page.")




    def setup_crawler(self, playwright):
        # browser = playwright.chromium.launch_persistent_context(user_data_dir=chrome_profile_directory, headless=self.is_headless)
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



class JSONFileHandler:
    def __init__(self, filename):
        self.filename = filename

    def read_names(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            names = [entry["name"] for entry in data]
            return names

    @staticmethod
    def write_info(name, url, write_mode='a'):
        with open("results/leads.txt", write_mode) as file:
            file.write(f"Name: {name}\nURL: {url}\n\n")

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

    json_reader = JSONFileHandler(filename)
    names = json_reader.read_names()


    google_search = GoogleSearch(config_path, max_threads=json_reader.calculate_percentage(50))


    for name in names:
        google_search.add_name(name)


    # Start the searches
    google_search.start_searches()




