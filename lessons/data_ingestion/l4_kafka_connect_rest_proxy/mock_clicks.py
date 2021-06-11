import time

from faker import Faker
import psycopg2

fake = Faker()

POSTGRES_HOST = "localhost"
POSTGRES_DB = "classroom"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
TABLE_NAME = "clicks"
PK_COLUMN = "id"
ROW_DISPLAY_LIMIT = 5


def mock_clicks(id_):
    """
    Gemerates a fake row for the clicks table
    :param id_: a monotonically increasing id, this is the table's PK
    :return: tuple
    """
    email = fake.email()
    timestamp = f'{fake.date()} {fake.time()}'
    uri = fake.uri()
    number = fake.random_number(2)

    return id_, email, timestamp, uri, number


def build_query(start, end):
    """
    Takes a start and end int, builds a row for each, and appends them to the INSERT statement
    :param start: the beginning of the range of rows to create
    :param end: the end of the range of rows to create
    :return: string, insert statement
    """
    query = "INSERT INTO {table} VALUES \n{values}"
    values = ""
    for _ in range(start, end + 1):
        row = mock_clicks(_)
        if _ == end:
            values += f"\t{row}\n"
        else:
            values += f"\t{row},\n"
    return query.format(table=TABLE_NAME, values=values).rstrip(",")


def execute_query(query, sample=False):
    """
    Executes a query against postgres, then optionally shows the last n rows of the table
    :param query: a SQL-formatted query string
    :param verbose: whether or not to display sample rows
    :return: None
    """

    conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST)
    cur = conn.cursor()

    cur.execute(query)
    print(f"Showing the last n rows of {ROW_DISPLAY_LIMIT}")
    if sample:
        cur.execute(f"select * from {TABLE_NAME} order by {PK_COLUMN} desc limit {ROW_DISPLAY_LIMIT}")
        for row in cur.fetchall():
            print(row)
    conn.commit()
    conn.close()
    cur.close()


def main():
    """
    Generates a bunch of fake users, and builds and executes an insert statement to populate the clicks
    table with that statement
    :return: None
    """
    # Set start and end values
    start, end = 1, 100000

    # Build and execute query
    start_ts = time.time()
    query = build_query(start, end)
    query_build_ts = time.time()
    execute_query(query)
    execute_ts = time.time()

    # Print runtime results
    query_build_time = query_build_ts - start_ts
    execute_time = execute_ts - query_build_ts
    print(f"Time to build query: {query_build_time:.2f}")
    print(f"Time to insert rows: {execute_time:.2f}")


if __name__ == "__main__":
    main()
