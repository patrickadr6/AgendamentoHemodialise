import time
import pyautogui
import calendario
from horario import horario_atual
from retrying import retry

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

def criar_viagem(driver, viagem, dia, w):

    # Criar nova viagem
    driver.get("https://rangsaude.atibaia.sp.gov.br/novaViagem.xhtml")

    cidade = viagem[0]['cidade']
    horario = dia[0] + " " + viagem[0]['horario_saida']
    objetivo = viagem[0]['objetivo']
    veiculo = viagem[0]['veiculo']
    motorista = viagem[0]['motorista']
    observacao = viagem[0]['obs']

    # Cidade
    input_cidade = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:municipio_destino_input")))
    input_cidade.click()
    input_cidade.send_keys(cidade)

    select_cidade = w.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-state-highlight")))
    select_cidade.click()

    # Horário
    input_horario = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:dataHoraSaida_input")))
    input_horario.send_keys(horario)

    # Objetivo
    input_objetivo = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:objetivoViagem_input")))
    input_objetivo.click()
    input_objetivo.send_keys(objetivo)
    
    select_objetivo = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:j_idt3772")))
    select_objetivo.click()
    

    # Veículo
    input_veiculo = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:veiculo_input")))
    input_veiculo.click()
    input_veiculo.send_keys(veiculo)
    

    btn_veiculo = w.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='viagemCompleta:veiculo_panel']/table/tbody/tr[1]")))
    btn_veiculo.click()


    # Motorista
    time.sleep(2) # area de alto risco
    btn_moto = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:motorista_label")))
    btn_moto.click()
    

    select_moto = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:motorista_1")))
    select_moto.click()

    # Observação
    input_viagem = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:obsViagem")))
    input_viagem.send_keys(observacao)

    # Salvar a viagem
    btn_salvar = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:j_idt3902")))
    btn_salvar.click()

    # Add pacientes
    btn_add = w.until(EC.element_to_be_clickable((By.ID, "viagemCompleta:j_idt3901")))
    btn_add.click()

    # Pegar id da viagem
    novo_paciente = w.until(EC.element_to_be_clickable((By.CLASS_NAME, "fa-user-plus")))
    novo_paciente.click()

    # Eliminar aquela janela extra
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    id_viagem = driver.current_url.split("=")[1]

    add_pacientes(driver, id_viagem, viagem, dia, w)

    print(f"{horario_atual()} Viagem {viagem[0]} agendada com sucesso!\n\n")

    # duplicar essa viagem completa para todos os dias do mês
    #duplicar_viagem(driver, viagem, id_viagem, dias)

