import sys
import logging

from spark import create_spark_connection
from spark import connect_to_kafka
from spark import create_structured_df_from_kafka
from spark import insert_data
from database import create_cassandra_connection
from database import create_keyspace
from database import create_tables

# Set up basic logging informatiojn
logging.basicConfig(level=logging.INFO)

def main():
    # 1. Create Spark Connection
    spark_conn = create_spark_connection()
    if not spark_conn:
        logging.error(f"Could not establish Spark Session")
        return
    
    # 2. Connect to Kakfa
    spark_df = connect_to_kafka(spark_conn)
    if not spark_df:
        logging.error(f"Could not connect to Kafka")
        return
    
    # 3. Parse Kafka messages into structured DataFrame
    struct_df = create_structured_df_from_kafka(spark_df)
    
    
    # 4. Create Cassandra connection
    cass_session = create_cassandra_connection()
    
    # 5. Create Keyspace in Cassandra
    cass_keyspace = create_keyspace(cass_session)
    
    # 6. Create Tables in Cassandra
    cass_tables = create_tables(cass_session, cass_keyspace)

    # 7. Insert data into Cassandra
    streaming_query = insert_data(struct_df, keyspace="user_logs", table="user_session_logs")
    
    if streaming_query:
        streaming_query.awaitTermination()
    else:
        logging.error(f"Streaming query failed to start")

if __name__ == "__main__":
    sys.exit(main())