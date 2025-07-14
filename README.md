# Brick E4: CI/CD for Spatial Pipelines

Welcome to Brick E4! In this exercise you’ll wire up a simple Airflow DAG, write tests to validate its structure, and hook it into a CI pipeline.

---

## 🚀 Quickstart

1. **Open in Gitpod**  
   From your repo root:  
   ```bash
   gp open .
````

or click your Gitpod badge. Gitpod will build your image and install dependencies.

2. **Inspect the scaffold**

   ```bash
   ls -R .
   ```

   You should see:

   ```
   dags/
   tests/
   scripts/
   .github/workflows/ci.yml
   .gitignore  .gitpod.yml  .gitpod.Dockerfile  README.md  requirements.txt
   ```

3. **Initialize Airflow (optional)**

   ```bash
   export AIRFLOW__CORE__LOAD_EXAMPLES=False
   airflow db init
   # launch UI if you like:
   airflow webserver --port 8080 &  
   airflow scheduler &
   ```

   Browse → `localhost:8080` to confirm no DAGs are present yet.

4. **Run the tests**

   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```

   You’ll see failures in `tests/test_dag_structure.py` pointing to missing tasks and dependencies.

---

## 🛠 Your To-Do

1. **Implement your DAG**

   * Edit `dags/storm_events_pipeline.py` (or `dags/my_spatial_pipeline.py`).
   * Define a single DAG with:

     * an `HttpSensor` pointing at the NOAA CSV – use `http_conn_id="noaa_http"` and the endpoint path.
     * a `PythonOperator` to download the file.
     * a `BashOperator` to decompress it.
     * a `PythonOperator` named `convert_to_geoparquet` to read the CSV and write GeoParquet.
   * Wire them in order:

     ```
     wait_for_noaa_file >> download_noaa_file >> decompress_noaa_file >> convert_to_geoparquet
     ```

2. **Fill in the test TODOs**
   Open `tests/test_dag_structure.py` and un-comment the `test_convert_task_exists_and_order` block. It contains two TODOs:

   ```python
   # 1) check the convert_to_geoparquet task is present
   # 2) check it's downstream of the decompress_noaa_file task
   ```

   Complete those assertions so the test passes once your DAG is wired correctly.

3. **Re-run tests**

   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```

   ✅ All tests should pass.

4. **Push & open a PR**

   ```bash
   git add .
   git commit -m "Implement storm_events_pipeline DAG + tests"
   git push origin feature/ci-cd
   ```

   On PR, your GitHub Actions workflow will:

   * install dependencies
   * lint & run pytest
   * generate `badge_proof.txt` on success
   * (on merge) deploy to your staging Airflow

---

## 📄 Submission & Badge

* **Badge proof:** your workflow writes `badge_proof.txt` in the repo root when CI passes.
* **Merge to main:** deploys your DAG to staging.
* Once merged, your E4 badge will be issued automatically.

---

## ✏️ Extension

Feel free to add any additional tests in `tests/`, for example:

* Validate HTTP sensor timeout and poke interval
* Assert that the GeoParquet file exists on disk
* Check that your `convert_to_geoparquet` operator actually runs without error (using a pytest mock)
