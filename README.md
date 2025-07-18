# 🧱 Brick E4 — CI/CD for Spatial Pipelines  

Welcome to **Brick E4: CI/CD for Spatial Pipelines** — where you’ll learn how to write, test, and automate your Airflow DAGs with confidence.  

This brick focuses on how **testing and continuous integration (CI)** ensure your spatial data pipelines are reliable, maintainable, and production-ready.

---

## 🎯 What You’ll Build  

- ✅ An Airflow DAG that:  
  - Waits for a NOAA storm events CSV file  
  - Downloads and decompresses it  
  - Converts it to a GeoParquet file  

- ✅ Pytest-based structural tests that check:  
  - Your DAG is valid and loads without errors  
  - The right tasks exist (Sensor, PythonOperator, BashOperator)  
  - Tasks run in the correct order  
  - A special test that you will complete yourself  

- ✅ A GitHub Actions workflow that runs your tests on every PR  

---

## 🛠️ How to Complete This Brick  

### 1️⃣ Open in Gitpod  

```bash
gp open .
````

### 2️⃣ Run the Tests (They Will Fail at First)

```bash
pytest --maxfail=1 --disable-warnings -q
```

You’ll see failures related to missing tasks or dependency errors — this is intentional.

---

### 3️⃣ Fix the DAG

Edit `dags/storm_events_pipeline.py` to make sure your DAG:

* ✅ Has a valid `HttpSensor` with correct parameters
* ✅ Contains a `convert_to_geoparquet` task with the correct `task_id`
* ✅ Has the correct task dependency order
* ✅ Matches the expected structure in `tests/test_dag_structure.py`

---

### 4️⃣ Complete Your Test

Open `tests/test_dag_structure.py` and fill in the TODOs for:

```python
def test_convert_task_exists_and_order(dag):
    # TODO: Check the convert_to_geoparquet task exists
    # TODO: Check it runs after decompress_noaa_file
```

---

### 5️⃣ Re-Run Tests Until They Pass

```bash
pytest --maxfail=1 --disable-warnings -q
```

---

### 6️⃣ Push Your Code & Open a PR

```bash
git add .
git commit -m "Fix DAG and complete E4 tests"
git push origin main
```

Your CI will lint, test, and — if everything passes — print your badge proof.

---

## 📝 What Happens in CI

* ✅ Lint your code with `flake8`
* ✅ Run all pytest tests
* ✅ Print your badge proof if successful
* ✅ (On merge) Deploy your DAG to staging

---

## 🏁 Submission Checklist

* [ ] All tests pass locally and in CI
* [ ] You fixed the intentional DAG errors
* [ ] You completed the missing test TODO
* [ ] You pushed your code to GitHub

---

## 💡 Want to Go Further?

* Add a test that checks for the correct output of your GeoParquet file
* Mock the HTTP call to the NOAA server
* Extend the DAG to write metadata or upload to S3

---

## 🏆 Earning Your Badge

Once your PR is merged with passing tests, your **E4 Badge** will be issued!

Keep pushing — your future self (and your pipelines) will thank you.