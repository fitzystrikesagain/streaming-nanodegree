# Lesson 2: Apache Kafka

## Topics covered

* Kafka's architecture
* How Kafka stores data
* High-availability and data-loss prevention with replication
* Retention policies

## Kafka architecture

Kafka servers are referred to as brokers. All of the brokers that work together
are a cluster. Clusters may consist of only one or up to thousands of brokers.

Brokers use Apache Zookeeper to determine which broker is the leader of a
partition and topic. Zookeeper keeps track of which brokers are part of the
cluster and stores topic and permission configurations (ACLs).

## How Kafka stores data

### File location and structure

All Kafka data is stored on the broker disk in  `/var/lib/kafka/data`. Each
topic has its own subdirectory with the name of the topic. Each topic may be
stored in multiple log files to increase concurrency. This can be configured
when the topic is created (and presumably later). A topic named `kafka-arch`
with six partitions, for example, will look like this:

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

A topic consists of one or more partition. A partition contains a strictly
ordered subset of all the data in the topic. Partitions enable Kafka to achieve
high throughput.

Each partition has a single leader broker, which is elected by Zookeeper. Each
broker may or may not be the leader for any partition. Any non-leaders are
replicas of the partitions led by leader broker. The leader broker is
responsible for sending data to, and receiving data from, clients.

Messages received from producers are hashed to determine which partition should
receive the message. Hashed messages are distributed evenly across partitions.
The benefits of this include:

* Parallelism; partitions are Kafka's unit of parallelism
* Consumers may parallelize data for each partition
* Producers may parallelize data from each partition
* Reduction of bottlenecks by using multiple brokers

### Message ordering

Ordering is only guaranteed within a single partition. No guarantees are
provided that messages from multi-partition topics will be consumed in the order
they were produces.

Producers may still add metadata to indicate ordering. It's important to point
out this logic is the responsibility of the producer and/or consumer rather than
Kafka.

## Data replication

Data is written to multiple brokers, not just the leader. When a leader broker
is lost, the remaining brokers will call an election using Zookeeper to
determine the new broker.

### Takeaways

* Number of replicas can be configured globally
* There can't be more replicas than brokers
* Replication incurs overhead
    * Production clusters should always use replication (a `replication_factor`
      greater than 1. )

## How Kafka Works - Summary

### What we learned

* A broker is an individual server
* A cluster is a group of brokers
* Zookeeper elects topic leaders and stores configurations
* Kafka writes log files to disk on the brokers
* Kafka uses topic partitions to achieve scale and parallelism
* Data replication provides resiliency and helps prevent data loss

### How is Kafka secured?

