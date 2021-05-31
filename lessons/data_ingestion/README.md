# Intro to Stream Processing
## Kafka notes

### Listing Topics (zookeeper)
List existing topics:
```
kafka-topics --list --zookeeper localhost:2181
```

### Creating topics (zookeeper)
Create a new topic:
```
kafka-topics --create \
--topic "my-first-topic" \
--partitions 1 \
--replication-factor 1 \
--zookeeper localhost:2181
```

Validate by listing the topic:
```
kafka-topics --list \
--zookeeper localhost:2181 \
--topic "my-first-topic"
```

### Producing data (broker)
Open an interactive shell and put messages on the topic:
```
[appuser@broker ~]$ kafka-console-producer --topic "my-first-topic" \
> --broker-list PLAINTEXT://localhost:9092

>put
>some
>messages
>into
>the
>topic
```

### Consuming data (broker)
Create a consumer (doesn't print messages before the consumer creation by default):
```
kafka-console-consumer --topic "my-first-topic" --bootstrap-server PLAINTEXT://localhost:9092

```

Adding the `--from-beginning switch will print out the messages we put on the topic above:
```
[appuser@broker ~]$ kafka-console-consumer --topic "my-first-topic" --bootstrap-server PLAINTEXT://localhost:9092 --from-beginning

put
some
messages
into
the
topic
```

## Deleting topics
Cleaning up the topic we created above:
```
[appuser@broker ~]$  kafka-topics --delete --topic "my-first-topic" --zookeeper localhost:2181
Topic my-first-topic is marked for deletion.
Note: This will have no impact if delete.topic.enable is not set to true.
```

List topics to validate deletion:
```
bash-4.4$ kafka-topics --list --zookeeper localhost:2181 | grep my-first-topic
bash-4.4$
```