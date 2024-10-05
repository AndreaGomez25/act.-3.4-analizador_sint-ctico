import tkinter as tk
from tkinter import filedialog

def abrir_archivo():
    # Usar filedialog para abrir un archivo
    ruta_archivo = filedialog.askopenfilename(
        title="Abrir archivo",
        filetypes=(("Archivos de texto", ".txt"), ("Todos los archivos", ".*"))
    )
    
    if ruta_archivo:
        # Si se selecciona un archivo, abrirlo y leer su contenido
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            area_texto_izquierda.delete("1.0", tk.END)  # Limpiar el área de texto
            area_texto_izquierda.insert(tk.END, contenido)  # Insertar el contenido en el área de texto

# Diccionarios para clasificar los tokens
palabras_reservadas = ["programa", "int", "read", "printf", "end"]
simbolos = {"(": "<Paréntesis de apertura>", ")": "<Paréntesis de cierre>", "{": "<Llave de apertura>", "}": "<Llave de cierre>", ";": "<Punto y coma>", "+": "<Suma>"}

def analizar_lexico():
    # Obtener el código de la área de texto
    codigo = area_texto_izquierda.get("1.0", tk.END).strip()  # Obtener todo el código
    
    # Dividir el código en líneas
    lineas = codigo.splitlines()
    
    resultado_analisis = ""
    
    # Analizar cada línea
    for numero_linea, linea in enumerate(lineas, start=1):
        tokens = separar_tokens(linea)  # Dividir la línea en tokens
        
        # Construir el análisis por línea
        resultado_analisis += f"LÍNEA {numero_linea}\n"
        for token in tokens:
            clasificacion = clasificar_token(token)
            resultado_analisis += f"{clasificacion: <20} {token}\n"
        resultado_analisis += "\n"  # Espacio entre líneas
    
    # Mostrar el resultado del análisis en el área de texto derecha
    area_texto_derecha.delete("1.0", tk.END)
    area_texto_derecha.insert(tk.END, resultado_analisis)

    # Analizar sintácticamente
    analizar_sintactico(codigo)

def separar_tokens(linea):
    # Reemplazar símbolos comunes por espacios para que se dividan también
    for simbolo in simbolos:
        linea = linea.replace(simbolo, f' {simbolo} ')
    
    # Dividir la línea por espacios para obtener los tokens
    tokens = linea.split()
    return tokens

def clasificar_token(token):
    # Clasificar cada token
    if token in palabras_reservadas:
        return f"<Palabra reservada: {token}>"
    elif token in simbolos:
        return simbolos[token]
    elif token.isidentifier():
        return "<Identificador>"
    elif token.isdigit():
        return "<Número>"
    return "<Desconocido>"

def analizar_sintactico(codigo):
    # Verificación de la estructura sintáctica básica
    lineas = codigo.splitlines()
    errores = []

    # Comprobamos si el código sigue la estructura básica
    if len(lineas) < 6:
        errores.append("Error: Código demasiado corto.")
    
    if not lineas[0].strip() == "programa suma ( ) {":
        errores.append("Error: Se esperaba 'programa suma ( ) {' en la línea 1.")
    if not lineas[1].strip() == "int":
        errores.append("Error: Se esperaba 'int' en la línea 2.")
    if not lineas[2].strip() == "read a ;":
        errores.append("Error: Se esperaba 'read a ;' en la línea 3.")
    if not lineas[3].strip() == "read b ;":
        errores.append("Error: Se esperaba 'read b ;' en la línea 4.")
    if not lineas[4].strip() == "c = a + b ;":
        errores.append("Error: Se esperaba 'c = a + b ;' en la línea 5.")
    if not lineas[5].strip() == 'printf ( "la suma es" );':
        errores.append('Error: Se esperaba \'printf ( "la suma es" );\' en la línea 6.')
    if not lineas[6].strip() == "end ;":
        errores.append("Error: Se esperaba 'end ;' en la última línea.")
    
    # Mostrar el resultado del análisis sintáctico en el área de texto de sintáctico
    area_texto_sintactico.delete("1.0", tk.END)
    if errores:
        resultado_sintactico = "ANÁLISIS SINTÁCTICO\n" + "\n".join(errores)
    else:
        resultado_sintactico = "ANÁLISIS SINTÁCTICO\nEl código está correcto."
    
    area_texto_sintactico.insert(tk.END, resultado_sintactico)

def limpiar():
    area_texto_izquierda.delete("1.0", tk.END)
    area_texto_derecha.delete("1.0", tk.END)
    area_texto_sintactico.delete("1.0", tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador Léxico y Sintáctico")

# Crear las áreas de texto
area_texto_izquierda = tk.Text(ventana, height=20, width=40)
area_texto_derecha = tk.Text(ventana, height=20, width=40)
area_texto_sintactico = tk.Text(ventana, height=20, width=40)

# Crear los botones
boton_analizar = tk.Button(ventana, text="Analizar", command=analizar_lexico)
boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar)

# Empaquetar los elementos en la ventana
area_texto_izquierda.pack(side=tk.LEFT)
area_texto_derecha.pack(side=tk.RIGHT)
area_texto_sintactico.pack(side=tk.BOTTOM)  # Añadir el área de texto de análisis sintáctico

boton_analizar.pack()
boton_limpiar.pack()

# Iniciar la aplicación
ventana.mainloop()
