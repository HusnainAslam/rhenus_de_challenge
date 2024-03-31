# Use python:3.11-slim-bullseye as the base image
FROM python:3.11-slim-bullseye

# Install Java (required for Spark) and other dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Java and Spark
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_VERSION 3.5.1
ENV SPARK_HOME /opt/spark
ENV PATH $PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Download and install Spark
RUN curl -fSL "https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz" -o /tmp/spark.tgz \
    && tar xzf /tmp/spark.tgz -C /opt \
    && mv /opt/spark-$SPARK_VERSION-bin-hadoop3 /opt/spark \
    && mkdir -p /opt/spark/work-dir \
    && touch /opt/spark/RELEASE \
    && rm /tmp/spark.tgz

# Install Jupyter Notebook
RUN pip install jupyter

# Install Python packages from requirements.txt
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Copy the contents of the current directory to the container
COPY . /app

# Set the working directory
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Expose the port Jupyter Notebook will run on
EXPOSE 8888

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root"]
