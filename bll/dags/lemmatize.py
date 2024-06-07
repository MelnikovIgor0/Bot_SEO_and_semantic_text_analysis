from airflow import DAG
from airflow.operators.python import PythonOperator
from nltk.stem import WordNetLemmatizer
import nltk


def process_message(**context):
    message = context['dag_run'].conf["message"]
    wnl = WordNetLemmatizer()
    result = ''
    i = 0
    while i < len(message):
        if message[i].isalpha():
            c = ''
            while i < len(message) and message[i].isalpha():
                c += message[i]
                i += 1
            result += wnl.lemmatize(c)
        else:
            result += message[i]
            i += 1
    context['ti'].xcom_push(key='result', value=result)


default_args = {
    'owner': 'airflow',
    'retries': 1,
}

dag = DAG(
    'lemmatize',
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
