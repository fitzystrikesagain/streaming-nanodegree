# Lesson 2: Apache Kafka
## Topics covered
* Kafka's architecture
* How Kafka stores data
* High-availability and data-loss prevention with replication
* Retention policies

## Kafka architecture
Kafka servers are referred to as brokers. All of the brokers that work together are a cluster. Clusters may consist of only one or up to thousands of brokers.

Brokers use Apache Zookeeper to determine which broker is the leader of a partition and topic. Zookeeper keeps track of which brokers are part of the cluster and stores topic and permission configurations (ACLs).

## How Kafka stores data
### File location and structure
All Kafka data is stored on the broker disk in  `/var/lib/kafka/data`.  Each topic has its own subdirectory  with the name of the topic. Each topic may be stored in multiple log files to increase concurrency. This can be configured when the topic is created (and presumably later).  A topic named `kafka-arch` with six partitions, for example, will look like this:
```
[appuser@broker data]$ ls -alh | grep arch
drwxr-xr-x   2 appuser appuser 4.0K May 31 23:43 kafka-arch-0
drwxr-xr-x   2 appuser appuser 4.0K May 31 23:46 kafka-arch-1
drwxr-xr-x   2 appuser appuser 4.0K May 31 23:46 kafka-arch-2
drwxr-xr-x   2 appuser appuser 4.0K Jun  1 01:01 kafka-arch-3
drwxr-xr-x   2 appuser appuser 4.0K Jun  1 01:01 kafka-arch-4
drwxr-xr-x   2 appuser appuser 4.0K Jun  1 01:01 kafka-arch-5
[appuser@broker data]$ pwd
/var/lib/kafka/data
```

### Data partitioning
A topic consists of one or more partition. A partition contains a strictly ordered subset of all the data in the topic. Partitions enable Kafka to achieve high throughput.

Each partition has a single leader broker, which is elected by Zookeeper. Each broker may or may not be the leader for any partition. Any non-leaders are replicas of the partitions led by leader broker. The leader broker is responsible for sending data to, and receiving data from, clients.

Messages received from producers are hashed to determine which partition should receive the message. Hashed messages are distributed evenly across partitions. The benefits of this include:

* Parallelism; partitions are Kafka's unit of parallelism
* Consumers may parallelize data for each partition
* Producers may  parallelize data from each partition
* Reduction of bottlenecks by using multiple brokers

### Message ordering
Ordering is only guaranteed within a single partition. No guarantees are provided that messages from multi-partition topics will be consumed in the order they were produces.

Producers may still add metadata to indicate ordering. It's important to point out this logic is the responsibility of the producer and/or consumer rather than Kafka.

## Data replication
Data is written to multiple brokers, not just the leader. When a leader broker is lost, the remaining brokers will call an election using Zookeeper to determine the new broker.

### Takeaways
* Number of replicas can be configured globally
* There can't be more replicas than brokers
* Replication incurs overhead
    * Production clusters should always use replication (a `replication_factor` greater than 1. )

## How Kafka Works - Summary
### What we learned
* A broker is an individual server
* A cluster is a group of brokers
* Zookeeper elects topic leaders and stores configurations
* Kafka writes log files to disk on the brokers
* Kafka uses topic partitions to achieve scale and parallelism
* Data replication provides resiliency and helps prevent data loss

