

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import *
import re

cursor = base.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS INGREDIENTES  ( Codigo_Ingrediente INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Unidad_Medida VARCHAR(50), Precio NUMBER, Detalles TEXT )')
cursor.execute('CREATE TABLE IF NOT EXISTS RECETAS (Codigo_Receta INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Costo FLOAT, Codigo_Ingrediente INT, Cantidad_De_Cada_Ingrediente NUMBER,Unidad VARCHAR(20),FOREIGN KEY (Codigo_Ingrediente) REFERENCES INGREDIENTES(Codigo_Ingrediente))')
cursor.execute('CREATE TABLE IF NOT EXISTS PLATOS (ID INTEGER PRIMARY KEY AUTOINCREMENT,Nombre VARCHAR(100),Ganancia NUMERIC,Precio_Final NUMERIC,Implementado_Menu BOOLEAN, Especificaciones VARCHAR(100));')
cursor.execute("CREATE TABLE IF NOT EXISTS Menu (Nombre_Plato VARCHAR(100), FOREIGN KEY (Nombre_Plato) REFERENCES Platos(Nombre) ON DELETE CASCADE)")
cursor.execute("CREATE TABLE IF NOT EXISTS RECETAS_INGREDIENTES (Codigo_Receta INTEGER,Codigo_Ingrediente INTEGER,Cantidad NUMBER,FOREIGN KEY (Codigo_Receta) REFERENCES RECETAS(Codigo_Receta),FOREIGN KEY (Codigo_Ingrediente) REFERENCES INGREDIENTES(Codigo_Ingrediente))")


def change_color_on_hover(widget, color_on_hover, color_on_leave):
	
	def on_enter(event):
		widget.config(bg=color_on_hover)
		widget["menu"].config(bg=color_on_hover)

	def on_leave(event):
		widget.config(bg=color_on_leave)
		widget["menu"].config(bg=color_on_leave)

	widget.bind("<Enter>", on_enter)
	widget.bind("<Leave>", on_leave)
	
def ingresar_ingrediente(frame):
	global cuantidad,unidad
	opciones_unidades = [
		"Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)",
		"Mililitros (ml)", "Litros (l)", "Cucharadas (tbsp)",
		"Cucharaditas (tsp)", "Tazas (cup)", "Unidad (Un)"
	]
	tk.Label(frame, text="Nombre del ingrediente:",bg='orange', fg='black', font="Lustria").pack()
	entry_nombre = tk.Entry(frame, bg='yellow', fg='black', justify="center", font="Lustria")
	entry_nombre.pack()
	tk.Label(frame, text="Unidad de medida:", bg='orange', fg='black').pack()
	variable_unidad = tk.StringVar(frame)
	variable_unidad.set(opciones_unidades[0])
	menu_unidad = tk.OptionMenu(frame, variable_unidad, *opciones_unidades)
	menu_unidad.config(bg="orange",fg='black', font="Lustria", activebackground="#000000", relief="groove")
	menu_unidad.pack()
	menu_unidad["menu"].config(bg='orange', fg='black', font="Lustria")

	tk.Label(frame, text="Precio:", bg='orange', fg='black').pack()
	entry_precio = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_precio.pack()
	def guardar_ingrediente():
		global unidad, cantidad
		nombre = entry_nombre.get()
		unidad = variable_unidad.get()
		precio = float(entry_precio.get())
		cursor.execute("INSERT INTO Ingredientes (Nombre, Unidad_Medida, Precio) VALUES (?, ?, ?)",
					   (nombre, unidad, precio))
		base.commit()
		frame.forget()
	separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
	separator.pack(fill=tk.X, pady=10)
	tk.Button(frame, text="Guardar", command=guardar_ingrediente, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

def ver_ingrediente(frame):
	cursor.execute("SELECT Codigo_Ingrediente, Nombre, Unidad_Medida, Precio FROM Ingredientes")
	ingredientes = cursor.fetchall()
	
	if not ingredientes:
		tk.Label(frame, text="No hay ingredientes para mostrar.", bg="orange").pack()
		return
	
	# Crear un estilo personalizado
	estilo = ttk.Style()
	estilo.theme_use('clam')  # Asegura que el tema base sea compatible
	estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0,  bg='orange', fg='black', background='orange', font=('Lucida Console', 9))

	tabla = ttk.Treeview(frame,columns=("Código", "Nombre", "Unidad de Medida", "Precio"), show="headings", style="mystyle.Treeview")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Unidad de Medida", text="Unidad de Medida")
	tabla.heading("Precio", text="Precio")
	tabla.pack(fill=tk.BOTH, expand=True)  # Asegura que el Treeview ocupe todo el espacio disponible
	scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
	tabla.configure(yscrollcommand=scrollbar.set)
	scrollbar.pack(side="right", fill="y")
	for ingrediente in ingredientes:
		codigo, nombre, unidad, precio = ingrediente
		tabla.insert("", "end", values=(codigo, nombre, unidad, precio))
	tabla.pack(padx=20, pady=20)

def ver_ingredientes(frame):
	cursor.execute("SELECT Codigo_Ingrediente, Nombre, Unidad_Medida, Precio FROM Ingredientes")
	ingredientes = cursor.fetchall()
	if not ingredientes:
		tk.Label(frame, text="No hay ingredientes para mostrar.", bg="orange").pack()
		return

	# Crear un estilo personalizado
	estilo = ttk.Style()
	estilo.theme_use('clam') 
	estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0,  bg='orange', fg='black', background='orange', font=('Lucida Console', 9))

	tabla = ttk.Treeview(frame, columns=("Código", "Nombre", "Unidad de Medida", "Precio"), show="headings", selectmode='browse', style="mystyle.Treeview")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Unidad de Medida", text="Unidad de Medida")
	tabla.heading("Precio",text="Precio")
	tabla.pack(fill=tk.BOTH, expand=True)  

	for ingrediente in ingredientes:
		codigo, nombre, unidad, precio = ingrediente
		tabla.insert("", "end", values=(codigo, nombre, unidad, precio))

	tabla.pack(padx=20, pady=20)
	
