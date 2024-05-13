"""
INGREDIENTES /// NADA
PLATOS /// INGRESAR

SI MODIFICAS UNA RECETA, AUTOMATIZAR QUE SE CAMBIEN LOS COSTOS DE TODOS LOS PLATOS QUE LA TENGAN
manejo de stock 

ingresar ingredientes, detalles 
ARREGLAR BIEN LA OPCION DE PLATOS 
MODIFICAR RECETAS error

tabla de unidades lista pero todavia no implementada

te tiene que mostrar una lista de cuales son los ingredientes y que cantidad llevan, puede ser mediante un text

PRECIOX UNIDAD
configurar el .geometry en todas las ventanas
HACER Manual D3E USO (OTRA FUNCION)
AGREGAR LOGO DE LA EMPRESA
HACERLO. EXE
"""


def Unidades_medida():
    opciones_unidades = ["Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)",
                         "Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
                         "Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
                         "Cucharaditas (tsp)", "Tazas (cup)"]

    def convertir():
        unidad_origen = combo_origen.get()
        unidad_destino = combo_destino.get()
        cantidad = float(entrada_cantidad.get())
        unidades_solidas = ["Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)"]
        unidades_liquidas = ["Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
                             "Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
                             "Cucharaditas (tsp)", "Tazas (cup)"]

        if unidad_origen in unidades_solidas and unidad_destino in unidades_solidas:
            resultado = cantidad
        elif unidad_origen in unidades_liquidas and unidad_destino in unidades_liquidas:
            resultado = cantidad
        else:
            resultado = "No se puede convertir entre unidades sólidas y líquidas."

        label_resultado.config(text=str(resultado))

        # Agregar botón para copiar el resultado al portapapeles
        #boton_copiar = ttk.Button(ventana, text="Copiar", command=lambda: pyperclip.copy(str(resultado)))
        #boton_copiar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    ventana = tk.Tk()
    ventana.title("Calculadora de Conversiones")
    label_cantidad = ttk.Label(ventana, text="Cantidad:")
    label_cantidad.grid(row=0, column=0, padx=5, pady=5)
    entrada_cantidad = ttk.Entry(ventana)
    entrada_cantidad.grid(row=0, column=1, padx=5, pady=5)
    label_origen = ttk.Label(ventana, text="Unidad Origen:")
    label_origen.grid(row=1, column=0, padx=5, pady=5)
    combo_origen = ttk.Combobox(ventana, values=opciones_unidades)
    combo_origen.grid(row=1, column=1, padx=5, pady=5)
    label_destino = ttk.Label(ventana, text="Unidad Destino:")
    label_destino.grid(row=2, column=0, padx=5, pady=5)
    combo_destino = ttk.Combobox(ventana, values=opciones_unidades)
    combo_destino.grid(row=2, column=1, padx=5, pady=5)
    boton_convertir = ttk.Button(ventana, text="Convertir", command=convertir)
    boton_convertir.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    label_resultado = ttk.Label(ventana, text="")
    label_resultado.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    ventana.mainloop()

def validar_opcion(opcion_n): #Funcion que valida las opciones
	try:
		if opcion_n < 0 or opcion_n > 4:
			print("El valor ingresado no es valido. ","\n","-"*15)
	except:
		print("Valor incorrecto, Ingrese nuevamente...", "\n", "-"*15)
def cambiar_otro(Cambot): #Preguntar si quiere modificar otro dato
	while True:
		if Cambot.upper() == "S" or Cambot.upper() == "SI":
			break
		else:
			while True:
				if Cambot.upper() == "S" or Cambot.upper() == "SI":
					break
				break
			break


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from pyperclip import *