### How is Kafka secured?
Mutual TLS (mTLS) or Simple Authentication and Security Layer (SASL). This is detailed in [this blog post](https://www.confluent.io/blog/secure-kafka-deployment-best-practices/)  but is not covered in this class.

### Additional Resources
*  [Why does Kafka need Zookeeper?](https://www.cloudkarafka.com/blog/2018-07-04-cloudkarafka_what_is_zookeeper.html)
*  [Kafka Design](https://kafka.apache.org/documentation/#design)
*  [Partitioning](https://kafka.apache.org/documentation/#intro_topics)
*  [Data Replication](https://kafka.apache.org/documentation/#replication)


## Kafka Topics in Depth
* Data replication can be set on a per-topic basis
* A broker must be an In Sync Replica (ISR) to become the new leader
* Desired number of ISRs can be set on topics
    * If the number of ISRs is set to two on a three-partition topic, then both ISRs must receive the message before the producer is sent a success message
    * This guarantees that another machine can take over quickly if the leader fails
    * This  leads to more overhead
* Producer must indicate how many brokers it wants to acknowledge the message with the ACK setting (covered later)

### Partitioning Topics
The right number of partitions depends on the situation. The most important number to consider is desired throughput. Partitions can easily be added by modifying topics later. Partitions require additional network latency and potential rebalances.

[Confluent recommends](https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster/) the following equation to determine the number of partitions used:
```
# Partitions = Max(Overall Throughput/Producer Throughput, Overall Throughput/Consumer Throughput)
```

### Naming Kafka Topics
Topic names must:
* Be fewer than 256 characters in length
* Consist of only alphanumeric characters, periods, underscores, and dashes (`a-zA-Z0-9._-`):
```
my-topic
my_topic
myTopic
my.topic
mY._tOp.C
```
* There is no idiomatic naming or casing convention, though naming conventions can reduce confusion and increase reusability
* One option is to use namespacing, which might look like this:
    * Start with a namespace like `com.udacity`
    * Segment on model type, like `com.udacity.lesson`, where `lesson` is the model
    * Further segment on event type, like `com.udacity.lesson.quiz_complete`, where `quiz_complete` is the event

Here are some good examples of topic names:
* `org.chicago.transit.transaction`
* `api-integration-called-v1`
* `com_abc_banner_clicks`
* `org.chicago.transit.transaction.failures`
* `com-xyz-loadtimes-timedout`

And some not so good ones:
* `clicks`
* `cpgProductClicks`

### Topic Data Management
Data retention is how long a service stores data. Topics may be configured to expire data, at which point Kafka deletes it from disk. Topic retention can be set on either time or size, specifically `retention.ms` or `retention.bytes`. Topics can even use both; that is, data is deleted when the first condition above is met. A third option exists: Log compaction. Compaction has no time size or limit. If a key appears more than once, old versions of that data are compacted (deleted).

* Compression can be configured on a topic using `lz4`, `ztsd`, `snappy`, or `zip`. `compression.type` controls the type of compression used by a topic.
* Data retention determines how long data is stored. `retention.bytes`, `retention.ms` control retention policy
* When data expires it is deleted from the topic. This is true if `cleanup.policy` is set to delete.
* The compaction policy is configured by setting `cleanup.policy` to `compact`

### Topic Creation
Kafka *can* create topics automatically, but this is anti-pattern and bad practice. There are many configuration settings to choose from during topic creation, so this should always be done manually and carefully. Scripts and other provisioning tools (Terraform, etc.) can help in the creation of topics.

There are more than a dozen different configuration options, some of which we’ve seen already. Here are a few of them:
* `cleanup.policy`: delete, compact, or both
* `compression.type`: the compression codec to apply to the topic
* `max.message.bytes`: the largest record batch size allowed by Kafka

These configuration options can be found in Kafka’s documentation [here](cleanup.policy).

## Kafka Producers
This section covers the creation and management of Kafka Producers, specifically:
* Synchronously or asynchronously sending data to Kafka
* Using key configuration options, such as:
    * batch size
    * client identifiers
    * compression
    * acknowledgements
* Specifying data serializers

### Synchronous Production

These producers block program execution until the message is acknowledged by the broker. This is pretty rare in Kafka but has its uses. Credit card transactions are one example of this.

### Asynchronous Production

This is the most common method and is useful when throughput should be maximized. Messages are taken from the application, put on a queue, and eventually processing by the Broker. Kafka clients offer callbacks for when messages are delivered or an error occurs. This gives programs a chance to rectify the error. Alternatively, producers can fire and forget, not wait for acknowledgment, and ignore errors. This should be the default choice for most implementations.

### Message Serialization

Most applications will want to publish an application instance, JSON, or some other formalized type of data. Transforming an application data model into a model suitable for data stores is known as serialization. Data sent to Kafka should be serialized into a specific format. Client libraries can assist in serialization, and the accepted formats are the following:
* binary
* string
* CSV
* JSON
* Avro.

Kafka expects data to be in one of these forms and does not handle serialization. The serialization type **should never be changed** on an existing topic; a new topic should always be created.

### Producer Configuration

Similar to topics, producers offer extensive configuration options. A complete list can be found in the [` librdkafka` documentation.](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md) All producers should:

* Provide a `client_id` setting. This is not required but is useful for debugging. This can also be used for limiting producers.
* Configure retries to ensure data is delivered
* Set `enable.idempotence` to `true` for in-order retry if ordering matters
* `acks` determine number of required ISR confirmations. This number does not have to equal the number of ISRs. Kafka will ensure the replicas are in sync, but won’t block the Producer. That said, this should be set to `all` or `-1`, which means that all ISRs must successfully receive the message before the Producer continues

Producers can set a compression codec on individual topics. The same codecs are typically available on the client. In these cases, compression occurs on the client machine. If compression is set on the Broker, it takes place on the Broker. The Topic’s compression setting will always take precedence. This means that codec mismatches between Producer and Topic will result in messages getting recompressed on the Broker.

#### Compression type comparison

| Algorithm | Pros | Cons |
| ————— | ————— | ————— |
| `lz4` | fast compression and decompression | low compression ration |
| `snappy` | fast compression and decompression | low compression ratio |
| `zstd` | high compression ratio | slower than `lz4` or `snappy` |
| `gzip` | ubiquitous, widely supported | cpu-intensive, significantly slower than  `lz4` or `snappy` |

[Squeezing the firehose: getting the most from Kafka compression](https://blog.cloudflare.com/squeezing-the-firehose/)

#### Batching Configuration

Client libraries do not send every message individually, but rather send messages in batches for efficiency. Messages may be batched by time, count, or size. The Python `confluent_kafka` library will transmit a batch when any of the following conditions are met:

* 10,000 messages have accumulated in the queue
* A half second has passed since the last batch was sent
* A gigabyte of data has been accumulated

These are the default settings and can be adjusted. For example, if the host is storage-constrained, the size setting can be decreased. If the messages aren’t time-sensitive, the time setting can be decreased. These parameters can also be disabled completely, but this is pretty atypical.

#### Kafka Producers - Summary

Kafka Producers come with rich configuration options. No one set of settings works in all scenarios. If the producer isn’t performing as expected, it’s worth revisiting the configuration to ensure that the settings make sense for the desired throughput level.

##### Further Reading
*  [confluent-kafka-python/librdkafka Configuration Options](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md)
*  [Apache Documentation on Producer Configuration](https://kafka.apache.org/documentation/#producerconfigs)
*  [confluent-kafka-python Producer class](https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=serializer#producer) 

