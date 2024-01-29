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

    with open("README.md", "w") as readme_file:
        readme_file.write("\n".join(readme_lines))

if __name__ == "__main__":
    with open("map.json", "r") as map_file:
        data = json.load(map_file)

    generate_readme(data)
