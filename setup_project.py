from pathlib import Path
dirs=['.vscode', 'configs', 'data/raw', 'data/bronze', 'data/silver', 'data/gold', 'data/archive', 'generators', 'pyspark/bronze', 'pyspark/silver', 'pyspark/gold', 'snowflake', 'sql/ddl', 'sql/analytics', 'sql/procedures', 'airflow/dags', 'dashboard', 'quality/reports', 'quality/expectations', 'tests', 'logs']
for d in dirs: Path(d).mkdir(parents=True,exist_ok=True)
print('Project folders created.')
