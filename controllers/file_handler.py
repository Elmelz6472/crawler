import json

class FileHandler:

    @staticmethod
    def read_names(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            names = [entry["name"] for entry in data]
            return names

    @staticmethod
    def increment_ids(filename):
        with open(filename, 'r+') as file:
            data = json.load(file)
            for i, entry in enumerate(data, start=1):
                entry["id"] = i

            file.seek(0)
            json.dump(data, file, indent=4, ensure_ascii=False)  # Ensure_ascii=False to preserve special characters
            file.truncate()



    @staticmethod
    def read_file(filename, file_type):
        with open(filename, 'r') as file:
            if file_type == 'json':
                return json.load(file)
            elif file_type == 'html' or file_type == 'txt':
                return file.read()
            else:
                raise ValueError("Invalid file type. Supported types are 'json', 'html', and 'txt'.")

    @staticmethod
    def write_file(data, filename, file_type):
        with open(filename, 'w') as file:
            if file_type == 'json':
                json.dump(data, file)
            elif file_type == 'html' or file_type == 'txt':
                file.write(data)
            else:
                raise ValueError("Invalid file type. Supported types are 'json', 'html', and 'txt'.")

    @staticmethod
    def append_file(data, filename, file_type):
        with open(filename, 'a') as file:
            if file_type == 'html' or file_type == 'txt':
                file.write(data)
            else:
                raise ValueError("Invalid file type. Supported types are 'html' and 'txt'.")

    @staticmethod
    def count_occurrences(substring, filename, file_type):
        with open(filename, 'r') as file:
            content = file.read()
            return content.count(substring)


    @staticmethod
    def remove_duplicates_by_name(filename):
        with open(filename, 'r+') as file:
            data = json.load(file)
            unique_names = set()
            unique_objects = []
            for entry in data:
                if entry["name"] not in unique_names:
                    unique_names.add(entry["name"])
                    unique_objects.append(entry)
            file.seek(0)
            json.dump(unique_objects, file, indent=4)
            file.truncate()


    @staticmethod
    def translate_to_human_readable(filename, output_filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            with open(output_filename, 'w') as output_file:
                output_file.write("ID     Name          Location\n")  # Adjust spacing as needed
                for entry in data:
                    id = entry.get("id", "")
                    name = entry.get("name", "")
                    location = entry.get("location", "")
                    output_file.write(f"{id:<7} {name:<20} {location}\n")  # Adjust spacing as needed
                    output_file.write("\n")  # Add new line between rows



    def get_number_of_entries(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return len(data)

    def calculate_percentage(self, percentage):
        total_entries = self.get_number_of_entries()
        return int(percentage * total_entries / 100)

    def __len__(self):
        return self.get_number_of_entries()



if __name__ == "__main__":
    filename = 'results/companies.json'
    FileHandler.remove_duplicates_by_name(filename)
    FileHandler.increment_ids(filename)
    FileHandler.translate_to_human_readable(filename, "final_leads.txt")