import dotenv

config = dotenv.dotenv_values()

API_IP = config["API_IP"]
API_PORT = config["API_PORT"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_USER = config["DB_USER"]
DB_HOST = config["DB_HOST"]
DB_PORT = config["DB_PORT"]
DB_NAME = config["DB_NAME"]