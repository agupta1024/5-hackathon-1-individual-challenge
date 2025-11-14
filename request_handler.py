import numpy as np
from db_access import sqlDB
HOST_NAME = "localhost"
USER_NAME = "root"
PASSWORD = "mysql123"

class RequestHandle():
    """
    A class to handle API endpoint requests and perform statistical operations on repository data.
    
    This class processes requests from Flask endpoints, queries the database for repository
    information, and performs calculations such as average, min, max, and standard deviation
    on stargazer counts.
    """
    
    def __init__(self, host_name = None, user_name = None, 
                 pwd = None):
        """
        Initialize the RequestHandle class with database credentials.
        
        Args:
            host_name (str, optional): MySQL server hostname. Defaults to localhost.
            user_name (str, optional): MySQL username. Defaults to 'root'.
            pwd (str, optional): MySQL password. Defaults to 'mysql123'.
        """
        self.host_name = host_name or HOST_NAME
        self.user_name = user_name if user_name else USER_NAME
        self.pwd = pwd if pwd else PASSWORD
        self.sqlDB = sqlDB(self.host_name, self.user_name, self.pwd)

    def process_endpoint(self, organisation, endpoint):
        """
        Process API endpoint requests and perform statistical calculations.
        
        Retrieves repository data for a given organization and performs the requested
        statistical operation (list, average, min, max, standard deviation, argmin, argmax).
        
        Args:
            organisation (str): Name of the GitHub organization. None for healthz endpoint.
            endpoint (str): The type of endpoint to process. Valid values:
                - 'healthz': Health check endpoint
                - 'list_all': List all repositories and their stargazer counts
                - 'avg': Calculate average stargazer count
                - 'min': Get minimum stargazer count
                - 'max': Get maximum stargazer count
                - 'argmin': Get repository with minimum stargazers
                - 'argmax': Get repository with maximum stargazers
                - 'std': Calculate standard deviation of stargazer counts
                
        Returns:
            dict or str or float or int: Response data depending on the endpoint:
                - 'healthy' for healthz endpoint
                - Dictionary of {repo_name: stargazer_count} for list_all
                - Float values for avg and std calculations
                - Integer values for min and max
                - String values for argmin and argmax (repository names)
        """
        if endpoint == "healthz":
            return 'healthy'
        result = self.sqlDB.process_user_request(organisation)
        user_data = {row['REPO_NAME'] : row['stargazers_count'] for row in result}
        if endpoint == "list_all":
            return user_data
        elif endpoint == "avg":
            total_count = sum(user_data.values())
            no_of_repos = len(user_data)
            avg = total_count / no_of_repos * 1.0
            return avg
        elif endpoint == "min":
            min_count = min(user_data.values())
            return min_count
        elif endpoint == "max":
            max_count = max(user_data.values())
            return max_count
        elif endpoint == "argmin":
            key_for_min_value = min(user_data, key=user_data.get)
            return key_for_min_value
        elif endpoint == "argmax":
            key_for_max_value = max(user_data, key=user_data.get)
            return key_for_max_value
        elif endpoint == "std":
            values_list = list(user_data.values())
            values = np.array(values_list)
            std_dev = np.std(values)
            return std_dev
