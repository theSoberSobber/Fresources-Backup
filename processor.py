import os
from logger import log

class DataProcessor:
    def __init__(self, api_handler, upload_handler):
        self.api_handler = api_handler
        self.upload_handler = upload_handler
        self.data = {}

    def process_resource(self, resource: dict) -> dict:
        """
        Download a resource given its ID.

        :param resource_id: The ID of the resource.
        """
        processed_resource = {}
        resource_name = resource.get('name')
        processed_resource['type'] = resource_type = resource.get('type')
        resource_url = resource.get('url')
        log(3, "Processing Resource", resource_type, resource_name)
        
        if resource_url:
            download_path = os.path.join(self.api_handler.data_dir, resource_name)
            self.api_handler.download_resource(resource_url, download_path)

            # Upload to Catbox
            upload_response = self.upload_handler.upload_single_file(download_path)
            log(4, "Uploaded Resource to Catbox", resource_type, resource_name, f"Catbox URL: {upload_response.get('file')}")
            processed_resource['url'] = upload_response.get('file')
            # Optional: Clean up downloaded file
            os.remove(download_path)
        return processed_resource

    def process_course_data(self, course_name: str, course_id: str) -> dict:
        """
        Process course data, extract resources, and download them.

        :param course_data: The data of a course containing resources.
        """
        log(2, "Processing course data", course_name, course_id)
        processed_course = {}
        course_data = self.api_handler.get_resource_by_course_id(course_id)[0]
        resources = course_data.get('result', {}).get('data', {}).get('json', [])
        for resource in resources:
            processed_course[resource.get('resource').get('name')] = self.process_resource(resource.get('resource'))

        return processed_course

    def process_branch_data(self, branch_name: str, branch_id: str) -> None:
        """
        Process branch data, extract courses, and process each course.

        :param branch_data: The data of a branch containing courses.
        """
        log(1, "Processing branch", branch_name, branch_id)
        processed_branch = {}
        branch_data = self.api_handler.get_course_by_branch_id(branch_id)[0]
        courses = branch_data.get('result', {}).get('data', {}).get('json', []).get('courses', [])
        for course in courses:
            course_id = course.get('id')
            course_name = course.get('name')
            processed_branch[course_name] = self.process_course_data(course_name, course_id)

        return processed_branch

    def process_college_data(self, college_name: str, college_id: str) -> None:
        """
        Process college data, extract branches, and process each branch.

        :param college_name: The name of the college.
        :param college_id: The ID of the college.
        """
        log(0, f"Processing college", college_name, college_id)
        processed_college = {}
        branch_data = self.api_handler.get_branch_by_college_id(college_id)[0]
        branches = branch_data.get('result', {}).get('data', {}).get('json', [])
        for branch in branches:
            branch_id = branch.get('id')
            branch_name = branch.get('name')
            processed_college[branch_name] = self.process_branch_data(branch_name, branch_id)

        return processed_college

    def process_all_colleges(self, college_ids: dict) -> None:
        """
        Process data for all colleges.

        :param college_ids: A dictionary of college names and IDs.
        """
        for college_name, college_id in college_ids.items():
            self.data[college_name] = self.process_college_data(college_name, college_id)
        return self.data