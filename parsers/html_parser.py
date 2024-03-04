import os
from bs4 import BeautifulSoup
import json

class HTMLParser:
    """Return a list of companies name based on a given html"""
    def __init__(self, path, id_counter=0):
        self.path = path
        self.company_info_list = None
        self.id_counter = id_counter

    def extract_company_info(self, html_file):
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            company_info_list = []

            job_items = soup.find_all('div', {'class': 'slider_item'})
            for job_item in job_items:
                company_name = job_item.find('span', {'data-testid': 'company-name'}).get_text(strip=True)
                location = job_item.find('div', {'data-testid': 'text-location'}).get_text(strip=True)

                company_info_list.append({"id": self.id_counter, "name": company_name, "location": location})
                self.id_counter += 1

            return company_info_list

    def list_html_files(self):
        html_files = []
        if os.path.isfile(self.path) and self.path.endswith(".html"):
            html_files.append(self.path)
        elif os.path.isdir(self.path):
            for file in os.listdir(self.path):
                if file.endswith(".html"):
                    html_files.append(os.path.join(self.path, file))
        return html_files

    def pretty_print_company_info(self):
        if self.company_info_list is None:
            self.company_info_list = []
            for html_file in self.list_html_files():
                self.company_info_list.extend(self.extract_company_info(html_file))

        print("Company Info:")
        for company_info in self.company_info_list:
            print(f"ID: {company_info['id']}, Name: {company_info['name']}, Location: {company_info['location']}")

    def export_to_json(self, output_file):
        if self.company_info_list is None:
            self.company_info_list = []
            for html_file in self.list_html_files():
                self.company_info_list.extend(self.extract_company_info(html_file))

        with open(output_file, 'a', encoding='utf-8') as json_file:
            json.dump(self.company_info_list, json_file, indent=4, ensure_ascii=False)
            json_file.write('\n')

    def run(self):
        self.pretty_print_company_info()



def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


if __name__ == "__main__":
    config = load_config("config.yaml")
    html_folder = config["parser_config"]["html_folder"]
    output_json_file = config["parser_config"]["output_json_file"]
    parser = HTMLParser(html_folder)
    parser.run()
    parser.export_to_json(output_json_file)
