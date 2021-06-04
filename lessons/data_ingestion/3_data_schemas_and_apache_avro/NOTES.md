# Lesson 3: Data Schemas and Apache Avro
This section will cover how schemas make producers and consumers more resilient to change. We’ll focus on Avro and see how it fits into the Kafka ecosystem with tools like the Schema Registry
## Understanding Data Schemas
Data schemas help define the shape and types of data through field names, data types,  and required vs. optional fields. Schemas provide expectations for applications so they can handle data that doesn’t match the spec. Schemas also help with more efficient compression. Finally, schemas decouple producers from consumers. If the consumer can inspect the schema, it doesn’t have to be developed along with the application that produces the schema or data.
### Real-world Usage
Defining a table is an example of using a schema:
```
CREATE TABLE store_location (
	id        INTEGER,
	name      VARCHAR(80),
	city      VARCHAR(40),
	latitude  NUMERIC(10),
	longitude NUMERIC(10)
)
```
Outside of databases, Hadoop, Hive, and Presto use schemas and Avro to load data and talk to other data sources. Data Engineers can write Avro schemas to tell these tools what to expect when it fetches data from various sources.

Kubernetes (k8s) uses gRPC , which is based on Google’s Protocol Buffer schema definition language (ProtoBuf), to facilitate communication with system components. Any third-party application can interact with k8s using these pre-defined schemas.
### Data Streaming without Schemas
Upstream changes in data types and fields can break downstream applications if there is not an agreed upon schema.
### Data Streaming with Schemas
Streaming applications are highly dependent on schemas. Schemas are important because:
* Data streams are constantly evolving
* No schema -> broken consumer on every data change
* Schemas allow consumers to function without updates
* They provide independence and scalability
## Apache Avro
Avro is widely used in data engineering, particularly in Kafka. This section will cover key concept relating to Avro and stream processing.
### What is Apache Avro?
Avro is a data serialization system that uses binary compression. One of the downsides of JSON is that it doesn’t tell us what datatypes each key should be. Avro contains binary data that adheres to the schema and contains the schema itself.
### How Avro Schemas are Defined
* Must include a type defined as `record`. This is always the top-level field
* Avro records are defined in JSON
* Records include a required name, such as “user”
* May optionally include namespace
* Must include array of fields that define expected fields and types:
```
"fields": [{"name": "age", "type", "int}]
```
* Support optional fields by specifying field type as either null or some other type. These are known as **union** types.
```
"fields": [{"name": "age", "type": ["null", "int"]}]
```
* Made up of complex and primitive types
  * Complex types include other records, arrays, maps, enums, etc.
