import random
import time

class ScraperController:
    def __init__(self, page):
        self.page = page

    def enter_data(self, selector, data):
        input_field = self.page.query_selector(selector)
        if not input_field:
            print(f"Element with selector '{selector}' not found")
            return

        input_field.fill('')

        input_field.focus()

        for char in data:
            self.page.keyboard.press(char)

            time.sleep(random.uniform(0.01, 0.2))

        time.sleep(0.5)


    def click(self, selector, custom_query=False):
        if custom_query:
             element = self.page.query_selector(f'{custom_query}')
        else:
            element = self.page.query_selector(selector)
        if not element:
            print(f"Element with selector '{selector}' not found")
            return
        element.click()
