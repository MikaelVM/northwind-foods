"""Module for running SQL queries against a database and returning the results in various formats.

Designer notes by Mikael Vind Mikkelsen (2026-03-04):
This implementation is too complex for the use case of this assignment, but I wanted to challenge myself and learn more
about abstract classes and the differences between SQLAlchemy and psycopg3.

I converted what was once a simple class that used SQLAlchemy to run SQL queries, into an abstract class with two
 concrete implementations: one using SQLAlchemy and another using psycopg3.

The abstract class defines the interface for running SQL queries and fetching results, while the concrete
 implementations provide the specific logic for each library.
"""
import configparser as cp
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List

import psycopg
from pandas import DataFrame
from sqlalchemy import Result, create_engine, text
from sqlalchemy.orm import sessionmaker


class QueryRunner(ABC):
    """Base class for running queries against a database."""

    @abstractmethod
    def __init__(self, warnings: bool = True):
        """Initialize the QueryRunner.

        Args:
            warnings (bool): Whether to print warnings if the query does not return any results or if an error occurs
             while fetching results (default: True).
        """
        self.warnings = warnings

    @abstractmethod
    def get_list_from_query(self, query: str | Path) -> List[List[Any]]:
        """Run a query and return the results as a list of lists (inner list represents a row of the result).

        Args:
            query (str|Path): A query as a string or a Path to a file containing the query.
        """
        pass

    @abstractmethod
    def get_dataframe_from_query(self, query: str | Path) -> DataFrame | None:
        """Run a query and return the results as a pandas DataFrame (with column names as DataFrame columns).

        Args:
            query (str|Path): A query as a string or a Path to a file containing the query.

        Result:
            DataFrame: The results of the query as a pandas DataFrame.
        """
        pass

    @abstractmethod
    def run_query(self, query: str | Path) -> bool:
        """Run a query against the database and return whether the query was executed successfully.

        Args:
            query (str|Path): A query as a string or a Path to a file containing the query.

        Result:
            bool: True if the query was executed successfully, False otherwise.
        """
        pass

    # TODO: Iterate on this method. Should be more generic and take a message argument,
    #  so that it can be used in different contexts, not only for fetching results.
    def _print_warning(self, error: Exception) -> None:
        """Print a warning message if fetching results fails or if the query does not return any results.

        Args:
            error (Exception): The exception that was raised while fetching results.
        """
        if self.warnings:
            print(f"Warning: An error occurred while fetching results. Did you run a query that does not return any "
                  f"results? \nError details: {error}")

    def _get_string_from_query(self, query: str | Path) -> str:
        """Take a query as a string or a Path to a file containing a query and returns the query as a string.

        Args:
            query (str|Path): A query as a string or a Path to a file containing the query.
        """
        if isinstance(query, Path):
            return self._query_path_to_string(query)
        elif isinstance(query, str):
            return query
        else:
            raise ValueError("Query must be a string or a Path to a file containing the query.")

    @staticmethod
    def _query_path_to_string(query_path: Path) -> str:
        """Take a Path to a file containing a SQL query and returns the query as a string.

        Args:
            query_path (Path): A Path to a file containing the SQL query.

        Raises:
            FileNotFoundError: If the file at the given path does not exist.
        """
        if not query_path.exists():
            raise FileNotFoundError(f"Query file '{query_path.name}' not found.")
        else:
            with open(query_path, 'r') as file:
                return file.read()


class PostgresSQLQueryRunner(QueryRunner, ABC):
    """Base class for running SQL queries against a PostgreSQL database.

    This class is not meant to be used directly, but rather to be inherited by concrete implementations that use
     specific libraries (e.g., SQLAlchemy, psycopg3) to run SQL queries against a PostgreSQL database.
    """

    def __init__(self, config_file: Path, warnings: bool = True):
        """Initialize the SQLRunner.

        Args:
            config_file (Path): Path to the configuration file containing database connection details.
            warnings (bool): Whether to print warnings if the query does not return any results or if an error occurs
             while fetching results (default: True).
        """
        super().__init__(warnings)
        self.config_file = config_file
        self.connection_string = self.__get_connection_string(self.config_file)

    @staticmethod
    def __get_connection_string(config_file: Path) -> str:
        """Construct a database connection string from the configuration file.

        The configuration file should have the following format:
        [DBCONFIG]
        User = your_username
        Password = your_password
        Host = your_host
        Port = your_port
        Database = your_database

        Args:
            config_file (Path): Path to the configuration file containing database connection details.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
        """
        config = cp.ConfigParser()

        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
        else:
            config.read(config_file)

        user = config['DBCONFIG']['User']
        password = config['DBCONFIG']['Password']
        host = config['DBCONFIG']['Host']
        port = config['DBCONFIG']['Port']
        database = config['DBCONFIG']['Database']

        return f'postgresql://{user}:{password}@{host}:{port}/{database}'


