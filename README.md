# Rhenus_de_challenge

## Task1: Spark Pipeline

### To Run Pipeline


Ensure Docker is installed on your system. Begin by navigating to the root directory of your project.

### Creating a Docker Image

Execute the command below to build your Docker image. Remember to replace `IMAGE-NAME` with a name of your choosing:

```sh
sudo docker build -t IMAGE-NAME .
```

### Starting a Jupyter Notebook

To launch a Jupyter notebook, use the following command:

```sh
docker run -p 8888:8888 IMAGE-NAME
```

### Persisting Notebook Changes

If you wish to preserve changes made in your notebooks locally, initiate the notebook using this command:

```sh
docker run -p 8888:8888 -v $(pwd)/notebooks:/app/notebooks IMAGE-NAME
```

This mounts the local `notebooks` directory to `/app/notebooks` within the container, ensuring that any modifications are saved to your local system.

### Running a Spark Job

To execute a Spark job directly, access the terminal from the Jupyter homepage and execute:

```sh
python pipelines/spark_pipeline/spark_event_analysis.py
```

### Running Tests

For executing tests, simply run:

```sh
pytest tests/
```


### CircleCI
CircleCI is integrated with repo and perform
* Conduct code quality check using flake8
* Execute unit Test <br>
*** Additionaly creating docker image/Artifact and pushing it to cloud and delpoyment steps can be included for production.

> *Note: This spark job/code is not for production. It just provides abstract way of working.*

### Optimization and Scalability:
There are several things that can be considered while it comes to optimization and scalability. Few of them are Data Formats, Data Locality, Partitioning, Efficient resource management, Broadcasting etc. In this specific job we can consider partitioning by time to reduce shuffling, further partitioning can be considered by action type but in this case not required. We can leverage it by using the approach of having data by each hour in a separate file.

When it comes to TBs of data we can consider scaling out efficiently, Incremental Processing of Data, Monitoring and Logging to identify bottlenecks and adjust accordingly.

## For production systems following points to be consider 
* **Finalize Spark Code:** Ensure thorough testing and externalize configurations.
* **Deployment Mode:** Choose between standalone, YARN, Mesos, or Kubernetes based on infrastructure.
* **Spark Configuration:** Optimize Spark parameters for resource management.
* **Monitoring:** Implement monitoring and logging for performance tracking and issue diagnosis.
* **Job Scheduling:** Use tools like Apache Airflow, Luigi etc for managing job execution and dependencies.
* **Data Management:** Ensure efficient access to input/output data and use optimized storage formats and cloud. Plan for data backups and cluster to ensure high availability to minimize downtime.
* **Cluster Management:** Properly size the Spark cluster and enable auto-scaling if necessary.
* **Security:** Enforce data encryption, access control, and comply with regulations.
* **Documentation and Training:** Maintain clear documentation and train the team on operational procedures.
<br><br>
> ## **[Task2: ETL Challenge](ETLChallenge.md)**<br><br>
> ## **[Task3: Data Pipeline Challenge](DataPipelineChallenge.md)**