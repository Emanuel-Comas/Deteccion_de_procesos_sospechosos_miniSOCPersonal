import psutil
import csv
from datetime import datetime
import time
from colorama import Fore, Style, init
import smtplib
from email.message import EmailMessage
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

# Inicializar colorama.
init(autoreset=True)

# Configuraciónes
# Lista de procesos considerados sospechosos.
suspiciousProcesses = [
    "cmd.exe",
    "powershell.exe",
    "python.exe",
    "python3",
    "notepad.exe"
]

# Email de alerta.
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_SERVER = os.getenv("EMAIL_SERVER")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
# Tiempo de repetición.
TIEMPO_ESPERA = int(os.getenv("TIEMPO_ESPERA", 300))


# Funciónes.
# Envia un correo con los procesos sospechosos.
def enviar_alerta_email(procesosSospechosos):
    if not procesosSospechosos:
        # No hay alerta, no se envia nada.
        return
    
    msg = EmailMessage()
    msg['Subject'] = 'Alerta Procesos Sospechosos'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    
    contenido = "Procesos sospechosos detectados: \n\n"
    for p in procesosSospechosos:
        contenido += f"{p['pid']} - {p['name']} - {p['status']}\n"

    msg.set_content(contenido)

    try:
        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(Fore.GREEN + "Email de alerta eviando correctamente.")
    except Exception as e:
        print(Fore.RED + f"No se pudo enviar el email: {e}")


def graficarProcesos(procesos_sospechosos, total_procesos):
    try:

        # Crea un gráfico de pastel con porcentaje de procesos sospechosos.
        sospechosos = len(procesos_sospechosos)
        normales = total_procesos - sospechosos
        etiquetas = ["Normales", "Sospechosos"]
        valores = [normales, sospechosos]

        plt.figure(figsize=(5,5))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', colors=['green','red'])
        plt.title("Distribución de procesos")
        plt.show()
    except Exception as e:
        print(Fore.RED + f"No se pudo generar el gráfico: {e}")


# Función principal para monitorear procesos, guardar CSVs, imprimir alertas, 
# enviar email y generar estadisticas.
def monitoriear_procesos():
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    procesos_sospechosos = []
    total_procesos = 0

    # Archivo csv para guardar los resultados.
    with open("procesos_todos.csv", mode="w", newline="") as file_todos, \
         open("procesos_alertas.csv", mode="w", newline="") as file_alertas:
        
        writer_todos = csv.writer(file_todos)
        writer_alertas = csv.writer(file_alertas)
        
        # Encabezados
        writer_todos.writerow(["FechaHora","PID","Nombre del proceso","Estado","Alerta"])
        writer_alertas.writerow(["FechaHora","PID","Nombre del proceso","Estado","Alerta"])
        
        # Iterar sobre procesos
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                pid = proc.info['pid']
                name = proc.info['name'] or ""
                status = proc.info['status']
                total_procesos += 1
                
                # Detección por substring
                alerta = "Normal"
                if any(s in name.lower() for s in suspiciousProcesses):
                    alerta = "Sospechoso"
                    procesos_sospechosos.append({'pid': pid, 'name': name, 'status': status})
                    print(Fore.RED + f"[ALERTA] {name} (PID: {pid})")
                else:
                    print(Fore.GREEN + f"{name} (PID: {pid}) - Normal")
                
                # Guardar en CSVs
                writer_todos.writerow([fecha_hora, pid, name, status, alerta])
                if alerta == "Sospechoso":
                    writer_alertas.writerow([fecha_hora, pid, name, status, alerta])
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    # Estadisticas.
    print(Style.BRIGHT + f"\nTotal procesos: {total_procesos}")
    print(Style.BRIGHT + f"\nProcesos sospechosos: {len(procesos_sospechosos)}")
    porcentaje = (len(procesos_sospechosos) / total_procesos) *100 if total_procesos else 0
    print(Style.BRIGHT + f"\nPorcentaje sospechoso: {porcentaje:.2f}%\n")

    # Graficación
    graficarProcesos(procesos_sospechosos, total_procesos)

    # Enviar alertas
    enviar_alerta_email(procesos_sospechosos)


if __name__ == "__main__":
    try:
        while True:
            monitoriear_procesos()
            print(f"Esperando {TIEMPO_ESPERA} segundos para la siguiente revisión... \n")
            time.sleep(TIEMPO_ESPERA)
    # Se evita la salida por consola fea al hacer 'Ctrl + c'
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario, todos los archivos y recursos se cerraron correctamente.")

print("Analisis completado, resultados guardados en 'procesos_sospechosos.csv")