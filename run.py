from app import create_app

from config import DevelopConfig

application = create_app(DevelopConfig)


if __name__ == "__main__":
    application.run("0.0.0.0")
