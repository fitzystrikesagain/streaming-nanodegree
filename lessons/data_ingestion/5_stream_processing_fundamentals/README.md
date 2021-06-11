# Lesson 5: Stream Processing Fundamentals
In this lesson, you will learn the core concepts and concerns involved in building stream processing applications:
* Strategies for Application Design
* Combining Streams
* Filtering Streams
* Remapping Streams
* Aggregating Streams
* Handling Time and Windowing
* Streams vs Tables

## Glossary of Terms for Lesson
* Join (Streams) - The process of combining one or more streams into an output stream, typically on some related key attribute.
* Filtering (Streams) - The process of removing certain events in a data stream based on a condition
* Aggregating (Streams) - The process of summing, reducing, or otherwise grouping data based on a key attribute
* Remapping (Streams) - The process of modifying the input stream data structure into a different output structure. This may include the addition or removal of fields on a given event.
* Windowing (Streams) - Defining a period of time from which data is analyzed. Once data falls outside of that period of time, it is no longer valid for streaming analysis.
* Tumbling Window (Streams) - The tumbling window defines a block of time which rolls over once the duration has elapsed. A tumbling window of one hour, started now, would collect all data for the next 60 minutes. Then, at the 60 minute mark, it would reset all of the data in the topic, and begin collecting a fresh set of data for the next 60 minutes.
* Hopping Window (Streams) - Hopping windows advance in defined increments of time. A hopping window consists of a window length, e.g. 30 minutes, and an increment time, e.g. 5 minutes. Every time the increment time expires, the window is advanced forward by the increment.
* Sliding Window (Streams) - Sliding Windows work identically to Hopping Windows, except the increment period is much smaller — typically measured in seconds. Sliding windows are constantly updated and always represent the most up-to-date state of a given stream aggregation.
* Stream - Streams contain all events in a topic, immutable, and in order. As new events occur, they are simply appended to the end of the stream.
* Table - Tables are the result of aggregation operations in stream processing applications. They are a roll-up, point-in-time view of data.
* Stateful - Stateful operations must store the intermediate results of combining multiple events to represent the latest point-in-time value for a given key

## Combining Streams
Combining, or joining, streams is the process of merging their data. This is the action of taking one or more streams and joining them. Joined streams always share some common attribute. State must be kept as events flow through the calculation until all related data has arrived. Only then can the new event be emitted, and the state flushed. If the data never fully arrives, the memory should be cleared. This is typically accomplished through windowing, which will be covered later.

## Filtering Streams
Filtering is removing unwanted data from one stream and putting it into a new stream. This may be a step in joining or combining two ore more streams. This is desirable when customers don’t need access to all the data. Applying filters early allows stream processing calculations to scale better.

## Remapping Streams
Remapping streams is transforming an input event and outputting it in a different form to a new stream. It’s frequently used in data engineering for data health and security reasons. For instance, downstream clients may need a different format. Another common scenario is removing sensitive or unnecessary fields.

## Aggregating Streams
Aggregation involves taking two or more streams and creating one or more new events based on a transformation function. Aggregate functions include max, min, sum, TopN, Histograms, Sets, Lists, and more. Aggregations almost always involve a timeframe unless the source topic is compacted.
## Handling Time
Streaming applications don’t look at all data at once, but are concerned with specific windows of time. This period is known as the window and has a definite start and end time. This section will cover different types of windows and windowing approaches. Not all frameworks implement the same windowing types, but most will support the types we cover here.

## Tumbling Window
A tumbling window is a fixed period of time that rolls over after the fixed window has ended. This could be fifteen minutes or an hour, but the window shifts are discrete rather than continuous. In other words, this is not a rolling window in the strict sense, but the blocks of time shift as the blocks come to an end. There is no overlap or gap between them.

## Hopping Window
Hopping windows are advanced by both a duration and increment time. A hopping window of 10 minutes with an incrementing time of 1 minute would cover the last 10 minutes and increment every minutes. We can have overlaps with this windowing type. If the incrementing period is too large, we can also have gaps.

## Sliding Window
Sliding windows are hopping windows that increment in near real time. The increment is not directly configurable.  A sliding window contains the most up-to-date data possible and is constantly being updated. Sliding windows typically overlap should not be gapless.

## Streams and Tables
This section will cover the distinction between streams and tables in streaming frameworks. We’ll also learn when each approach is appropriate. A table implies state and an aggregation of some type. A stream is a never-ending, immutable series of events.
## Streams
Streams contain all events in an ordered immutable topic. New events are added to the stream as they occur. Streams often get processed and fed into another stream. Streams are not aggregates, they are boundless series of events.

## Tables
Streaming tables are the result of aggregation operations in stream processing. Tables are bounded, mutable, and not necessarily ordered. Tables are how we gain insights from streaming data. As new data arrives into our calculations, our streaming applications update an aggregated view of that data in real time.

## Streams vs Tables
Streams and tables solve different problems and give us different data, but they are complement each other, rather than being at opposition. Applications performing aggregations across incoming data are creating tables. Applications that are transforming incoming data into an unending sequence of events are streams.
### Further Reading
[Of Streams and Tables in Kafka and Stream Processing, Part 1](https://www.michael-noll.com/blog/2018/04/05/of-stream-and-tables-in-kafka-and-stream-processing-part1/)
## Data Storage
Table operations are stateful, that is, we must store the intermediate results of combined events to represent the latest point-in-time value for a given key. As such, they need to be stored. this can be done in memory or dedicated  databases.
* All stream frameworks require a changelog. KSQL, Faust, and Flink all use Kafka to store changes
* Changelog topic tracks all changes in stream
* Changelog topic are compacted
* This topic aids in fault tolerance and recovery
### RocksDB
Most streaming frameworks use in-memory stores. While fast and fault-tolerant, there are better approaches. RocksDB is a highly-optimized local state store built at Facebook to handle these types of situations. RocksDB can run on every application node and store state for that application. This state speeds up reboot and recovery times. RocksDB is used by many streaming frameworks as an option to store state: KStreams, Faust, and Flink.

### Further Optional Reading - Data Storage
*  [RocksDB](https://rocksdb.org/)
*  [Kafka Streams State](https://docs.confluent.io/current/streams/architecture.html?&_ga=2.265603023.1364268795.1565759077-2091975159.1565759077#state)

#dsnd/kafka