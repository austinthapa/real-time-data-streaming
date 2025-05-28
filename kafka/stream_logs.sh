#!/bin/bash

cd "$(dirname "$0")"

source ../data-stream-venv/bin/activate

python3 kafka_producer.py