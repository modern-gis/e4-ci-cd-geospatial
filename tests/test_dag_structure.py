# File: bricks/E4-ci-cd/tests/test_dag_structure.py
import pytest
from airflow.models import DagBag

NOAA_FILENAME = "StormEvents_details-ftp_v1.0_d2025_c20250520.csv.gz"

@pytest.fixture(scope="module")
def dag():
    """Load your DAG from dags/ and return the single Dag object."""
    dagbag = DagBag(dag_folder="dags", include_examples=False)
    assert dagbag.dags, "No DAGs found in dags/ folder"
    # expect exactly one DAG in this brick
    assert len(dagbag.dags) == 1, f"Expected 1 DAG, found {len(dagbag.dags)}"
    return list(dagbag.dags.values())[0]

def test_contains_python_bash_and_sensor(dag):
    """Ensure we have at least one PythonOperator, one BashOperator, and one sensor."""
    python_ops = [t for t in dag.tasks if t.task_type == "PythonOperator"]
    bash_ops   = [t for t in dag.tasks if t.task_type == "BashOperator"]
    sensors    = [t for t in dag.tasks if t.task_type in ("HttpSensor", "FileSensor")]

    assert python_ops, "No PythonOperator tasks found"
    assert bash_ops,   "No BashOperator tasks found"
    assert sensors,    "No HttpSensor or FileSensor tasks found"

def test_sensor_targets_noaa_file(dag):
    """Verify the sensor is configured to poke the NOAA file name."""
    # pick the first sensor we find
    sensor = next(t for t in dag.tasks if t.task_type in ("HttpSensor", "FileSensor"))

    if sensor.task_type == "HttpSensor":
        # HttpSensor has an .endpoint attribute
        assert NOAA_FILENAME in sensor.endpoint, (
            f"HttpSensor.endpoint must include {NOAA_FILENAME}"
        )
    else:
        # FileSensor has an .fs_path or .filepath attribute
        path_attr = getattr(sensor, "fs_path", None) or getattr(sensor, "filepath", "")
        assert NOAA_FILENAME in path_attr, (
            f"FileSensor.fs_path/filepath must include {NOAA_FILENAME}"
        )

def test_convert_task_exists_and_order(dag):
    # TODO: 1) check the convert_to_geoparquet task is present
    # convert_tasks = [t for t in dag.tasks if t.task_id == "convert_to_geoparquet"]
    # assert convert_tasks, "Missing task: convert_to_geoparquet"

    # TODO: 2) check it's downstream of the decompress_noaa_file task
    # decompress = dag.get_task("decompress_noaa_file")
    # downstream_ids = {t.task_id for t in decompress.get_flat_relatives(upstream=False)}
    # assert "convert_to_geoparquet" in downstream_ids, \
    #     "convert_to_geoparquet must run after decompress_noaa_file"

    pass

def test_sensor_upstream_of_tasks(dag):
    """Check that both PythonOperator and BashOperator tasks are downstream of the sensor."""
    # find our sensor task_id
    sensor_id = next(t.task_id for t in dag.tasks if t.task_type in ("HttpSensor", "FileSensor"))

    # gather all downstream task_ids from the sensor
    sensor_task = dag.get_task(sensor_id)
    downstream = {t.task_id for t in sensor_task.get_flat_relatives(upstream=False)}

    # collect all Python & Bash task_ids
    data_tasks = [
        t.task_id
        for t in dag.tasks
        if t.task_type in ("PythonOperator", "BashOperator")
    ]

    for tid in data_tasks:
        assert tid in downstream, f"Task {tid} must run after sensor {sensor_id}"
