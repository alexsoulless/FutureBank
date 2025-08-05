import dotenv

config = dotenv.dotenv_values()


if config["TELEGRAM_API_KEY"] is None:
    raise RuntimeError("No TELEGRAM_API_KEY in config")
else:
    TELEGRAM_API_KEY = config["TELEGRAM_API_KEY"]
