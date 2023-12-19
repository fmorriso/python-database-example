"""
https://www.sqlite.org/lang_datefunc.html
https://docs.python.org/3/library/datetime.html
https://www.sqlite.org/index.html
"""
import sys, sqlite3
from datetime import datetime


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def display_all_rows(table_name: str, cur: sqlite3.Cursor):
    """Displays all rows in the specified table using the specified cursor."""
    for row in cursor.execute(f"SELECT * FROM {table_name};"):
        print(row)


def get_server_datetime(cur: sqlite3.Cursor) -> datetime:
    """returns a Python datetime object containing the current SQLlite server's date/time."""
    query: str = """
    SELECT datetime('now', 'localtime') LocalTime;
    """
    results = cur.execute(query)
    row_local = results.fetchone()
    datetime_str: str = str(row_local[0])
    # column_name: str = results.description[0][0]
    # print(type(datetime_str))
    # print(datetime_str)
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return dt


def table_exists(name: str, cur: sqlite3.Cursor) -> bool:
    """Returns True of the speicifed table exists; otherwise returns False"""
    query_exists: str = f"""
                SELECT EXISTS (
                    SELECT 
                        name
                    FROM 
                        sqlite_schema 
                    WHERE 
                        type='table' AND 
                        name= '{name}'
                    );
            """
    print(query_exists)
    res = cur.execute(query_exists)
    fo_exists = res.fetchone()
    success_exists: bool = False
    if fo_exists is not None:
        success_exists: bool = bool(
            fo_exists[0]
        )  # (1,) is the expected "shape" of result.fetchall
    return success_exists


if __name__ == "__main__":
    print(f"Python version {get_python_version()}")

    print(f"SQL Lite version: {sqlite3.version}")
    # https://docs.python.org/3/library/sqlite3.html
    with sqlite3.connect(":memory:") as connection:
        # print(connection)
        cursor: sqlite3.Cursor = connection.cursor()
        # print(cursor)
        get_server_datetime(cursor)
        table_name = "movie"
        exists = table_exists(table_name, cursor)
        print(f"Before CREATE table exists = {exists}")

        query = f"CREATE TABLE {table_name}(title, year, score)"
        print(query)
        result = cursor.execute(query)
        fo = result.fetchone()
        success: bool = False
        if fo is not None:
            success: bool = bool(
                fo[0]
            )  # (1,) is the expected "shape" of result.fetchall
        print(f"CREATE table command result = {success}")

        exists = table_exists(table_name, cursor)
        print(f"After CREATE table exists = {exists}")
        cursor.execute("BEGIN TRANSACTION;")
        data = [
            ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
            ("Monty Python's The Meaning of Life", 1983, 7.5),
            ("Monty Python's Life of Brian", 1979, 8.0),
        ]
        cursor.executemany(f"INSERT INTO {table_name} VALUES(?, ?, ?)", data)
        connection.commit()  # Remember to commit the transaction after executing INSERT.

        """
        for row in cursor.execute(f"SELECT year, title FROM {table_name} ORDER BY year"):
            print(row)
        """
        display_all_rows(table_name, cursor)
