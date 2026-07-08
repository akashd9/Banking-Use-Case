from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def dedup_transactions(df: DataFrame, subset: list[str] | None = None) -> DataFrame:
    """Remove duplicate transaction rows, optionally keyed on a subset of columns."""
    return df.dropDuplicates(subset) if subset else df.dropDuplicates()


def filter_null_amounts(df: DataFrame, amount_col: str = "amount") -> DataFrame:
    """Drop rows where the amount column is null."""
    return df.filter(col(amount_col).isNotNull())
