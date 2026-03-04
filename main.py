"""Scripts that demonstrates the completion of a set of exercises related to SQL and database management."""
from pathlib import Path

import pandas as pd
from figures import bar_plot
from sql import SQLAlchemySQLRunner


if __name__ == "__main__":
    config_file = Path('./db_config.ini')
    sqlalchemy_runner = SQLAlchemySQLRunner(config_file)

    # Exercise 2: Fundamental data extraction using SQL queries
    for file in Path('sql_query/exercise2').glob('*.sql'):
        print(f"Running query from file: {file.name}")
        print(sqlalchemy_runner.get_dataframe_from_query(file))
        print('-' * 200)

    # Exercise 4: Testing the connection and running a simple query
    query = "SELECT * FROM products LIMIT 5;"
    print(f'Running simple query: {query}')
    print(sqlalchemy_runner.get_dataframe_from_query(query))
    print('-' * 200)

    # Exercise 5: Extracting data from the database and analyzing it using pandas
    print("Running query to extract total sales per country and creating a bar plot...")
    query = Path('./sql_query/exercise5/bar_plot/01_sales_per_country.sql')
    df = pd.DataFrame(sqlalchemy_runner.get_list_from_query(query), columns=['country', 'total_sales'])
    figures_save_path = Path('./output/figures/sales_per_country.png')

    bar_plot(
        df,
        x_col='country', y_col='total_sales',
        title='Total Sales per Country',
        x_label='Country', y_label='Total Sales',
        save_path=figures_save_path
    )
    print(f"Bar plot saved to: {figures_save_path}")
    print('-' * 200)

    # Exercise 6: CRUD operations on a new separate table
    sql_folder = Path('./sql_query/exercise6')
    print("Part 1: Creating a new table - 'rpt_sales'")
    if sqlalchemy_runner.run_query(sql_folder / '00_rpt_sales.sql'):
        print("Table 'rpt_sales' created successfully.")
    else:
        print("Failed to create the table 'rpt_sales'.")
    print('-' * 100)

    print("Part 2: Performing CRUD operations on the 'rpt_sales' table")
    print("Creating new records in the 'rpt_sales' table")
    result = sqlalchemy_runner.get_list_from_query(sql_folder / '01_create.sql')
    print(f"Number of records created: {len(result)}")
    print('-' * 100)

    print("Reading records from the 'rpt_sales' table")
    result = sqlalchemy_runner.get_list_from_query(sql_folder / '02_read.sql')
    print(pd.DataFrame(result))
    print('-' * 100)

    print("Updating records in the 'rpt_sales' table - Updating revenue for the year 1997 by increasing it by 10%")
    result = sqlalchemy_runner.get_list_from_query(sql_folder / '03_update.sql')
    print(f"Number of records updated: {len(result)}")
    print('-' * 100)

    print("Deleting records from the 'rpt_sales' table - Deleting records from the year 1997")
    result = sqlalchemy_runner.get_list_from_query(sql_folder / '04_delete.sql')
    print(f"Number of records deleted: {len(result)}")
    print('-' * 100)

    print("Part 3: Dropping the 'rpt_sales' table to clean up the database")
    if sqlalchemy_runner.run_query(sql_folder / '05_drop.sql'):
        print("Table 'rpt_sales' dropped successfully.")
    else:
        print("Failed to drop the table 'rpt_sales'.")
    print('-' * 200)