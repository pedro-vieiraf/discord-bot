import json
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Configurações do Firefox
firefox_options = Options()
firefox_options.profile = r"C:\Users\Gaming\AppData\Roaming\Mozilla\Firefox\Profiles\qonl30w6.BOT"

# Inicializa o driver do Firefox
service = Service(GeckoDriverManager().install())
navegador = webdriver.Firefox(service=service, options=firefox_options)

# Caminho do arquivo JSON
json_path = "bot_data.json"
last_modified = 0

while True:
    modified_time = os.path.getmtime(json_path)

    if modified_time > last_modified:
        last_modified = modified_time  # Atualiza referência de modificação

        # Lê o JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            link = data.get("Link")

        if link:
            print(f"Abrindo: {link}")
            navegador.get(link)

    time.sleep(5)
