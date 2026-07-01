import json
import logging
from core.ports.task_service import EventPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogEventPublisher(EventPublisher):
    """
    aqui seria onde ficaria o rabbitMQ ou seja teria um adapter de infra pra publicar o evento
    """

    def publish(self, event_name: str, payload: dict) -> None:
        logger.info(f"[EVENT] {event_name} → {json.dumps(payload)}")
