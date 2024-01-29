import json
import cloudscraper
from logger import log

class FresourcesUtil:
    """
    A utility class for handling API requests related to 'fresources.tech'.
    """

    BASE_URL: str = 'https://fresources.tech/api/trpc/example.'
    data_dir: str = './data'

    def __init__(self) -> None:
        """
        Initialize a new instance of FresourceUtil.
        """
        self.scraper = cloudscraper.create_scraper()

    def make_api_request(self, endpoint: str, params: str) -> dict:
        """
        Make an API request to the specified endpoint with the given parameters.

        :param endpoint: The API endpoint.
        :param params: The parameters for the API request.
        :return: The API response as a dictionary.
        """
        url = f'{self.BASE_URL}{endpoint}?batch=1&input={params}'
        try:
            response = self.scraper.get(url)
            response.raise_for_status()
        except Exception as e:
            log(0, f"Error in {__name__}", url)
            raise Exception(e)
        res = response.text
        return json.loads(res)

    def get_branch_by_college_id(self, college_id: str) -> dict:
        """
        Get branch information by college ID.

        :param college_id: The ID of the college.
        :return: Branch information as a dictionary.
        """
        params = f'{{"0":{{"json":{{"collegeId":"{college_id}"}}}}}}'
        return self.make_api_request('getBranchNamesByCollegeId', params)

    def get_course_by_branch_id(self, branch_id: str) -> dict:
        """
        Get course information by branch ID.

        :param branch_id: The ID of the branch.
        :return: Course information as a dictionary.
        """
        params = f'{{"0":{{"json":{{"branchId":"{branch_id}"}}}}}}'
        return self.make_api_request('getCourseByBranchId', params)

    def get_resource_by_course_id(self, course_id: str) -> dict:
        """
        Get resource information by course ID.

        :param course_id: The ID of the course.
        :return: Resource information as a dictionary.
        """
        params = f'{{"0":{{"json":{{"courseId":"{course_id}"}}}}}}'
        return self.make_api_request('getResourcesByCourseId', params)

    def download_resource(self, resource_url: str, download_path: str) -> None:
        """
        Download a resource given its URL and save it to the specified path.

        :param resource_url: The URL of the resource to be downloaded.
        :param download_path: The path where the downloaded resource will be saved.
        """
        try:
            # Fetch resource content using make_api_request
            resource_content = self.scraper.get(resource_url).content

            # Save content to the specified path
            with open(download_path, 'wb') as file:
                file.write(resource_content)
        except Exception as e:
            log(0, "Error downloading resource", resource_url)
            raise Exception(e)