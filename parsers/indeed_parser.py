from bs4 import BeautifulSoup

def parse_html_file(file_path, ul_selector):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        ul = soup.select_one(ul_selector)
        if ul:
            li_elements = ul.find_all('li')
            return li_elements
        else:
            print(f"No <ul> element found with selector '{ul_selector}'")
            return []

def pretty_print_li_elements(li_elements):
    for li in li_elements:
        print(li.text.strip())

# Example usage:
file_path = 'html/test.html'
ul_selector = '#mosaic-provider-jobcards > ul'
li_elements = parse_html_file(file_path, ul_selector)
if li_elements:
    pretty_print_li_elements(li_elements)
