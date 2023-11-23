import serial
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mysql.connector
import datetime
from scipy.optimize import curve_fit

#Global
base_usuarios = []
datos_canal1 = []
datos_canal2 = []

# Función para encender/apagar el canal 1
def toggle_channel1():
    calcular_temperatura(datos_canal1,'Canal 1')
    
# Función para encender/apagar el canal 2
def toggle_channel2():
    calcular_temperatura(datos_canal2,'Canal 2')

## Función para trazar los datos de voltaje en el gráfico
#def plot_data(data_buffer,canal):
#    ax.clear()
#    
#    ax.plot(range(len(data_buffer)), data_buffer, label=canal)
#
#    ax.set_xlabel('Tiempo (s)')
#    ax.set_ylabel('Voltaje (V)')
#    ax.legend()
#    canvas.draw()
#    
#    # Pasar al calculo de tempratura tambien
#    #calcular_temperatura(data_buffer,canal)

# Definir la ecuación diferencial de la Ley de Newton de enfriamiento
def newton_cooling(t, T, T_inf, k):
    return k * (T - T_inf)

# Función para trazar los datos de temperatura en el gráfico    
def calcular_temperatura(data_buffer,canal):
    data_temp = []
    ax.clear()
    
    # la relacion es 10mV/°C
    #Conversion de voltaje a temperatura
    for d in data_buffer:
        valorTemp = d/0.01
        #print("Valor temp", valorTemp)
        data_temp.append(valorTemp)

    ax.plot(range(len(data_temp)), data_temp, label=canal)

    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Temperatura (°C)')
    ax.legend()
    canvas.draw()
    
    # Ajustar la curva a los datos experimentales
    params, covariance = curve_fit(newton_cooling,range(len(data_temp)), data_temp)

    # Obtener los parámetros ajustados, incluido el valor de k
    var_k = params[0]
    T_inf = params[1]
    #print(f"Valor de k: {var_k}")

    # Mostrar informacion sobre la temperatura
    var_k_str = "3.Valor de K = " + str(var_k)

    Temp_frame = ttk.LabelFrame(root, text="Calculos de temperatura")
    Temp_frame.grid(row=2, column=2, columnspan=2, sticky='nsew')

    instTemp1 = ttk.Label(Temp_frame, text="1.Fórmula: dT/dt = k(T-Tam)")
    instTemp2 = ttk.Label(Temp_frame, text="2.Tam = Temperatural ambiental")
    instTemp3 = ttk.Label(Temp_frame, text=var_k_str)

    instTemp1.pack()
    instTemp2.pack()
    instTemp3.pack()

def leer_base_de_datos():
    numero_usuario = var.get() # Obtener el numero del usuario en los radio buttons
    nombre_usuario = base_usuarios[numero_usuario - 1] # Obtener el nombre del usuario
    print(f"Nombre del usuario: {nombre_usuario[0]}")
    
    # Limpia las listas
    datos_canal1.clear()
    datos_canal2.clear()

    # Extraer datos de la tabla
    cursor.execute("SELECT * FROM datos WHERE Nombre_Usuario = %s", (nombre_usuario))
    
    # Recuperar todos los resultados en una lista de tuplas
    resultados = cursor.fetchall()

    # Imprimir los resultados en consola
    for fila in resultados:
        #print(f"Nombre_Usuario: {fila[0]}, Fecha: {fila[1]}, Canal: {fila[2]}, Unidades_Fisicas: {fila[3]}, Vector_Datos: {fila[4]}")
        if fila[2] == 1:
            datos_canal1.append(fila[4])
        elif fila[2] == 2:
            datos_canal2.append(fila[4])
    
    #for i in datos_canal1:
    #    print(f"Valor en canal 1: ",i)
        
    #for i in datos_canal2:
    #    print(f"Valor en canal 2: ",i)

    # Guardar cambios
    conn.commit()
    #print("Datos leidos")

def cargar_Usuarios():
    # Extraer datos de la tabla
    cursor.execute("SELECT Nombre_Usuario FROM datos")
    
    # Recuperar todos los resultados en una lista de tuplas
    base_usuarios_Completa = cursor.fetchall()
    
    for i in range(len(base_usuarios_Completa)):
        if base_usuarios_Completa[i] != base_usuarios_Completa[i-1]:
            base_usuarios.append(base_usuarios_Completa[i])
        
    # Crear los radio buttons de los usuarios
    for cont,u in enumerate(base_usuarios):
        radio_button = tk.Radiobutton(usuarios_frame, text=u, variable=var, value=cont+1)
        radio_button.pack()

    # Guardar cambios
    conn.commit()
    

# Configura la ventana principal
root = tk.Tk()
root.title('Calculo de temperatura y constante K')
root.geometry('1000x700')

# Configura el gráfico y lo coloca a la izquierda en la parte superior
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Variable para almacenar el valor seleccionado
var = tk.IntVar()

# Crear radio botones para los usuarios con datos
instrucciones_frame = ttk.LabelFrame(root, text="Instrucciones")
instrucciones_frame.grid(row=0, column=2, columnspan=2, sticky='nsew')

inst1 = ttk.Label(instrucciones_frame, text="1.Cargue los usuarios")
inst2 = ttk.Label(instrucciones_frame, text="2.Extraiga los datos")
inst3 = ttk.Label(instrucciones_frame, text="3.Seleccione el canal")

inst1.pack()
inst2.pack()
inst3.pack()

# Configura los botones para escoger el canal
channel1_button = tk.Button(root, text="Canal 1", command=toggle_channel1)
channel1_button.grid(row=0, column=4, padx=10, pady=10)

channel2_button = tk.Button(root, text="Canal 2", command=toggle_channel2)
channel2_button.grid(row=0, column=5, padx=10, pady=10)

# Crear radio botones para los usuarios con datos
usuarios_frame = ttk.LabelFrame(root, text="Usuarios")
usuarios_frame.grid(row=1, column=0, sticky='nsew')

# Botón para cargar los usuarios que estan en la base
cargar_usuariosButton = tk.Button(root, text="Cargar usuarios", command=cargar_Usuarios)
cargar_usuariosButton.grid(row=2, column=0, padx=10, pady=10)

# Botón para leer los datos del usuario seleccionado
boton_leer_base_de_datos = tk.Button(root, text="Extraer datos de la base", command=leer_base_de_datos)
boton_leer_base_de_datos.grid(row=3, column=0, padx=10, pady=10)

## Botón para calcular temperatura
#boton_leer_base_de_datos = tk.Button(root, text="Calcular temperatura", command=calcular_temperatura)
#boton_leer_base_de_datos.grid(row=3, column=0, padx=10, pady=10)


# Establecer la conexión
conn = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="ti1234",
    database="ti_g2"
)
cursor = conn.cursor()

# Configura el sistema de cuadrícula para expandir correctamente los elementos
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Inicializa las variables de estado de los canales
plot_channel1 = True
plot_channel2 = True


root.mainloop()






