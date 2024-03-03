from bs4 import BeautifulSoup
import pprint


def print_tables_without_role_presentation(file_path, ul_selector):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        ul = soup.select_one(ul_selector)
        if ul:
            table_tags = ul.find_all('table', recursive=True)  # Search only immediate children
            if table_tags:
                for table in table_tags:
                    # if not table.has_attr('role'):
                        print(table.prettify())
            else:
                print(f"No <table> elements found that are children of '{ul_selector}'")
        else:
            print(f"No <ul> element found with selector '{ul_selector}'")


def parse_li_elements(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        li_elements = soup.find_all('li')
        for i, li in enumerate(li_elements):
            # Get the text content of the li element
            text = li.get_text(strip=True)
            # Get the href attribute value if it exists
            href = li.find('a')['href'] if li.find('a') else None
            # Print the text content and href attribute value
            print(f"Text: {text}, Href: {href}")
            # Print a separator line between entries except for the last one
            if i < len(li_elements) - 1:
                print("-" * 40)


def parse_html_file(file_path):
    # Read HTML content from file
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <li> elements
    list_items = soup.find_all("li", class_="css-5lfssm eu4oa1w0")

    for item in list_items:
        h2_tags = item.find_all("h2", class_="jobTitle css-14z7akl eu4oa1w0")
        for h2_tag in h2_tags:
            job_title = h2_tag.text.strip()
            job_href = h2_tag.a['href'] if h2_tag.a else "N/A"
            print("Job Title:", job_title)
            print("Job Href:", job_href)
            print()


# Example usage:
file_path = 'html/test.html'
ul_selector = '#mosaic-provider-jobcards > ul'

jobs = parse_html_file(file_path)

# Pretty print the jobs
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(jobs)