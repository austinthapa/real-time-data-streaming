# Real-Time Data (Logs) Streaming Pipeline

This project demonstrates a fully Dockerized real-time data streaming pipeline using **Apache Kafka (via Confluent Platform)**, **Apache Spark**, and **Apache Cassandra**. The pipeline ingests `user_session_logs`, `user_auth_logs`, and `user_activity_logs` through **Kafka**, processes them in real-time using **Spark Structured Streaming**, and stores the results in **Cassandra**. It leverages **Confluent’s Schema Registry** to enforce and validate Avro schemas for Kafka topics and provides an intuitive web-based interface through **Kafka Control Center** for monitoring Kafka events. All components, including producers, Spark jobs, Kafka services, and Cassandra, run inside Docker for a consistent and production-ready architecture.
---

## Architecture

```
                             +---------------------+
                             |    Log Generators   |   (Python Script)
                             +---------------------+
                                        | Publishes
                                        v
                          +--------------------------+
                          |           Kafka          |   
                          |           Topics:        |  (Confluent Kafka Broker)
                          |  session, auth, activity |
                          +--------------------------+
                                        |
                                        v
                            +----------------------+         +------------------------+
                            | Kafka Stream Source  | ------->| Spark Streaming Engine |
                            +----------------------+         | (Parse, Transform)     |
                                                             +------------------------+
                                                                         |  Write Stream
                                                                         v
                                                                 +---------------+
                                                                 |   Cassandra   |  
                                                                 +---------------+
                                ─────────────────────────────────────
                               All components run in Docker containers  
                             Managed and orchestrated via Docker Compose
                          ─────────────────────────────────────────────────
```
## Components:

1. **Kafka**: Manages real-time log streams.
2. **Spark**: Reads, transforms, and processes data from Kafka topics.
3. **Cassandra**: Stores the processed structured data.

---


## Data Flow

- `Log Generators` simulate user activity and send events through Kafka producers.
- These events are published to specific Kafka topics: `user_auth_logs`, `user_session_logs`, and `user_activity_logs`.
- Spark Structured Streaming consumes the data from these Kafka topics in real-time, parses the messages (Avro), and applies necessary transformations.
- The cleaned and structured data is then written into corresponding Cassandra tables for scalable, low-latency storage and querying.


---

## Directory Structure
```
real-time-data-streaming/                     # Root
├── kafka/                                    
│ ├── create_topics.sh                        # Shell script to simulate real time logs
│ ├── logs_generators.py                      # Script to generate fake log events
│ └── kafka_producer.py                       # Sends generated logs to Kafka topics
├── spark/                                    
│ ├── __init__.py                             # Marks spark directory as a package
│ └── spark_streaming.py                      # Main Spark Structured Streaming job
├── database/                                 
│ ├── __init__.py                             # Marks database directory as a package
│ └── cassandra_connection.py                 # Handles Cassandra session logic
├── .env                                      # Environment variables
├── .gitignore                                # Files to be ignored by Git
├── docker-compose.yml                        # Defines and runs multi-container Docker apps
├── main.py                                   # Main Entry point
├── requirements.txt                          # Python dependencies
└── README.md                                 # Project documentation
```
---


##  Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/real-time-data-streaming.git
cd real-time-data-streaming
```

2. **Start All Services (Kafka, Cassandra, Spark, Producers)**

```bash
docker-compose up --build -d
```

3. **Create Kafka Topics**

```bash
docker exec -it kafka bash kafka/create_topics.sh
```

4. **Create Cassandra Keyspace and Tables**

```bash
docker exec -it cassandra cqlsh -f cassandra/cassandra_setup.cql
```

5. **Start Spark Streaming Job**

```bash
docker exec -it spark-driver spark-submit --master spark://spark-master:7077 spark/spark_streaming.py
```

## Kafka Topics

- user_session_logs
- user_auth_logs
- user_activity_logs

## Cassandra Tables

- auth_logs - Stores  session data
- session_logs - Contains authentication events
- activity_logs - Holds user activity details


## Technologies

- Apache Kafka - Distributed event Streaming pipeline for real-time data ingestion.
- Apache Spark - Real-time stream processing using Structured Streaming.
- Apache Cassandra - Scalable NOSQL database for fast write-heavy loads.
- Python
- Docker - Contanierization and Orchestration of all components.

## Author

Austin Thapa

## License

This project is licensed under the MIT License.
