# Lesson 2, Lecture 7: Explore how Kafka Works

In this section you reviewed Kafka's architecture and how it stores data. In
this exercise, you will spend some time seeing how Kafka works.

## Topic Storage

First, let's create a topic

```
kafka-topics --create \
--topic kafka-arch \
--partitions 1 \
--replication-factor 1 \
--zookeeper localhost:2181
```

### Inspecting the Directory Structure

Now that the topic is successfully created, let's see how Kafka stored it on
disk.

```markdown
ls -alh /var/lib/kafka/data | grep kafka-arch
```

What does the output look like?

```markdown
[appuser@broker ~]$ ls -alh /var/lib/kafka/data | grep kafka-arch drwxr-xr-x 2
appuser appuser 4.0K May 31 23:43 kafka-arch-0
```

What kind of data is kept inside of the directory?

Logs and metadata

```markdown
total 24K drwxr-xr-x 2 appuser appuser 4.0K May 31 23:43 . drwxrwxrwx 276
appuser appuser 20K May 31 23:44 .. -rw-r--r-- 1 appuser appuser 10M May 31 23:
43 00000000000000000000.index -rw-r--r-- 1 appuser appuser 0 May 31 23:43
00000000000000000000.log -rw-r--r-- 1 appuser appuser 10M May 31 23:43
00000000000000000000.timeindex -rw-r--r-- 1 appuser appuser 0 May 31 23:43
leader-epoch-checkpoint
```

If you try to open the file ending in `.log` is there anything in it? 

Not yet

### Produce Data

Now that we have this topic, let's produce some data into it.

`kafka-console-producer --topic "kafka-arch" --broker-list localhost:9092`

Produce 5-10 messages.

Once you're done, hit Ctrl+C to exit.

Repeat the steps
from [Inspecting the Directory Structure](#inspecting-the-directory-structure)
and see how the results have changed.

## Topics and Partitions

Now that you've seen what a topic with a single partition looks like, let's see
what happens if we modify the number of partitions

`kafka-topics --alter --topic kafka-arch --partitions 3 --zookeeper localhost:2181`

Try repeating the steps
from [the previous section](#inspecting-the-directory-structure). How many
folders do you see now?

3
```markdown
[appuser@broker data]$ ls -alh | grep arch
drwxr-xr-x   2 appuser appuser 4.0K May 31 23:43 kafka-arch-0
drwxr-xr-x   2 appuser appuser 4.0K May 31 23:46 kafka-arch-1
drwxr-xr-x   2 appuser appuser 4.0K May 31 23:46 kafka-arch-2
```

Try modifying the number of partitions a few more times to see how Kafka
modifies the data on disk.

