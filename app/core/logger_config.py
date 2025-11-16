from rusty_logger import Logger, LogConfig

logger = Logger.get_logger(__file__, LogConfig(level="debug", color=True))