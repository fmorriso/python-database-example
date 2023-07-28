import sys, sqlite3


def get_python_version() -> str:
    return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f'Python version {get_python_version()}')

    print(sqlite3.version)

    connection : sqlite3.Connection = sqlite3.connect(":memory:")
    print(connection)

    cursor: sqlite3.Cursor = connection.cursor()
    print(cursor)
