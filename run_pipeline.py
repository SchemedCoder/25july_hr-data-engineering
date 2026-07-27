import os
import pandas as pd
from datetime import datetime

base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, 'data')

def setup_directories():
    for layer in ['bronze', 'silver', 'gold']:
        os.makedirs(os.path.join(data_dir, layer), exist_ok=True)

def process_bronze():
    print("--- Running Bronze Layer (Ingestion) ---")
    # Read Raw CSVs and add ingestion metadata, save as Parquet
    emp_df = pd.read_csv(os.path.join(data_dir, 'raw', 'employees.csv'))
    att_df = pd.read_csv(os.path.join(data_dir, 'raw', 'attendance.csv'))
    
    emp_df['ingested_at'] = datetime.now()
    att_df['ingested_at'] = datetime.now()
    
    emp_df.to_parquet(os.path.join(data_dir, 'bronze', 'employees.parquet'))
    att_df.to_parquet(os.path.join(data_dir, 'bronze', 'attendance.parquet'))
    print("Bronze Layer complete.")

def process_silver():
    print("--- Running Silver Layer (Cleaning & Deduplication) ---")
    emp_df = pd.read_parquet(os.path.join(data_dir, 'bronze', 'employees.parquet'))
    att_df = pd.read_parquet(os.path.join(data_dir, 'bronze', 'attendance.parquet'))
    
    # Clean Employees: Keep latest record based on ingested_at (simulating SCD Type 1)
    clean_emp = emp_df.sort_values('ingested_at').drop_duplicates(subset=['emp_id'], keep='last')
    
    # Clean Attendance: Drop nulls
    clean_att = att_df.dropna()
    
    clean_emp.to_parquet(os.path.join(data_dir, 'silver', 'employees_clean.parquet'))
    clean_att.to_parquet(os.path.join(data_dir, 'silver', 'attendance_clean.parquet'))
    print("Silver Layer complete.")

def process_gold():
    print("--- Running Gold Layer (Business Datamarts) ---")
    emp_df = pd.read_parquet(os.path.join(data_dir, 'silver', 'employees_clean.parquet'))
    att_df = pd.read_parquet(os.path.join(data_dir, 'silver', 'attendance_clean.parquet'))
    
    # Datamart 1: Department Headcount & Salary
    dept_mart = emp_df.groupby('department').agg(
        headcount=('emp_id', 'count'),
        avg_salary=('salary', 'mean'),
        total_salary=('salary', 'sum')
    ).reset_index()
    
    # Datamart 2: Employee Attendance Summary
    att_df['punch_in'] = pd.to_datetime(att_df['punch_in'])
    att_df['punch_out'] = pd.to_datetime(att_df['punch_out'])
    att_df['hours_worked'] = (att_df['punch_out'] - att_df['punch_in']).dt.total_seconds() / 3600
    
    att_summary = att_df.groupby('emp_id').agg(
        days_present=('work_date', 'count'),
        total_hours=('hours_worked', 'sum')
    ).reset_index()
    
    # Join with employee details
    final_att_mart = pd.merge(att_summary, emp_df[['emp_id', 'first_name', 'last_name', 'department']], on='emp_id')
    
    dept_mart.to_parquet(os.path.join(data_dir, 'gold', 'department_summary.parquet'))
    final_att_mart.to_parquet(os.path.join(data_dir, 'gold', 'attendance_summary.parquet'))
    print("Gold Layer complete.")

if __name__ == "__main__":
    print("Starting Pipeline...")
    setup_directories()
    process_bronze()
    process_silver()
    process_gold()
    print("Pipeline Execution Finished Successfully!")