def sisisi(frame):
	tk.Label(frame, text="Código del ingrediente a modificar:", bg='orange', fg='black').pack()
	entry_codigo_modificar = tk.Entry(frame, bg='yellow', fg='black', justify="center", font="Lustria")
	entry_codigo_modificar.pack()

	def mostrar_detalle_modificar():
		codigo_modificar = int(entry_codigo_modificar.get())
		cursor.execute("SELECT * FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_modificar,))
		resultado_verificacion = cursor.fetchone()
		if not resultado_verificacion:
			tk.messagebox.showerror("Error", "No se encontró ningún ingrediente con ese código.")
		else:
			tk.Label(frame, text=f"Nombre: {resultado_verificacion[1]}", bg='orange', fg='black').pack()
			tk.Label(frame, text=f"Unidad de Medida: {resultado_verificacion[2]}", bg='orange', fg='black').pack()
			tk.Label(frame, text=f"Precio: {resultado_verificacion[3]}", bg='orange', fg='black').pack()
			opciones_modificar = ["Nombre", "Unidad de Medida", "Precio", "Todos"]
			variable_opcion_modificar = tk.StringVar(frame)
			variable_opcion_modificar.set(opciones_modificar[0])  # Valor predeterminado
			option_menu_modificar = tk.OptionMenu(frame, variable_opcion_modificar, *opciones_modificar)
			option_menu_modificar.config(bg="orange", font="Lustria", activebackground="orange", relief="groove")
			option_menu_modificar.pack()
			option_menu_modificar["menu"].config(bg='orange', fg='black', font="Lustria")
			entry_nuevo_valor = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
			entry_nuevo_valor.pack()

			def confirmar_modificacion():
				opcion_modificar = variable_opcion_modificar.get()
				nuevo_valor = entry_nuevo_valor.get()
				if opcion_modificar == "Unidad de Medida":
					opciones_unidades = [
		"Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)",
		"Mililitros (ml)", "Litros (l)", "Cucharadas (tbsp)",
		"Cucharaditas (tsp)", "Tazas (cup)", "Unidad (Un)"
	]
					entry_nuevo_valor.destroy()
					nueva_unidad = tk.StringVar(frame)
					nueva_unidad.set(resultado_verificacion[3])  # Establecer el valor actual como predeterminado
					menu_unidades = tk.OptionMenu(frame, nueva_unidad, *opciones_unidades)
					menu_unidades.pack()
				else:
					entry_nuevo_valor.delete(0, tk.END)
					entry_nuevo_valor.insert(0, resultado_verificacion[opciones_modificar.index(opcion_modificar) + 1])
				def guardar_modificacion():
					if opcion_modificar == "Todos":
						campos = ["Nombre", "Unidad_Medida", "Precio"]
						for campo in campos:
							cursor.execute(f"UPDATE Ingredientes SET {campo} = ? WHERE Codigo_Ingrediente = ?",
										   (nuevo_valor, codigo_modificar))
					else:
						cursor.execute(f"UPDATE Ingredientes SET {opcion_modificar} = ? WHERE Codigo_Ingrediente = ?",
									   (nuevo_valor, codigo_modificar))
					base.commit()
					tk.messagebox.showinfo("Éxito", f"Se ha modificado el valor del campo {opcion_modificar}.")
				
				separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
				separator.pack(fill=tk.X, pady=10)
				boton_confirmar = tk.Button(frame, text="Confirmar", command=guardar_modificacion)
				boton_confirmar.pack()

			boton_guardar_cambios = tk.Button(frame, text="Guardar Cambios", command=confirmar_modificacion, bg='orange', fg='black', font="Lustria", activebackground="orange")
			boton_guardar_cambios.pack()
	tk.Button(frame, text="Mostrar Detalle", command=mostrar_detalle_modificar, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	tk.Button(frame,command=ver_ingredientes(frame), bg='orange', fg='black', font="Lustria", activebackground="orange")

def eliminar_ingredientes(frame):
	tk.Label(frame, text="Código del ingrediente a eliminar:", bg='orange', fg='black').pack()
	entry_codigo_eliminar = tk.Entry(frame, bg='yellow', fg='black', justify="center", font="Lustria")
	entry_codigo_eliminar.pack()
	def confirmar_eliminacion():
		codigo_eliminar = int(entry_codigo_eliminar.get())
		cursor.execute("DELETE FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_eliminar,))
		base.commit()
		tk.messagebox.showinfo("Éxito", "El ingrediente ha sido eliminado correctamente.")
		frame.destroy()
	boton_confirmar_eliminacion = tk.Button(frame, text="Confirmar Eliminación", command=confirmar_eliminacion, bg='orange', fg='black', font="Lustria", activebackground="orange")
	boton_confirmar_eliminacion.pack()
	tk.Button(frame, text="        Ver        ",command=ver_ingredientes(frame), bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

# ------------------------------------------- INGRESAR RECETA --------------------------------------------------------

def ingresar_receta(frame):
	ingredientes_receta = []
	ingredientes_codigos = []
	unidad_valores = []
	def calcular_costo_total(ingredientes_receta):
		costo_total = 0
		print(ingredientes_receta)

		for nombre, cantidad in ingredientes_receta:
			cursor.execute("SELECT Precio FROM Ingredientes WHERE Nombre =?", (nombre,))
			precio_ingrediente = cursor.fetchone()
			
			if precio_ingrediente is None:
				messagebox.showerror("Error", f"No se encontró el precio para el ingrediente {nombre}.")
			else:
				precio_actual = precio_ingrediente[0]
				costo_ingle = cantidad * precio_actual
				costo_total += costo_ingle
		
		return costo_total
		
	def agregar_ingrediente():
		nombre_ingrediente = entry_nombre.get()
		cantidad_ingrediente = float(entry_cantidad.get())
		unidad_val = unidad.get()
		cursor.execute("SELECT Nombre FROM INGREDIENTES WHERE Nombre like ?", (nombre_ingrediente,))
		nombre_ing = cursor.fetchone()[0]
		ingredientes_receta.append((nombre_ing, cantidad_ingrediente))
		unidad_valores.append(unidad_val)
		ingredientes_codigos.append(nombre_ingrediente)
		listbox_ingredientes.insert(tk.END, f"{nombre_ing}: {cantidad_ingrediente} {unidad.get()}")
	def eliminar_ingrediente(indice):
		if indice < len(ingredientes_receta):
			nombre_ing, _ = ingredientes_receta.pop(indice)
			unidad_valores.pop(indice)
			ingredientes_codigos.pop(indice)
			listbox_ingredientes.delete(indice)
			messagebox.showinfo("Éxito", f"Ingrediente '{nombre_ing}' eliminado correctamente.")

	def guardar_receta():
		nombre_receta = entry_nombre_receta.get()
		
		if not nombre_receta:
			tk.messagebox.showerror("Error", "Por favor, ingrese el nombre de la receta.")
			return
		if not ingredientes_receta:
			tk.messagebox.showerror("Error", "La receta debe tener al menos un ingrediente.")
			return
		nombre_ingredientes = ", ".join([ingrediente[0] for ingrediente in ingredientes_receta])
		cantidades = ", ".join([str(cantidad[1]) for cantidad in ingredientes_receta])
		unidades = ", ".join(unidad for unidad in unidad_valores)	
		costo_total = calcular_costo_total(ingredientes_receta)
		cantidades_ingredientes = ", ".join(str(ingrediente[1]) + " " + unidad.get() for ingrediente in ingredientes_receta)
		cursor.execute("INSERT INTO Recetas (Nombre, Costo, Codigo_Ingrediente, Cantidad_De_Cada_Ingrediente, unidad) VALUES (?, ?, ?, ?, ?)",
					   (nombre_receta, costo_total, nombre_ingredientes, cantidades, unidades))
		codigo_receta = cursor.lastrowid
		cursor.execute("INSERT INTO RECETAS_INGREDIENTES (Codigo_Receta, Codigo_Ingrediente, Cantidad) VALUES (?,?,?)", (codigo_receta,ingredientes_codigos[-1],cantidades_ingredientes))
		base.commit()
		tk.messagebox.showinfo("Éxito", "Receta ingresada correctamente.")

	tk.Label(frame, text="Nombre de la receta:", bg='orange', fg='black').pack()
	entry_nombre_receta = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_nombre_receta.pack()
	tk.Label(frame, text="Nombre del ingrediente:", bg='orange', fg='black').pack()
	entry_nombre = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_nombre.pack()
	tk.Label(frame, text="Cantidad del ingrediente:", bg='orange', fg='black').pack()
	entry_cantidad = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_cantidad.pack()
	unidad = tk.StringVar(frame)
	unidades = [
		"Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)",
		"Mililitros (ml)", "Litros (l)", "Cucharadas (tbsp)",
		"Cucharaditas (tsp)", "Tazas (cup)", "Unidad (Un)"
	]
	unidad.set(unidades[0])
	menu_uni = tk.OptionMenu(frame, unidad, *unidades)
	menu_uni.pack()
	menu_uni.config(bg="orange", font="Lustria", activebackground="orange", relief="groove")
	menu_uni["menu"].config(bg='orange', fg='black', font="Lustria")
	tk.Button(frame, text="Agregar Ingrediente", command=agregar_ingrediente, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	listbox_ingredientes = tk.Listbox(frame, bg='orange', fg='black', font="Lustria")
	listbox_ingredientes.pack()
	tk.Button(frame, text="Eliminar Ingrediente", command=lambda: eliminar_ingrediente(listbox_ingredientes.curselection()[0]), bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	tk.Button(frame, text="Guardar Receta", command=guardar_receta, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

#-------------------------------------------- VER RECETA --------------------------------------------------
def mostrar_receta(frame):
	cursor.execute("SELECT * FROM RECETAS")
	recetas = cursor.fetchall()
	if not recetas:
		tk.Label(frame, text="No hay recetas para mostrar.", bg="orange").pack()
		return
	
	# Crear un estilo personalizado
	estilo = ttk.Style()
	estilo.theme_use('clam') 
	estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0,  bg='orange', fg='black', background='orange', font=('Lucida Console', 9))

	tabla = ttk.Treeview(frame, columns=("Código", "Nombre", "Costo", "Ingredientes", "Cantidades", "Unidad"), show="headings", selectmode='browse', style="mystyle.Treeview")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Costo", text="Costo")
	tabla.heading("Ingredientes", text="Ingredientes")
	tabla.heading("Cantidades", text="Cantidades")
	tabla.heading("Unidad", text="Unidad")
	tabla.pack(fill=tk.BOTH, expand=True)

	for receta in recetas:
		codigo, nombre, costo, ingredientes, cantidad, unidad = receta
		tabla.insert("", "end", values=(codigo, nombre, costo, ingredientes, cantidad, unidad))
	tabla.pack(padx=20, pady=20)

def mostrar_receta_top(frame):
	cursor.execute("SELECT * FROM RECETAS")
	recetas = cursor.fetchall()
	if not recetas:
		tk.Label(frame, text="No hay recetas para mostrar.", bg="orange").pack()
		return
	
	# Crear un estilo personalizado
	estilo = ttk.Style()
	estilo.theme_use('clam') 
	estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0,  bg='orange', fg='black', background='orange', font=('Lucida Console', 9))

	tabla = ttk.Treeview(frame, columns=("Código", "Nombre", "Costo", "Ingredientes", "Cantidades", "Unidad"), show="headings", selectmode='browse', style="mystyle.Treeview")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Costo", text="Costo")
	tabla.heading("Ingredientes", text="Ingredientes")
	tabla.heading("Cantidades", text="Cantidades")
	tabla.heading("Unidad", text="Unidad")
	tabla.pack(fill=tk.BOTH, expand=True)

	for receta in recetas:
		codigo, nombre, costo, ingredientes, cantidad, unidad = receta
		tabla.insert("", "end", values=(codigo, nombre, costo, ingredientes, cantidad, unidad))

	tabla.pack(padx=20, pady=20)

# ------------------------------------------- MODIFICAR RECETA --------------------------------------------------------
def modificar_receta(frame):
	def mostrar_opciones_modificar():
		codigo_receta = entry_codigo_modificar.get()
		cursor.execute("SELECT * FROM Recetas WHERE Codigo_Receta = ?", (codigo_receta,))
		receta = cursor.fetchone()
		if receta:
			tk.Label(frame, text="Opciones de modificación:", bg='orange', fg='black').pack()
			tk.Button(frame, text="Ingresar Ingredientes", command=lambda: ingresar_ingredientes(frame, receta), bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
			tk.Button(frame, text="Eliminar Ingredientes", command=lambda: eliminar_ingredientes(frame, receta), bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
			tk.Button(frame, text="Modificar Nombre", command=lambda: modificar_nombre(frame, receta), bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
		else:
			tk.messagebox.showerror("Error", "La receta especificada no existe.")

	tk.Label(frame, text="Código de la receta a modificar:", bg='orange', fg='black').pack()
	entry_codigo_modificar = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_codigo_modificar.pack()
	tk.Button(frame, text="Modificar", command=mostrar_opciones_modificar, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	tk.Button(frame, text="        Ver        ",command=mostrar_receta(frame), bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	
def modificar_ingredientes(frame, receta):
	tk.Label(frame, text="Modificar Ingredientes", bg='orange', fg='black').pack()
	entry_codigo_ingrediente = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_codigo_ingrediente.pack()
	entry_nueva_cantidad = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_nueva_cantidad.pack()
	unidad = tk.StringVar(frame)
	unidades = ["Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Mililitros (ml)", "Litros (l)", "Cucharadas (tbsp)", "Cucharaditas (tsp)", "Tazas (cup)", "Unidad (Un)"]
	unidad.set(unidades[0])
	menu_uni = tk.OptionMenu(frame, unidad, *unidades)
	menu_uni.pack()
	menu_uni.config(bg="orange", font="Lustria", activebackground="orange", relief="groove")
	menu_uni["menu"].config(bg='orange', fg='black', font="Lustria")

	def confirmar_modificacion_ingrediente():
		codigo_ingrediente = entry_codigo_ingrediente.get().strip()
		nueva_cantidad = float(entry_nueva_cantidad.get().strip())
		nueva_unidad = unidad.get().strip()
		cursor.execute("UPDATE RECETAS_INGREDIENTES SET Cantidad = ? WHERE Codigo_Receta = ? AND Codigo_Ingrediente = ?", (nueva_cantidad, receta[0], codigo_ingrediente))
		base.commit()
		tk.messagebox.showinfo("Éxito", "Ingrediente modificado correctamente.")
	
	tk.Button(frame, text="Confirmar", command=confirmar_modificacion_ingrediente, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

def ingresar_ingredientes(frame, receta):
	ingredientes_receta = []
	ingredientes_codigos = []
	unidad_valores = []

	def agregar_ingrediente():
		nombre_ingrediente = entry_nombre.get()
		cantidad_ingrediente = float(entry_cantidad.get())
		unidad_val = unidad.get()
		cursor.execute("SELECT Codigo_Ingrediente FROM INGREDIENTES WHERE Nombre = ?", (nombre_ingrediente,))
		codigo_ingrediente = cursor.fetchone()[0]
		ingredientes_receta.append((codigo_ingrediente, cantidad_ingrediente))
		unidad_valores.append(unidad_val)
		ingredientes_codigos.append(codigo_ingrediente)
		listbox_ingredientes.insert(tk.END, f"{nombre_ingrediente}: {cantidad_ingrediente} {unidad_val}")

	def eliminar_ingrediente(indice):
		if indice < len(ingredientes_receta):
			ingredientes_receta.pop(indice)
			unidad_valores.pop(indice)
			ingredientes_codigos.pop(indice)
			listbox_ingredientes.delete(indice)
			messagebox.showinfo("Éxito", f"Ingrediente eliminado correctamente.")

	def guardar_ingredientes():
		if not ingredientes_receta:
			tk.messagebox.showerror("Error", "Debe agregar al menos un ingrediente.")
			return
		for codigo_ingrediente, cantidad in ingredientes_receta:
			unidad_val = unidad_valores[ingredientes_codigos.index(codigo_ingrediente)]
			cursor.execute("INSERT INTO RECETAS_INGREDIENTES (Codigo_Receta, Codigo_Ingrediente, Cantidad) VALUES (?, ?, ?)",
						   (receta[0], codigo_ingrediente, cantidad))
		base.commit()
		tk.messagebox.showinfo("Éxito", "Ingredientes ingresados correctamente.")

	tk.Label(frame, text="Nombre del ingrediente:", bg='orange', fg='black').pack()
	entry_nombre = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_nombre.pack()
	tk.Label(frame, text="Cantidad del ingrediente:", bg='orange', fg='black').pack()
	entry_cantidad = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_cantidad.pack()
	unidad = tk.StringVar(frame)
	unidades = ["Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Mililitros (ml)", "Litros (l)", "Cucharadas (tbsp)", "Cucharaditas (tsp)", "Tazas (cup)", "Unidad (Un)"]
	unidad.set(unidades[0])
	menu_uni = tk.OptionMenu(frame, unidad, *unidades)
	menu_uni.pack()
	menu_uni.config(bg="orange", font="Lustria", activebackground="orange", relief="groove")
	menu_uni["menu"].config(bg='orange', fg='black', font="Lustria")
	tk.Button(frame, text="Agregar Ingrediente", command=agregar_ingrediente, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	listbox_ingredientes = tk.Listbox(frame, bg='orange', fg='black', font="Lustria")
	listbox_ingredientes.pack()
	tk.Button(frame, text="Eliminar Ingrediente", command=lambda: eliminar_ingrediente(listbox_ingredientes.curselection()[0]), bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	tk.Button(frame, text="Guardar Ingredientes", command=guardar_ingredientes, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

def eliminar_ingredientes(frame, receta):
	tk.Label(frame, text="Lista de Ingredientes de la Receta", bg='orange', fg='black').pack()
	cursor.execute("SELECT ri.Codigo_Ingrediente, i.Nombre, ri.Cantidad FROM RECETAS_INGREDIENTES ri JOIN INGREDIENTES i ON ri.Codigo_Ingrediente = i.Codigo_Ingrediente WHERE ri.Codigo_Receta = ?", (receta[0],))
	ingredientes = cursor.fetchall()
	
	if not ingredientes:
		tk.Label(frame, text="No hay ingredientes para mostrar.", bg='orange', fg='black').pack()
		return
	
	estilo = ttk.Style()
	estilo.theme_use('clam')
	estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0, bg='orange', fg='black', background='orange', font=('Lucida Console', 9))

	tabla = ttk.Treeview(frame, columns=("Código", "Nombre", "Cantidad"), show="headings", selectmode='browse', style="mystyle.Treeview")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Cantidad", text="Cantidad")
	tabla.pack(fill=tk.BOTH, expand=True)

	for ingrediente in ingredientes:
		codigo, nombre, cantidad = ingrediente
		tabla.insert("", "end", values=(codigo, nombre, cantidad))
	tabla.pack(padx=20, pady=20)

	tk.Label(frame, text="Nombre del ingrediente a eliminar:", bg='orange', fg='black').pack()
	entry_nombre_eliminar = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_nombre_eliminar.pack()

	def confirmar_eliminacion_ingrediente():
		nombre_ingrediente = entry_nombre_eliminar.get().strip()
		cursor.execute("SELECT Codigo_Ingrediente FROM INGREDIENTES WHERE Nombre = ?", (nombre_ingrediente,))
		codigo_ingrediente = cursor.fetchone()
		if codigo_ingrediente:
			cursor.execute("DELETE FROM RECETAS_INGREDIENTES WHERE Codigo_Receta = ? AND Codigo_Ingrediente = ?", (receta[0], codigo_ingrediente[0]))
			base.commit()
			tk.messagebox.showinfo("Éxito", "Ingrediente eliminado correctamente.")
		else:
			tk.messagebox.showerror("Error", "El ingrediente especificado no existe en la receta.")
	
	tk.Button(frame, text="Eliminar Ingrediente", command=confirmar_eliminacion_ingrediente, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

def modificar_nombre(frame, receta):
	def confirmar_modificacion_nombre():
		nuevo_nombre = entry_nuevo_nombre.get().strip()
		cursor.execute("UPDATE RECETAS SET Nombre = ? WHERE Codigo_Receta = ?", (nuevo_nombre, receta[0]))
		base.commit()
		tk.messagebox.showinfo("Éxito", "Nombre de la receta modificado correctamente.")

	tk.Label(frame, text="Modificar Nombre de la Receta", bg='orange', fg='black').pack()
	entry_nuevo_nombre = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_nuevo_nombre.pack()
	tk.Button(frame, text="Confirmar", command=confirmar_modificacion_nombre, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

# ------------------------------------------- ELIMINAR RECETA --------------------------------------------------------
def eliminar_receta(frame):
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
		else:
			tk.messagebox.showerror("Error", "La receta especificada no existe.")

	tk.Label(frame, text="Código de la receta a eliminar:", bg='orange', fg='black').pack()
	entry_codigo_eliminar = tk.Entry(frame, bg='yellow', fg='black', font="Lustria")
	entry_codigo_eliminar.pack()

	tk.Button(frame, text="Confirmar", command=confirmar_eliminacion, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	tk.Button(frame, text="        Ver        ",command=mostrar_receta(frame), bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

# ------------------------------------------- INGRESAR PLATO --------------------------------------------------------
def ingresar_plato(frame):
	def implementar_en_menu():
		nombre_plato = nombre_entry.get()
		cursor.execute("SELECT Implementado_Menu FROM Platos WHERE Nombre=?", (nombre_plato,))
		plato = cursor.fetchone()
		if plato:
			if plato[0] == 1:
				messagebox.showinfo("Error", "El plato ya está implementado en el menú.")
			else:
				cursor.execute("UPDATE Platos SET Implementado_Menu=1 WHERE Nombre=?", (nombre_plato,))
				base.commit()
				messagebox.showinfo("Éxito", "El plato se ha implementado en el menú correctamente.")
				
	def guardar_plato(entry_nombre, entry_ganancia, implementar_menu_check, detalles):
		nombre = entry_nombre.get()
		ganancia_porcentaje = float(entry_ganancia.get())
		detalles_plato = detalles.get()

		cursor.execute("SELECT COSTO FROM RECETAS WHERE NOMBRE LIKE?", ("%" + nombre + "%",))
		costo = cursor.fetchone()[0]

		ganancia_final = costo + (costo * (ganancia_porcentaje / 100))
		print(ganancia_final)

		campos_obligatorios = [nombre, ganancia_porcentaje, detalles_plato]
		campos_faltantes = [campo for campo in campos_obligatorios if not campo]

		if campos_faltantes:
			mensaje_error = "Por favor completa los siguientes campos obligatorios: "
			for campo in campos_faltantes:
				mensaje_error += f"{campo} "

			messagebox.showinfo("Error", mensaje_error.strip())
		else:
			implementado_menu_value = "Si" if implementado_menu.get() == "on" else "No"
			cursor.execute("INSERT INTO PLATOS (Nombre, Ganancia,Precio_final ,Implementado_Menu, Especificaciones) VALUES (?,?,?,?,?)",
						(nombre, ganancia_porcentaje, ganancia_final, implementado_menu.get(), detalles_plato))
			base.commit()
			messagebox.showinfo("Éxito", "Plato ingresado correctamente.")

	nombre_label = tk.Label(frame, text="Nombre del Plato:",bg='orange', fg='black')
	nombre_label.grid(row=0, column=1, padx=10, pady=10 )

	nombre_entry = tk.Entry(frame,bg='yellow', fg='black', justify="center", font="Lustria")
	nombre_entry.grid(row=0, column=2, padx=10, pady=10 )

	ganancia_label = tk.Label(frame, text="Ganancia:",bg='orange', fg='black')
	ganancia_label.grid(row=1, column=1, padx=10, pady=10 )

	ganancia_entry = tk.Entry(frame,bg='yellow', fg='black', justify="center", font="Lustria")
	ganancia_entry.grid(row=1, column=2, padx=10, pady=10)

	detalles_lab = tk.Label(frame, text="Detalles del plato",bg='orange', fg='black')
	detalles_lab.grid(row=3, column=1, padx=10, pady=10)

	detalles = tk.Entry(frame,bg='yellow', fg='black', justify="center", font="Lustria")
	detalles.grid(row=3, column=2, padx=10, pady=10)

	implementar_menu_lab = tk.Label(frame, text= "Implementar al menu",bg='orange', font="Lustria").grid(row=4, column=1, padx=10, pady=10)
	implementado_menu = tk.StringVar()
	implementar_menu_check = tk.Checkbutton(frame, text="Implementar menu", offvalue="No", onvalue="Si", variable=implementado_menu,bg='orange', font="Lustria")
	implementado_menu.set("No") 
	implementar_menu_check.grid(row=4, column=2, padx=10, pady=10)

	guardar_button = tk.Button(frame, text="Guardar",bg='orange', fg='black', font="Lustria", activebackground="orange", command=lambda: guardar_plato(nombre_entry, ganancia_entry, implementar_menu_check, detalles))
	guardar_button.grid(row=5, column=2, padx=10, pady=10)
	implementar_menu_button = tk.Button(frame, text="Verificar si esta en el Menú",bg='orange', fg='black', font="Lustria",activebackground="orange",command=implementar_en_menu)
	implementar_menu_button.grid(row=5, column=0, padx=10, pady=10)

# ------------------------------------------- VER PLATO --------------------------------------------------------
def mostrar_platos_menu(frame):
	cursor.execute("SELECT * FROM Platos")
	platos = cursor.fetchall()
	if not platos:
		tk.Label(frame, text="No hay platos para mostrar.", bg="orange").pack()
		return
	
	# Crear un estilo personalizado
	estilo = ttk.Style()
	estilo.theme_use('clam') 
	estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0,  bg='orange', fg='black', background='orange', font=('Lucida Console', 9))

	tabla = ttk.Treeview(frame, columns=("Nombre", "Ganancia", "Precio Final", "Implementado en Menú", "Especificaciones"), show="headings", selectmode='browse', style="mystyle.Treeview")
	tabla.heading("#0", text="Índice")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Ganancia", text="Ganancia")
	tabla.heading("Precio Final", text="Precio Final")
	tabla.heading("Implementado en Menú", text="Implementado en Menú")
	tabla.heading("Especificaciones", text="Especificaciones")
	tabla.pack(fill=tk.BOTH, expand=True)

	for index, plato in enumerate(platos, start=1):
		tabla.insert('', 'end', text=str(index), values=(plato[1], plato[2], plato[3], plato[4], plato[5]))
	tabla.pack(padx=20, pady=20)
	
def mostrar_platos_menus(frame):
	rootT = tk.Tk()
	rootT.title("Aplicación CRUD")
	rootT.geometry("900x800")
	cursor.execute("SELECT * FROM Platos")
	platos = cursor.fetchall()
	if not platos:
		tk.Label(frame, text="No hay platos para mostrar.", bg="orange").pack()
		return
	tabla = ttk.Treeview(rootT, columns=("Nombre", "Ganancia", "Precio Final", "Implementado en Menú", "Especificaciones"))
	tabla.heading("#0", text="Índice")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Ganancia", text="Ganancia")
	tabla.heading("Precio Final", text="Precio Final")
	tabla.heading("Implementado en Menú", text="Implementado en Menú")
	tabla.heading("Especificaciones", text="Especificaciones")
	for index, plato in enumerate(platos, start=1):
		implementado = "Sí" if plato[3] else "No"
		tabla.insert('', 'end', text=str(index), values=(plato[1], plato[2], plato[3], implementado))
	tabla.pack(fill="both", expand=True)

def guardar_platos_menu(frame):
	cursor.execute("SELECT * FROM Platos")
	platos = cursor.fetchall()

	tabla = ttk.Treeview(frame, columns=("Nombre", "Ganancia", "Precio Final", "Implementado en Menú", "Especificaciones"))
	tabla.heading("#0", text="Índice")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Ganancia", text="Ganancia")
	tabla.heading("Precio Final", text="Precio Final")
	tabla.heading("Implementado en Menú", text="Implementado en Menú")
	for index, plato in enumerate(platos, start=1):
		implementado = "Sí" if plato[3] else "No"
		tabla.insert('', 'end', text=str(index), values=(plato[0], plato[1], plato[2], implementado))

	tabla.pack(fill="both", expand=True)

	# Validar si se ha agregado al menos un plato al menú antes de guardar
	if len(platos) == 0:
		messagebox.showwarning("Advertencia", "No has añadido ningún plato al menú. Por favor, asegúrate de añadir al menos un plato al menú antes de guardar los cambios.")

# ------------------------------------------- MODIFICAR PLATO --------------------------------------------------------
def mostrar_detalle_modificar(frame):
	tk.Label(frame, text="Nombre del plato a modificar:", bg='orange', fg='black').pack()
	entry_nombre_modificar = tk.Entry(frame, bg='yellow', fg='black', justify="center", font="Lustria")
	entry_nombre_modificar.pack()
	implementado_menu = tk.StringVar()
	implementado_menu.set("No")  # Por defecto se establece en No
	def obtener_datos_modificar():
		nombre_plato = entry_nombre_modificar.get()
		cursor.execute("SELECT * FROM Platos WHERE Nombre = ?", (nombre_plato,))
		plato = cursor.fetchone()
		if plato:
			tk.Label(frame, text=f"Nombre: {plato[1]}", bg='orange', fg='black').pack()
			tk.Label(frame, text=f"Ganancia: {plato[2]}", bg='orange', fg='black').pack()
			tk.Label(frame, text=f"Precio Final: {plato[3]}", bg='orange', fg='black').pack()
			def modificar_plato():
				tk.Label(frame, text="Nuevo valor para Ganancia:", bg='orange', fg='black').pack()
				entry_ganancia = tk.Entry(frame, bg='yellow', fg='black', justify="center", font="Lustria")
				entry_ganancia.pack()
				tk.Label(frame, text="Nuevo valor para Precio Final:", bg='orange', fg='black').pack()
				entry_precio = tk.Entry(frame, bg='yellow', fg='black', justify="center", font="Lustria")
				entry_precio.pack()
				tk.Label(frame, text="¿Modificar implementación en menú?", bg='orange', fg='black').pack()
				tk.Radiobutton(frame, text="Sí", variable=implementado_menu, value="Si", bg='orange', fg='black').pack()
				tk.Radiobutton(frame, text="No", variable=implementado_menu, value="No", bg='orange', fg='black').pack()
				def guardar_modificacion():
					nueva_ganancia = float(entry_ganancia.get())
					nuevo_precio = float(entry_precio.get())
					nueva_implementacion = implementado_menu.get()
					cursor.execute(
						"UPDATE Platos SET Ganancia = ?, Precio_Final = ?, Implementado_Menu = ? WHERE Nombre = ?",
						(nueva_ganancia, nuevo_precio, nueva_implementacion, nombre_plato)
					)
					base.commit()
					tk.messagebox.showinfo("Éxito", "Plato modificado correctamente.")
				tk.Button(frame, text="Guardar Modificación", command=guardar_modificacion, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
			tk.Button(frame, text="Modificar", command=modificar_plato, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
		else:
			tk.messagebox.showerror("Error", "El plato especificado no existe.")
	tk.Button(frame, text="Obtener Detalle", command=obtener_datos_modificar, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	tk.Button(frame, text="Ver", command=mostrar_platos_menus, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

# ------------------------------------------- ELIMINAR PLATO --------------------------------------------------------
def eliminar_plato(frame):
	tk.Label(frame, text="Nombre del plato a eliminar:", bg='orange', fg='black').pack()
	entry_nombre_eliminar = tk.Entry(frame, bg='yellow', fg='black', justify="center", font="Lustria")
	entry_nombre_eliminar.pack()

	def confirmar_eliminacion():
		nombre_plato = entry_nombre_eliminar.get()
		confirmacion = tk.messagebox.askyesno("Confirmación", f"¿Está seguro de querer eliminar el plato '{nombre_plato}'?")
		if confirmacion:
			cursor.execute("DELETE FROM Platos WHERE Nombre = ?", (nombre_plato,))
			base.commit()
			tk.messagebox.showinfo("Éxito", "Plato eliminado correctamente.")

	tk.Button(frame, text="Confirmar", command=confirmar_eliminacion, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	tk.Button(frame, text="        Ver        ", command=mostrar_platos_menus, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

#_________________________________ M e n u 
def ver_carta(frame):
	def cargar_carta():
		for row in table.get_children():
			table.delete(row)
		cursor.execute("SELECT Nombre, Precio_Final, Especificaciones FROM Platos WHERE Implementado_menu = 'Si'")
		platos = cursor.fetchall()
		for plato in platos:
			nombre = plato[0]
			precio_final = plato[1]
			Especificaciones = plato[2]
			table.insert('', 'end', text=nombre, values=(precio_final, Especificaciones))

	table = ttk.Treeview(frame)
	table['columns'] = ('Precio Final', "Especificaciones")
	table.heading('#0', text='Plato')
	table.heading('Precio Final', text='Precio Final')
	table.heading('Especificaciones', text = 'Especificaciones')

	table.pack(padx=10, pady=10)
	btn_cargar = tk.Button(frame, text="Cargar Carta", command=cargar_carta, bg='orange', fg='black', font="Lustria", activebackground="orange") 
	btn_cargar.pack(pady=10)

def menu_modificar_precios(frame):
	def modificar_precio_plato_individual():
		def guardar_modificacion():
			nombre_plato = entry_nombre_plato.get()
			nuevo_precio = float(entry_nuevo_precio.get())
			cursor.execute("UPDATE Platos SET Precio_Final = ? WHERE Nombre = ?", (nuevo_precio, nombre_plato))
			base.commit()
			tk.messagebox.showinfo("Exito", f"Se ha modificado el precio del plato '{nombre_plato}' correctamente.")

		tk.Label(frame, text="Nombre del plato:", bg='orange', fg='black').pack()
		entry_nombre_plato = tk.Entry(frame,bg='orange', fg='black', justify="center", font="Lustria")
		entry_nombre_plato.pack()
		tk.Label(frame, text="Nuevo precio:", bg='orange', fg='black').pack()
		entry_nuevo_precio = tk.Entry(frame,bg='orange', fg='black', justify="center", font="Lustria")
		entry_nuevo_precio.pack()
		tk.Button(frame, text="Guardar", command=guardar_modificacion, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()
	def modificar_precio_todos():
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
		tk.Label(frame, text="Porcentaje de aumento para todos los platos (%):", bg='orange', fg='black').pack()
		entry_porcentaje = tk.Entry(frame,bg='orange', fg='black', justify="center", font="Lustria")
		entry_porcentaje.pack()
		tk.Button(frame, text="Guardar", command=guardar_modificacion, bg='orange', fg='black', font="Lustria", activebackground="orange").pack()

	tk.Button(frame, text="Modificar Precio de Plato Individual", command=modificar_precio_plato_individual, bg='orange', fg='black', font="Lustria", activebackground="orange").pack(pady=10)
	tk.Button(frame, text="Modificar Precio de Todos los Platos", command=modificar_precio_todos, bg='orange', fg='black', font="Lustria", activebackground="orange").pack(pady=10)
	tk.Button(frame, text="        Ver        ", bg='orange', fg='black', font="Lustria", activebackground="orange").pack()


def crear_menu(menu_principal, nombre_menu, opciones, root):
	submenu = tk.Menu(menu_principal)
	menu_principal.add_cascade(label=nombre_menu, menu=submenu)

	for opcion in opciones:
		if opcion == "Ingresar":
			submenu.add_command(label=opcion, command=lambda: mostrar_frame("Ingresar", nombre_menu ,root))
		elif opcion == "Ver":
			submenu.add_command(label=opcion, command=lambda: mostrar_frame("Ver", nombre_menu ,root))
		elif opcion == "Modificar":
			submenu.add_command(label=opcion,command=lambda: mostrar_frame("Modificar", nombre_menu ,root))
		elif opcion == "Eliminar":
			submenu.add_command(label=opcion, command=lambda: mostrar_frame("Eliminar", nombre_menu ,root))
		else:
			submenu.add_command(label=opcion)

	submenu.add_separator()
	submenu.add_command(label="Salir", command=root.quit)

def mostrar_frame(opcion,menu ,root):
	global current_frame
	if current_frame is not None:
		current_frame.pack_forget()
	current_frame = tk.Frame(root)
	current_frame.config(bg="orange")
	current_frame.pack(fill="both", expand=True)

	if menu == "Ingredientes":
		if opcion == "Ingresar":
			ingresar_ingrediente(current_frame)
		elif opcion == "Ver":
			ver_ingrediente(current_frame)
		elif opcion == "Modificar":
			sisisi(current_frame)
		elif opcion == "Eliminar":
			eliminar_ingredientes(current_frame)

	elif menu == "Recetas":
		if opcion == "Ingresar":
			ingresar_receta(current_frame)
		if opcion == "Ver":
			mostrar_receta(current_frame)
		if opcion == "Modificar":
			modificar_receta(current_frame)
		if opcion == "Eliminar":
			eliminar_receta(current_frame)

	elif menu == "Platos":
		if opcion == "Ingresar":
			ingresar_plato(current_frame)
		if opcion == "Ver":
			mostrar_platos_menu(current_frame)
		if opcion == "Modificar":
			mostrar_detalle_modificar(current_frame)
		if opcion == "Eliminar":
			eliminar_plato(current_frame)

	elif menu == "Carta":
		if opcion == "Ver":
			ver_carta(current_frame)
		if opcion == "Modificar":
			menu_modificar_precios(current_frame)

def main():
	root = tk.Tk()
	root.title("RecipeCostX")
	root.geometry("900x800")
		
	global current_frame
	current_frame = None

	menu = tk.Menu(root, bg='orange')
	root.config(bg='orange',menu=menu)

	opciones_menu = ["Ingresar", "Ver", "Modificar", "Eliminar"]
	opc_menu_carta = ["Ver", "Modificar"]
	menus = [("Ingredientes", opciones_menu), ("Recetas", opciones_menu), ("Platos", opciones_menu), ("Carta", opc_menu_carta)]

	for nombre_menu, opciones in menus:
		crear_menu(menu, nombre_menu, opciones, root)
	root.mainloop()

if __name__ == "__main__":
	main()