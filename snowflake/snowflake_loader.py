import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

def get_snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
    )

def upload_gold_layer():
    print("Connecting to Snowflake...")
    try:
        conn = get_snowflake_conn()
    except Exception as e:
        print(f"Failed to connect to Snowflake: {e}")
        return

    base_dir = os.path.dirname(os.path.dirname(__file__))
    gold_dir = os.path.join(base_dir, 'data', 'gold')
    
    # Upload Department Summary
    dept_file = os.path.join(gold_dir, 'department_summary.parquet')
    if os.path.exists(dept_file):
        print("Uploading Department Summary to Snowflake...")
        df = pd.read_parquet(dept_file)
        df.columns = [c.upper() for c in df.columns]
        success, _, nrows, _ = write_pandas(conn, df, 'DEPARTMENT_SUMMARY_GOLD', auto_create_table=True, overwrite=True)
        if success:
            print(f"Uploaded {nrows} rows to DEPARTMENT_SUMMARY_GOLD")

    # Upload Attendance Summary
    att_file = os.path.join(gold_dir, 'attendance_summary.parquet')
    if os.path.exists(att_file):
        print("Uploading Attendance Summary to Snowflake...")
        df = pd.read_parquet(att_file)
        df.columns = [c.upper() for c in df.columns]
        success, _, nrows, _ = write_pandas(conn, df, 'ATTENDANCE_SUMMARY_GOLD', auto_create_table=True, overwrite=True)
        if success:
            print(f"Uploaded {nrows} rows to ATTENDANCE_SUMMARY_GOLD")

    conn.close()
    print("Snowflake Upload Complete!")

if __name__ == "__main__":
    upload_gold_layer()
