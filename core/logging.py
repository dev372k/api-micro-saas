import logging
from core.config import settings

logging.basicConfig(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)