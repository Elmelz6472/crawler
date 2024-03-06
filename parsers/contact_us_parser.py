import re
import yaml
import pprint
import phonenumbers
from bs4 import BeautifulSoup

class ContactUsParser:
    def __init__(self, filename):
        self.filename = filename
        self.html_content = self.load_html_file()

    def load_html_file(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            return file.read()

    def extract_phone_numbers(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        phone_numbers = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']):
            text = tag.get_text()
            matches = re.findall(r'(\+?1\s?)?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', text)
            for match in matches:
                number = "".join(match)
                parsed_number = self.parse_north_american_number(number)
                if parsed_number:
                    phone_numbers.append(parsed_number.national_number)
        return phone_numbers

    def parse_north_american_number(self, number):
        try:
            parsed_number = phonenumbers.parse(number, "US")
            if phonenumbers.is_valid_number(parsed_number):
                return parsed_number
        except phonenumbers.phonenumberutil.NumberParseException:
            pass
        return None

    def extract_emails(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']):
            text = tag.get_text()
            matches = re.findall(email_regex, text)
            emails.extend(matches)
        return emails

    def extract_names(self):
        name_regex = r'(?i)(?:(?:mr|mrs|ms|miss|dr)\.? ?)?([A-Z][a-z]+(?: [A-Z][a-z]+)?)'
        return re.findall(name_regex, self.html_content)

    def extract_last_names(self):
        last_name_regex = r'(?i)\b([A-Z][a-z]+)\b'
        return re.findall(last_name_regex, self.html_content)



def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config



if __name__ == "__main__":
    config = load_config("config.yaml")
    contact_folder = config["parser_config"]["contact_filder"]
    contact_us_file = config["parser_config"]["contact_us_file"]

    parser = ContactUsParser(contact_us_file)

    phone_numbers = parser.extract_phone_numbers()
    print("Phone Numbers:")
    pprint.pprint(phone_numbers)

    # Extract emails
    emails = parser.extract_emails()
    print("\nEmails:")
    pprint.pprint(emails)

    # # Extract names
    # names = parser.extract_names()
    # print("Names:", names)

    # # Extract last names
    # last_names = parser.extract_last_names()
    # print("Last Names:", last_names)
