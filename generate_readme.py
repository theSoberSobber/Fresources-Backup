import json
import os

def generate_readme(data):
    readme_lines = ["# Mirror of Fresources"]

    for college, branches in data.items():
        readme_lines.append(f"- {college}")
        
        for branch, courses in branches.items():
            readme_lines.append(f"\t- {branch}")
            
            for course, resources in courses.items():
                readme_lines.append(f"\t\t- {course}")

                for resource, details in resources.items():
                    resource_type = details["type"]
                    resource_url = details["url"]
                    readme_lines.append(f"\t\t\t- [{resource}]({resource_url}), {resource_type}")

    return readme_lines

def main():
    # Get a list of all data files in the current directory
    data_files = [file for file in os.listdir() if file.startswith("data-") and file.endswith(".json")]

    # Initialize an empty dictionary to store aggregated data
    aggregated_data = {}

    # Iterate through each data file and load its content into the aggregated_data dictionary
    for data_file in data_files:
        with open(data_file, "r") as file:
            college_name = data_file.replace("data-", "").replace(".json", "")
            aggregated_data[college_name] = json.load(file)[college_name]

    # Generate the README content based on the aggregated data
    readme_content = generate_readme(aggregated_data)

    # Write the README content to the README.md file
    with open("README.md", "w") as readme_file:
        readme_file.write("\n".join(readme_content))

if __name__ == "__main__":
    main()