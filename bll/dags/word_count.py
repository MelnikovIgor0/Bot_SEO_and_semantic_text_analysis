from airflow import DAG
from airflow.operators.python import PythonOperator


def process_message(**context):
    message = context['dag_run'].conf["message"]
    result = f"Word count: {len(message.split())}"
    context['ti'].xcom_push(key='result', value=result)


default_args = {
    'owner': 'airflow',
    'retries': 1,
}

dag = DAG(
    'count',
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