class SQLAlchemyQueryRunner(PostgresSQLQueryRunner):
    """Class for running SQL queries against a given database engine using the SQLAlchemy library."""

    def __init__(self, config_file: Path, warnings: bool = True):
        """Initialize the SQLRunner with a SQLAlchemy engine.

        Args:
            config_file (Path): Path to the configuration file containing database connection details.
            warnings (bool): Whether to print warnings if the query does not return any results or if an error occurs
             while fetching results (default: True).
        """
        super().__init__(config_file, warnings)
        self.Session = sessionmaker(bind=create_engine(self.connection_string))

    def get_list_from_query(self, query: str | Path) -> List[List[Any]]:
        """Run a SQL query and return the results.

        Args:
            query (str|Path): A SQL query as a string or a Path to a file containing the SQL query.
        """
        result = self._execute_query(query)

        try:
            return [list(row) for row in result.fetchall()]
        except Exception as e:
            self._print_warning(e)
            return []

    def get_dataframe_from_query(self, query: str | Path) -> DataFrame | None:
        """Run a SQL query and return the results as a pandas DataFrame.

        Args:
            query (str|Path): A SQL query as a string or a Path to a file containing the SQL query.
        """
        query = self._query_path_to_string(query) if isinstance(query, Path) else query

        try:
            return DataFrame(self._execute_query(query))
        except Exception as e:
            self._print_warning(e)
            return None

    def get_result_from_query(self, query: str | Path) -> Result:
        """Run a SQL query and return the raw Result object from SQLAlchemy.

        NOTE:
            This method is specifically for SQLAlchemy and is not part of the abstract base class, as it is not
            applicable to other libraries.

        Args:
            query (str|Path): A SQL query as a string or a Path to a file containing the SQL query.
        """
        query = self._query_path_to_string(query) if isinstance(query, Path) else query

        return self._execute_query(query)

    def run_query(self, query: str | Path) -> bool:
        """Run a SQL query against the database and return whether the query was executed successfully.

        Args:
            query (str|Path): A SQL query as a string or a Path to a file containing the SQL query.

        Result:
            bool: True if the query was executed successfully, False otherwise.
        """
        query = self._query_path_to_string(query) if isinstance(query, Path) else query

        try:
            with self.Session() as session:
                session.execute(text(self._get_string_from_query(query)))
                session.commit()
            return True
        except Exception as e:
            self._print_warning(e)
            return False

    def _execute_query(self, query: str | Path) -> Result:
        """Execute a SQL query and return the result.

        Args:
            query (str): A SQL query as a string.
        """
        with self.Session() as session:
            result = session.execute(text(self._get_string_from_query(query)))
            session.commit()
            return result


class Psycopg3QueryRunner(PostgresSQLQueryRunner):
    """Class for running SQL queries against a given database engine using the SQLAlchemy library."""

    def __init__(self, config_file: Path, warnings: bool = True):
        """Initialize the SQLRunner with a psycopg3 connection string.

        Args:
            config_file (Path): Path to the configuration file containing database connection details.
            warnings (bool): Whether to print warnings if the query does not return any results or if an error occurs
             while fetching results (default: True).
        """
        super().__init__(config_file, warnings)

    def get_list_from_query(self, query: str | Path) -> list[list[Any]]:
        """Run a SQL query and return the results.

        Args:
            query (str|Path): A SQL query as a string or a Path to a file containing the SQL query.
        """
        query = self._query_path_to_string(query) if isinstance(query, Path) else query

        # TODO: Verify that the connection is properly closed after the query is executed, even if an error occurs.
        with psycopg.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                try:
                    return [list(row) for row in cur.execute(query).fetchall()]
                except Exception as e:
                    self._print_warning(e)
                    return []

    def get_dataframe_from_query(self, query: str | Path) -> DataFrame | None:
        """Run a SQL query and return the results as a pandas DataFrame.

        Args:
            query (str|Path): A SQL query as a string or a Path to a file containing the SQL query.
        """
        query = self._query_path_to_string(query) if isinstance(query, Path) else query

        with psycopg.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                try:
                    return DataFrame(cur.execute(query))
                except Exception as e:
                    self._print_warning(e)
                    return None
