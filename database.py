import sqlite3
import pandas as pd


DB_NAME = "business_data.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def save_dataframe_to_db(df, table_name="sales"):
    conn = create_connection()
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()


def run_sql_query(query):
    conn = create_connection()
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result