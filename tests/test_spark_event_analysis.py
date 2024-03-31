from pipelines.spark_pipeline.spark_event_analysis import transform_data, \
    aggregate_data, compute_averages, top_intervals


def test_transform_data(spark_session):
    test_data = [(" open ", "2023-03-28 00:00:00"), ("close", "2023-03-28 00:09:00")]
    schema = ["action", "time"]
    df = spark_session.createDataFrame(test_data, schema=schema)

    transformed_df = transform_data(df)
    actions = transformed_df.select("action").collect()

    # Verify that actions are correctly transformed to title case and trimmed
    assert actions[0][0] == "Open"
    assert actions[1][0] == "Close"


def test_aggregate_data(spark_session):
    test_data = [
        ("2023-03-28 00:00:00", "open"),
        ("2023-03-28 00:09:00", "close"),
    ]
    schema = ["time", "action"]
    df = spark_session.createDataFrame(test_data, schema=schema)

    aggregated_df = aggregate_data(df)
    # Verify the aggregation logic
    assert aggregated_df.count() > 0


def test_compute_averages(spark_session):
    test_data = [("2023-03-28 00:00:00", 1, 1)]
    schema = ["window", "open_count", "close_count"]
    df = spark_session.createDataFrame(test_data, schema=schema)

    avg_df = compute_averages(df)
    # Verify that the avg_actions column exists and has correct values
    assert avg_df.where("avg_actions = 1").count() == 1


def test_top_intervals(spark_session):
    test_data = [(1, "2023-03-28 00:00:00", 10), (2, "2023-03-28 00:10:00", 20)]
    schema = ["id", "window", "open_count"]
    df = spark_session.createDataFrame(test_data, schema=schema)

    top_df = top_intervals(df)
    # Verify that the top interval is correctly identified
    assert top_df.collect()[0][2] == 20
