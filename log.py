from loguru import logger

logger.add(
    "file.log",
    level="DEBUG",
    format="{time:DD-MM-YYYY HH:mm:ss} {level} {message}",
    rotation="100 MB"
)

def debug(msg):
    logger.debug(msg)
    
def info(msg):
    logger.info(msg)
    
def warning(msg):
    logger.warning(msg)
    
def error(msg):
    logger.error(msg)
    



