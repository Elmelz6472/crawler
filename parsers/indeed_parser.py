from bs4 import BeautifulSoup
import json

class HTMLParser:
    """Return a list of companies name based on a given html"""
    def __init__(self, html_file):
        self.html_file = html_file
        self.company_info_list = None

    def extract_company_info(self):
        with open(self.html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            company_info_list = []

            job_items = soup.find_all('div', {'class': 'slider_item'})
            for job_item in job_items:
                company_name = job_item.find('span', {'data-testid': 'company-name'}).get_text(strip=True)
                location = job_item.find('div', {'data-testid': 'text-location'}).get_text(strip=True)

                company_info_list.append({"name": company_name, "location": location})

            return company_info_list

    def pretty_print_company_info(self):
        if self.company_info_list is None:
            self.company_info_list = self.extract_company_info()

        print("Company Info:")
        for company_info in self.company_info_list:
            print(f"Name: {company_info['name']}, Location: {company_info['location']}")

    def export_to_json(self, output_file):
        if self.company_info_list is None:
            self.company_info_list = self.extract_company_info()

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.company_info_list, json_file, indent=4, ensure_ascii=False)

    def run(self):
        self.pretty_print_company_info()


html_file = 'html/page.html'
parser = HTMLParser(html_file)
parser.run()
parser.export_to_json('results/companies.json')
