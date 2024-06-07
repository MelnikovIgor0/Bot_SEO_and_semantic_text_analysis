import urllib

from flask import Flask, request, jsonify
import requests
import time
import nltk
import ssl

app = Flask(__name__)

AIRFLOW_API_URL = 'http://localhost:8080/api/v1/dags/{dag_id}/dagRuns'


@app.route('/trigger_dag', methods=['POST'])
def trigger_dag():
    dag_id = request.args.get('dag_id')
    message = request.args.get('message')

    payload = {
        'conf': {
            'message': message
        }
    }

    if dag_id == 'translate':
        lang_from = request.args.get('lang_from')
        lang_to = request.args.get('lang_to')
        payload = {
            'conf': {
                'message': message,
                'lang_from': lang_from,
                'lang_to': lang_to
            }
        }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(AIRFLOW_API_URL.format(dag_id=dag_id), headers=headers, json=payload, auth=('admin', 'eEA2XBB3YVhRtHNA'))

    if response.status_code == 200:
        run_id = response.json()['dag_run_id']

        # Polling for DAG result
        result = poll_for_result(dag_id, run_id)
        if result:
            return jsonify({"status": "success", "response": result}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to get result from DAG"}), 500
    else:
        return jsonify({"status": "error", "message": response.text}), response.status_code


def poll_for_result(dag_id, run_id, poll_interval=10, timeout=300):
    elapsed_time = 0
    auth=('admin', 'eEA2XBB3YVhRtHNA')
    while elapsed_time < timeout:
        response = requests.get(AIRFLOW_API_URL.format(dag_id=dag_id) + f"/{run_id}", auth=auth)
        if response.status_code == 200:
            dag_status = response.json()
            if dag_status['state'] == 'success':
                response_xcom = requests.get(
                    f"http://localhost:8080/api/v1/dags/{dag_id}/dagRuns/{urllib.parse.quote(run_id)}/taskInstances",
                    auth=auth)
                if response_xcom.status_code == 200:
                    task_instances = response_xcom.json()['task_instances']
                    for task in task_instances:
                        print(task['task_id'])
                        if task['task_id'] == 'process_message':
                            result_response = requests.get(f"http://localhost:8080/api/v1/dags/{dag_id}/dagRuns/{urllib.parse.quote(run_id)}/taskInstances/process_message/xcomEntries/result", auth=auth)
                            if result_response.status_code == 200:
                                result = result_response.json()['value']
                                return result
        time.sleep(poll_interval)
        elapsed_time += poll_interval
    return None


if __name__ == '__main__':
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('wordnet')
    app.run(host='0.0.0.0', port=8765)
