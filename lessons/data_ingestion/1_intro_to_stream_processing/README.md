# `kafka_python.py`
This is a sample application that utilizes the Python kafka client to stand 
up a producer and consumer. This can be run as follows:
1. Mount this directory as a volume in the `docker-compose.yml` in the root 
   directory. It should point to `/home/appuser` on the container, like so:
   ```
   volumes:
     - ./lessons/data_ingestion/1_intro_to_stream_processing:/home/appuser
   ```
2. Activate the virtualenv from the root directory:
   ```
   $ . venv/bin/activate
   ```
   
3. Run `kakfa_python`:
   ```
   $ python lessons/data_ingestion/1_intro_to_stream_processing/kafka_python.
   py
   ```
   
The consumer will start polling the topic for new messages. After a few 
seconds we'll see the messages put on the topic by the producer:
```
No message received
No message received
No message received
No message received
No message received
No message received
Key: None, Value: b'Message: 6'
Key: None, Value: b'Message: 7'
Key: None, Value: b'Message: 8'
Key: None, Value: b'Message: 9'
Key: None, Value: b'Message: 10'
```