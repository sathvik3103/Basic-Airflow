from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def startnumber(**context):
    context["ti"].xcom_push(key="current_value", value=18) 
    print("Starting with number 18")

def addtwenty(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids='start_task')
    newvalue = current_value + 20
    context["ti"].xcom_push(key="current_value", value=newvalue)
    print(f"Added twenty to {current_value}+20={newvalue}")


def subseven(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids='add_twenty')
    newvalue = current_value-7
    context["ti"].xcom_push(key="current_value", value=newvalue)
    print(f"Subtracted seven to {current_value}-7={newvalue}")

def multiplyten(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids='sub_seven')
    newvalue = current_value*10
    context["ti"].xcom_push(key="current_value", value=newvalue)
    print(f"Multipled seven to {current_value}*10={newvalue}")


with DAG(
    'math_seq_dag',
    start_date=datetime(2024,12,1),
    schedule_interval = '@weekly',
    catchup=False

) as dag:
     
    start_task = PythonOperator(
        task_id='start_task',
        python_callable=startnumber, #function to use
        provide_context=True
    )
    add_twenty = PythonOperator(
        task_id='add_twenty',
        python_callable=addtwenty, #function to use
        provide_context=True
    )
    sub_seven = PythonOperator(
        task_id='sub_seven',
        python_callable=subseven, #function to use
        provide_context=True
    )
    multiply_ten = PythonOperator(
        task_id='multiply_ten',
        python_callable=multiplyten, #function to use
        provide_context=True
    )
    #order of execution - setting dependencies
    start_task >> add_twenty >> sub_seven >> multiply_ten