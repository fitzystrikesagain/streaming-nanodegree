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