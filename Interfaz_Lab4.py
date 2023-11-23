import serial
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mysql.connector
import datetime
import subprocess


arduino_port = 'COM5'  
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

def ejecutar_python2():
    # Coloca aquí el código que deseas ejecutar antes de abrir la otra ventana o solo ejecutar un script externo
    subprocess.Popen(["python", "Calculo_Temperatura_k.py"])

# Función para enviar el número seleccionado al Arduino
def enviar_numero():
    valor = var.get()
    if valor <= 7:
        comando = str(valor)
    else:
        comando = chr(96 + valor - 7)  # Convierte el número a la letra correspondiente
    ser.write(comando.encode() + b'\n')

# Función para actualizar los datos desde Arduino
def update_data():
    while ser.in_waiting > 0:
        data = ser.readline().decode().strip().split(',')
        if len(data) == 2:
            try:
                data = [float(val) for val in data]  # Lee valores decimales
                if len(data_buffer) >= 50:
                    data_buffer.pop(0)
                data_buffer.append(data)
            except ValueError:
                pass
    plot_data()
    root.after(200, update_data)  

# Función para encender/apagar el canal 1
def toggle_channel1():
    global plot_channel1
    plot_channel1 = not plot_channel1
    plot_data()

# Función para encender/apagar el canal 2
def toggle_channel2():
    global plot_channel2
    plot_channel2 = not plot_channel2
    plot_data()

# Función para trazar los datos en el gráfico
def plot_data():
    ax.clear()
    if plot_channel1:
        ax.plot(range(len(data_buffer)), [d[0] for d in data_buffer], label='Canal 1')
    if plot_channel2:
        ax.plot(range(len(data_buffer)), [d[1] for d in data_buffer], label='Canal 2')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Voltaje (V)')
    ax.legend()
    canvas.draw()

# Función para agregar datos a la base de datos SQLite
def agregar_a_base_de_datos():
    
    cursor = conn.cursor()

    # Crear una tabla
    cursor.execute('''CREATE TABLE IF NOT EXISTS datos (Nombre_Usuario VARCHAR(255), Fecha DATE, Canal INT, Unidades_Fisicas VARCHAR(255), Vector_Datos DOUBLE)''')
    
    nombre_usuario = nombre_usuario_entry.get()  # Obtener el nombre del usuario
    print(f"Nombre del usuario: {nombre_usuario}")
    
    # Extraer la fecha 
    fecha_actual = datetime.date.today()

    for data in data_buffer:
        # Insertar datos
        cursor.execute("INSERT INTO datos (Nombre_Usuario, Fecha, Canal, Unidades_Fisicas, Vector_Datos) VALUES (%s, %s, %s, %s, %s)", (nombre_usuario, fecha_actual, 1, 'Voltios(V)', data[0]))
        
        cursor.execute("INSERT INTO datos (Nombre_Usuario, Fecha, Canal, Unidades_Fisicas, Vector_Datos) VALUES (%s, %s, %s, %s, %s)", (nombre_usuario, fecha_actual, 2, 'Voltios(V)', data[1]))
        
    # Guardar cambios
    conn.commit()
    print("Datos agregados")


# Configura la ventana principal
root = tk.Tk()
root.title('Control y Visualización en Tiempo Real de Arduino')
root.geometry('1000x700')

# Configura el gráfico y lo coloca a la izquierda en la parte superior
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
data_buffer = []

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Variable para almacenar el valor seleccionado
var = tk.IntVar()

# Cuadro de entrada de texto para el nombre de usuario
nombre_usuario_label = ttk.Label(root, text="Nombre de Usuario:")
nombre_usuario_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
nombre_usuario_entry = ttk.Entry(root)
nombre_usuario_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

# Crear radio botones para el canal 1 a la derecha del gráfico
canal1_frame = ttk.LabelFrame(root, text="Control de Canal 1")
canal1_frame.grid(row=0, column=2, padx=10, pady=10, rowspan=2, sticky='nsew')

radio_button1 = tk.Radiobutton(canal1_frame, text="Atenuación 1", variable=var, value=1)
radio_button2 = tk.Radiobutton(canal1_frame, text="Atenuación 2", variable=var, value=2)
radio_button3 = tk.Radiobutton(canal1_frame, text="Atenuación 3", variable=var, value=3)
radio_button4 = tk.Radiobutton(canal1_frame, text="Seguidor", variable=var, value=4)
radio_button5 = tk.Radiobutton(canal1_frame, text="Ganancia 1", variable=var, value=5)
radio_button6 = tk.Radiobutton(canal1_frame, text="Ganancia 2", variable=var, value=6)
radio_button7 = tk.Radiobutton(canal1_frame, text="Ganancia 3", variable=var, value=7)

radio_button1.pack()
radio_button2.pack()
radio_button3.pack()
radio_button4.pack()
radio_button5.pack()
radio_button6.pack()
radio_button7.pack()

# Crear radio botones para el canal 2 a la derecha de los del canal 1
canal2_frame = ttk.LabelFrame(root, text="Control de Canal 2")
canal2_frame.grid(row=0, column=3, padx=10, pady=10, rowspan=2, sticky='nsew')

radio_button_a = tk.Radiobutton(canal2_frame, text="Atenuación 1", variable=var, value=8)
radio_button_b = tk.Radiobutton(canal2_frame, text="Atenuación 2", variable=var, value=9)
radio_button_c = tk.Radiobutton(canal2_frame, text="Atenuación 3", variable=var, value=10)
radio_button_d = tk.Radiobutton(canal2_frame, text="Seguidor", variable=var, value=11)
radio_button_e = tk.Radiobutton(canal2_frame, text="Ganancia 1", variable=var, value=12)
radio_button_f = tk.Radiobutton(canal2_frame, text="Ganancia 2", variable=var, value=13)
radio_button_g = tk.Radiobutton(canal2_frame, text="Ganancia 3", variable=var, value=14)

radio_button_a.pack()
radio_button_b.pack()
radio_button_c.pack()
radio_button_d.pack()
radio_button_e.pack()
radio_button_f.pack()
radio_button_g.pack()

# Configura los botones de encendido/apagado debajo del gráfico
channel1_button = tk.Button(root, text="Canal 1", command=toggle_channel1)
channel1_button.grid(row=2, column=0, padx=10, pady=10)

channel2_button = tk.Button(root, text="Canal 2", command=toggle_channel2)
channel2_button.grid(row=2, column=1, padx=10, pady=10)

# Botón para enviar el valor seleccionado al Arduino al lado abajo de los radio botones
enviar_button = tk.Button(root, text="Enviar", command=enviar_numero)
enviar_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky='nsew')

# Establecer la conexión
conn = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="ti1234",
    database="ti_g2"
)
#cursor = conn.cursor()

# Botón para agregar datos a la base de datos al lado abajo del botón de enviar
boton_agregar_a_base_de_datos = tk.Button(root, text="Agregar a la Base de Datos", command=agregar_a_base_de_datos)
boton_agregar_a_base_de_datos.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

# Boton para ejecutar codigo externo
boton = tk.Button(root, text="Calculo temperatura", command=ejecutar_python2)
boton.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')

# Configura el sistema de cuadrícula para expandir correctamente los elementos
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Inicializa las variables de estado de los canales
plot_channel1 = True
plot_channel2 = True

# Inicia la actualización de datos
update_data()

# Cierra el puerto serie al cerrar la ventana
def close_serial_port():
    ser.close()
    root.destroy()

root.protocol('WM_DELETE_WINDOW', close_serial_port)

root.mainloop()






