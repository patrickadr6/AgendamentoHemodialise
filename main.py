# Módulos
import time
import pyautogui
import criarViagem
import viagens
import calendario
import argparse
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

# Configurar driver
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
chrome_options.add_argument("window-size=1200x600")

w = WebDriverWait(driver, 120)

# Pegar os dias q são segunda quarta e sexta, ou terça quinta e sabado
mes = int(input("Digite o mês (9, 10, 11) a ser agendado:\n"))
ano = int(input("Digite o ano do mês a ser agendado:\n"))
segunda_quarta_sexta, terca_quinta_sabado = calendario.separar_dias_do_mes(mes, ano)

# Logar no sistema
driver.get("https://rangsaude.atibaia.sp.gov.br/login.xhtml")

login = driver.find_element(By.ID, "formLogin:login").send_keys(usuario)
senha = driver.find_element(By.ID, "formLogin:password").send_keys(senha)
entrar = driver.find_element(By.ID, "formLogin:save").send_keys(Keys.ENTER)

driver.implicitly_wait(2)
estabelecimento = driver.find_element(By.CLASS_NAME, "ui-commandlink").click()
time.sleep(2)

# Pegar viagens das 2 listas
viagens_sqs = viagens.viagens_segunda_quarta_sexta
viagens_tqs = viagens.viagens_terca_quinta_sabado

# criar viagem e adicionar pacientes
for viagem in viagens_sqs:
    for dia in segunda_quarta_sexta.items():
        criarViagem.criar_viagem(driver, viagem, list(dia), w)

for viagem in viagens_tqs:
    for dia in terca_quinta_sabado.items():
        criarViagem.criar_viagem(driver, viagem, list(dia), w)

print("Todas as viagens foram agendadas com sucesso!")

#print(viagem)







































#LISTAS DE TODAS AS VIAGENS PROVIDENCIAR!!

# para cada viagem na viagens_segunda_quarta_sexta:
#   para cada dia em segunda_quarta_sexta:
#       url_viagem = criarViagem(viagem[0] <- dados da viagem, dia)
#       FUNÇÃO PARA ADICIONAR CADA PACIENTE NA VIAGEM!
#           adicionar_pacientes(url_viagem, viagem[1])










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

# van ou carro

# para cada viagem, farei uma lista com 2 listas:
# [cidade, horário, objetivo, motorista, observação, hospital, caminho (ida, volta ou ambos)]
#  e a segunda, uma lista de listas com os dados dos pacientes:
# [[nome/cartão sus/cpf, tem acompanhante?, dia diferente ("N" ou "" por ex)?], [nome, tem acompanhante?, horário diferente?]]


# viagem1 = [["Bragança Paulista", "03:00", "05:00", "TRANSPORTE DE PACIENTES", "A", "ABASTECIMENTO ", "HUSF", "IDA/VOLTA"], [["PATRICK ADRIEL RIBAS", "N", "N"]]]

# colocar todas as viagens da msm frequencia em uma lista?

# para cada segunda, quarta e sexta do mês:
#    