Mutual TLS (mTLS) or Simple Authentication and Security Layer (SASL). This is
detailed
in [this blog post](https://www.confluent.io/blog/secure-kafka-deployment-best-practices/)
but is not covered in this class.

### Additional Resources

* [Why does Kafka need Zookeeper?](https://www.cloudkarafka.com/blog/2018-07-04-cloudkarafka_what_is_zookeeper.html)
* [Kafka Design](https://kafka.apache.org/documentation/#design)
* [Partitioning](https://kafka.apache.org/documentation/#intro_topics)
* [Data Replication](https://kafka.apache.org/documentation/#replication)

## Kafka Topics in Depth

* Data replication can be set on a per-topic basis
* A broker must be an In Sync Replica (ISR) to become the new leader
* Desired number of ISRs can be set on topics
    * If the number of ISRs is set to two on a three-partition topic, then both
      ISRs must receive the message before the producer is sent a success
      message
    * This guarantees that another machine can take over quickly if the leader
      fails
    * This leads to more overhead
* Producer must indicate how many brokers it wants to acknowledge the message
  with the ACK setting (covered later)

### Partitioning Topics

The right number of partitions depends on the situation. The most important
number to consider is desired throughput. Partitions can easily be added by
modifying topics later. Partitions require additional network latency and
potential rebalances.

[Confluent recommends](https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster/)
the following equation to determine the number of partitions used:

```
# Partitions = Max(Overall Throughput/Producer Throughput, Overall Throughput/Consumer Throughput)
```

### Naming Kafka Topics

Topic names must:

* Be fewer than 256 characters in length
* Consist of only alphanumeric characters, periods, underscores, and
  dashes (`a-zA-Z0-9._-`):

```
my-topic
my_topic
myTopic
my.topic
mY._tOp.C
```

* There is no idiomatic naming or casing convention, though naming conventions
  can reduce confusion and increase reusability
* One option is to use namespacing, which might look like this:
    * Start with a namespace like `com.udacity`
    * Segment on model type, like `com.udacity.lesson`, where `lesson` is the
      model
    * Further segment on event type, like `com.udacity.lesson.quiz_complete`,
      where `quiz_complete` is the event

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

Data retention is how long a service stores data. Topics may be configured to
expire data, at which point Kafka deletes it from disk. Topic retention can be
set on either time or size, specifically `retention.ms` or `retention.bytes`.
Topics can even use both; that is, data is deleted when the first condition
above is met. A third option exists: Log compaction. Compaction has no time size
or limit. If a key appears more than once, old versions of that data are
compacted (deleted).

* Compression can be configured on a topic using `lz4`, `ztsd`, `snappy`,
  or `zip`. `compression.type` controls the type of compression used by a topic.
* Data retention determines how long data is stored. `retention.bytes`
  , `retention.ms` control retention policy
* When data expires it is deleted from the topic. This is true
  if `cleanup.policy` is set to delete.
* The compaction policy is configured by setting `cleanup.policy` to `compact`

### Topic Creation

Kafka *can* create topics automatically, but this is anti-pattern and bad
practice. There are many configuration settings to choose from during topic
creation, so this should always be done manually and carefully. Scripts and
other provisioning tools (Terraform, etc.) can help in the creation of topics.

There are more than a dozen different configuration options, some of which we’ve
seen already. Here are a few of them:

* `cleanup.policy`: delete, compact, or both
* `compression.type`: the compression codec to apply to the topic
* `max.message.bytes`: the largest record batch size allowed by Kafka

These configuration options can be found in Kafka’s
documentation [here](cleanup.policy).

## Kafka Producers

This section covers the creation and management of Kafka Producers,
specifically:

* Synchronously or asynchronously sending data to Kafka
* Using key configuration options, such as:
    * batch size
    * client identifiers
    * compression
    * acknowledgements
* Specifying data serializers

### Synchronous Production

These producers block program execution until the message is acknowledged by the
broker. This is pretty rare in Kafka but has its uses. Credit card transactions
are one example of this.

### Asynchronous Production

This is the most common method and is useful when throughput should be
maximized. Messages are taken from the application, put on a queue, and
eventually processing by the Broker. Kafka clients offer callbacks for when
messages are delivered or an error occurs. This gives programs a chance to
rectify the error. Alternatively, producers can fire and forget, not wait for
acknowledgment, and ignore errors. This should be the default choice for most
implementations.

### Message Serialization

Most applications will want to publish an application instance, JSON, or some
other formalized type of data. Transforming an application data model into a
model suitable for data stores is known as serialization. Data sent to Kafka
should be serialized into a specific format. Client libraries can assist in
serialization, and the accepted formats are the following:

* binary
* string
* CSV
* JSON
* Avro.

Kafka expects data to be in one of these forms and does not handle
serialization. The serialization type **should never be changed** on an existing
topic; a new topic should always be created.

### Producer Configuration

Similar to topics, producers offer extensive configuration options. A complete
list can be found in
the [` librdkafka` documentation.](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md)
All producers should:

* Provide a `client_id` setting. This is not required but is useful for
  debugging. This can also be used for limiting producers.
* Configure retries to ensure data is delivered
* Set `enable.idempotence` to `true` for in-order retry if ordering matters
* `acks` determine number of required ISR confirmations. This number does not
  have to equal the number of ISRs. Kafka will ensure the replicas are in sync,
  but won’t block the Producer. That said, this should be set to `all` or `-1`,
  which means that all ISRs must successfully receive the message before the
  Producer continues

Producers can set a compression codec on individual topics. The same codecs are
typically available on the client. In these cases, compression occurs on the
client machine. If compression is set on the Broker, it takes place on the
Broker. The Topic’s compression setting will always take precedence. This means
that codec mismatches between Producer and Topic will result in messages getting
recompressed on the Broker.

### Compression type comparison

| Algorithm | Pros | Cons | 
| --------- | ---- | ---- | 
| `lz4` | fast compression and decompression | low compression ration | 
| `snappy` | fast compression and decompression | low compression ratio | 
| `zstd` | high compression ratio | slower than `lz4` or `snappy` | 
| `gzip` | ubiquitous, widely supported | cpu-intensive, significantly slower than  `lz4` or `snappy` |

[Squeezing the firehose: getting the most from Kafka compression](https://blog.cloudflare.com/squeezing-the-firehose/)

### Batching Configuration

Client libraries do not send every message individually, but rather send
messages in batches for efficiency. Messages may be batched by time, count, or
size. The Python `confluent_kafka` library will transmit a batch when any of the
following conditions are met:

* 10,000 messages have accumulated in the queue
* A half second has passed since the last batch was sent
* A gigabyte of data has been accumulated

These are the default settings and can be adjusted. For example, if the host is
storage-constrained, the size setting can be decreased. If the messages aren’t
time-sensitive, the time setting can be decreased. These parameters can also be
disabled completely, but this is pretty atypical.

### Kafka Producers - Summary

Kafka Producers come with rich configuration options. No one set of settings
works in all scenarios. If the producer isn’t performing as expected, it’s worth
revisiting the configuration to ensure that the settings make sense for the
desired throughput level.

##### Further Reading

* [confluent-kafka-python/librdkafka Configuration Options](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md)
* [Apache Documentation on Producer Configuration](https://kafka.apache.org/documentation/#producerconfigs)
* [confluent-kafka-python Producer class](https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=serializer#producer)

## Consumer Basics

Kafka consumers subscribe to one or more Topics. Subscribing to a non-existent
Topics will create it with default settings. Automatic topic creation can be
disabled in the Consumer topic configuration, but Consumers should first assert
a Topic doesn’t exist before trying to subscribe to it. Once a Consumers
subscribes to a Topic, it will poll the Topic for data. Just like the Producer,
the Consumer’s data queue can be configured by length, time, and size.

* `client.id` is an optional setting which is useful in debugging/limiting
  resources
* Poll for data to read from Kafka Topic using the `poll` or `consume` 
  methods

### Consumer Offsets

Each Topic has a counter to track the last message processed by the Consumer.
This is known as the **offset**, and Kafka will increment the offset with every
message, tracking offsets in a private internal Topic. Many client
implementations (including `confluent_kafka` in Python) automatically report the
offset position on the program’s behalf.

This doesn’t happen automatically after every consumed message, but is
controlled in the Consumer configuration by modifying the commit settings.

The offsets:

* Tell the Consumer where to start on restart (in the event of a crash)
* Are committed to Kafka, usually automatically

Commits are made asynchronously by most client libraries, but can be made
synchronously if needed. Commits can be manually managed if needed,
but [this isn’t recommended](https://docs.confluent.io/current/clients/confluent-kafka-python/index.html#confluent_kafka.Consumer.commit)
without a specific use case. The consumer can start from the first known message
by setting `auto.offset.reset` to `earliest`. This will only work the first time
the Consumer runs; subsequent runs will pick up wherever they left off. To
always start from the earliest known message, the Consumer must
be [manually assigned](https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=serializer#confluent_kafka.Consumer.assign)
to the start of the Topic on boot.

### Consumer Groups

When a Consumer is created, a `group.id` must be specified to indicate which
group it belongs to. Groups are collections of Kafka consumers that work
together to consume the same topic. These may exist within the same application
or are multiple instances of the same application.

Kafka uses `group.id` to assign partitions to specific Consumers so that each
Consumer is responsible for a portion of the data. This spreads the load to
increase throughput. Only one Consumer in a group receives a message from a
particular partition from the Broker.

When a Consumer process joins or leaves the group, a group coordinator broker
begins a partition rebalance. The broker will reassign partitions to the current
Consumer group. Rebalances are expensive, and during this time messages may not
be processed or consumed.

### Consumer Subscriptions

Kafka
supports [regexp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp)
when it comes to Topic subscriptions. Given the following Topics:

```
com.udacity.lesson2.exercise1
com.udacity.lesson2.exercise2
com.udacity.lesson2.exercise3
```

we could subscribe to all three simultaneously with the following expression:

```
consumer.subscribe(
	“^com.udacity.lesson2.*”
)
```

More information can be found under `subscribe()` in
the `confluent_kafka_python` documentation.

### Consumer Deserializers

Data being consumed must be deserialized in the same format in which it was
serialized. Failure to deserialize correctly may cause crashes or inconsistent
data.

### Retrieving data from Kafka

Most Consumers will have an infinite poll loop which ingests data from Kafka.
Example:

```
...
while True:
	message = consumer.poll(timeout=1.0)
	if not message:
		continue # No data was retrieved
	elif message.error() is not None:
		continue # Log error in production
	else:
		print(message.key(), message.value()
```

Once a Consumer decides to exit, it should call `.close()` to close the
connection. This allows the client to flush its offset and process any remaining
messages. Failure to do so may leave the client in an inconsistent state. This
also means the Broker has to determine that the Consumer has left the group.
This can cause issues for the rest of the Consumer group and delay rebalances.

The `.consume()` method can also be used, but `poll` has slightly richer
features. The `consume` method can fetch multiple messages at once:

```
while True:
	messages = consumer.consume(5, timeout=1.0)
	for message in messages:
		if not message:
			continue # No data was retrieved
		elif message.error() is not None:
			continue # Log error in production
		else:
			print(message.key(), message.value()
```

### Kafka Consumers Summary/Further Reading

This section covered:
* high-level config options for Consumers
* what Consumer Groups are
* what rebalances are and when they happen
* how offsets are used to track what a Consumer has consumed
* how to subscribe a Consumer to a Topic
* writing poll loops
* deserializing data from Kafka

#### Additional Consumer Resources
*  [Consumer Configuration Options](https://kafka.apache.org/documentation/#consumerconfigs)
*  [confluent_kafka_python Options](https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=serializer#consumer)
*  [librdkafka consumer options shared with confluent_kafka_python](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md) 

## Performance
Monitoring Producers, Consumers, and Brokers is an important part of Kafka. Below we’ll cover a few key performance metrics.

### Consumer Performance

* **Consumer lag** measures how far behind a consumer is by subtracting the Latest Topic offset by the Consumer Topic offset. It’s okay if this falls a little behind. If lag grows over time, the Consumer can’t keep up and will need additional processes.
* **Messages per second** indicates throughput of the Topic and can help assess performance goals. Low throughput may indicate that the Consumer can’t keep up.
* **JMX** Kafka exports metrics through the Java Metrics Exporter, which can be connected to alerting and monitoring tools

### Producer Performance

* latency = time broker received - time produced
* High latency may indicate: one of the following
    * `acks` is set too high
    * too many partitions
    *  too many replicas

### Broker Performance

* Disk usage: Kafka may retain data indefinitely, so we should monitor
* Network usage: high usage may slow consumption/production rates
* Elections should happen infrequently
    * very disruptive, they stop all consumption and production
    * may indicate instability or inappropriate configuration

### Further Reading
*  [DataDog blog post on monitoring Kafka](https://www.datadoghq.com/blog/monitoring-kafka-performance-metrics)
*  [Confluent article on monitoring Kafka](https://docs.confluent.io/current/kafka/monitoring.html)
*  [New Relic article on monitoring Kafka](https://blog.newrelic.com/engineering/new-relic-kafkapocalypse/) 

