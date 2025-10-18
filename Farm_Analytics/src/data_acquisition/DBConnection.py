import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, exc
import sqlalchemy
import mysql.connector

class DBConnection:
    _instance = None
    _engine = None
    _params = None
    
    def __new__(cls):
        """
        The method __new__ is called before __init__ and it creates a new instance for the class DBConnection in the memory. 
        
        This method ensure that only one instance of the class can be created(Singleton Pattern):
            -when called, it checks if an instance already exists and returns it if so.
            -if not it creates a new instance and loads the environment variables from .env file.

        Args:
            cls: the reference to the DBConnection class itself.
        Returns:
            DBConnection: The singleton instance of DBConnection class.
        """
        if cls._instance is None:
            cls._instance = super(DBConnection,cls).__new__(cls)
            load_dotenv()
            cls._params = {
                "host" : os.getenv("DB_HOST", "localhost"),
                "port" : int(os.getenv("DB_PORT", "3306")),
                "user" : os.getenv("DB_USER", "your_username"),
                "password" : os.getenv("DB_PASSWORD", "your_password"),
                "database" : os.getenv("DB_NAME", "your_database_name")
            }
            cls.engine = None 
        return cls._instance
    
    def get_engine(self):
        """
        Create a SQLAlchemy engine to connect MySQL database only one time.
        
        The engine uses the PyMySQL driver to establish a connection
          and connection parameters are loaded from the environment variables in the Singleton constructor.
          
        The function returns an engine connection object that can handle a pool of connections.

        You dont't need to install the necessary database drivers pymysql, sqlalchemy and mysql-connector-python for the connection to work because
           all dependencies are included in the dependencies.txt file and you can install them by running the command from the root project directory:
               pip install -r dependencies.txt

        Args:
            self: the Singleton instance of DBConnection class.
        Returns:
            sqlalchemy.engine.Engine: The SQLAlchemy Engine object for connecting to the MySQL database.
        """
        if self._engine is None:
            try:
                self._engine = create_engine(
                    f"mysql+pymysql://{self._params['user']}:{self._params['password']}@{self._params['host']}:{self._params['port']}/{self._params['database']}"
                )
            except exc.ArgumentError as e:
                print(f"Connection string error: {e}")
            except exc.NoSuchModuleError:
                print("""
                      pymysql driver not found ensure you execute the command pip install -r dependencies.txt in the root project
                      to install all dependencies.
                      """)
            except Exception as e:
                print(f"Error creating SQLAlchemy engine: {e}")            
        return self._engine
    
    def get_mysql_connection(self):
        return mysql.connector.connect(**self._params)
