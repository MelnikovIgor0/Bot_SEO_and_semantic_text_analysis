from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import openai

def translate_text(**context):
    conf = context['dag_run'].conf
    message = conf.get('message', '')
    lang_from = conf.get('lang_from', 'en')
    lang_to = conf.get('lang_to', 'ru')

    OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

    openai.api_key = OPENAI_API_KEY

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following text from {lang_from} to {lang_to}:\n\n{message}",
        max_tokens=1000
    )

    if response:
        translation = response.choices[0].text.strip()
        context['ti'].xcom_push(key='result', value=translation)
    else:
        raise ValueError("Translation API error")

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

dag = DAG(
    'translate',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
)

translate_task = PythonOperator(
    task_id='process_message',
    python_callable=translate_text,
    provide_context=True,
    dag=dag,
)

translate_task
