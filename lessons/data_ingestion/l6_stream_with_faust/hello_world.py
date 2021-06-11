import faust

BROKER_URL = "PLAINTEXT://localhost:9092"
TOPIC_NAME = "com.udacity.streams.purchases"

app = faust.App(
    'hello-world',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

purchases_topic = app.topic(TOPIC_NAME)


@app.agent(purchases_topic)
async def purchase(purchases):
    async for p in purchases:
        print(p)


if __name__ == "__main__":
    app.main()
