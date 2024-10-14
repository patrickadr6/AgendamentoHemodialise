import datetime, calendar

def separar_dias_do_mes(mes, ano):
    # Pegar todos os dias do mês

    # ! PERGUNTAR MES E ANO NO COMEÇO DO PROGRAMA

    dias_por_mes = calendar.monthrange(ano, mes)[1]
    lista_dias = [datetime.date(ano, mes, dia) for dia in range(1, dias_por_mes + 1)]

    segunda_quarta_sexta = {}
    terca_quinta_sabado = {}

    for dia in lista_dias:

        if dia.weekday() == 0:
            segunda_quarta_sexta[dia.strftime('%d/%m/%Y')] = 'seg'
        elif dia.weekday() == 1:
            terca_quinta_sabado[dia.strftime('%d/%m/%Y')] = 'ter'
        elif dia.weekday() == 2:
            segunda_quarta_sexta[dia.strftime('%d/%m/%Y')] = 'qua'
        elif dia.weekday() == 3:
            terca_quinta_sabado[dia.strftime('%d/%m/%Y')] = 'qui'
        elif dia.weekday() == 4:
            segunda_quarta_sexta[dia.strftime('%d/%m/%Y')] = 'sex'
        elif dia.weekday() == 5:
            terca_quinta_sabado[dia.strftime('%d/%m/%Y')] = 'sab'

    return [segunda_quarta_sexta, terca_quinta_sabado]