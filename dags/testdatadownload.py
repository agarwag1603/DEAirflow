
import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_wikipedia_page(url):
    import requests

    print("Getting wikipedia page...", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # check if the request is successful

        return response.text
    except requests.RequestException as e:
        print(f"An error occured: {e}")

def extract_data_from_wiki(**kwargs):
    url = kwargs['url']
    html = get_wikipedia_page(url)
    print("Html data is written in text file")

    with open('/opt/airflow/data/response_wiki.txt', 'w') as file:
        file.write(html)

dag = DAG(
    dag_id='wiki_flow',
    default_args={
        "owner": "Gaurav",
        "start_date": datetime(2023, 10, 1),
    },
    schedule=None,
    catchup=False
)

extract_data_from_wiki = PythonOperator(
    task_id="extract_data_from_wikipedia",
    python_callable=extract_data_from_wiki,
    #provide_context=True,
    op_kwargs={"url": "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"},
    dag=dag
)




#data.to_csv('data/' + file_name, index=False)