# tests/conftest.py
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_session(request):
    spark = SparkSession.builder \
        .master("local[2]") \
        .appName("pytest-spark-testing") \
        .getOrCreate()

    request.addfinalizer(lambda: spark.stop())

    return spark
