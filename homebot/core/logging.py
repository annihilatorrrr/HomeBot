from logging import basicConfig, INFO

def setup_logging(level: int = INFO):
	basicConfig(format='[%(asctime)s] [%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s',
	            level=level, force=True)
