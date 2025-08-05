import dotenv

config = dotenv.dotenv_values()

TELEGRAM_API_KEY = config["TELEGRAM_API_KEY"]

if TELEGRAM_API_KEY is None:
	raise RuntimeError("No TELEGRAM_API_KEY in config")