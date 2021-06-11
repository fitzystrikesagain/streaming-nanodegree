
# Lesson 1 Glossary
* **Stream** - An unbounded sequence of ordered, immutable data
* **Stream Processing** - Continual calculations performed on one or more *Streams*
* **Immutable Data** - Data that cannot be changed once it has been created
* **Event** - An immutable fact regarding something that has occurred in our system.
* **Batch Processing** - Scheduled, periodic analysis of one or more groups of related data.
* **Data Store** - A generic place that holds data of some kind, like a message queue or data store
* **Stream Processing Application** - An application which is downstream of one or more data streams and performs some kind of calculation on incoming data, typically producing one or more output data streams
* **Stream Processing Framework** - A set of tools, typically bundled as a library, used to construct a Stream Processing Application
* **Real-time** - In relation to processing, this implies that a piece of data, or an event, is processed almost as soon as it is produced. Strict time-based definitions of real-time are controversial in the industry and vary widely between applications. For example, a Computer Vision application may consider real-time to be 1 millisecond or less, whereas a data engineering team may consider it to be 30 seconds or less. In this class when the term "real-time" is used, the time-frame we have in mind is *seconds*.
* **Append-only Log** - files in which incoming events are written to the end of the file as they are received
* **Change Data Capture (CDC)** - The process of capturing change events, typically in SQL database systems, in order to accurately communicate and synchronize changes from primary to replica nodes in a clustered system.
* **Log-Structured Storage** - Systems built on Append-Only Logs, in which system data is stored in log format.
* **Merge** (Log Files) - When two or more log files are joined together into a single output log file
* **Compact** (Log Files) - When data from one or more files is deleted, typically based on the age of data
* **Source** (Kafka) - A term sometimes used to refer to Kafka clients which are producing data into Kafka, typically in reference to another data store
* **Sink** (Kafka) - A term sometimes used to refer to Kafka clients which are extracting data from Kafka, typically in reference to another data store
* **Topic** (Kafka) - A logical construct used to organize and segment datasets within Kafka, similar to how SQL databases use tables
* **Producer** (Kafka) - An application which is sending data to one or more Kafka Topics.
* **Consumer** (Kafka) - An application which is receiving data from one or more Kafka Topics.
