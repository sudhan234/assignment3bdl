#imports
import os
import zipfile
import requests
from bs4 import BeautifulSoup
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime

#function for scrape task
def scrape_data(ds, year, num_files, **kwargs):
    print('cwd:',os.getcwd())
    base_url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}'
    os.makedirs(f'/opt/airflow/data/{year}', exist_ok=True)
    url = base_url.format(year=year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table')
    anchors = table.find_all('a')
    #finds all links with csv included in it
    anchors = [a for a in anchors if 'csv' in a.text]
    files_downloaded=0
    #crashflag for empty links
    crashflag=0
    for anchor in anchors:
        if crashflag>2:
            break
        #limit on number of files downloaded per year
        if files_downloaded>=num_files:
            break
        file = anchor.text
        file_url = f'{url}/{file}'
        if(requests.get(file_url)==None):
            crashflag+=1
            continue
        #gets the files from the url
        res = requests.get(file_url)
        csv = res.text
        with open(f'/opt/airflow/data/{year}/{file}', 'w') as f:
            f.write(csv)
        files_downloaded=files_downloaded+1

#function for zip task
def zip_directory():
    os.makedirs('/opt/airflow/output', exist_ok=True)
    source_dir = '/opt/airflow/data'
    zip_filename = '/opt/airflow/output/data.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname=arcname)

#default dag arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
}

#DAG definition
dag = DAG(
    'task1dag',
    default_args=default_args,
    schedule_interval="@daily",  
    catchup=False
)

#gather task
gather_task = DummyOperator(
    task_id='gather_scraped_files',
    dag=dag,
)

#archive task
archive_task = PythonOperator(
    task_id='archive_data',
    python_callable=zip_directory,
    provide_context=True,
    dag=dag,
)

#year range can be specified
for year in range(2010,2023):
    task_id = f'scrape_data_{year}'
    scrape_task = PythonOperator(
        task_id=task_id,
        python_callable=scrape_data,
        #number of files per year
        op_kwargs={'year':year, 'num_files':10},
        provide_context=True,
        dag=dag,
    )
    scrape_task >> gather_task  


#dependencies order
gather_task >> archive_task  
