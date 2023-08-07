import logging
import os

def say_and_do(cmd):
    logging.info(f"${cmd}")
    os.system(cmd)