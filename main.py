"""Scripts that demonstrates the completion of a set of exercises related to SQL and database management."""
from pathlib import Path

from sql import SQLRunner, get_engine

if __name__ == "__main__":
    config_file = Path('./db_config.ini')
    sql_runner = SQLRunner(get_engine(config_file))
    query = "SELECT * FROM orders LIMIT 10;"

    result = sql_runner.run_query(query)

    for row in result:
        print(row)
