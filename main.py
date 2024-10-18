# Módulos
import time
import pyautogui
import criarViagem
import viagens
import calendario
from horario import horario_atual
import argparse
import logging
logger = logging.getLogger(__name__)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



print("\n\n\n\n\n*************          AGENDAMENTO DE HEMODIALISE 3000          *************\n")

# Pegar usuário e senha dos parâmetros passados.
parser = argparse.ArgumentParser(description='Script para agendamento de transporte de hemodiálise. Segunda, quarta e sexta, e terça, quinta e sábado.')
parser.add_argument("--usuario", type=str, default="")
parser.add_argument("--senha", type=str, default="")

args = parser.parse_args()
usuario = args.usuario
senha = args.senha

if senha == "":
    raise KeyError

logging.basicConfig(filename='relatorio.log', level=logging.INFO)

# Configurar driver
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
chrome_options.add_argument("window-size=1200x600")

w = WebDriverWait(driver, 120)

# Pegar os dias q são segunda quarta e sexta, ou terça quinta e sabado
mes = int(input("Digite o mês (9, 10, 11) a ser agendado:\n"))
ano = int(input("Digite o ano do mês a ser agendado:\n"))
conf_vans = input("Agendar as vans normais (S/N)?\n")
conf_hemo = input("Agendar hemodiálise (S/N)?\n")

# Logar no sistema
driver.get("https://rangsaude.atibaia.sp.gov.br/login.xhtml")

login = driver.find_element(By.ID, "formLogin:login").send_keys(usuario)
senha = driver.find_element(By.ID, "formLogin:password").send_keys(senha)
entrar = driver.find_element(By.ID, "formLogin:save").send_keys(Keys.ENTER)

driver.implicitly_wait(2)
estabelecimento = driver.find_element(By.CLASS_NAME, "ui-commandlink").click()
time.sleep(2)

# Pegar viagens das 3 listas
logger.info(f"\n\n\n\n\n{horario_atual()} Nova execução!\n\n")
if conf_vans == "S":
    logger.info(f"\n{horario_atual()} Agendando as vans comuns...\n")
    viagens_van = viagens.viagens_van
    segunda_a_sexta = calendario.separar_segunda_a_sexta(mes, ano)

    for viagem in viagens_van:
        for dia in segunda_a_sexta.items():
            criarViagem.criar_viagem(driver, viagem, list(dia), w)
elif conf_vans == "N":
    pass
else:
    raise


if conf_hemo == "S":
    logger.info(f"\n{horario_atual()} Agendando hemodiálise...\n\n")
    viagens_sqs = viagens.viagens_segunda_quarta_sexta
    viagens_tqs = viagens.viagens_terca_quinta_sabado

    segunda_quarta_sexta, terca_quinta_sabado = calendario.separar_dias_hemo(mes, ano)

    # criar viagem e adicionar pacientes
    for viagem in viagens_sqs:
        for dia in segunda_quarta_sexta.items():
            criarViagem.criar_viagem(driver, viagem, list(dia), w)

    for viagem in viagens_tqs:
        for dia in terca_quinta_sabado.items():
            criarViagem.criar_viagem(driver, viagem, list(dia), w)
elif conf_hemo == "N":
    pass
else:
    raise

logger.info(f"\n{horario_atual()} Todas as viagens foram agendadas com sucesso!")







# Adicionar pacientes na viagem

# segunda, quarta e sexta
# 1º turno
# 2º turno
# 3º turno
# 4º turno



# terça, quinta e sábado
# 1º turno
# 2º turno
# 3º turno
# 4º turno
# ???
