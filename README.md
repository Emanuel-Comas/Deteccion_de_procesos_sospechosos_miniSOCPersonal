# Monitoreo de Procesos Sospechosos en Python

Este proyecto es un **sistema de monitoreo de procesos en Windows** que detecta procesos sospechosos, genera estadísticas, guarda registros en CSV y envía alertas por correo electrónico.

---

## 🔹 Funcionalidades principales

1. **Monitoreo de procesos activos**  
   - Detecta todos los procesos en ejecución usando `psutil`.
   - Clasifica los procesos como **Normal** o **Sospechoso** según una lista configurable.

2. **Registro en CSV**  
   - Todos los procesos se registran en `procesos_todos.csv`.
   - Los procesos sospechosos también se registran en `procesos_alertas.csv`.
   - Cada registro incluye:  
     `FechaHora | PID | Nombre del proceso | Estado | Alerta`

3. **Alerta por correo electrónico**  
   - Si se detectan procesos sospechosos, se envía un correo al destinatario configurado.
   - Compatible con Gmail usando **token de aplicación** como contraseña (recomendado).

4. **Gráficos de distribución de procesos**  
   - Genera un gráfico circular (`pie chart`) mostrando la proporción de procesos normales vs sospechosos.
   - Se muestra al usuario al finalizar el escaneo de procesos.
   - Al cerrar el gráfico se envia un correo al destinatario con los detalles de las alertas de procesos.

5. **Configuración con `.env`**  
   - Datos sensibles (correo, contraseña, servidor, puerto) se cargan desde un archivo `.env`.
   - Ejemplo de `.env`:
     ```
     EMAIL_SENDER=tu_email@gmail.com
     EMAIL_PASSWORD=tu_token
     EMAIL_RECEIVER=destino@gmail.com
     EMAIL_SERVER=smtp.gmail.com
     EMAIL_PORT=587
     TIEMPO_ESPERA=300
     ```

6. **Ejecución continua**  
   - Monitorea los procesos en un bucle infinito con tiempo de espera configurable.
   - Permite detenerse de manera segura con `Ctrl + C` sin errores de consola.

7. **Manejo de errores**  
   - Ignora procesos inaccesibles o eliminados.
   - Maneja errores de envío de correo y problemas de gráficos.

---

## 🔹 Requisitos

- Python 3.8 o superior
- Librerías necesarias:

```bash
pip install psutil colorama matplotlib python-dotenv
```

## 🔹 Uso

    1 - Crear un archivo .env en el mismo directorio que el script con la configuración de correo y tiempo de espera.

    2 - Ejecutar el script:

        python main.py

    3 - Cada TIEMPO_ESPERA segundos:

            -- Escanea los procesos.

            -- Guarda registros en CSV.

            -- Muestra un gráfico de distribución de procesos.

            -- Envía correos si detecta procesos sospechosos (Despues de cerrar el gráfico).

    4 - Para detener el programa de forma segura, presiona Ctrl + C.


## 🔹 Notas importantes

    Token de Gmail: Se recomienda usar un token de aplicación en lugar de la contraseña normal de Gmail.

    CSV: Cada ejecución sobrescribe los archivos procesos_todos.csv y procesos_alertas.csv.

    Gráficos: Mostrar gráficos en ventana puede bloquear la ejecución en bucle; se recomienda cerrarlos manualmente para que continúe el siguiente ciclo de monitoreo.

    Compatibilidad: El script está pensado para Windows, aunque puede funcionar en Linux o Mac con ajustes menores en los nombres de procesos y rutas.


## 🔹 Ejemplo de salida por consola 

    [ALERTA] cmd.exe (PID: 1234)
    python.exe (PID: 5678) - Normal
    Total procesos: 10
    Procesos sospechosos: 2
    Porcentaje sospechoso: 20.00%
    Esperando 300 segundos para la siguiente revisión...


## 🔹 Archivos generados

    procesos_todos.csv → Registro completo de todos los procesos.

    procesos_alertas.csv → Registro exclusivo de procesos sospechosos.