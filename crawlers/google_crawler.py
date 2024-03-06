import threading
from playwright.sync_api import sync_playwright


GOOGLE_SELECTOR_INPUT = '#APjFqb'

class GoogleSearch:
    def __init__(self, is_headless=True, user_agent=None, max_threads=2):
        self.is_headless = is_headless
        self.user_agent = user_agent
        self.names = []
        self.max_threads = max_threads
        self.threads = []

    def add_name(self, name):
        self.names.append(name)

    def search(self, names):
        with sync_playwright() as p:
            browser, page = self.setup_crawler(p)
            for name in names:
                page.fill(GOOGLE_SELECTOR_INPUT, name)  # Updated selector for search input
                page.press(GOOGLE_SELECTOR_INPUT, "Enter")
                page.wait_for_load_state("networkidle")
                results = page.query_selector_all('.tF2Cxc')
                for result in results[:5]:
                    print(result.inner_text())
            browser.close()

    def setup_crawler(self, playwright):
        browser = playwright.chromium.launch(headless=self.is_headless)
        page = browser.new_page()
        page.set_default_timeout(60000)
        if self.user_agent:
            page.set_extra_http_headers({"User-Agent": self.user_agent})
        page.goto("https://www.google.com")
        return browser, page

    def start_searches(self):
        for i in range(0, len(self.names), self.max_threads):
            chunk = self.names[i:i+self.max_threads]
            thread = threading.Thread(target=self.search, args=(chunk,))
            self.threads.append(thread)
            thread.start()

        for thread in self.threads:
            thread.join()

if __name__ == "__main__":
    # Create an instance of GoogleSearch with non-headless mode and custom user agent
    google_search = GoogleSearch(is_headless=False, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36", max_threads=2)

    # Add names to search
    google_search.add_name("John Doe")
    google_search.add_name("Jane Doe")
    google_search.add_name("Alice Smith")
    google_search.add_name("Bob Johnson")

    # Start the searches
    google_search.start_searches()




