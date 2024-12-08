from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

#defining task 1

def preprocess_data():
    print("Preprocessing the data.....")

#defining task 2

def train_model():
    print("Training model.....")

#defining task 3

def evaluate_model():
    print("Evaluating model.....")

with DAG(
    'mlpipeline',
    start_date=datetime(2024,12,1),
    schedule_interval = '@weekly'
) as dag:
     
    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data, #function to use
    )
    train = PythonOperator(
        task_id='train_model',
        python_callable=train_model,  
    ) 
    evaluate = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,  
    ) 

    #order of execution - setting dependencies
    preprocess_data_task >> train >> evaluate