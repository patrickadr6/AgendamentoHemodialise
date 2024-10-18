from datetime import datetime

def horario_atual():
    current_time = datetime.now()

    horario = f"({current_time.day}/{current_time.month}/{current_time.year} {current_time.hour}:{current_time.minute})"

    return horario