base = sqlite3.connect('sistema.db')
cursor = base.cursor()
#---------------------------------------- I N G R E D I E N T E S 
def ingresar_ingredientes():
    ventana_ingrediente = tk.Toplevel()
    ventana_ingrediente.title("Ingresar Ingrediente")
    opciones_unidades = ["Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)",
                         "Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
                         "Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
                         "Cucharaditas (tsp)", "Tazas (cup)"]
    tk.Label(ventana_ingrediente, text="Nombre del ingrediente:").pack()
    entry_nombre = tk.Entry(ventana_ingrediente)
    entry_nombre.pack()
    tk.Label(ventana_ingrediente, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(ventana_ingrediente)
    entry_cantidad.pack()
    tk.Label(ventana_ingrediente, text="Unidad de medida:").pack()
    variable_unidad = tk.StringVar(ventana_ingrediente)
    variable_unidad.set(opciones_unidades[0])  # Configurar la primera opción como la predeterminada
    menu_unidad = tk.OptionMenu(ventana_ingrediente, variable_unidad, *opciones_unidades)
    menu_unidad.pack()
    tk.Label(ventana_ingrediente, text="Precio por unidad:").pack()
    entry_precio = tk.Entry(ventana_ingrediente)
    entry_precio.pack()
    def guardar_ingrediente():
        nombre = entry_nombre.get()
        cantidad = float(entry_cantidad.get())
        unidad = variable_unidad.get()
        precio = float(entry_precio.get())
        cursor.execute("INSERT INTO Ingredientes (Nombre, Unidad_Medida, Cantidad, Precio) VALUES (?, ?, ?, ?)",
                       (nombre, unidad, cantidad, precio))
        base.commit()
        print("¡Ingrediente ingresado correctamente!")
        ventana_ingrediente.destroy()
    tk.Button(ventana_ingrediente, text="Guardar", command=guardar_ingrediente).pack()

def ver_ingredientes():
    cursor.execute("SELECT Codigo_Ingrediente, Nombre, Cantidad, Unidad_Medida, Precio FROM Ingredientes")
    ingredientes = cursor.fetchall()
    ventana = tk.Tk()
    ventana.title("Lista de Ingredientes")
    tabla = ttk.Treeview(ventana, columns=("Código", "Nombre", "Cantidad", "Unidad de Medida", "Precio por Unidad"), show="headings")
    tabla.heading("Código", text="Código")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Unidad de Medida", text="Unidad de Medida")
    tabla.heading("Precio por Unidad", text="Precio por Unidad")
    for ingrediente in ingredientes:
        codigo, nombre, cantidad, unidad, precio = ingrediente
        precio_por_unidad = precio / cantidad  # Calcula el precio por unidad
        tabla.insert("", "end", values=(codigo, nombre, cantidad, unidad, precio_por_unidad))
    tabla.pack(padx=20, pady=20)
    ventana.mainloop()

def sisisi():
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar Ingrediente")
    tk.Label(ventana_modificar, text="Código del ingrediente a modificar:").pack()
    entry_codigo_modificar = tk.Entry(ventana_modificar)
    entry_codigo_modificar.pack()

    def mostrar_detalle_modificar():
        codigo_modificar = int(entry_codigo_modificar.get())
        cursor.execute("SELECT * FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_modificar,))
        resultado_verificacion = cursor.fetchone()
        if not resultado_verificacion:
            tk.messagebox.showerror("Error", "No se encontró ningún ingrediente con ese código.")
        else:
            ventana_detalle = tk.Toplevel()
            ventana_detalle.title("Detalle del Ingrediente")
            tk.Label(ventana_detalle, text=f"Nombre: {resultado_verificacion[1]}").pack()
            tk.Label(ventana_detalle, text=f"Cantidad: {resultado_verificacion[3]}").pack()
            tk.Label(ventana_detalle, text=f"Unidad de Medida: {resultado_verificacion[2]}").pack()
            tk.Label(ventana_detalle, text=f"Precio: {resultado_verificacion[4]}").pack()
            opciones_modificar = ["Nombre", "Cantidad", "Unidad de Medida", "Precio", "Todos"]
            variable_opcion_modificar = tk.StringVar(ventana_detalle)
            variable_opcion_modificar.set(opciones_modificar[0])  # Valor predeterminado
            option_menu_modificar = tk.OptionMenu(ventana_detalle, variable_opcion_modificar, *opciones_modificar)
            option_menu_modificar.pack()
            entry_nuevo_valor = tk.Entry(ventana_detalle)
            entry_nuevo_valor.pack()

            def confirmar_modificacion():
                opcion_modificar = variable_opcion_modificar.get()
                nuevo_valor = entry_nuevo_valor.get()
                if opcion_modificar == "Unidad de Medida":
                    opciones_unidades = ["Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)",
                                         "Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
                                         "Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
                                         "Cucharaditas (tsp)", "Tazas (cup)"]
                    entry_nuevo_valor.destroy()
                    nueva_unidad = tk.StringVar(ventana_detalle)
                    nueva_unidad.set(resultado_verificacion[3])  # Establecer el valor actual como predeterminado
                    menu_unidades = tk.OptionMenu(ventana_detalle, nueva_unidad, *opciones_unidades)
                    menu_unidades.pack()
                else:
                    entry_nuevo_valor.delete(0, tk.END)
                    entry_nuevo_valor.insert(0, resultado_verificacion[opciones_modificar.index(opcion_modificar) + 1])
                def guardar_modificacion():
                    if opcion_modificar == "Todos":
                        campos = ["Nombre", "Cantidad", "Unidad_Medida", "Precio"]
                        for campo in campos:
                            cursor.execute(f"UPDATE Ingredientes SET {campo} = ? WHERE Codigo_Ingrediente = ?",
                                           (nuevo_valor, codigo_modificar))
                    else:
                        cursor.execute(f"UPDATE Ingredientes SET {opcion_modificar} = ? WHERE Codigo_Ingrediente = ?",
                                       (nuevo_valor, codigo_modificar))
                    base.commit()
                    tk.messagebox.showinfo("Éxito", f"Se ha modificado el valor del campo {opcion_modificar}.")
                    ventana_detalle.destroy()
                boton_confirmar = tk.Button(ventana_detalle, text="Confirmar", command=guardar_modificacion)
                boton_confirmar.pack()
            boton_guardar_cambios = tk.Button(ventana_detalle, text="Guardar Cambios", command=confirmar_modificacion)
            boton_guardar_cambios.pack()
    tk.Button(ventana_modificar, text="Mostrar Detalle", command=mostrar_detalle_modificar).pack()
def eliminar_ingredientes():
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Ingrediente")
    tk.Label(ventana_eliminar, text="Código del ingrediente a eliminar:").pack()
    entry_codigo_eliminar = tk.Entry(ventana_eliminar)
    entry_codigo_eliminar.pack()
    def confirmar_eliminacion():
        codigo_eliminar = int(entry_codigo_eliminar.get())
        cursor.execute("DELETE FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_eliminar,))
        base.commit()
        tk.messagebox.showinfo("Éxito", "El ingrediente ha sido eliminado correctamente.")
        ventana_eliminar.destroy()
    boton_confirmar_eliminacion = tk.Button(ventana_eliminar, text="Confirmar Eliminación", command=confirmar_eliminacion)
    boton_confirmar_eliminacion.pack()



#-------------------------------------------------------------------------
def ingresar_receta(cursor, base):
    ingredientes_receta = []
    def calcular_costo_total(ingredientes_receta):
        costo_total = 0
        for nombre, cantidad in ingredientes_receta:
            cursor.execute("SELECT Precio FROM Ingredientes WHERE Nombre = ?", (nombre,))
            precio_ingrediente = cursor.fetchone()[0]
            costo_ingrediente = precio_ingrediente * cantidad
            costo_total += costo_ingrediente
        return costo_total
    def agregar_ingrediente():
        codigo_ingrediente = int(entry_codigo.get())
        cantidad_ingrediente = float(entry_cantidad.get())
        cursor.execute("SELECT Nombre FROM INGREDIENTES WHERE Codigo_Ingrediente = ?", (codigo_ingrediente,))
        nombre_ing = cursor.fetchone()[0]
        ingredientes_receta.append((nombre_ing, cantidad_ingrediente))
        listbox_ingredientes.insert(tk.END, f"{nombre_ing}: {cantidad_ingrediente} {unidad.get()}")
    def guardar_receta():
        nombre_receta = entry_nombre_receta.get()
        if not nombre_receta:
            tk.messagebox.showerror("Error", "Por favor, ingrese el nombre de la receta.")
            return
        if not ingredientes_receta:
            tk.messagebox.showerror("Error", "La receta debe tener al menos un ingrediente.")
            return
        nombre_ingredientes = ", ".join(ingrediente[0] for ingrediente in ingredientes_receta)
        cantidades_ingredientes = ", ".join(str(ingrediente[1]) + " " + unidad.get() for ingrediente in ingredientes_receta)
        costo_total = calcular_costo_total(ingredientes_receta)
        cursor.execute("INSERT INTO Recetas (Nombre, Costo, Codigo_Ingrediente, Cantidad_De_Cada_Ingrediente) VALUES (?, ?, ?, ?)",
                       (nombre_receta, costo_total, nombre_ingredientes, cantidades_ingredientes))
        base.commit()
        tk.messagebox.showinfo("Éxito", "Receta ingresada correctamente.")
    root = tk.Tk()
    root.title("Ingresar Receta")
    tk.Label(root, text="Nombre de la receta:").pack()
    entry_nombre_receta = tk.Entry(root)
    entry_nombre_receta.pack()
    tk.Label(root, text="Código del ingrediente:").pack()
    entry_codigo = tk.Entry(root)
    entry_codigo.pack()
    tk.Label(root, text="Cantidad del ingrediente:").pack()
    entry_cantidad = tk.Entry(root)
    entry_cantidad.pack()
    unidad = tk.StringVar(root)
    unidades = [
        "Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)",
        "Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
        "Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
        "Cucharaditas (tsp)", "Tazas (cup)"
    ]
    unidad.set(unidades[0])
    tk.OptionMenu(root, unidad, *unidades).pack()
    tk.Button(root, text="Agregar Ingrediente", command=agregar_ingrediente).pack()
    listbox_ingredientes = tk.Listbox(root)
    listbox_ingredientes.pack()
    tk.Button(root, text="Guardar Receta", command=guardar_receta).pack()
    root.mainloop()

def obtener_recetas_con_costo():
    try:
        consulta = "SELECT * FROM RECETAS"
        cursor.execute(consulta)
        recetas = cursor.fetchall()
        return recetas
    except Exception as e:
        raise e
    
def mostrar_recetas_con_costo():
    try:
        recetas = obtener_recetas_con_costo()
        if recetas:
            ventana = tk.Tk()
            ventana.title("Recetas y Costo")
            tabla = ttk.Treeview(ventana, columns=("Código Receta", "Nombre Receta", "Costo Receta" ,"Ingredientes"))
            tabla.heading("#0", text="Índice")
            tabla.heading("Código Receta", text="Código Receta")
            tabla.heading("Nombre Receta", text="Nombre Receta")
            tabla.heading("Costo Receta", text="Costo Receta")
            tabla.heading("Ingredientes", text="Ingredientes")            
            tabla.pack(fill="both", expand=True)
            for index, receta in enumerate(recetas, start=1):
                tabla.insert('', 'end', text=str(index), values=receta)
            ventana.mainloop()
        else:
            print("No hay recetas disponibles.")
    except Exception as e:
        print("Error al mostrar recetas con costo:", e)
        
def modificar_receta():
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar Receta")
    tk.Label(ventana_modificar, text="Código de la receta a modificar:").pack()
    entry_codigo_modificar = tk.Entry(ventana_modificar)
    entry_codigo_modificar.pack()
    def mostrar_detalle_modificar():
        codigo_receta = entry_codigo_modificar.get()
        cursor.execute("SELECT * FROM Recetas WHERE Codigo_Receta = ?", (codigo_receta,))
        receta = cursor.fetchone()
        print(f"receta {receta}")
        if receta:
            ventana_detalle = tk.Toplevel()
            ventana_detalle.title("Detalle de la Receta")
            cursor.execute("SELECT Nombre, Cantidad_De_Cada_Ingrediente FROM Recetas WHERE Codigo_Ingrediente IN (SELECT Codigo_Ingrediente FROM Ingredientes)")
            ingredientes = cursor.fetchall()
            detalle_texto = "Ingredientes:\n"
            for ingrediente in ingredientes:
                detalle_texto += f"{ingrediente[0]} - {ingrediente[1]}\n"
            tk.Label(ventana_detalle, text=detalle_texto).pack()
            tk.Label(ventana_detalle, text="Nuevo nombre de la receta:").pack()
            entry_nuevo_nombre = tk.Entry(ventana_detalle)
            entry_nuevo_nombre.pack()
            tk.Label(ventana_detalle, text="Nuevo costo de la receta:").pack()
            entry_nuevo_costo = tk.Entry(ventana_detalle)
            entry_nuevo_costo.pack()
            tk.Label(ventana_detalle, text="Nuevo código de ingrediente:").pack()
            entry_nuevo_codigo_ingrediente = tk.Entry(ventana_detalle)
            entry_nuevo_codigo_ingrediente.pack()
            tk.Label(ventana_detalle, text="Nueva cantidad de cada ingrediente:").pack()
            entry_nueva_cantidad_ingrediente = tk.Entry(ventana_detalle)
            entry_nueva_cantidad_ingrediente.pack()
            def confirmar_modificacion():
                nuevo_nombre = entry_nuevo_nombre.get().strip()
                nuevo_costo = float(entry_nuevo_costo.get().strip()) if entry_nuevo_costo.get().strip() else None
                nuevo_codigo_ingrediente = entry_nuevo_codigo_ingrediente.get().strip()
                nueva_cantidad_ingrediente = float(entry_nueva_cantidad_ingrediente.get().strip()) if entry_nueva_cantidad_ingrediente.get().strip() else None
                if nuevo_nombre:
                    cursor.execute("UPDATE Recetas SET Nombre = ? WHERE Codigo_Receta = ?", (nuevo_nombre, receta[0]))
                if nuevo_costo is not None:
                    cursor.execute("UPDATE Recetas SET Costo = ? WHERE Codigo_Receta = ?", (nuevo_costo, receta[0]))
                if nuevo_codigo_ingrediente:
                    cursor.execute("UPDATE Recetas SET Codigo_Ingrediente = ? WHERE Codigo_Receta = ?", (nuevo_codigo_ingrediente, receta[0]))
                if nueva_cantidad_ingrediente is not None:
                    cursor.execute("UPDATE Recetas SET Cantidad_De_Cada_Ingrediente = ? WHERE Codigo_Receta = ?", (nueva_cantidad_ingrediente, receta[0]))

                base.commit()
                tk.messagebox.showinfo("Éxito", "Receta modificada correctamente.")
                ventana_detalle.destroy()

            tk.Button(ventana_detalle, text="Confirmar", command=confirmar_modificacion).pack()
        else:
            tk.messagebox.showerror("Error", "La receta especificada no existe.")

    tk.Button(ventana_modificar, text="Mostrar Detalle", command=mostrar_detalle_modificar).pack()

def eliminar_receta():
    def confirmar_eliminacion():
        codigo_receta = entry_codigo_eliminar.get()
        cursor.execute("SELECT * FROM Recetas WHERE Codigo_Receta = ?", (codigo_receta,))
        receta = cursor.fetchone()
        if receta:
            confirmacion = tk.messagebox.askyesno("Confirmación", f"¿Está seguro de querer eliminar la receta '{receta[1]}'?")
            if confirmacion:
                cursor.execute("DELETE FROM Recetas WHERE Codigo_Receta = ?", (codigo_receta,))
                base.commit()
                tk.messagebox.showinfo("Éxito", "Receta eliminada correctamente.")
                ventana_eliminar.destroy()
        else:
            tk.messagebox.showerror("Error", "La receta especificada no existe.")

    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Receta")

    tk.Label(ventana_eliminar, text="Código de la receta a eliminar:").pack()
    entry_codigo_eliminar = tk.Entry(ventana_eliminar)
    entry_codigo_eliminar.pack()

    tk.Button(ventana_eliminar, text="Confirmar", command=confirmar_eliminacion).pack()

# Función para obtener el precio de un ingrediente por su código
def obtener_precio_ingrediente(codigo_ingrediente):
    cursor.execute("SELECT Precio FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_ingrediente,))
    precio_ingrediente = cursor.fetchone()[0]
    return precio_ingrediente

#................................ P l a t o s 
def ingresar_plato():
    def mostrar_top_label():
        global nombre_receta
        win = tk.Toplevel()
        win.title("Ingrese el nombre de la receta")
        tk.Label(win, text="Ingrese el nombre de la receta asociada al plato:").pack()
        entry_nombre_receta = tk.Entry(win)
        entry_nombre_receta.pack()
        nombre_receta = entry_nombre_receta.get()
        tk.Button(win, text="Confirmar", command=lambda: confirmar_nombre_receta(entry_nombre_receta)).pack()

    def calcular_receta():
        cursor.execute("SELECT Codigo_Ingrediente, Cantidad_De_Cada_Ingrediente FROM Recetas WHERE Nombre = ?", (nombre_receta,))
        ingredientes_receta = cursor.fetchall()
        costo_total = 0
        for codigo_ingrediente, cantidad_ingrediente in ingredientes_receta:
            cursor.execute("SELECT Precio FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_ingrediente,))
            precio_ingrediente = cursor.fetchone()[0]
            costo_total += precio_ingrediente * cantidad_ingrediente
        tk.messagebox.showinfo("Costo de la Receta", f"El costo total de la receta '{nombre_receta}' es: {costo_total}")

    def confirmar_nombre_receta(entry_nombre_receta):
        nombre_receta = entry_nombre_receta.get()
        consulta = """SELECT COSTO FROM RECETAS WHERE NOMBRE = ?"""
        cursor.execute(consulta, (nombre_receta,))
        registro = cursor.fetchone()[0]
        cursor.execute("INSERT INTO PLATOS(PRECIO_FINAL) VALUES (?)", (registro,))
        base.commit()
        tk.messagebox.showinfo("Éxito", "Plato ingresado correctamente.")
    def guardar_plato(entry_nombre, entry_ganancia, implementado_var, veganos_var, vegetarianos_var, celiacos_var):
        nombre = entry_nombre.get()
        ganancia_porcentaje = float(entry_ganancia.get())
        implementado_menu = implementado_var.get()
        apto_veganos = veganos_var.get()
        apto_vegetarianos = vegetarianos_var.get()
        apto_celiacos = celiacos_var.get()

        def calcular_precio():
            respuesta = tk.messagebox.askyesno("Calcular Precio", "¿Desea calcular automáticamente el precio final?")
            if respuesta:
                mostrar_top_label()
            else:
                precio_manual = tk.messagebox.askfloat("Ingresar Precio Manualmente", "Ingrese el precio final del plato:")
                if precio_manual is not None:
                    precio_final = precio_manual

                if precio_final is not None:
                    cursor.execute("INSERT INTO Platos (Nombre, Ganancia, Precio_Final, Implementado_Menu, Apto_Veganos, Apto_Vegetarianos, Apto_Celiacos) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (nombre, ganancia_porcentaje, precio_final, implementado_menu, apto_veganos, apto_vegetarianos, apto_celiacos))
                    base.commit()
                    tk.messagebox.showinfo("Éxito", "Plato ingresado correctamente.")
        
        calcular_precio()

    root = tk.Tk()
    root.title("Ingresar Plato")
    root.geometry("400x200")
    tk.Label(root, text="Nombre del plato:").pack()
    entry_nombre = tk.Entry(root)
    entry_nombre.pack()
    tk.Label(root, text="% Ganancia del plato:").pack()
    entry_ganancia = tk.Entry(root)
    entry_ganancia.pack()
    implementado_var = tk.BooleanVar()
    tk.Checkbutton(root, text="¿Está implementado en el menú?", variable=implementado_var).pack()
    veganos_var = tk.BooleanVar()
    tk.Checkbutton(root, text="¿Es apto para veganos?", variable=veganos_var).pack()
    vegetarianos_var = tk.BooleanVar()
    tk.Checkbutton(root, text="¿Es apto para vegetarianos?", variable=vegetarianos_var).pack()
    celiacos_var = tk.BooleanVar()
    tk.Checkbutton(root, text="¿Es apto para celiacos?", variable=celiacos_var).pack()
    tk.Button(root, text="Guardar", command=lambda: guardar_plato(entry_nombre, entry_ganancia, implementado_var, veganos_var, vegetarianos_var, celiacos_var)).pack()
    tk.Button(root, text="Calcular Precio", command=calcular_receta).pack()  # Llamada a la función calcular_receta
    root.mainloop()

def mostrar_platos_menu():
	cursor.execute("SELECT * FROM Platos")
	platos = cursor.fetchall()

	ventana_platos = tk.Toplevel()
	ventana_platos.title("Platos")

	tabla = ttk.Treeview(ventana_platos, columns=("Nombre", "Ganancia", "Precio Final", "Implementado en Menú", "Apto Veganos", "Apto Vegetarianos", "Apto Celiacos"))
	tabla.heading("#0", text="Índice")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Ganancia", text="Ganancia")
	tabla.heading("Precio Final", text="Precio Final")
	tabla.heading("Implementado en Menú", text="Implementado en Menú")
	tabla.heading("Apto Veganos", text="Apto Veganos")
	tabla.heading("Apto Vegetarianos", text="Apto Vegetarianos")
	tabla.heading("Apto Celiacos", text="Apto Celiacos")

	for index, plato in enumerate(platos, start=1):
		implementado = "Sí" if plato[3] else "No"
		tabla.insert('', 'end', text=str(index), values=(plato[0], plato[1], plato[2], implementado, plato[4], plato[5], plato[6]))

	tabla.pack(fill="both", expand=True)

def modificar_plato():
    def mostrar_detalle_modificar():
        ventana_modificar.title("Modificar Plato")
        tk.Label(ventana_modificar, text="Nombre del plato a modificar:").pack()
        entry_nombre_modificar = tk.Entry(ventana_modificar)
        entry_nombre_modificar.pack()
        def obtener_datos_modificar():
            nombre_plato = entry_nombre_modificar.get()
            cursor.execute("SELECT * FROM Platos WHERE Nombre = ?", (nombre_plato,))
            plato = cursor.fetchone()
            if plato:
                ventana_detalle = tk.Toplevel()
                ventana_detalle.title("Detalle del Plato")
                tk.Label(ventana_detalle, text=f"Nombre: {plato[0]}").pack()
                tk.Label(ventana_detalle, text=f"Ganancia: {plato[1]}").pack()
                tk.Label(ventana_detalle, text=f"Precio Final: {plato[2]}").pack()
                tk.Label(ventana_detalle, text=f"Implementado en Menú: {'Sí' if plato[3] else 'No'}").pack()
                tk.Label(ventana_detalle, text=f"Apto Veganos: {'Sí' if plato[4] else 'No'}").pack()
                tk.Label(ventana_detalle, text=f"Apto Vegetarianos: {'Sí' if plato[5] else 'No'}").pack()
                tk.Label(ventana_detalle, text=f"Apto Celiacos: {'Sí' if plato[6] else 'No'}").pack()
                def modificar_plato():
                    ventana_modificar.title("Modificar Plato")
                    tk.Label(ventana_modificar, text="Nuevo valor para Ganancia:").pack()
                    entry_ganancia = tk.Entry(ventana_modificar)
                    entry_ganancia.pack()
                    tk.Label(ventana_modificar, text="Nuevo valor para Precio Final:").pack()
                    entry_precio = tk.Entry(ventana_modificar)
                    entry_precio.pack()
                    tk.Label(ventana_modificar, text="¿Modificar implementación en menú? (S/N):").pack()
                    entry_implementado = tk.Entry(ventana_modificar)
                    entry_implementado.pack()
                    tk.Label(ventana_modificar, text="¿Modificar apto para veganos? (S/N):").pack()
                    entry_veganos = tk.Entry(ventana_modificar)
                    entry_veganos.pack()
                    tk.Label(ventana_modificar, text="¿Modificar apto para vegetarianos? (S/N):").pack()
                    entry_vegetarianos = tk.Entry(ventana_modificar)
                    entry_vegetarianos.pack()
                    tk.Label(ventana_modificar, text="¿Modificar apto para celiacos? (S/N):").pack()
                    entry_celiacos = tk.Entry(ventana_modificar)
                    entry_celiacos.pack()
                    def guardar_modificacion():
                        nueva_ganancia = float(entry_ganancia.get())
                        nuevo_precio = float(entry_precio.get())
                        nueva_implementacion = entry_implementado.get().upper() == "S"
                        nuevo_veganos = entry_veganos.get().upper() == "S"
                        nuevo_vegetarianos = entry_vegetarianos.get().upper() == "S"
                        nuevo_celiacos = entry_celiacos.get().upper() == "S"
                        cursor.execute("UPDATE Platos SET Ganancia = ?, Precio_Final = ?, Implementado_Menu = ?, Apto_Veganos = ?, Apto_Vegetarianos = ?, Apto_Celiacos = ? WHERE Nombre = ?",
                                       (nueva_ganancia, nuevo_precio, nueva_implementacion, nuevo_veganos, nuevo_vegetarianos, nuevo_celiacos, nombre_plato))
                        base.commit()
                        tk.messagebox.showinfo("Éxito", "Plato modificado correctamente.")
                        ventana_modificar.destroy()
                    tk.Button(ventana_modificar, text="Guardar Modificación", command=guardar_modificacion).pack()
                tk.Button(ventana_detalle, text="Modificar", command=modificar_plato).pack()
            else:
                tk.messagebox.showerror("Error", "El plato especificado no existe.")
        tk.Button(ventana_modificar, text="Obtener Detalle", command=obtener_datos_modificar).pack()
    mostrar_detalle_modificar()

def eliminar_plato():
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Plato")

    tk.Label(ventana_eliminar, text="Nombre del plato a eliminar:").pack()
    entry_nombre_eliminar = tk.Entry(ventana_eliminar)
    entry_nombre_eliminar.pack()

    def confirmar_eliminacion():
        nombre_plato = entry_nombre_eliminar.get()
        confirmacion = tk.messagebox.askyesno("Confirmación", f"¿Está seguro de querer eliminar el plato '{nombre_plato}'?")
        if confirmacion:
            cursor.execute("DELETE FROM Platos WHERE Nombre = ?", (nombre_plato,))
            base.commit()
            tk.messagebox.showinfo("Éxito", "Plato eliminado correctamente.")
            ventana_eliminar.destroy()

    tk.Button(ventana_eliminar, text="Confirmar", command=confirmar_eliminacion).pack()
#_________________________________ M e n u 
def ver_carta():
    def cargar_carta():
        for row in table.get_children():
            table.delete(row)
        cursor.execute("SELECT Nombre, Precio_Final, Apto_Veganos, Apto_Vegetarianos, Apto_Celiacos FROM Platos")
        platos = cursor.fetchall()
        for plato in platos:
            nombre = plato[0]
            precio_final = plato[1]
            apto_veganos = "Sí" if plato[2] else "No"
            apto_vegetarianos = "Sí" if plato[3] else "No"
            apto_celiacos = "Sí" if plato[4] else "No"
            table.insert('', 'end', text=nombre, values=(precio_final, apto_veganos, apto_vegetarianos, apto_celiacos))

    ventana_ver_carta = tk.Toplevel()
    ventana_ver_carta.title("Ver Carta")
    table = ttk.Treeview(ventana_ver_carta)
    table['columns'] = ('Precio Final', 'Vegano', 'Vegetariano', 'Celiaco')
    table.heading('#0', text='Plato')
    table.heading('Precio Final', text='Precio Final')
    table.heading('Vegano', text='Vegano')
    table.heading('Vegetariano', text='Vegetariano')
    table.heading('Celiaco', text='Celiaco')
    table.pack(padx=10, pady=10)
    btn_cargar = tk.Button(ventana_ver_carta, text="Cargar Carta", command=cargar_carta) 
    btn_cargar.pack(pady=10)

def menu_modificar_precios():
    def modificar_precio_plato_individual():
        ventana_modificar = tk.Toplevel()
        ventana_modificar.title("Modificar Precio de Plato Individual")
        def guardar_modificacion():
            nombre_plato = entry_nombre_plato.get()
            nuevo_precio = float(entry_nuevo_precio.get())
            cursor.execute("UPDATE Platos SET Precio_Final = ? WHERE Nombre = ?", (nuevo_precio, nombre_plato))
            base.commit()
            tk.messagebox.showinfo("Éxito", f"Se ha modificado el precio del plato '{nombre_plato}' correctamente.")
            ventana_modificar.destroy()
        tk.Label(ventana_modificar, text="Nombre del plato:").pack()
        entry_nombre_plato = tk.Entry(ventana_modificar)
        entry_nombre_plato.pack()
        tk.Label(ventana_modificar, text="Nuevo precio:").pack()
        entry_nuevo_precio = tk.Entry(ventana_modificar)
        entry_nuevo_precio.pack()
        tk.Button(ventana_modificar, text="Guardar", command=guardar_modificacion).pack()
    def modificar_precio_todos():
        ventana_modificar = tk.Toplevel()
        ventana_modificar.title("Modificar Precio de Todos los Platos")
        def guardar_modificacion():
            porcentaje_aumento = float(entry_porcentaje.get())
            cursor.execute("SELECT Nombre, Precio_Final FROM Platos")
            platos = cursor.fetchall()
            for plato in platos:
                nombre_plato = plato[0]
                precio_actual = plato[1]
                nuevo_precio = precio_actual * (1 + porcentaje_aumento / 100)
                cursor.execute("UPDATE Platos SET Precio_Final = ? WHERE Nombre = ?", (nuevo_precio, nombre_plato))
                base.commit()
            tk.messagebox.showinfo("Éxito", f"Se ha modificado el precio de todos los platos correctamente.")
            ventana_modificar.destroy()
        tk.Label(ventana_modificar, text="Porcentaje de aumento para todos los platos (%):").pack()
        entry_porcentaje = tk.Entry(ventana_modificar)
        entry_porcentaje.pack()
        tk.Button(ventana_modificar, text="Guardar", command=guardar_modificacion).pack()
    ventana_menu = tk.Toplevel()
    ventana_menu.title("Menú Modificar Precios")
    tk.Button(ventana_menu, text="Modificar Precio de Plato Individual", command=modificar_precio_plato_individual).pack(pady=10)
    tk.Button(ventana_menu, text="Modificar Precio de Todos los Platos", command=modificar_precio_todos).pack(pady=10)


cursor.execute('CREATE TABLE IF NOT EXISTS INGREDIENTES  ( Codigo_Ingrediente INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Unidad_Medida VARCHAR(50), Cantidad NUMBER, Precio NUMBER, Detalles TEXT )')
cursor.execute('CREATE TABLE IF NOT EXISTS RECETAS (Codigo_Receta INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Costo NUMBER, Codigo_Ingrediente INT, Cantidad_De_Cada_Ingrediente NUMBER, FOREIGN KEY (Codigo_Ingrediente) REFERENCES INGREDIENTES(Codigo_Ingrediente))')
cursor.execute('CREATE TABLE IF NOT EXISTS PLATOS ( Nombre VARCHAR(100) PRIMARY KEY, Ganancia NUMBER, Precio_Final NUMBER, Implementado_Menu BOOLEAN , Apto_Veganos BOOLEAN, Apto_Vegetarianos BOOLEAN, Apto_Celiacos BOOLEAN)')
cursor.execute("CREATE TABLE IF NOT EXISTS Menu (Nombre_Plato VARCHAR(100), FOREIGN KEY (Nombre_Plato) REFERENCES Platos(Nombre) ON DELETE CASCADE)")

def mostrar_ingredientess():
    def seleccionar_opcion(opcion):
        if opcion == "Ingresar":
            ingresar_ingredientes()
        elif opcion == "Ver":
            ver_ingredientes()
        elif opcion == "Modificar":
            sisisi()
        elif opcion == "Eliminar":
            eliminar_ingredientes()
        elif opcion == "Volver":
            root.destroy()
    root = tk.Tk()
    root.title("Menú de Ingredientes")
    root.configure(bg="black")
    titulo_label = tk.Label(root, text="Menú de Ingredientes", font=("Helvetica", 20), fg="light blue", bg="black")
    titulo_label.pack(pady=10)
    estilo_botones = {"bg": "light blue", "fg": "black", "font": ("Helvetica", 14)}
    ingresar_btn = tk.Button(root, text="Ingresar", command=lambda: seleccionar_opcion("Ingresar"), **estilo_botones)
    ingresar_btn.pack(pady=10)
    ver_btn = tk.Button(root, text="Ver", command=lambda: seleccionar_opcion("Ver"), **estilo_botones)
    ver_btn.pack(pady=10)
    modificar_btn = tk.Button(root, text="Modificar", command=lambda: seleccionar_opcion("Modificar"), **estilo_botones)
    modificar_btn.pack(pady=10)
    eliminar_btn = tk.Button(root, text="Eliminar", command=lambda: seleccionar_opcion("Eliminar"), **estilo_botones)
    eliminar_btn.pack(pady=10)
    volver_btn = tk.Button(root, text="Volver", command=lambda: seleccionar_opcion("Volver"), **estilo_botones)
    volver_btn.pack(pady=10)
    root.mainloop()

def mostrar_recetas():
    def seleccionar_opcion(opcion):
        if opcion == "Ingresar":
            ingresar_receta(cursor, base)
        elif opcion == "Ver":
            mostrar_recetas_con_costo()
        elif opcion == "Modificar":
            modificar_receta()
        elif opcion == "Eliminar":
            eliminar_receta()
        elif opcion == "Volver":
            root.destroy()
    
    root = tk.Tk()
    root.title("Menú de Recetas")
    root.configure(bg="black")
    titulo_label = tk.Label(root, text="Menú de Recetas", font=("Helvetica", 20), fg="light blue", bg="black")
    titulo_label.pack(pady=10)
    estilo_botones = {"bg": "light blue", "fg": "black", "font": ("Helvetica", 14)}
    ingresar_btn = tk.Button(root, text="Ingresar", command=lambda: seleccionar_opcion("Ingresar"), **estilo_botones)
    ingresar_btn.pack(pady=10)
    ver_btn = tk.Button(root, text="Ver", command=lambda: seleccionar_opcion("Ver"), **estilo_botones)
    ver_btn.pack(pady=10)
    modificar_btn = tk.Button(root, text="Modificar", command=lambda: seleccionar_opcion("Modificar"), **estilo_botones)
    modificar_btn.pack(pady=10)
    eliminar_btn = tk.Button(root, text="Eliminar", command=lambda: seleccionar_opcion("Eliminar"), **estilo_botones)
    eliminar_btn.pack(pady=10)
    volver_btn = tk.Button(root, text="Volver", command=lambda: seleccionar_opcion("Volver"), **estilo_botones)
    volver_btn.pack(pady=10)
    root.mainloop()

def mostrar_platos():
    def seleccionar_opcion(opcion):
        if opcion == "Ingresar":
            ingresar_plato()
        elif opcion == "Ver":
            mostrar_platos_menu()
        elif opcion == "Modificar":
            modificar_plato()
        elif opcion == "Eliminar":
            eliminar_plato()
        elif opcion == "Volver":
            root.destroy()
    root = tk.Tk()
    root.title("Menú de Platos")
    root.configure(bg="black")
    titulo_label = tk.Label(root, text="Menú de Platos", font=("Helvetica", 20), fg="light blue", bg="black")
    titulo_label.pack(pady=10)
    estilo_botones = {"bg": "light blue", "fg": "black", "font": ("Helvetica", 14)}
    ingresar_btn = tk.Button(root, text="Ingresar", command=lambda: seleccionar_opcion("Ingresar"), **estilo_botones)
    ingresar_btn.pack(pady=10)
    ver_btn = tk.Button(root, text="Ver", command=lambda: seleccionar_opcion("Ver"), **estilo_botones)
    ver_btn.pack(pady=10)
    modificar_btn = tk.Button(root, text="Modificar", command=lambda: seleccionar_opcion("Modificar"), **estilo_botones)
    modificar_btn.pack(pady=10)
    eliminar_btn = tk.Button(root, text="Eliminar", command=lambda: seleccionar_opcion("Eliminar"), **estilo_botones)
    eliminar_btn.pack(pady=10)
    volver_btn = tk.Button(root, text="Volver", command=lambda: seleccionar_opcion("Volver"), **estilo_botones)
    volver_btn.pack(pady=10)
    root.mainloop()


def mostrar_carta():
    def seleccionar_opcion(opcion):
        if opcion == "Ver Carta":
            ver_carta()
        elif opcion == "Modificar Carta":
            menu_modificar_precios()
        elif opcion == "Volver":
            root.destroy()
    root = tk.Tk()
    root.title("Menú de Carta")
    root.configure(bg="black")
    titulo_label = tk.Label(root, text="Menú de Carta", font=("Helvetica", 20), fg="light blue", bg="black")
    titulo_label.pack(pady=10)
    estilo_botones = {"bg": "light blue", "fg": "black", "font": ("Helvetica", 14)}
    ver_carta_btn = tk.Button(root, text="Ver Carta", command=lambda: seleccionar_opcion("Ver Carta"), **estilo_botones)
    ver_carta_btn.pack(pady=10)
    modificar_carta_btn = tk.Button(root, text="Modificar Carta", command=lambda: seleccionar_opcion("Modificar Carta"), **estilo_botones)
    modificar_carta_btn.pack(pady=10)
    volver_btn = tk.Button(root, text="Volver", command=lambda: seleccionar_opcion("Volver"), **estilo_botones)
    volver_btn.pack(pady=10)
    root.mainloop()
def seleccionar_opcion(opcion):
    if opcion == "Ingredientes":
        mostrar_ingredientess()
    elif opcion == "Recetas":
        mostrar_recetas()
    elif opcion == "Platos":
        mostrar_platos()
    elif opcion == "Carta":
        mostrar_carta()
    elif opcion == "Salir":
        root.destroy()

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Menú")
root.configure(bg="black")  # Fondo negro
root.geometry("600x400")
# Título del menú
titulo_label = tk.Label(root, text="M E N U", font=("Helvetica", 20), fg="light blue", bg="black")
titulo_label.pack(pady=10)
# Estilo para los botones
estilo_botones = {"bg": "light blue", "fg": "black", "font": ("Helvetica", 14)}
# Botones de selección de opción
ingredientes_btn = tk.Button(root, text="Ingredientes", command=lambda: seleccionar_opcion("Ingredientes"), **estilo_botones)
ingredientes_btn.pack(pady=10)
recetas_btn = tk.Button(root, text="Recetas", command=lambda: seleccionar_opcion("Recetas"), **estilo_botones)
recetas_btn.pack(pady=10)
platos_btn = tk.Button(root, text="Platos", command=lambda: seleccionar_opcion("Platos"), **estilo_botones)
platos_btn.pack(pady=10)
carta_btn = tk.Button(root, text="Carta", command=lambda: seleccionar_opcion("Carta"), **estilo_botones)
carta_btn.pack(pady=10)
# Botón para salir del programa
salir_btn = tk.Button(root, text="Salir", command=lambda: seleccionar_opcion("Salir"), **estilo_botones)
salir_btn.pack(pady=10)
# Ejecutar el bucle principal de la interfaz gráfica
root.mainloop()