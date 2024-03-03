import random
import time

class ScraperController:
    def __init__(self, page):
        self.page = page

    def enter_data(self, selector, data):
        # Get the input field element
        input_field = self.page.query_selector(selector)
        if not input_field:
            print(f"Element with selector '{selector}' not found")
            return

        # Clear the input field by filling it with an empty string
        input_field.fill('')

        # Focus on the input field
        input_field.focus()

        # Simulate typing each character with a delay between keystrokes
        for char in data:
            # Simulate pressing the key
            self.page.keyboard.press(char)

            # Sleep for a random duration between 0.1 to 0.3 seconds
            time.sleep(random.uniform(0.01, 0.2))

        # Wait for the input field to update its value
        time.sleep(0.5)  # Adjust as needed


    def click(self, selector):
        # Click on the element specified by the selector
        element = self.page.query_selector(selector)
        if not element:
            print(f"Element with selector '{selector}' not found")
            return
        element.click()
