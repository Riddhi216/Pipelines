from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'export_to_formats',
    default_args=default_args,
    description='Export database tables to CSV, Parquet, and Avro',
    schedule_interval=timedelta(days=1),
)

def export_task():
    # Code to export data
    engine = get_engine('user', 'password', 'host', 'port', 'database')
    output_dir = '/path/to/outputws'
    table_name = 'export_datas'
    export_table_to_formats(engine, table_name, output_dir)

export_data = PythonOperator(
    task_id='export_data',
    python_callable=export_task,
    dag=dag,
)

export_data