* Example schema for a stock ticker price:
```
{
  “type”: “record”,
  “name”: “stock.price_change”,
  “namespace”: “com.udacity”,
  “fields”: [
      {“name”: “ticker”, “type”: “string”},
      {“name”: “prev_price”, “type”: “int”},
      {“name”: “price”, “type”: “int”},
      {“name”: “cause”, “type”: [“null”, “string”]}
  ]
}
```
[Avro documentation](https://avro.apache.org/docs/1.8.2/spec.html#schemas)
### Practice: Defining an Avro Record
\# TODO: Add link to `defining_a_schema.py`
### Apache Avro Data Types
The following primitive types are defined by Avro:
* `null`
* `boolean`
* `int`, `long`, `float`, `double`
* `bytes`
* `string`
  Complex types allow nesting and composition and include:
* records
* enum
* array
* map
* union
* field
#### Enum
Enumerations are a set of named symbols:
```
{
	"type": "enum",
	"name": "us_states",
	"symbols": ["AL", "AK", "AZ", "AR", "CA"]
}
```
#### Arrays and Maps
##### Arrays
Arrays store ordered fields of either primitive or complex types:
**Primitive**
```
{
	"type": "array",
	"values": "string"
}
```
**Complex**
```
{
	"type": "array",
	"items": {
		"type": "record",
		"fields": [
			{"name": "id", "type", "int"}
		]
}
```

##### Maps
Maps store fields a a string key value store of either primitive or complex types. Keys in Maps are always strings
**Primitive**
```
{
	"type": "map",
	"values": "int"
}
```
**Complex**
```
{
	"type": "map",
	"values": {
		"type": "record",
		"fields": [
			{"name": "id", "type", "int"}
		]
}
```
#### Unions
Unions are used when a field can be one of multiple types. Unions aren’t explicit but are denoted by square brackets:
```
{
	"type": "map",
	"values": {
		"type": "record",
		"fields": [
			{"name": "zipcode", "type": ["null", "int", "string"]}
		]
	}
}
```
#### Fixed
Fixed denotes a fixed size entry in bytes:
```
{
	"name": "md5",
	"type": "fixed",
	"size": 16
}
```
#### Further Reading
[Avro Schema docs](https://avro.apache.org/docs/1.8.2/spec.html#schema_primitive)
[Primitive Types](https://avro.apache.org/docs/1.8.2/spec.html#schema_primitive)
[Complex Types](https://avro.apache.org/docs/1.8.2/spec.html#schema_complex)
### Complex Records in Avro
\#TODO: Add link to exercise
### Apache Avro Summary
* Avro has primitive types, such as `int`, `string`, and `float`
* Avro has complex types, such as `record`, `map`, and `array`
* Avro data is sent alongside the schema definition, so that downstream consumers can make use of it
* Avro is used widely in data engineering and the Kafka ecosystem

#### Further Reading
*  [Python fastavro Library](https://fastavro.readthedocs.io/en/latest/index.html)
*  [Apache Avro Specification](https://avro.apache.org/docs/1.8.2/spec.html#Maps)

### Apache Avro and Kafka
Avro has been used extensively in the Kafka ecosystem since the beginning. It’s not required but makes things much easier. A Producer must define an Avro schema and encode the data. Many client libraries have built-in support for this. Python’s `confluent-kafka` library’s `AvroConsumer` will automatically unpack and deserialize data based on the schema provided with the data.
*  [`confluent_kafka_python` Avro Producer](https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=partition#confluent_kafka.avro.AvroProducer)
*  [`confluent_kafka_python` Avro Consumer](https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=partition#confluent_kafka.avro.AvroConsumer)
## Schema Registry
The  [Confluent Schema Registry](https://docs.confluent.io/current/schema-registry/index.html)  is a tool that provides centralized Avro Schema storage. This section will cover how to use the Schema Registry to improve streaming applications.
### Kafka - Schema Registry Integration
#### Producing/Consuming data with Schema Registry
Including a schema definition in in every message adds unnecessary overhead. It also puts the onus for serialization and deserialization on the producer and consumer. The Registry is built by Confluent and deployed along with Kafka. Instead the Kafka client can send the schema to the registry.
The Registry assigns the schema a version number and stores it in a private topic until it is changed. When consumers consume topic data, the Kafka client library will automatically pull the schema from the registry. The Registry can pull historic schemas as well, so that all messages can be serialized and deserialized.
Schemas only need to be sent to the Registry once, and clients will fetch the schema from there as needed. The Registry doesn’t support deletes by default, but deleting is not recommended. It also has an HTTP REST interface, making it easy to use, and is not limited to Kafka producers and consumers; any application can interact with the schema registry.
#### Schema Registry Architecture
* Web server built on the JVM using Scala and Java
* Highly portable, runs on almost all operating systems
* Stores all state in Kafka rather than database
* Uses compaction to ensure no data is deleted
* Exposes an HTTP web server with a REST API
* Can run standalone or clustered with many nodes
  * Uses ZooKeeper to elect leader when in cluster mode
### Integrating Schema Registry
\# TODO: Add link to `integrating_schema_registry.py`
### Schema Registry Summary
As a recap, the Schema Registry:
* Provides a REST API for managing Avro Schemas
* Many clients natively support Registry interactions
* Reduces overhead, allowing producers/consumers to register schemas once
* Simplifies Avro, lowering barrier to entry
* Uses a Topic to store state
* Deployed on one or more web servers, with one leader
* Uses ZooKeeper to manage elections when in a cluster
### Further Reading
*  [`confluent_kafka_python` Avro and Schema Registry support](https://docs.confluent.io/current/clients/confluent-kafka-python/index.html?highlight=partition#module-confluent_kafka.avro)
*  [Schema Registry Overview](https://docs.confluent.io/current/schema-registry/index.html)
*  [Schema Registry HTTP API Documentation](https://docs.confluent.io/current/schema-registry/develop/api.html)
## Schema Evolution; Compatibility
Data software doesn’t remain static, so neither should schemas. This section is about how schemas evolve over time and what compatibility guarantees Kafka provides.
### Understanding Schema Evolution
Evolution is the process of changing the schema of a given data set. These changes may be adding, removing or changing a field. Schemas can be updated by publishing an updated schema to the Registry, along with some compatibility information.
### Schema Compatibility
The Schema Registry tracks compatibility between schema versions. As Consumers fetch data from Kafka, the client will fetch the updated schema. Clients can also request compatibility information with an HTTP request. If the schema is compatible, the Consumer can continue pulling data. If the schema is not compatible, the Consumer will stop pulling data until the schema is updated.

The Schema Registry supports  [four categories of compatibility](https://docs.confluent.io/current/schema-registry/avro.html)
* Backward / Backward Transitive
* Forward / Forward Transitive
* Full / Full Transitive
* None
### Backward Compatibility
[Backward compatibility](https://docs.confluent.io/current/schema-registry/avro.html#backward-compatibility) means that Consumers developed against the latest schema can use older data.  Consumers should be updated before Producers to ensure the new schema and data types can be handled. Examples of backward compatibility include:
* Deletion of a field
* Addition of an optional field
  Schema Registry always assumes changes are `BACKWARD` compatible. There’s also `BACKWARD_TRANSITIVE`, which indicates compatibility with **all** prior schema versions.
### Forward Compatibility
[Forward compatibility](https://docs.confluent.io/current/schema-registry/avro.html#forward-compatibility)  means that consumer code developed against the previous version of an Avro Schema can consume data using the newest version of a schema without modification. Producers should be updated before Consumers. Examples of `FORWARD` compatibility include:
* The deletion of an optional field
* The addition of a new field
### Full Compatibility
[Full compatibility](https://docs.confluent.io/current/schema-registry/avro.html#full-compatibility)  means that consumers developed against the latest schema can use the previous schema and consumers developed against the previous schema can use the latest schema. These changes are both forward and backward compatible. The order in which producers/consumers are updated does not matter. Examples of full compatibility include changing the default value of a field. `FULL` compatibility indicates data is forward and backward compatible with the current and previous schemas, where `FULL_TRANSITIVE` compatibility indicates data is both forward and backward compatible with all previous schema versions.
### No Compatibility
Otherwise known as `NONE` compatibility,  [no compatibility](https://docs.confluent.io/current/schema-registry/avro.html#no-compatibility-checking)  disables compatibility validation by Schema Registry, which simply becomes a repository. Use of `NONE` is not recommended, but schemas will sometimes need to undergo a change that is neither forward nor backward compatible. An example of this might be changing the type of a field.

The best practice is to create a new topic and point consumers of the old topic at it. Managing multiple schemas with the same topic is difficult to maintain and should be avoided.
### Further Reading on Schema Evolution and Compatibility
*  [Confluent’s Schema Evolution and Compatibility Documentation](https://docs.confluent.io/current/schema-registry/avro.html#schema-evolution-and-compatibility)
*  [Avro Schema Resolution Rules for backward compatibility](http://avro.apache.org/docs/1.8.2/spec.html#Schema+Resolution)
