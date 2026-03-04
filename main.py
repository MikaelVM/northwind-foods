"""Scripts that demonstrates the completion of a set of exercises related to SQL and database management."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sql import SQLRunner, get_engine


def bar_plot(
        dataframe: pd.DataFrame,
        *,
        x_col: str,
        y_col: str,
        title: str,
        x_label: str,
        y_label: str,
        save_path: Path
) -> None:
    """Create a bar plot from a DataFrame and save it to a file.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the data to plot.
        x_col (str): The name of the column to use for the x-axis.
        y_col (str): The name of the column to use for the y-axis.
        title (str): The title of the plot.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        save_path (Path): The path where the plot image will be saved.
    """
    plt.figure().set_size_inches(10, 6)
    plt.bar(dataframe[x_col], dataframe[y_col])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=50)
    plt.savefig(save_path, format='png')
    plt.close()


if __name__ == "__main__":
    config_file = Path('./db_config.ini')
    sql_runner = SQLRunner(get_engine(config_file))

    # Exercise 2: Fundamental data extraction using SQL queries
    for file in Path('sql_query/exercise2').glob('*.sql'):
        print(f"Running query from file: {file.name}")
        result = sql_runner.run_query(file)

        for row in result:
            print(row)
        print('-' * 200)

    # Exercise 4: Testing the connection and running a simple query
    query = "SELECT * FROM products LIMIT 5;"

    result = sql_runner.run_query(query)

    print(f'Running simple query: {query}')
    for row in result:
        print(row)

    # Exercise 5: Extracting data from the database and analyzing it using pandas
    query = Path('./sql_query/exercise5/bar_plot/01_sales_per_country.sql')
    df = pd.DataFrame(sql_runner.run_query(query), columns=['country', 'total_sales'])
    figures_save_dir = Path('./output/figures')

    bar_plot(
        df,
        x_col='country', y_col='total_sales',
        title='Total Sales per Country',
        x_label='Country', y_label='Total Sales',
        save_path=figures_save_dir / 'sales_per_country.png'
    )

    # Exercise 6: CRUD operations on a new separate table
    # TODO: Create a new table that is a merge of employeeterritories, territories and region, as the last 2 tables are
    #       redundant. Then, perform CRUD operations on the new table and demonstrate the changes in the database.
