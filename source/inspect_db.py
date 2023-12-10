import os
import sqlite3

import pandas as pd


def main():
    db_path = os.path.abspath("database/commands.db")
    connection = sqlite3.connect(db_path)

    df = pd.read_sql_query("SELECT * FROM commands", connection)

    errors = df[(df["error"].notna())]
    print(errors)


if __name__ == "__main__":
    main()
