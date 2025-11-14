import mysql.connector
from mysql.connector import Error
from git_access_api import RemoteRepoInit

DB_NAME = "Stargazers_Database"
ORG_TABLE_NAME = "Github_organisations"
ORG_NAME_COL = "Organisation_name"
ORG_ID_COL = "Org_id"
REPO_TABLE_NAME = "Repos"
FOREIGN_KEY_COLUMN = "Parent_Org_id"

class sqlDB():
    """
    A class to manage MySQL database operations for GitHub organization and repository data.
    
    This class handles database connections, table creation, and CRUD operations for
    storing GitHub organization and repository information including stargazer counts.
    """
    
    def __init__(self, host_name, user_name, pwd):
        """
        Initialize the sqlDB class and establish database connection.
        
        Args:
            host_name (str): The hostname of the MySQL server.
            user_name (str): The username for MySQL authentication.
            pwd (str): The password for MySQL authentication.
        """
        self.host_name = host_name
        self.user_name = user_name
        self.pwd = pwd
        self.db_connection = None
        self.db_connection = self.check_db_connection(host_name=self.host_name, 
                                                       user_name=self.user_name, 
                                                       user_password=self.pwd)
        self.table_exists = self.create_table_if_not_exist(self.db_connection, ORG_TABLE_NAME, REPO_TABLE_NAME)

    def create_new_entry_in_org_and_repos(self, connection, table_name,
                                          org_column_name, org_name):
        """
        Create a new entry in both the organizations and repositories tables.
        
        Inserts a new organization into the organization table and then retrieves
        its repositories from the GitHub API to populate the repositories table.
        
        Args:
            connection: MySQL database connection object.
            table_name (str): Name of the organization table.
            org_column_name (str): Column name for the organization name field.
            org_name (str): Name of the GitHub organization to add.
            
        Returns:
            int: The ID of the newly created organization entry, or None if failed.
            
        Raises:
            Exception: If a valid ID cannot be retrieved after organization creation.
        """
        new_org_id = self.create_org_table_entry(connection, table_name,
                                             org_column_name, org_name)
        connection.commit()
        # Check if we have a valid ID before proceeding to Table 2
        if new_org_id is None:
             raise Exception("Failed to retrieve or generate a valid ID.")

        # --- 2. CREATE ENTRY IN Repos TABLE (TABLE 2) ---
        print(f"Adding Repo entry to {REPO_TABLE_NAME} table...")
        data = self.get_data_from_remote_api(org_name)
        data_to_insert = [(new_org_id, value['name'], value['stargazers_count']) for value in data]
        insert2_query = f"""
        INSERT INTO {REPO_TABLE_NAME} ({FOREIGN_KEY_COLUMN}, 
        REPO_NAME, stargazers_count)
        VALUES (%s, %s, %s);
        """
        # The values passed are the ID and the extra data value
        cursor = connection.cursor()
        try:
            cursor.executemany(insert2_query, data_to_insert)

            # Commit the transaction to save the Extras entry
            connection.commit()
            print(f"Successfully inserted {cursor.rowcount} entries.")
            return new_org_id
        except mysql.connector.Error as err:
            print(f"Error when adding repo entry: '{err}'")
            return None


    def get_data_from_remote_api(self, org):
        """
        Fetch repository data from GitHub API for a given organization.
        
        Args:
            org (str): Name of the GitHub organization.
            
        Returns:
            list: A list of dictionaries containing repository information from GitHub API.
        """
        remote_access_data = RemoteRepoInit(org).get_data_from_github()
        # for repo in remote_access_data:
        #     print(repo['name'], repo['stargazers_count'])
        #     break
        return remote_access_data

    def process_user_request(self, organisation):
        """
        Process a user request for repository data of a specific organization.
        
        Retrieves all repositories associated with a given organization from the database.
        Creates a new entry if the organization doesn't exist.
        
        Args:
            organisation (str): Name of the GitHub organization.
            
        Returns:
            list: A list of dictionaries containing repository data (REPO_NAME, stargazers_count),
                  or None if tables don't exist or organization data cannot be retrieved.
        """
        if self.table_exists:
            org_id = self.get_or_create_table_id(self.db_connection, ORG_TABLE_NAME, 
                                                   ORG_NAME_COL, organisation)
            print(f"Got the org_id : {org_id}")
            if org_id != None:
                all_repos_data = self.get_matching_repos(self.db_connection, REPO_TABLE_NAME,
                                        FOREIGN_KEY_COLUMN, org_id)
                return all_repos_data
        else:
             print(f"Requested data does not exist")

    def get_matching_repos(self, connection, repos_table, fk_column, target_id):
        """
        Retrieve all repositories associated with a specific organization ID.
        
        Executes a SQL query to fetch repository names and stargazer counts for a given
        organization ID from the repositories table.
        
        Args:
            connection: MySQL database connection object.
            repos_table (str): Name of the repositories table.
            fk_column (str): Name of the foreign key column linking to organization ID.
            target_id (int): The organization ID to search for.
            
        Returns:
            list: A list of dictionaries containing repository data, or empty list if no
                  results found or connection is invalid.
        """
        if not connection or not connection.is_connected():
            print("Database connection is not active.")
            return []
            
        if target_id is None:
            print("Target ID is None. Cannot query the Repos table.")
            return []
        print(f"Fetching the repos for Parent_Org_ID: {target_id}")
        cursor = connection.cursor(dictionary=True) # dictionary=True returns results as dicts
        
        # SQL Query: Select ALL columns (*) from the Extras table
        # where the FOREIGN_KEY_COLUMN matches the target_id.
        query = f"""
        SELECT REPO_NAME, stargazers_count
        FROM {repos_table}
        WHERE {fk_column} = %s;
        """
        
        try:
            # Pass the ID as a tuple to the execute method
            cursor.execute(query, (target_id,)) 
            
            # fetchall() returns a list of all matching rows
            results = cursor.fetchall()
            
            if results:
                print(f"Found {len(results)} repos associated with ORG_ID {target_id}.")
                return results
            else:
                print(f"No repos found for ORG_ID {target_id}.")
                return []
                
        except Error as e:
            print(f"Error executing Repos retrieval query: {e}")
            return []
        finally:
            cursor.close()

    def create_org_table_entry(self, connection, table_name, column_name, target_value):
        """
        Create a new entry in the organizations table.
        
        Inserts a new organization name into the organization table using INSERT with
        DUPLICATE KEY UPDATE to handle existing entries gracefully. Then retrieves and
        returns the organization ID.
        
        Args:
            connection: MySQL database connection object.
            table_name (str): Name of the organization table.
            column_name (str): Column name for the organization name field.
            target_value (str): Name of the organization to insert.
            
        Returns:
            int: The ID of the organization entry, or None if retrieval fails.
        """
        if not connection or not connection.is_connected():
            print("Database connection is not active.")
            return False
    
        cursor = connection.cursor()
        insert_query = f"""
        INSERT INTO {table_name} ({column_name})
        VALUES (%s)
        ON DUPLICATE KEY UPDATE
        {column_name} = {column_name};
        """
        cursor.execute(insert_query, (target_value,))

        # Commit the transaction to make the changes permanent
        connection.commit()
        
        # Get the ID of the newly inserted row
        select_query = f"""
        SELECT Org_id
        FROM {table_name}
        WHERE {column_name} = %s;
        """
        cursor.execute(select_query, (target_value,))
        
        # Fetch the ID
        result = cursor.fetchone()
        if result:        
            print(f"Github_Organisation entry for {target_value}. ID: {result[0]}")
            return result[0]
        else:
            return None

    def get_or_create_table_id(self, connection, table_name, column_name, target_value):
        """
        Get the ID of an existing organization or create it if it doesn't exist.
        
        Searches for an organization by name in the table. If found, returns its ID.
        If not found, creates a new entry and returns the new ID.
        
        Args:
            connection: MySQL database connection object.
            table_name (str): Name of the organization table.
            column_name (str): Column name for the organization name field.
            target_value (str): Name of the organization to find or create.
            
        Returns:
            int: The organization ID, or None if an error occurs.
        """
        if not connection or not connection.is_connected():
            print("Database connection is not active.")
            return False
    
        cursor = connection.cursor()
    
        # Use prepared statements (placeholders %s) to prevent SQL Injection
        query = f"""
        SELECT {ORG_ID_COL}
        FROM {table_name}
        WHERE {column_name} = %s
        LIMIT 1;
        """
    
        try:
            # Pass the value as a tuple to the execute method
            cursor.execute(query, (target_value,)) 
            
            # fetchone() returns the row or None if no rows found
            result = cursor.fetchone()
            
            if result:
                org_id = result[0]
                print(f"Entry with {column_name}='{target_value}' exists.")
                return org_id
            else:
                org_id = self.create_new_entry_in_org_and_repos(connection, table_name, 
                                        column_name, target_value)
                print(f"Entry with {column_name}='{target_value}' created with ID {org_id}."  )
                return org_id
                
        except Error as e:
            print(f"Error executing entry check query: {e}")
            return None
        finally:
            cursor.close()

    def create_table_if_not_exist(self, connection, org_table_name, repo_table_name):
        """
        Create the organizations and repositories tables if they don't already exist.
        
        Creates two tables with proper relationships:
        - Organization table: Stores unique organization information with auto-incrementing ID
        - Repository table: Stores repository data with foreign key reference to organization
        
        Args:
            connection: MySQL database connection object.
            org_table_name (str): Name of the organization table to create.
            repo_table_name (str): Name of the repository table to create.
            
        Returns:
            bool: True if tables are created or already exist, False if an error occurs.
        """
        if not connection or not connection.is_connected():
            print("Database connection is not active.")
            return False
        
        cursor = connection.cursor()
        # Define the table structure using the target table name
        create_org_table_query = f"""
        CREATE TABLE IF NOT EXISTS {org_table_name} (
            Org_id INT AUTO_INCREMENT PRIMARY KEY,
            Organisation_name VARCHAR(255) NOT NULL UNIQUE
        );
        """
        create_repo_table_query = f"""
        CREATE TABLE IF NOT EXISTS {repo_table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {FOREIGN_KEY_COLUMN} INT NOT NULL,
            REPO_NAME VARCHAR(100) NOT NULL,
            stargazers_count INT,
            FOREIGN KEY ({FOREIGN_KEY_COLUMN}) REFERENCES {org_table_name}(Org_id)
        );
        """
            
        try:
            # Execute the query
            cursor.execute(create_org_table_query)
            cursor.execute(create_repo_table_query)
            
            # Commit the transaction to apply the table creation
            connection.commit()
            print(f"Table '{org_table_name}' checked/created successfully.")
            return True
            
        except Error as e:
            connection.rollback()
            print(f"Error creating table '{org_table_name}': {e}")
            return False
        finally:
            cursor.close()

    def check_db_connection(self, host_name, user_name, user_password):
        """
        Establish a connection to the MySQL database.
        
        Attempts to connect to the specified MySQL database. If already connected,
        returns the existing connection. Handles connection errors gracefully.
        
        Args:
            host_name (str): The hostname of the MySQL server.
            user_name (str): The username for authentication.
            user_password (str): The password for authentication.
            
        Returns:
            Connection: The database connection object if successful, or None if failed.
        """
        if self.db_connection:
            return self.db_connection

        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                password=user_password,
                database=DB_NAME
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection
    
    def create_database(self, connection):
        """
        Create the Stargazers_Database if it doesn't exist.
        
        Args:
            connection: MySQL database connection object.
        """
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {DB_NAME}")

    def create_server_connection(host_name, user_name, user_password):
        """
        Create a connection to the MySQL server without specifying a database.
        
        This is a static method that connects to the MySQL server at the root level,
        useful for operations that need to create databases.
        
        Args:
            host_name (str): The hostname of the MySQL server.
            user_name (str): The username for authentication.
            user_password (str): The password for authentication.
            
        Returns:
            Connection: The database connection object if successful, or None if failed.
        """
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                password=user_password
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection