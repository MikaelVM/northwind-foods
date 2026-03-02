"""Module for running SQL queries against a database using SQLAlchemy."""
import configparser as cp
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, Result, create_engine, text
from sqlalchemy.orm import sessionmaker


class SQLRunner:
    """Run SQL queries against a given database engine."""

    def __init__(self, engine: Engine):
        """Initialize the SQLRunner with a SQLAlchemy engine.

        Args:
            engine (Engine): A SQLAlchemy Engine instance to connect to the database.
        """
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

    def run_query(self, query: str) -> Result[Any]:
        """Run a SQL query and return the results.

        Args:
            query (str): The SQL query to be executed.
        """
        with self.Session() as session:
            result = session.execute(text(query))
            return result


def get_engine(config_file: Path) -> Engine:
    """Create a SQLAlchemy engine based on the configuration file.

    Args:
        config_file (Path): Path to the configuration file containing database connection details.
    """
    connection_string = _get_connection_string(config_file)
    keep_alive_args = {
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5
    }
    return create_engine(connection_string, pool_pre_ping=True, connect_args=keep_alive_args)


def _get_connection_string(config_file: Path) -> str:
    """Construct a database connection string from the configuration file.

    Args:
        config_file (Path): Path to the configuration file containing database connection details.
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
