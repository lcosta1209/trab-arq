import json
import logging
from core.ports.task_service import EventPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogEventPublisher(EventPublisher):
    """
    Adapter de saída: implementação simples do publicador de eventos via log.
    Em produção, poderia ser substituído por RabbitMQ, Kafka, etc.
    """

    def publish(self, event_name: str, payload: dict) -> None:
        logger.info(f"[EVENT] {event_name} → {json.dumps(payload)}")
