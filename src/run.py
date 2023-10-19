from loguru import logger
from src.managers.main import MainManager


# @logger.catch
def main():
    manager = MainManager()
    manager.work()


if __name__ == "__main__":
    main()
