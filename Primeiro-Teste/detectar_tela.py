import pyautogui
import time
import cv2
import numpy as np

def detectar_e_clicar():
    """
    Detecta a área escura de compartilhamento no Discord e clica nela automaticamente.
    """
    time.sleep(3)  # Dá tempo para a interface carregar

    # Tira um print da tela para análise
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)

    # Converte para escala de cinza
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    # Define a cor do quadrado da interface (ajuste se necessário)
    cor_min = np.array([20, 18, 16])  # Tons escuros da interface
    cor_max = np.array([50, 48, 46])  # Tons um pouco mais claros

    # Cria uma máscara para encontrar a área do quadrado
    mascara = cv2.inRange(screenshot_np, cor_min, cor_max)

    # Encontra contornos
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Se encontrar a área, clica no centro dela
    if contornos:
        for cnt in contornos:
            x, y, w, h = cv2.boundingRect(cnt)
            centro_x = x + w // 2
            centro_y = y + h // 2

            # Clica no centro do quadrado
            pyautogui.click(centro_x, centro_y)
            print(f"Clicando em {centro_x}, {centro_y}")

            # Pressiona Seta para Baixo e Enter para confirmar o compartilhamento
            time.sleep(1)
            pyautogui.press("down")
            pyautogui.press("enter")
            print("Compartilhamento iniciado!")
            return True  # Retorna sucesso

    print("Não foi possível encontrar a área para clicar.")
    return False  # Retorna falha
