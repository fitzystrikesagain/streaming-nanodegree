# Lesson 6: Stream Processing with Faust
## Glossary of Terms in Lesson
* DSL - Domain Specific Language. A metaprogramming language for specific tasks, such as building database queries or stream processing applications.
* Dataclass (Python) - A special type of Class in which instances are meant to represent data, but not contain mutating functions
* Changelog - An append-only log of changes made to a particular component. In the case of Faust and other stream processors, this tracks all changes to a given processor.
* Processor (Faust) - Functions that take a value and return a value. Can be added in a pre-defined list of callbacks to stream declarations.
* Operations (Faust) - Actions that can be applied to an incoming stream to create an intermediate stream containing some modification, such as a group-by or filter

## Stream Processing with Faust
Faust was created by the Data Engineering team at Robinhood. They wanted to implement streaming applications but were most comfortable with Python, rather than all the JVM frameworks. Their goal was to replicate KStreams in Python. It’s written in Python and contains concepts applicable to other frameworks.
## Introduction to Faust
Writing Faust is a Pythonic library that provides a standard API. It doesn’t have any dependencies other than Kafka. Faust keeps a changelog in a topic to track state, so resource managers like Yarn or Mesos or not needed. Faust uses Asyncio and therefore requires at least Python 3.6. Finally, Faust does not have native support for Avro or the Schema Registry.

### Key points
*  [Built at Robinhood to tackle stream processing problems natively in Python](https://robinhood.engineering/faust-stream-processing-for-python-a66d3a51212d?gi=25dc91767251)
* Faust takes its design inspiration from  [Kafka Streams, a JVM-only framework](https://kafka.apache.org/documentation/streams/)
* Faust is built using  [modern Python features like asyncio, and requires Python 3.6 or higher](https://docs.python.org/3/library/asyncio.html)
* Faust’s API implements the storage, windowing, aggregation, and other concepts discussed in Lesson 5
* Faust is a native Python API, not a Domain Specific Language (DSL) for metaprogramming
* Requires no external dependency other than Kafka. Does not require a resource manager like Yarn or Mesos.
* Faust **does not natively support Avro or Schema Registry**

## Your First Faust Application
```python
import faust

app = faust.App("demo-app", broker="PLAINTEXT://localhost:9092")
topic = app.topic("a-kafka-topic")

@app.agent(topic)
async def purchase(purchases):
	async for purchase in purchases:
		# do something

if __name__ == "__main__":
	app.main()
```

### Further Optional Research - Exploring Faust Functionality in More Depth
*  [See the Faust documentation for in-depth documentation of how Faust works](https://faust.readthedocs.io/en/latest/introduction.html)
* Every Faust application has an  [App which instantiates the top-level Faust application](https://faust.readthedocs.io/en/latest/userguide/application.html#what-is-an-application)
* The application must be assigned a  [topic to subscribe to](https://faust.readthedocs.io/en/latest/userguide/application.html#app-topic-create-a-topic-description)
* An output  [Table](https://faust.readthedocs.io/en/latest/userguide/tables.html#id1)  or stream receives the output of the processing
* An asynchronous function is decorated with an  [agent](https://faust.readthedocs.io/en/latest/introduction.html#id6)  which register the function as a callback for the application when data is received

## Serialization and Deserialization in Faust
Dataclasses are syntactical shortcuts for building objects meant to represent data. They contain only typed fields. They typically don’t have any functions other than helpers and/or serializers and deserializers.

```python
@dataclass(frozen=True)
class Purchase:
	username: str = ""
	currency: str = ""
	amount: int = 0
```

Instances are meant to represent data, but not contain mutating functions. A `dataclass` object can be marked as `frozen` , which makes them immutable. `dataclass` objects require type annotations and will enforce those constraints. It can be paired with the `asdict` function to quickly transform dataclasses into dicts. These are new in Python 3.7 and should be the default when working with Faust.

[dataclasses — Data Classes — Python 3.9.5 documentation](https://docs.python.org/3/library/dataclasses.html#frozen-instances)
[`dataclasses.asdict`](https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict)
[PEP 557 — Data Classes | Python.org](https://www.python.org/dev/peps/pep-0557/)

## Deserialization in Faust
Deserialiization is handled by specifying a type to the Faust topic:
```python
import faust

class Purchase(faust.Record, validation=True, serializer="json"):
	username: str
	currency: str
	amount: int

app = faust.App("demo-app", broker="PLAINTEXT://localhost:9092")
topic = app.topic("a-kafka-topic", **key_type=str, value_type=Purchase**)

@app.agent(topic)
async def purchase(purchases):
	async for purchase in purchases:
		# do something

if __name__ == "__main__":
	app.main()
```

### Key points
* Data model classes **must** inherit from `faust.Record` if used with a Faust topic
* `serializer` type *should* be specified so that Faust will deserialize in this format by default
* Setting `validation=True` is a good practice, since this will tell Faust to enforce types on the data being deserialized
* Faust does not support Avro, but [we can build custom (de)serializers](https://faust.readthedocs.io/en/latest/userguide/models.html#codec-registry)

[Faust records](https://faust.readthedocs.io/en/latest/userguide/models.html#records)
[Faust Serialization/deserialization](https://faust.readthedocs.io/en/latest/userguide/models.html#serialization-deserialization)
[Faust validation](https://faust.readthedocs.io/en/latest/userguide/models.html#model-validation)
[Faust codec registry](https://faust.readthedocs.io/en/latest/userguide/models.html#codec-registry)

## Serialization in Faust
Serialization leverages the same `faust.Record` class. Faust runs the serializer in reverse to serialize the data for the output stream. Multiple codes may be specified!:
```python
class Purchase(faust.Record, validation=True, serializer="binary|json")
```

For this exercise, we’ll create a new `dataclass` and convert `amount` from cents to dollars. We’ll create a new topic, perform the transformation, and publish to that topic:

```python
dollars_topic = app.topic(
    f"{TOPIC_NAME}.dollars",
    key_type=str,
    value_type=PurchaseDollars
)


@app.agent(purchases_topic)
async def purchase(purchases):
    async for p in purchases:
        purchase_in_dollars = PurchaseDollars(
            username=p.username,
            currency=p.currency,
            amount=p.amount / 100.0
        )
        await dollars_topic.send(key=p.username, value=purchase_in_dollars)


```

Reading off the topic with `kafka-console-consumer`, we can see our topic has the converted `amount` as a `float`. Faust also provides some metadata so we can see what created the messages:

```bash
{"username": "youngcarol", "currency": "QAR", "amount": 1185.98, "__faust": {"ns": "l6_stream_with_faust.data_ingestion.lessons.hello_world.PurchaseDollars"}}
{"username": "stewartscott", "currency": "SGD", "amount": 377.6, "__faust": {"ns": "l6_stream_with_faust.data_ingestion.lessons.hello_world.PurchaseDollars"}}
{"username": "xpayne", "currency": "GYD", "amount": 1232.5, "__faust": {"ns": "l6_stream_with_faust.data_ingestion.lessons.hello_world.PurchaseDollars"}}
```
[Manual serialization](https://faust.readthedocs.io/en/latest/userguide/models.html#manual-serialization)
