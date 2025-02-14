import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Defina o caminho do executável do Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Altere conforme necessário



chrome_options = Options()

#----------------------------------------------ALTERE O USUARIO DO CHROME-----------------------------------------------
chrome_options.add_argument(r"--user-data-dir=C:\Users\Gaming\AppData\Local\Google\Chrome\User Data")  # Caminho do perfil
chrome_options.add_argument("--profile-directory=Profile 2")  # Nome do perfil (pode ser outro, como "Profile 1")
#-----------------------------------------------------------------------------------------------------------------------
chrome_options.binary_location = chrome_path  # Define o caminho do Chrome
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service, options=chrome_options)

# Caminho do arquivo JSON
json_path = "bot_data.json"

# Última modificação do arquivo
last_modified = 0

while True:
    # Verifica se o arquivo foi modificado
    modified_time = os.path.getmtime(json_path)

    if modified_time > last_modified:
        last_modified = modified_time  # Atualiza a referência de modificação

        # Lê o JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            link = data.get("Link")  # Obtém o link

        if link:
            print(f"Abrindo: {link}")
            navegador.get(link)  # Abre o link no navegador

    time.sleep(5)
    #TESTE: para deixar em fullScreen no youtube

