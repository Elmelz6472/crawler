import sys
import yaml
from crawlers.indeed_crawler import IndeedScraper
from crawlers.google_crawler import GoogleSearch, JSONFileHandler
from parsers.html_parser import HTMLParser

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python main.py [crawler | parser] or none")
        sys.exit(1)

    action = sys.argv[1] if len(sys.argv) == 2 else None
    config = load_config("config.yaml")

    if not action or action == "crawler":
        scraper = IndeedScraper(config["scraper_config"]["config_path"], depth=25)
        scraper.run()

    if not action or action == "parser":
        html_folder = config["parser_config"]["html_folder"]
        output_json_file = config["parser_config"]["output_json_file"]
        parser = HTMLParser(html_folder)
        parser.run()
        parser.export_to_json(output_json_file)

    if not action or action == "google":
        config_path = "config.yaml"
        filename = "results/companies.json"
        json_reader = JSONFileHandler(filename)
        names = json_reader.read_names()
        google_search = GoogleSearch(config_path, max_threads=json_reader.calculate_percentage(25))
        for name in names: google_search.add_name(name)
        google_search.start_searches()