@retry(stop_max_attempt_number=5)
def add_pacientes(driver, id_viagem, viagem, dia, w):

    for paciente in viagem[1]:
        local_espera = ""

        # E SE NAO TIVER NENHUM PACIENTE INDO PARA UM DIA DA SEMANA? VIAGEM VAI SER CRIADA SEM NGM
        if dia[1] not in paciente['dias']:
            continue

        driver.get('https://rangsaude.atibaia.sp.gov.br/addPacienteViagem.xhtml?cod=' + id_viagem)


        paciente_input = w.until(EC.element_to_be_clickable((By.ID, "formCadastro:paciente_input")))
        paciente_input.send_keys(paciente['id'])
        paciente_panel = w.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='formCadastro:paciente_panel']/table/tbody/tr[1]")))
        paciente_panel.click()
        time.sleep(1)

        if paciente['tipo'] == 'IDA':
            tipo_ida = driver.find_element(By.XPATH, '//label[@for="formCadastro:tipoViagem:1"]')
            tipo_ida.click()

        elif paciente['tipo'] == 'VOLTA':
            tipo_volta = driver.find_element(By.XPATH, '//label[@for="formCadastro:tipoViagem:2"]')
            tipo_volta.click()

            # PEGAR ENDEREÇO DO PACIENTE
            if paciente['destino']:
                local_espera = paciente['destino']

            elif not paciente['destino']:
                w.until(EC.element_to_be_clickable((By.XPATH, '//span[.="Add. Endereço"]'))).click()

                endereco_cadastrado = w.until(EC.element_to_be_clickable((By.ID, 'formCadastro:esperaNovo')))
                local_espera = endereco_cadastrado.get_attribute('value')

                w.until(EC.element_to_be_clickable((By.XPATH, '//span[.="Add. Endereço"]'))).click()

        elif paciente['tipo'] == 'IDA/VOLTA':
            pass
        else:
            raise

        # TIPO VOLTA HÁ DE TER PACIENTE['LOCAL_ESPERA']
        if not paciente['local_espera']:
            w.until(EC.element_to_be_clickable((By.XPATH, '//span[.="Add. Endereço"]'))).click()

        time.sleep(.5)

        # ABRIR DESTINO
        w.until(EC.element_to_be_clickable((By.XPATH, '//span[.="Destinos"]'))).click()
        time.sleep(2)

        # COLOCAR DESTINO
        botao_destino = w.until(EC.element_to_be_clickable((By.ID, 'j_idt4024')))
        botao_destino.click()

        destino_novo = w.until(EC.element_to_be_clickable((By.ID, 'destinoNovo')))

        if paciente['tipo'] == 'IDA/VOLTA' or paciente['tipo'] == 'IDA':
            destino_novo.send_keys(paciente['destino'])
        elif paciente['tipo'] == 'VOLTA':
            destino_novo.send_keys(local_espera)
        else:
            raise

        
        municipio_destino = w.until(EC.element_to_be_clickable((By.ID, "municipio_destino_input")))
        municipio_destino.send_keys(paciente['cidade_destino'])

        select_municipio = w.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="municipio_destino_panel"]/table/tbody/tr')))
        select_municipio.click()

        # HORARIO DE CHEGADA
        datahora = w.until(EC.presence_of_element_located((By.ID, "dataHoraSaida_input")))
        # handle timeout
        datahora = w.until(EC.element_to_be_clickable((By.ID, "dataHoraSaida_input")))
        datahora.click()
        datahora.send_keys(Keys.CONTROL + "a")
        datahora.send_keys(Keys.DELETE)

        try:
            if paciente['horario_dias']:
                # pegar o valor da chave que é igual o dia[1]
                horario = paciente['horario_dias'].get(dia[1])
                datahora.send_keys(dia[0] + " " + horario)
        except KeyError as err:
            datahora.send_keys(dia[0] + " " + paciente['horario_chegada'])
        
        # ESPECIALIDADE
        driver.implicitly_wait(2)
        esp = 'especialidade'
        if esp in paciente.keys():
                w.until(EC.element_to_be_clickable((By.ID, "especialidade_input"))).send_keys(paciente['especialidade'])
                w.until(EC.presence_of_element_located((By.XPATH, '//*[@id="especialidade_panel"]/table/tbody/tr[1]')))
                w.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="especialidade_panel"]/table/tbody/tr[1]'))).click()
        else:
            w.until(EC.element_to_be_clickable((By.ID, "especialidade_input"))).send_keys("HEMODIÁLISE")
            w.until(EC.presence_of_element_located((By.XPATH, '//*[@id="especialidade_panel"]/table/tbody/tr[2]')))
            w.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="especialidade_panel"]/table/tbody/tr[2]'))).click()

        # DATA E HORA P/ O PACIENTE ESTAR LÁ
        w.until(EC.element_to_be_clickable((By.ID, 'dataHoraSaida_input'))).click()

        # OBSERVAÇÃO
        if paciente['obs']:
            w.until(EC.element_to_be_clickable((By.ID, "obs"))).send_keys(paciente['obs'])

        driver.implicitly_wait(1)

        # SALVAR DESTINO
        w.until(EC.element_to_be_clickable((By.ID, 'j_idt4083'))).click()

        time.sleep(2) # SENÃO, PODE BUGAR E O DESTINO Ñ FECHAR DIREITO

        # FECHAR DESTINO
        w.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog_search_destino_id"]/div[1]/a'))).click()

        driver.implicitly_wait(2)

        # ADICIONAR LOCAL DE ESPERA CUSTOM - aquele bug chato
        if paciente['local_espera']:
            w.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formCadastro:j_idt3871"]'))).click()

            try:
                w.until(EC.element_to_be_clickable((By.ID, "formCadastro:esperaNovo"))).send_keys(paciente['local_espera'])
            except StaleElementReferenceException as err:
                pass

            driver.implicitly_wait(2)

        # COLOCAR ACOMPANHANTE
        if paciente['acompanhante'] == "S":
        
            w.until(EC.element_to_be_clickable((By.XPATH, '//span[.="Acompanhante"]'))).click()
            time.sleep(1)

            # POPUP ACOMPANHANTE
            w.until(EC.element_to_be_clickable((By.ID, 'j_idt3957'))).click()
            w.until(EC.element_to_be_clickable((By.ID, 'nomeNaoMun'))).send_keys("A")

            time.sleep(2)

            if paciente['tipo'] == 'IDA' or paciente['tipo'] == 'VOLTA':
                w.until(EC.element_to_be_clickable((By.ID, 'tipoViagemAcomp_label'))).click()

            if paciente['tipo'] == 'IDA':
                w.until(EC.element_to_be_clickable((By.ID, 'tipoViagemAcomp_1'))).click()
            elif paciente['tipo'] == 'VOLTA':
                w.until(EC.element_to_be_clickable((By.ID, 'tipoViagemAcomp_2'))).click()

            w.until(EC.element_to_be_clickable((By.ID, 'esperaAcomp_input'))).send_keys("O MESMO")
            w.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="esperaAcomp_panel"]/ul/li[1]'))).click()

            w.until(EC.element_to_be_clickable((By.ID, 'j_idt4006'))).click() 

            w.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog_search_acompanhante_id"]/div[1]/a'))).click()

        # APERTAR BOTAO DE SALVAR
        print(f"{horario_atual()} Paciente {paciente['id']} adicionado no dia {dia}")


# def duplicar_viagem(driver, viagem, url_viagem, dias):

#     segunda_quarta_sexta = calendario.separar_dias_do_mes()[0]

#     for dia in list(dias.keys())[1:]:
#         dia_atual = dia

#         driver.get("https://rangsaude.atibaia.sp.gov.br/novaViagemPaciente.xhtml?cod=" + url_viagem)
#         time.sleep(2)

#         # COLOCAR DATA E HORA DE SAÍDA
#         driver.find_element(By.ID, "formCadastro:dataHoraSaida_input").send_keys(Keys.CONTROL + "a")
#         driver.find_element(By.ID, "formCadastro:dataHoraSaida_input").send_keys(Keys.DELETE)
#         driver.find_element(By.ID, "formCadastro:dataHoraSaida_input").send_keys(dia[0] + " " + viagem[0]['horario_saida'])
#         time.sleep(2)

#         # GERAR DATA
#         driver.find_element(By.ID, "formCadastro:viagemDataDestinos").click()
#         time.sleep(2)

#         pyautogui.press("space")
#         time.sleep(2)
        
#         # IR PARA PACIENTES
#         driver.find_element(By.ID, 'formCadastro:buttonPaciente').click()
#         time.sleep(2)

#         # SALVAR
#         driver.find_element(By.ID, 'formCadastro:j_idt4207').click()
#         time.sleep(2)
