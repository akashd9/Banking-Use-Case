from src.transformations import dedup_transactions, filter_null_amounts


def test_dedup_transactions_removes_exact_duplicates(spark):
    data = [
        ("T1", "A", 100.0),
        ("T1", "A", 100.0),
        ("T2", "B", 200.0),
    ]
    df = spark.createDataFrame(data, ["transaction_id", "account", "amount"])

    result = dedup_transactions(df)

    assert result.count() == 2


def test_dedup_transactions_with_subset_keeps_first_by_key(spark):
    data = [
        ("T1", "A", 100.0),
        ("T1", "A", 999.0),
        ("T2", "B", 200.0),
    ]
    df = spark.createDataFrame(data, ["transaction_id", "account", "amount"])

    result = dedup_transactions(df, subset=["transaction_id"])

    assert result.count() == 2


def test_filter_null_amounts_removes_nulls(spark):
    data = [
        ("T1", "A", 100.0),
        ("T2", "B", None),
        ("T3", "C", 300.0),
    ]
    df = spark.createDataFrame(data, ["transaction_id", "account", "amount"])

    result = filter_null_amounts(df)

    assert result.count() == 2
    assert all(row.amount is not None for row in result.collect())


def test_filter_null_amounts_custom_column(spark):
    data = [("T1", 100.0), ("T2", None)]
    df = spark.createDataFrame(data, ["transaction_id", "value"])

    result = filter_null_amounts(df, amount_col="value")

    assert result.count() == 1
