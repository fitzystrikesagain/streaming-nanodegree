# Lesson 1: Intro to Stream Processing
## Kafka notes
### Listing Topics (zookeeper)
List existing topics:
```
kafka-topics --list --zookeeper localhost:2181
```

List an existing topic in extreme detail:
```
docker exec -ti broker kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name org.udacity.exercise3.purchases --describe --all

All configs for topic org.udacity.exercise3.purchases are:
  compression.type=producer sensitive=false synonyms={DEFAULT_CONFIG:compression.type=producer}
  confluent.value.schema.validation=false sensitive=false synonyms={}
  leader.replication.throttled.replicas= sensitive=false synonyms={}
  confluent.key.subject.name.strategy=io.confluent.kafka.serializers.subject.TopicNameStrategy sensitive=false synonyms={}
  message.downconversion.enable=true sensitive=false synonyms={DEFAULT_CONFIG:log.message.downconversion.enable=true}
  min.insync.replicas=1 sensitive=false synonyms={DEFAULT_CONFIG:min.insync.replicas=1}
  segment.jitter.ms=0 sensitive=false synonyms={}
  cleanup.policy=delete sensitive=false synonyms={DEFAULT_CONFIG:log.cleanup.policy=delete}
  flush.ms=9223372036854775807 sensitive=false synonyms={}
  confluent.tier.local.hotset.ms=86400000 sensitive=false synonyms={DEFAULT_CONFIG:confluent.tier.local.hotset.ms=86400000}
  follower.replication.throttled.replicas= sensitive=false synonyms={}
  confluent.tier.local.hotset.bytes=-1 sensitive=false synonyms={DEFAULT_CONFIG:confluent.tier.local.hotset.bytes=-1}
  confluent.value.subject.name.strategy=io.confluent.kafka.serializers.subject.TopicNameStrategy sensitive=false synonyms={}
  segment.bytes=1073741824 sensitive=false synonyms={DEFAULT_CONFIG:log.segment.bytes=1073741824}
  retention.ms=604800000 sensitive=false synonyms={}
  flush.messages=9223372036854775807 sensitive=false synonyms={DEFAULT_CONFIG:log.flush.interval.messages=9223372036854775807}
  confluent.tier.enable=false sensitive=false synonyms={DEFAULT_CONFIG:confluent.tier.enable=false}
  confluent.tier.segment.hotset.roll.min.bytes=104857600 sensitive=false synonyms={DEFAULT_CONFIG:confluent.tier.segment.hotset.roll.min.bytes=104857600}
  confluent.segment.speculative.prefetch.enable=false sensitive=false synonyms={DEFAULT_CONFIG:confluent.segment.speculative.prefetch.enable=false}
  message.format.version=2.7-IV2 sensitive=false synonyms={DEFAULT_CONFIG:log.message.format.version=2.7-IV2}
  max.compaction.lag.ms=9223372036854775807 sensitive=false synonyms={DEFAULT_CONFIG:log.cleaner.max.compaction.lag.ms=9223372036854775807}
  file.delete.delay.ms=60000 sensitive=false synonyms={DEFAULT_CONFIG:log.segment.delete.delay.ms=60000}
  max.message.bytes=1048588 sensitive=false synonyms={DEFAULT_CONFIG:message.max.bytes=1048588}
  min.compaction.lag.ms=0 sensitive=false synonyms={DEFAULT_CONFIG:log.cleaner.min.compaction.lag.ms=0}
  message.timestamp.type=CreateTime sensitive=false synonyms={DEFAULT_CONFIG:log.message.timestamp.type=CreateTime}
  preallocate=false sensitive=false synonyms={DEFAULT_CONFIG:log.preallocate=false}
  confluent.placement.constraints= sensitive=false synonyms={}
  min.cleanable.dirty.ratio=0.5 sensitive=false synonyms={DEFAULT_CONFIG:log.cleaner.min.cleanable.ratio=0.5}
  index.interval.bytes=4096 sensitive=false synonyms={DEFAULT_CONFIG:log.index.interval.bytes=4096}
  unclean.leader.election.enable=false sensitive=false synonyms={DEFAULT_CONFIG:unclean.leader.election.enable=false}
  retention.bytes=-1 sensitive=false synonyms={DEFAULT_CONFIG:log.retention.bytes=-1}
  delete.retention.ms=86400000 sensitive=false synonyms={DEFAULT_CONFIG:log.cleaner.delete.retention.ms=86400000}
  confluent.prefer.tier.fetch.ms=-1 sensitive=false synonyms={DEFAULT_CONFIG:confluent.prefer.tier.fetch.ms=-1}
  confluent.key.schema.validation=false sensitive=false synonyms={}
  segment.ms=604800000 sensitive=false synonyms={}
  message.timestamp.difference.max.ms=9223372036854775807 sensitive=false synonyms={DEFAULT_CONFIG:log.message.timestamp.difference.max.ms=9223372036854775807}
  segment.index.bytes=10485760 sensitive=false synonyms={DEFAULT_CONFIG:log.index.size.max.bytes=10485760}
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

#dsnd/kafka#	#clutch