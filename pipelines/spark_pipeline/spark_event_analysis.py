"""
Spark Job to Load data from csv file, perform temporal aggregation over 10 min,
 Compute average over action,Display top 10 min with 'Open Action'
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import window, col
from pyspark.sql.functions import initcap, trim


def spark_session() -> SparkSession:
    """ Initialize Spark Session """
    return SparkSession.builder.appName("SparkChallenge").getOrCreate()


def load_data(spark: SparkSession) -> DataFrame:
    """ Create Dataframe by reading CSV file """
    df = spark.read.csv("/app/data/events.csv", header=True, inferSchema=True)
    return df


def transform_data(df: DataFrame) -> DataFrame:
    """
    Transforms the data by converting 'action' column values to title case and
    removing leading and trailing spaces.
    """
    return df.withColumn("action", initcap(trim(col("action"))))


def aggregate_data(df: DataFrame) -> DataFrame:
    """ Perform temporal aggregation, count actions, and compute averages """
    return df.groupBy(window(col("time"), "10 minutes"), col("action")) \
             .count() \
             .groupBy("window") \
             .pivot("action", ["Open", "Close"]) \
             .sum("count") \
             .withColumnRenamed("open", "open_count") \
             .withColumnRenamed("close", "close_count") \
             .na.fill(0)  # Replace nulls with zeros for missing actions


def compute_averages(df: DataFrame) -> DataFrame:
    """ Compute average over actions """
    return df.withColumn(
        "avg_actions",
        (col("open_count") + col("close_count")) / 2
        )


def top_intervals(df: DataFrame, action: str = 'open', limit: int = 1) -> DataFrame:
    """ Identify top 10 minutes intervals with the highest number of given action"""
    return df.orderBy(col(f"{action}_count").desc()).limit(limit)


def main():
    """ Driver """
    spark = spark_session()
    df = load_data(spark)
    df_transformed = transform_data(df)
    df_aggregated = aggregate_data(df_transformed)
    final_df = compute_averages(df_aggregated)
    final_df.show()
    max_open_interval = top_intervals(final_df)
    max_open_interval.show()


if __name__ == '__main__':
    main()
