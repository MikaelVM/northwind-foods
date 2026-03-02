import configparser as cp
from pathlib import Path
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import sessionmaker

class SQLRunner:
    """Run SQL queries against a given database engine."""
    def __init__(self, engine: Engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

    def run_query(self, query: str):
        """Run a SQL query and return the results."""
        with self.Session() as session:
            result = session.execute(text(query))
            return result.fetchall()


def get_engine(config_file: Path) -> Engine:
    """Create a SQLAlchemy engine based on the configuration file."""
    connection_string = _get_connection_string(config_file)
    keep_alive_args = {
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5
    }
    return create_engine(connection_string, pool_pre_ping=True, connect_args=keep_alive_args)

def _get_connection_string(config_file: Path) -> str:
    """Construct a database connection string from the configuration file."""
    config = cp.ConfigParser()
    config.read(config_file)

    user = config['DBCONFIG']['User']
    password = config['DBCONFIG']['Password']
    host = config['DBCONFIG']['Host']
    port = config['DBCONFIG']['Port']
    database = config['DBCONFIG']['Database']

    return f'postgresql://{user}:{password}@{host}:{port}/{database}'