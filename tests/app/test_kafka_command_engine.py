import unittest

from event_sourcing.app.kafka_command_engine import KafkaCommandEngine


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_something():
        kafka = KafkaCommandEngine[str, str, str]()
        assert kafka.offer() is True


if __name__ == '__main__':
    unittest.main()
