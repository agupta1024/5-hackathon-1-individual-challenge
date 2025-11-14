import requests
from requests.exceptions import HTTPError

BASE_URL = "https://api.github.com/orgs/"
HEADERS = {"Accept": "application/vnd.github.v3+json"}

class RemoteRepoInit():
    """
    A class to fetch repository data from the GitHub API for a given organization.
    
    This class initializes a connection to the GitHub API and retrieves repository
    information for a specified organization.
    """
    
    def __init__(self, org, extra_header=None):
        """
        Initialize the RemoteRepoInit class with organization name and headers.
        
        Args:
            org (str): The name of the GitHub organization.
            extra_header (dict, optional): Additional headers to merge with default headers.
                                          Defaults to None.
        """
        self.org = org
        self.url = BASE_URL + self.org + "/repos"
        self.headers = HEADERS
        if extra_header:
            self.headers.update(extra_header)

    def get_data_from_github(self):
        """
        Fetch repository data from the GitHub API.
        
        Makes an HTTP GET request to the GitHub API to retrieve all repositories
        for the initialized organization. Handles HTTP and general errors gracefully.
        
        Returns:
            list: A list of dictionaries containing repository information from the GitHub API.
                  Each dictionary contains repository metadata such as name, description,
                  stargazers_count, etc.
                  
        Raises:
            HTTPError: If an HTTP error occurs (caught and printed).
            Exception: If any other error occurs (caught and printed).
        """
        try:
            response_obj = requests.get(self.url, self.headers)
            response_obj.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occured: {http_err}")
        except Exception as err:
            print(f"Other error occured: {err}")

        data = response_obj.json()
        return data


if __name__ == "__main__":
    pass