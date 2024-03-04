import sys
import yaml
from crawlers.indeed_crawler import IndeedScraper
from parsers.html_parser import HTMLParser

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python main.py [scraper | parser] or none")
        sys.exit(1)

    action = sys.argv[1] if len(sys.argv) == 2 else None

    config = load_config("config.yaml")

    if not action or action == "scraper":
        scraper = IndeedScraper(config["scraper_config"]["config_path"])
        scraper.run()

    if not action or action == "parser":
        html_folder = config["parser_config"]["html_folder"]
        output_json_file = config["parser_config"]["output_json_file"]
        parser = HTMLParser(html_folder)
        parser.run()
        parser.export_to_json(output_json_file)
