from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config['TOKEN']
GROUP_IDS = [int(id.strip()) for id in config["GROUP_IDS"].split(",")]
ADMIN_ID = [int(id.strip()) for id in config["ADMIN_ID"].split(",")]