from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
 
def process_message(**context):
    message = context['dag_run'].conf.get('message')
    result = f"Word count: {len(message.split())}"
    context['ti'].xcom_push(key='result', value=result)
 
default_args = {
    'owner': 'airflow',
    'retries': 1,
}
 
dag = DAG(
    'count_dag',
    default_args=default_args,
    schedule_interval=None,
)
 
process_message_task = PythonOperator(
    task_id='process_message',
    python_callable=process_message,
    provide_context=True,
    dag=dag,
)
 
process_message_task