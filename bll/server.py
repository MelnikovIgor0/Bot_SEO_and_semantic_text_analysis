from flask import Flask, request, jsonify
import requests
import time
 
app = Flask(__name__)
 
AIRFLOW_API_URL = 'http://localhost:8080/api/v1/dags/{dag_id}/dag_runs'
 
@app.route('/trigger_dag', methods=['POST'])
def trigger_dag():
    data = request.json
    dag_id = data['dag_id']
    message = data['message']
 
    payload = {
        'conf': {
            'message': message
        }
    }
 
    response = requests.post(AIRFLOW_API_URL.format(dag_id=dag_id), json=payload, auth=('airflow', 'airflow'))
 
    if response.status_code == 200:
        run_id = response.json()['dag_run_id']
 
        # Polling for DAG result
        result = poll_for_result(dag_id, run_id)
        if result:
            return jsonify({"status": "success", "result": result}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to get result from DAG"}), 500
    else:
        return jsonify({"status": "error", "message": response.text}), response.status_code
 
def poll_for_result(dag_id, run_id, poll_interval=10, timeout=300):
    elapsed_time = 0
    while elapsed_time < timeout:
        response = requests.get(AIRFLOW_API_URL.format(dag_id=dag_id) + f"/{run_id}", auth=('airflow', 'airflow'))
        if response.status_code == 200:
            dag_status = response.json()
            if dag_status['state'] == 'success':
                response_xcom = requests.get(f"http://localhost:8080/api/v1/dags/{dag_id}/dag_runs/{run_id}/task_instances", auth=('airflow', 'airflow'))
                if response_xcom.status_code == 200:
                    task_instances = response_xcom.json()['task_instances']
                    for task in task_instances:
                        if task['task_id'] == 'process_message':
                            result_response = requests.get(f"http://localhost:8080/api/v1/dags/{dag_id}/dag_runs/{run_id}/task_instances/{task['task_id']}/xcom_entries/{task['task_id']}", auth=('airflow', 'airflow'))
                            if result_response.status_code == 200:
                                result = result_response.json()['value']
                                return result
        time.sleep(poll_interval)
        elapsed_time += poll_interval
    return None
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)
