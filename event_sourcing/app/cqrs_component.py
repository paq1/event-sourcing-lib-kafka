from event_sourcing.app.kafka.kafka_component import KafkaComponent


class CqrsComponent(KafkaComponent):
    def __init__(
            self,
            kafka_producer_host="192.168.1.19:9092",
            kafka_consumer_host="192.168.1.19:9092",

    ):
        super().__init__(kafka_producer_host=kafka_producer_host, kafka_consumer_host=kafka_consumer_host)
