# Enterprise HR Data Engineering Pipeline & AI Copilot

This project demonstrates a full end-to-end Enterprise Data Engineering pipeline, featuring a **Medallion Architecture (Bronze, Silver, Gold)**, **Snowflake integration**, and a **Unified Streamlit Dashboard** with an embedded **AI Data Engineering Copilot**.

## Features
- **Data Generation**: Procedurally generates realistic HR datasets (Employees, Attendance).
- **Medallion Pipeline (Pandas Engine)**:
  - 🥉 **Bronze Layer**: Raw data ingestion into Parquet.
  - 🥈 **Silver Layer**: Data cleaning, schema enforcement, and deduplication (SCD Type 1).
  - 🥇 **Gold Layer**: Aggregated business Datamarts (Headcount, Payroll, Attendance Summaries).
- **Cloud Integration**: Uses the Snowflake Python Connector to push Gold layer datamarts directly to the cloud.
- **Streamlit Dashboard**: A dual-tab UI featuring interactive Plotly analytics and an embedded LLM Copilot trained specifically on this codebase.

---

## How to Run This Project Locally

If you are an interviewer or a peer reviewing this project, follow these exact steps to spin up the pipeline and dashboard on your local machine:

### 1. Clone & Setup
```bash
git clone https://github.com/SchemedCoder/25july_hr-data-engineering.git
cd 25july_hr-data-engineering

python -m venv .venv
# Windows: .\.venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables
You must provide your own API keys and Data Warehouse credentials for the pipeline to execute.
1. Create a file named `.env` in the root folder.
2. Add the following variables:
```env
GROQ_API_KEY=your_groq_api_key

SNOWFLAKE_ACCOUNT=your_snowflake_account_locator
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=PUBLIC
```

### 3. Execute the Pipeline
Run these three commands in order to generate data, process it through the Medallion architecture, and train the AI Copilot:

```bash
# 1. Generate Raw Data
python generators\generate_hr_data.py

# 2. Run the Medallion Pipeline (Bronze -> Silver -> Gold)
python run_pipeline.py

# 3. Train the AI Copilot on the codebase
python ingest_knowledge.py
```

### 4. Launch the Dashboard
Finally, start the Streamlit web application:
```bash
streamlit run dashboard\app.py
```
This will automatically open `http://localhost:8501/` in your browser. 
- Tab 1 contains the **HR Analytics**.
- Tab 2 contains the **AI Copilot** (Ask it: *"How does the Silver layer handle deduplication?"*)
