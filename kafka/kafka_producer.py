import json
import time
import logging

from kafka import KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable
from logs_generators import generate_session_data, generate_user_session_log, generate_user_auth_log, generate_user_activity_log

# Logging set up
logging.basicConfig(level=logging.INFO)

def set_up_broker():
    """
    Creates a Kafka Producer with error handling
    
    Returns:
        kafka producer or None
    """
    try:
        return KafkaProducer(
            bootstrap_servers = "localhost:9092",
            value_serializer = lambda log:json.dumps(log).encode("utf-8")
        )
    except NoBrokersAvailable:
        logging.error(f"Failed to connect to Kafka")
    except KafkaError as e:
        logging.error(f"Error creating Kafka producer: {e}")
    return None
    
def log_to_kafka(producer):
    """
    Continuously send logs to Kafka topics
    """
    try:
        while True:
            try:
                session = generate_session_data()
                producer.send("user_session_logs", generate_user_session_log(session))
                producer.send("user_auth_logs", generate_user_auth_log(session))
                producer.send("user_activity_logs", generate_user_activity_log(session))
                logging.info("Logs sent to Kafka")
                time.sleep(1)
                producer.flush()
            except KafkaError as e:
                logging.error(f"Kafka error while sending logs to Kafka: {e}")
            except Exception as e:
                logging.error(f"Unexpected error occured: {e}")
    except KeyboardInterrupt as e:
        logging.info("Interrupted by user. Shutting down...")
    finally:
        logging.info('Closing Kafka Producer')
        producer.flush()
        producer.close()
        
producer = set_up_broker()

if producer:
    log_to_kafka(producer)
else:
    logging.error("Kakfa producer not initialized. Exiting")