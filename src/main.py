from pyspark.sql import SparkSession

from transformations import dedup_transactions, filter_null_amounts

# TODO: replace with the real source/target tables for this workspace
SOURCE_TABLE = "banking_use_case.transactions"
TARGET_TABLE = "banking_use_case.transactions_clean"


def main():
    spark = SparkSession.builder.appName("banking-transformations").getOrCreate()

    df = spark.read.table(SOURCE_TABLE)
    result = filter_null_amounts(dedup_transactions(df))
    result.write.mode("overwrite").saveAsTable(TARGET_TABLE)


if __name__ == "__main__":
    main()
