from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import requests


def translate_text(**context):
    conf = context['dag_run'].conf
    message = conf.get('message', '')
    lang_from = conf.get('lang_from', 'en')
    lang_to = conf.get('lang_to', 'ru')

    TRANSLATE_API_URL = 'https://translation.googleapis.com/language/translate/v2'
    TRANSLATE_API_KEY = 'YOUR_GOOGLE_TRANSLATE_API_KEY'

    payload = {
        'q': message,
        'source': lang_from,
        'target': lang_to,
        'format': 'text'
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TRANSLATE_API_KEY}'
    }

    response = requests.post(TRANSLATE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        translation = response.json()['data']['translations'][0]['translatedText']
        context['ti'].xcom_push(key='result', value=translation)
    else:
        raise ValueError(f"Translation API error: {response.text}")


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