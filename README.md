# Real-Time User Log Data Pipeline

This project demonstrates a real-time data streaming pipeline using Kafka, Spark, and Cassandra. It ingests `user_session_logs`, `user_auth_logs`, and `user_activity_logs`, processes them using Spark, and stores them in a Cassandra database.

---

## Architecture


                                +----------------+
                                | Log Generators |
                                |(Python Scripts)|
                                +----------------+  
                                        |
                                        v
                            +-----------------------+
                            |         Kafka         |
                            |      (3 Topics)       |
                            | auth/session/activity |
                            +-----------------------+
                                        |
                                        v
+-------------------------+      +--------------+
|    Spark Structured     | <----| Kafka Stream |
|    Streaming Engine     |      +--------------+
| (Read, Parse, Transform)|
+-------------------------+
            |
            v
    +-------------------+
    | Cassandra DB      |
    | Keyspace: user_db |
    | Tables:           |
    | - auth_logs       |
    | - session_logs    |
    | - activity_logs   |
    +-------------------+

1. **Kafka**: Manages real-time log streams.
2. **Spark**: Reads, transforms, and processes data from Kafka topics.
3. **Cassandra**: Stores the processed structured data.

---

## Data Flow

- `Log Generator` → `Kafka Producer` → `Kafka Topics`
- `Spark Streaming` reads from Kafka and transforms the logs
- Transformed logs are written to `Cassandra`

---

## Directory Structure

real-time-data-pipeline/
├── kafka/
│ ├── create_topics.sh
│ └── kafka_producer.py # Create Kafka topics and
├── spark/
│ └── spark_streaming.py
├── cassandra/
│ ├── cassandra_setup.cql
│ └── cassandra_connection.py
├── data/
│ └── sample_logs/
│ ├── auth_log.json
│ ├── session_log.json
│ └── activity_log.json
├── utils/
│ ├── schemas.py
│ └── config.py
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md
---




## Setup Instructions

1. **Start Kafka and Cassandra**

```bash
cd kafka
docker-compose up -d
```

2. **Create Kafka Topics**

```
bash kafka/create_topics.sh
```

3. **Run Kafka Producer**

```
python kafka/kafka_producer.py
```

4. **Create Cassandra Schema**

```
cqlsh -f cassandra/cassandra_setup.cql
```

5. Start Spark Stream

```
python spark/spark_streaming.py
```

### Kafka Topics

- user_session_logs
- user_auth_logs
- user_activity_logs

### Cassandra Tables

- auth_logs
- session_logs
- activity_logs

## Technologies

- Apache Kafka
- Apache Spark
- Apache Cassandra
- Python
- Docker

## Author

Anil Thapa

## License

MIT License
