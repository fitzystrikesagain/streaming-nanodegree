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
*
### Summary: Data Schemas
## Apache Avro
### What is Apache Avro
### How Avro Schemas are Defined
### Practice: Defining an Avro Record
### Apache Avro Data Types
### Complex Records in Avro
### Apache Avro Summary
### Apache Avro and Kafka
## Schema Registry
### Kafka - Schema Registry Integration
### Review: Kafka - Schema Registry Integration
### Integrating Schema Registry
### Schema Registry Summary
## Schema Evolution; Compatibility
### Understanding Schema Evolution
### Schema Compatibility
### Backward Compatibility
### Forward Compatibility
### Full Compatibility
### No Compatibility
### Summary: Schema Evolution & Compatibility

#dsnd/kafka 