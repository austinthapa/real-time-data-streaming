import sys
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType


def create_spark_connection():
    """
    Creates a SparkSession with support for Kafka and Cassandra
    
    Returns:
        SparkSession object if succeded, else None
    """
    try:
        spark_conn = SparkSession \
                    .builder \
                    .appName("spark-data-streaming") \
                    .master("spark://localhost:7077") \
                    .config("spark.driver.host", "host.docker.internal") \
                    .config("spark.driver.bindAddress", "0.0.0.0") \
                    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,com.github.jnr:jnr-posix:3.1.15") \
                    .config("spark.cassandra.connection.host", "cassandra") \
                    .getOrCreate()
        spark_conn.sparkContext.setLogLevel("INFO")
        logging.info("Succesfully created the spark connection")
        return spark_conn
    except Exception as e:
        logging.error(f"Unexpected error occured during spark connecion: {e}")
        return None
    
def connect_to_kafka(spark_conn):
    """
    Connect to Kafka topic and return the straming dataframe
    
    Args:
        spark_conn: Active SparkSession Object.
    Returns:
        DataFrame: Streaming DataFrame from Kafka if successful, else None.
    """
    spark_df = None
    try:
        spark_df = spark_conn \
                    .readStream \
                    .format("kafka") \
                    .option("kafka.bootstrap.servers", "kafka:29092") \
                    .option("subscribe", "user_session_logs") \
                    .option("startingOffsets", "earliest") \
                    .load()
        logging.info(f"Connected to Kafka and created a spark dataframe: {spark_df}")
        return spark_df
    except Exception as e:
        logging.error(f"Unexpected error occured during Kafka connection: {e}")
        return None
    
def create_structured_df_from_kafka(spark_df):
    """
    Create a Kafka streaming DataFrame into a structured DataFrame using predefined schema.
    
    Args:
        spark_df (DataFrame): Raw streaming data from Kafka
    
    Returns:
        DataFrame: Parsed and Structured DataFrame
    """
    session_logs_schema = StructType([
        StructField("user_id", StringType(), False),
        StructField("session_id", StringType(), False),
        StructField("login_time", TimestampType(), False),
        StructField("logout_time", TimestampType(), False),
        StructField("duration", StringType(), False),
        StructField("device", StringType(), False),
        StructField("os", StringType(), False),
        StructField("browser", StringType(), False),
        StructField("location", StringType(), False),
        StructField("ip_address", StringType(), False)
    ])
    
    structured_df = spark_df \
                .selectExpr("CAST(value AS STRING)") \
                .select(from_json(col("value"), session_logs_schema).alias("data")) \
                .select("data.*")
    logging.info(f"Succesfully created structured dataframe")
    return structured_df
    
def insert_data(df, keyspace, table):
    """
    Write a Structured DataFrame into Cassandra table
    
    Args:
        df (DataFrame): Structured streaming DataFrame
        keyspace (str): Cassandra keyspace
        table (str): Cassandra table name
    
    Returns:
        StreamingQuery object
    """
    try:
        query = (df.writeStream \
                .format("org.apache.spark.sql.cassandra") \
                .option("checkpointLocation", f"/tmp/checkpoints/{keyspace}_{table}") \
                .option("keyspace", keyspace) \
                .option("table", table) \
                .outputMode("append") \
                .start())
                
        logging.info(f"Started writing to Cassandra: {keyspace}:{table}")
        return query
    except Exception as e:
        logging.error(f"Failed to write to Cassandra: {keyspace}:{table}")
        return None
        