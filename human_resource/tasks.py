from celery.decorators import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task(name="send_candidate_message_task")
def send_candidate_message_task():
    logger.info("Candidate message sent.")
    return send_candidate_message_task()
