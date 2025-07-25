import logging
import sys
import builtins

logger = logging.getLogger(__name__)

logging.basicConfig(
    filename='sweetmeter.log',
    level=logging.INFO,
    format='%(asctime)s [%(created)d] %(levelname)s: %(message)s'
)



def logging_print_hijack(*args):
    log_message = ""

    for arg in args:
        log_message += " " + str(arg)

    logger.info( log_message )

builtins.print = logging_print_hijack



def print(*args):
    log_message = ""

    for arg in args:
        log_message += " " + str(arg)

    logger.info( log_message )
    sys.stdout.write( log_message + "\n" )



def error( *args ):
    log_message = ""

    for arg in args:
        log_message += " " + str(arg)

    logger.error( log_message )



def panic( *args ):
    log_message = ""

    for arg in args:
        log_message += " " + str(arg)

    logger.error( log_message )
    exit(-1)

