from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import re


def censure_text(**context):
    conf = context['dag_run'].conf
    message = conf.get('message', '')

    bad_words = re.compile(r'\b(damn|hell|shit|fuck)\b', re.IGNORECASE)
    censored_message = bad_words.sub('****', message)

    context['ti'].xcom_push(key='result', value=censored_message)


default_args = {
    'owner': 'airflow',
    'retries': 1,
}

dag = DAG(
    'censure',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
)

censure_task = PythonOperator(
    task_id='process_message',
    python_callable=censure_text,
    provide_context=True,
    dag=dag,
)

censure_task