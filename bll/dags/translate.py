from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

def translate_text(**context):
    conf = context['dag_run'].conf
    message = conf.get('message', '')
    lang_from = conf.get('lang_from', 'en')
    lang_to = conf.get('lang_to', 'ru')

    chat = GigaChat(
        credentials='GIGACHAT_KEY',
        verify_ssl_certs=False)

    messages = [SystemMessage(
        content="Ты бот переводчик, выдавать в сообщении ничего кроме переведенного текста не нужно."
    ), HumanMessage(content=f"Translate from {lang_from} to {lang_to} '{message}'")]

    res = chat(messages)
    messages.append(res)
    context['ti'].xcom_push(key='result', value=res.content)

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
