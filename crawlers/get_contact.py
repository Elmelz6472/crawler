import os
import re
from playwright.sync_api import sync_playwright

class PageNavigator:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def navigate_to_about_or_contact_page(self, url, filename):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            try:
                page.goto(url)
                page.wait_for_load_state("networkidle")

                # Priority: Look for "Contact Us" links on the homepage
                contact_us_link = page.query_selector('a[href*="contact"]')
                if contact_us_link:
                    contact_us_link.click()
                    page.wait_for_load_state("networkidle")
                    print("Navigated to Contact Us page.")
                else:
                    # If "Contact Us" link not found, perform a broader search
                    print("Contact Us link not found. Performing broader search...")

                    # Look for links whose text element matches "Contact Us" or similar using regex
                    contact_us_regex = re.compile(r"contact\s*us", re.IGNORECASE)
                    about_us_regex = re.compile(r"about\s*us", re.IGNORECASE)

                    links = page.query_selector_all('a')
                    for link in links:
                        text = link.inner_text()
                        if contact_us_regex.search(text):
                            link.click()
                            page.wait_for_load_state("networkidle")
                            print("Navigated to Contact Us page.")
                            break
                        elif about_us_regex.search(text):
                            link.click()
                            page.wait_for_load_state("networkidle")
                            print("Navigated to About Us page.")
                            break
                    else:
                        # If neither "Contact Us" nor "About Us" link found, print a message
                        print("No specific link found on the homepage. Try another approach or check other pages...")
                        return

                # Save the page HTML content to a file
                self.save_page_content(page, filename)

            except Exception as e:
                print("An error occurred:", e)
            finally:
                browser.close()

    def save_page_content(self, page, filename):
        # Create the folder if it does not exist
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        # Write the page content to a file
        file_path = os.path.join(self.folder_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page.content())

if __name__ == "__main__":
    website_url = "https://www.infowaygroup.com/"  # Replace with the actual website URL
    folder_path = "contact_page"  # Specify the folder path to save the pages
    navigator = PageNavigator(folder_path)
    navigator.navigate_to_about_or_contact_page(website_url, "contact_us.html")
