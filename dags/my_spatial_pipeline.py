# File: dags/storm_events_pipeline.py

from datetime import datetime
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Constants
NOAA_URL = (
    "https://www.ncei.noaa.gov/"
    "pub/data/swdi/stormevents/csvfiles/"
    "StormEvents_details-ftp_v1.0_d2025_c20250520.csv.gz"
)
LOCAL_GZ = "/tmp/StormEvents_details-ftp_v1.0_d2025_c20250520.csv.gz"
LOCAL_CSV = "/tmp/StormEvents_details-ftp_v1.0_d2025_c20250520.csv"
PARQUET_PATH = "/tmp/StormEvents_details-ftp_v1.0_d2025_c20250520.parquet"
NOAA_ENDPOINT = (
    "pub/data/swdi/stormevents/csvfiles/"
    "StormEvents_details-ftp_v1.0_d20250520.csv.gz"
)

def download_noaa_file():
    import requests
    resp = requests.get(NOAA_URL, stream=True)
    resp.raise_for_status()
    with open(LOCAL_GZ, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

def convert_to_geoparquet():
    import geopandas as gpd
    # read the CSV
    df = gpd.read_csv(LOCAL_CSV)
    # create geometry from latitude/longitude columns
    df["geometry"] = gpd.points_from_xy(df["BEGIN_LON"], df["BEGIN_LAT"])
    df = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    # write out as GeoParquet
    df.to_parquet(PARQUET_PATH, index=False)

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 7, 11),
    "retries": 1,
}

with DAG(
    dag_id="storm_events_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=["E4", "ci-cd"],
) as dag:

    wait_for_noaa = HttpSensor(
        task_id="wait_for_noaa_file",
        http_conn_id="noaa_http",
        end_point=NOAA_ENDPOINT,            # ERROR #1: typo—should be `endpoint`
        response_check=lambda response: response.status_code == 200,
        poke_interval=60,
        timeout=600,
        mode="poke",
    )

    download = PythonOperator(
        task_id="download_noaa_file",
        python_callable=download_noaa_file,
    )

    decompress = BashOperator(
        task_id="decompress_noaa_file",
        bash_command=f"gunzip -f {LOCAL_GZ}",
    )

    convert = PythonOperator(
        task_id="convert_to_parquet",      # ERROR #2: wrong task_id—should be `convert_to_geoparquet`
        python_callable=convert_to_geoparquet,
    )

    # define the dependency chain
    wait_for_noaa >> download >> decompress >> convert
