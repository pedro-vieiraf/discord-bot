import pyautogui
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def obter_tamanho_navegador(navegador):
    """Obtém o tamanho da janela do navegador."""
    tamanho = navegador.get_window_rect()  # Retorna {'width': largura, 'height': altura, 'x': pos_x, 'y': pos_y}
    return tamanho['width'], tamanho['height'], tamanho['x'], tamanho['y']

def garantir_navegador_maximizado(navegador):
    """Maximiza o navegador se ele estiver menor que o esperado."""
    largura, altura, _, _ = obter_tamanho_navegador(navegador)

    if largura < 1000 or altura < 600:  # Se o navegador estiver muito pequeno, maximiza
        print("Navegador não está maximizado. Maximizando...")
        navegador.maximize_window()
        time.sleep(2)  # Dá tempo para o navegador ajustar o tamanho
        return True  # Indica que o navegador foi maximizado
    return False  # Já estava maximizado

def calcular_posicao_pop_up(navegador):
    """Calcula dinamicamente a posição do pop-up de compartilhamento."""
    largura, altura, pos_x, pos_y = obter_tamanho_navegador(navegador)

    # Como o pop-up é centralizado, estimamos sua posição
    largura_popup = largura * 0.4  # O pop-up ocupa cerca de 40% da largura do navegador
    altura_popup = altura * 0.5  # O pop-up ocupa cerca de 50% da altura do navegador
    x_popup = pos_x + (largura - largura_popup) // 2  # Centralizado horizontalmente
    y_popup = pos_y + (altura - altura_popup) // 2  # Centralizado verticalmente

    return int(x_popup), int(y_popup), int(largura_popup), int(altura_popup)

def clicar_na_area_clicavel(navegador):
    """Clica na área clicável do pop-up de compartilhamento."""
    x_popup, y_popup, largura_popup, altura_popup = calcular_posicao_pop_up(navegador)

    # A área clicável está dentro do pop-up, ajustamos para o local correto
    x_clicavel = x_popup + largura_popup * 0.3  # Ajuste horizontal (~30% da largura do pop-up)
    y_clicavel = y_popup + altura_popup * 0.35  # Ajuste vertical (~35% da altura do pop-up)

    print(f"Clicando na área de compartilhamento: ({int(x_clicavel)}, {int(y_clicavel)})")
    pyautogui.click(int(x_clicavel), int(y_clicavel))

    time.sleep(1)  # Pequeno delay para garantir que o clique foi processado
    pyautogui.press("down")  # Move para a opção de compartilhamento
    pyautogui.press("enter")  # Confirma o compartilhamento
    print("Compartilhamento iniciado com sucesso!")

def compartilhar_tela(navegador):
    """Fluxo completo para compartilhar a tela no Discord."""
    try:
        # Verifica e maximiza o navegador se necessário
        navegador_maximizado = garantir_navegador_maximizado(navegador)

        # Aguarda o botão de compartilhar estar visível
        botao_compartilhar = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/section/div[1]/div/div[2]/button[2]'))
        )

        # Clica no botão de compartilhar
        botao_compartilhar.click()
        print("Botão de compartilhar clicado.")

        # Aguarda um pouco para o pop-up aparecer
        time.sleep(2)

        # Executa o clique na área correta
        clicar_na_area_clicavel(navegador)

    except Exception as e:
        print("Erro ao compartilhar a tela:", e)
