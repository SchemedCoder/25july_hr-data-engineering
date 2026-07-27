import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_data():
    print("Generating HR Data...")
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)

    # 1. Generate Employees
    np.random.seed(42)
    num_employees = 200
    emp_ids = range(1001, 1001 + num_employees)
    depts = ['Engineering', 'Sales', 'HR', 'Marketing', 'Finance']
    
    employees = pd.DataFrame({
        'emp_id': emp_ids,
        'first_name': [f"First_{i}" for i in emp_ids],
        'last_name': [f"Last_{i}" for i in emp_ids],
        'department': np.random.choice(depts, num_employees),
        'salary': np.random.randint(50000, 150000, num_employees),
        'hire_date': [datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1000)) for _ in range(num_employees)]
    })
    
    # Add some duplicate/updated records to test Silver layer deduplication
    updates = employees.sample(20).copy()
    updates['salary'] = updates['salary'] + 10000
    employees = pd.concat([employees, updates])
    
    employees.to_csv(os.path.join(raw_dir, 'employees.csv'), index=False)
    
    # 2. Generate Attendance
    dates = [datetime.today().date() - timedelta(days=x) for x in range(30)]
    attendance_records = []
    
    for emp_id in emp_ids:
        for d in dates:
            if d.weekday() < 5: # Monday to Friday
                # 90% chance they showed up
                if random.random() < 0.9:
                    punch_in = datetime.combine(d, datetime.min.time()) + timedelta(hours=9, minutes=random.randint(-30, 30))
                    punch_out = punch_in + timedelta(hours=8, minutes=random.randint(0, 60))
                    attendance_records.append({
                        'emp_id': emp_id,
                        'work_date': d,
                        'punch_in': punch_in,
                        'punch_out': punch_out
                    })
                    
    attendance = pd.DataFrame(attendance_records)
    attendance.to_csv(os.path.join(raw_dir, 'attendance.csv'), index=False)
    
    print(f"Generated {len(employees)} employee records and {len(attendance)} attendance records.")
    print(f"Data saved to {raw_dir}")

if __name__ == "__main__":
    generate_data()
