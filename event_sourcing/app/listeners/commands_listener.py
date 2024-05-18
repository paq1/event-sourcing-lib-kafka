import json
import logging
from typing import Generic, TypeVar

import asyncio
from kafka import KafkaConsumer

from event_sourcing.app.command_handlers.command_dispacher import CommandDispatcher
from event_sourcing.core.queue_message_producer import QueueMessageProducerHandler
from event_sourcing.models.command import Command
from event_sourcing.models.from_dict import CreateFromDict

COMMAND = TypeVar('COMMAND', bound=CreateFromDict)
STATE = TypeVar('STATE')
EVENT = TypeVar('EVENT')


class CommandsListener(Generic[STATE, COMMAND, EVENT]):
    logger = logging.getLogger(f"{__name__}#CommandsListener")

    def __init__(
            self,
            topic_commands_name: str,
            queue_message_producer_handler: QueueMessageProducerHandler,
            command_dispatcher: CommandDispatcher[STATE, COMMAND, EVENT]
    ):
        self.command_dispatcher = command_dispatcher
        self.consumer = KafkaConsumer(
            topic_commands_name,
            bootstrap_servers='192.168.1.19:9092',
            group_id=f"consumer_cqrs_grp_2",
            auto_offset_reset="latest"  # "earliest"
        )
        self.queue_message_producer_handler = queue_message_producer_handler
        self.running = True

    def run(self):
        for msg in self.consumer:
            key = msg.key.decode('utf-8')
            value = msg.value.decode('utf-8')
            self.logger.debug(f"received message {key} {value}")
            # mkdmkd todo traitement de la command ici avec le command dispatcher
            # step 1 from str to dict
            dict_command_record_value = json.loads(value)

            entity_id = dict_command_record_value["entityId"]
            ch_name = dict_command_record_value["name"]
            command_dict: dict = dict_command_record_value["body"]
            command: Command = Command(entity_id, ch_name, command_dict)
            # # step 1 from value(json) to Command

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            task = loop.create_task(self.command_dispatcher.exec(command))
            loop.run_forever()
            r = task.result()
            resp = self.command_dispatcher.exec(command)

            self.logger.warning("[not implemented] le gestionnaire de commande n'est pas encore implémenté")
            self.logger.warning("[not implemented] pas de génération d'evenements")
            # mkdmkd todo appeler le reducer et générer le nouvel etat
            self.logger.warning("[not implemented] pas de reducer")
            # mkdmkd todo insertion en db
            self.logger.warning("[not implemented] pas de persistance des evenements")
            self.logger.warning("[not implemented] pas de persistance des états")

            self.queue_message_producer_handler.produce_message_sync(
                topic="subject-cqrs-results",
                message={"result": "autre donnees"},
                key=key
            )

            if not self.running:
                self.logger.info("stopping loop")
                break
        self.logger.info("thread finished")

    def stop(self):
        self.running = False
