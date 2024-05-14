
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import *
from PIL import ImageTk, Image
#from pyperclip import *

base = sqlite3.connect('sistemaa.db')
cursor = base.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS INGREDIENTES  ( Codigo_Ingrediente INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Unidad_Medida VARCHAR(50), Cantidad NUMBER, Precio NUMBER, Detalles TEXT )')
cursor.execute('CREATE TABLE IF NOT EXISTS RECETAS (Codigo_Receta INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Costo FLOAT, Codigo_Ingrediente INT, Cantidad_De_Cada_Ingrediente NUMBER, FOREIGN KEY (Codigo_Ingrediente) REFERENCES INGREDIENTES(Codigo_Ingrediente))')
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
# entry:  ,bg="#FFBFF1", justify="center", font="Segoe_UI"
# label:  ,bg='#FFE3F3', font="Segoe_UI
# button: ,bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4"
def ingresar_ingrediente(frame):
	opciones_unidades = ["Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)",
						"Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
						"Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
						"Cucharaditas (tsp)", "Tazas (cup)"]
	tk.Label(frame, text="Nombre del ingrediente:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_nombre = tk.Entry(frame, bg="#FFBFF1", justify="center", font="Segoe_UI")
	entry_nombre.pack()
	tk.Label(frame, text="Cantidad:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_cantidad = tk.Entry(frame, bg="#FFBFF1", font="Segoe_UI")
	entry_cantidad.pack()
	tk.Label(frame, text="Unidad de medida:", bg='#FFE3F3', font="Segoe_UI").pack()
	variable_unidad = tk.StringVar(frame)
	variable_unidad.set(opciones_unidades[0])
	menu_unidad = tk.OptionMenu(frame, variable_unidad, *opciones_unidades)
	menu_unidad.config(bg="#FFE3F3", font="Segoe_UI", activebackground="#FFBFF1", relief="groove")
	menu_unidad.pack()
	menu_unidad["menu"].config(bg="#FFBFF1", font="Segoe_UI")

	tk.Label(frame, text="Precio por unidad:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_precio = tk.Entry(frame, bg='#FFBFF1', font="Segoe_UI")
	entry_precio.pack()

	def guardar_ingrediente():
		nombre = entry_nombre.get()
		cantidad = float(entry_cantidad.get())
		unidad = variable_unidad.get()
		precio = float(entry_precio.get())
		cursor.execute("INSERT INTO Ingredientes (Nombre, Unidad_Medida, Cantidad, Precio) VALUES (?, ?, ?, ?)",
					   (nombre, unidad, cantidad, precio))
		base.commit()
		frame.forget()
	separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
	separator.pack(fill=tk.X, pady=10)
	tk.Button(frame, text="Guardar", command=guardar_ingrediente, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()

def ver_ingrediente(frame):
	cursor.execute("SELECT Codigo_Ingrediente, Nombre, Cantidad, Unidad_Medida, Precio FROM Ingredientes")
	ingredientes = cursor.fetchall()
	if not ingredientes:
		print("No hay ingredientes para mostrar.")
		return
	
	# Crear un estilo personalizado
	estilo = ttk.Style()
	estilo.theme_use('clam')  # Asegura que el tema base sea compatible
	estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0, background='#FFBFF1', font=('Lucida Console', 9))

	tabla = ttk.Treeview(frame, columns=("Código", "Nombre", "Cantidad", "Unidad de Medida", "Precio por Unidad"), show="headings", style="mystyle.Treeview")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Cantidad", text="Cantidad")
	tabla.heading("Unidad de Medida", text="Unidad de Medida")
	tabla.heading("Precio por Unidad", text="Precio por Unidad")
	tabla.pack(fill=tk.BOTH, expand=True)  # Asegura que el Treeview ocupe todo el espacio disponible
	
	scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
	tabla.configure(yscrollcommand=scrollbar.set)
	scrollbar.pack(side="right", fill="y")
	
	for ingrediente in ingredientes:
		codigo, nombre, cantidad, unidad, precio = ingrediente
		precio_por_unidad = precio / cantidad
		tabla.insert("", "end", values=(codigo, nombre, cantidad, unidad, precio_por_unidad))
	tabla.pack(padx=20, pady=20)

def ver_ingredientes(frame):

	cursor.execute("SELECT Codigo_Ingrediente, Nombre, Cantidad, Unidad_Medida, Precio FROM Ingredientes")
	ingredientes = cursor.fetchall()
	if not ingredientes:
		tk.Label(frame, text="No hay ingredientes para mostrar.").pack()
		return

	# Crear un estilo personalizado
	estilo = ttk.Style()
	estilo.theme_use('clam') 
	estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0, background='#FFE3F3', font=('Lucida Console', 9))

	tabla = ttk.Treeview(frame, columns=("Código", "Nombre", "Cantidad", "Unidad de Medida", "Precio por Unidad"), show="headings", selectmode='browse', style="mystyle.Treeview")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Cantidad", text="Cantidad")
	tabla.heading("Unidad de Medida", text="Unidad de Medida")
	tabla.heading("Precio por Unidad", text="Precio por Unidad")
	tabla.pack(fill=tk.BOTH, expand=True)  

	for ingrediente in ingredientes:
		codigo, nombre, cantidad, unidad, precio = ingrediente
		precio_por_unidad = precio / cantidad
		tabla.insert("", "end", values=(codigo, nombre, cantidad, unidad, precio_por_unidad))

	tabla.pack(padx=20, pady=20)
	
def sisisi(frame):
	tk.Label(frame, text="Código del ingrediente a modificar:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_codigo_modificar = tk.Entry(frame, bg="#FFBFF1", justify="center", font="Segoe_UI")
	entry_codigo_modificar.pack()

	def mostrar_detalle_modificar():
		codigo_modificar = int(entry_codigo_modificar.get())
		cursor.execute("SELECT * FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_modificar,))
		resultado_verificacion = cursor.fetchone()
		if not resultado_verificacion:
			tk.messagebox.showerror("Error", "No se encontró ningún ingrediente con ese código.")
		else:
			tk.Label(frame, text=f"Nombre: {resultado_verificacion[1]}", bg='#FFE3F3', font="Segoe_UI").pack()
			tk.Label(frame, text=f"Cantidad: {resultado_verificacion[3]}", bg='#FFE3F3', font="Segoe_UI").pack()
			tk.Label(frame, text=f"Unidad de Medida: {resultado_verificacion[2]}", bg='#FFE3F3', font="Segoe_UI").pack()
			tk.Label(frame, text=f"Precio: {resultado_verificacion[4]}", bg='#FFE3F3', font="Segoe_UI").pack()
			opciones_modificar = ["Nombre", "Cantidad", "Unidad de Medida", "Precio", "Todos"]
			variable_opcion_modificar = tk.StringVar(frame)
			variable_opcion_modificar.set(opciones_modificar[0])  # Valor predeterminado
			option_menu_modificar = tk.OptionMenu(frame, variable_opcion_modificar, *opciones_modificar)
			option_menu_modificar.config(bg="#FFE3F3", font="Segoe_UI", activebackground="#FFBFF1", relief="groove")
			option_menu_modificar.pack()
			option_menu_modificar["menu"].config(bg="#FFBFF1", font="Segoe_UI")
			entry_nuevo_valor = tk.Entry(frame, bg="#FFBFF1", font="Segoe_UI")
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
					nueva_unidad = tk.StringVar(frame)
					nueva_unidad.set(resultado_verificacion[3])  # Establecer el valor actual como predeterminado
					menu_unidades = tk.OptionMenu(frame, nueva_unidad, *opciones_unidades)
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
				
				separator = ttk.Separator(frame, orient=tk.HORIZONTAL)
				separator.pack(fill=tk.X, pady=10)
				boton_confirmar = tk.Button(frame, text="Confirmar", command=guardar_modificacion)
				boton_confirmar.pack()

			boton_guardar_cambios = tk.Button(frame, text="Guardar Cambios", command=confirmar_modificacion, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4")
			boton_guardar_cambios.pack()
	tk.Button(frame, text="Mostrar Detalle", command=mostrar_detalle_modificar, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
	tk.Button(frame, text="        Ver        ",command=ver_ingredientes, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()

def eliminar_ingredientes(frame):
	tk.Label(frame, text="Código del ingrediente a eliminar:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_codigo_eliminar = tk.Entry(frame, bg="#FFBFF1", justify="center", font="Segoe_UI")
	entry_codigo_eliminar.pack()
	def confirmar_eliminacion():
		codigo_eliminar = int(entry_codigo_eliminar.get())
		cursor.execute("DELETE FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_eliminar,))
		base.commit()
		tk.messagebox.showinfo("Éxito", "El ingrediente ha sido eliminado correctamente.")
		frame.destroy()
	boton_confirmar_eliminacion = tk.Button(frame, text="Confirmar Eliminación", command=confirmar_eliminacion, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4")
	boton_confirmar_eliminacion.pack()
	tk.Button(frame, text="        Ver        ",command=ver_ingredientes, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()

#-----------------------------------------------------------------------------------------------------------------------------

def ingresar_receta(frame):
	ingredientes_receta = []
	ingredientes_codigos = []
	def calcular_costo_total(ingredientes_receta):
		costo_total = 0
		for nombre, cantidad in ingredientes_receta:
			cursor.execute("SELECT Precio FROM Ingredientes WHERE Nombre = ?", (nombre,))
			precio_ingrediente = cursor.fetchone()
			if precio_ingrediente:
				precio_ingrediente = precio_ingrediente[0]
				costo_ingrediente = precio_ingrediente * cantidad
				costo_total += costo_ingrediente
			else:
				messagebox.showerror("Error", f"No se encontró el precio para el ingrediente {nombre}.")
		return costo_total
	def agregar_ingrediente():

		codigo_ingrediente = int(entry_codigo.get())
		cantidad_ingrediente = float(entry_cantidad.get())
		cursor.execute("SELECT Nombre FROM INGREDIENTES WHERE Codigo_Ingrediente = ?", (codigo_ingrediente,))
		nombre_ing = cursor.fetchone()[0]
		ingredientes_receta.append((nombre_ing, cantidad_ingrediente))
		ingredientes_codigos.append(codigo_ingrediente)
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
		codigo_receta = cursor.lastrowid
		cursor.execute("INSERT INTO RECETAS_INGREDIENTES (Codigo_Receta, Codigo_Ingrediente) VALUES (?,?)", (codigo_receta,ingredientes_codigos[-1]))
		base.commit()
		tk.messagebox.showinfo("Éxito", "Receta ingresada correctamente.")

	tk.Label(frame, text="Nombre de la receta:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_nombre_receta = tk.Entry(frame, bg='#FFBFF1', font="Segoe_UI")
	entry_nombre_receta.pack()
	tk.Label(frame, text="Código del ingrediente:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_codigo = tk.Entry(frame, bg='#FFBFF1', font="Segoe_UI")
	entry_codigo.pack()
	tk.Label(frame, text="Cantidad del ingrediente:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_cantidad = tk.Entry(frame, bg='#FFBFF1', font="Segoe_UI")
	entry_cantidad.pack()
	unidad = tk.StringVar(frame)
	unidades = [
		"Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)",
		"Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
		"Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
		"Cucharaditas (tsp)", "Tazas (cup)"
	]
	unidad.set(unidades[0])
	menu_uni = tk.OptionMenu(frame, unidad, *unidades)
	menu_uni.pack()
	menu_uni.config(bg="#FFE3F3", font="Segoe_UI", activebackground="#FFBFF1", relief="groove")
	menu_uni["menu"].config(bg="#FFBFF1", font="Segoe_UI")
	tk.Button(frame, text="Agregar Ingrediente", command=agregar_ingrediente, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
	listbox_ingredientes = tk.Listbox(frame, bg="#FFBFF1", font="Segoe_UI")
	listbox_ingredientes.pack()
	tk.Button(frame, text="Guardar Receta", command=guardar_receta, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()

def obtener_recetas_con_costo():
	try:
		consulta = """
		SELECT Codigo_Receta, Nombre, 
			   (SELECT SUM(I.Precio * R.Cantidad_De_Cada_Ingrediente) 
				FROM INGREDIENTES I 
				WHERE I.Codigo_Ingrediente = R.Codigo_Ingrediente) AS Costo_Total
		FROM RECETAS R
		"""
		cursor.execute(consulta)
		recetas = cursor.fetchall()
		
		consulta = "SELECT PRECIO FROM INGREDIENTES"
		cursor.execute(consulta)
		precio = cursor.fetchone()[0]
		print(precio)

		consulta = "SELECT CANTIDAD_DE_CADA_INGREDIENTE FROM RECETAS"
		cursor.execute(consulta)
		cantidad_de_cada = cursor.fetchone()[0]
		print(cantidad_de_cada)

		costo_total = int(precio) * int(cantidad_de_cada)
		print(f"costo_total = {costo_total}")
		return recetas, costo_total
	except Exception as e:
		raise e

def obtener_ingredientes_por_receta(id_receta):
	try:
		consulta = """
		SELECT I.Nombre, I.Cantidad, I.Precio
		FROM INGREDIENTES I
		JOIN RECETAS_INGREDIENTES RI ON I.Codigo_Ingrediente = RI.Codigo_Ingrediente
		WHERE RI.Codigo_Receta = ?
		"""
		cursor.execute(consulta, (id_receta,))
		ingredientes = cursor.fetchall()
		return ingredientes
	except Exception as e:
		print(f"Error fetching ingredients: {e}")  # Log the error
		raise e

def calcular_costo_ingredientes(ingredientes):
	costo_total = 0
	for ingrediente in ingredientes:
		nombre, cantidad, precio_unitario = ingrediente
		costo_total += cantidad * precio_unitario
	return costo_total

def mostrar_recetas_con_costo(frame):
	try:
		recetas = obtener_recetas_con_costo()
		if recetas:

			# Crear un estilo personalizado
			estilo = ttk.Style()
			estilo.theme_use('clam')  # Asegura que el tema base sea compatible
			estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0, background='#FFBFF1', font=('Lucida Console', 9))

			# Crear la tabla dentro del frame interior
			# background='#FFBFF1', font=('Lucida Console', 9)
			#
			tabla = ttk.Treeview(frame, columns=("Código Receta", "Nombre Receta", "Costo Receta" ,"Ingredientes"), style="mystyle.Treeview")
			tabla.heading("#0", text="Índice")
			tabla.heading("Código Receta", text="Código Receta")
			tabla.heading("Nombre Receta", text="Nombre Receta")
			tabla.heading("Costo Receta", text="Costo Receta")
			tabla.heading("Ingredientes", text="Ingredientes")            
			tabla.pack(fill="both", expand=True)

			scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
			tabla.configure(yscrollcommand=scrollbar.set)
			scrollbar.pack(side="right", fill="y")
			# Main script starts here
			ingredientes = []
			costo_ingredientes = 0

			for index, receta in enumerate(recetas, start=1):
				id_receta = receta[0]
				ingredientes = obtener_ingredientes_por_receta(id_receta)
				costo_ingredientes = calcular_costo_ingredientes(ingredientes)
				tabla.insert('', 'end', text=str(index), values=(receta[0], receta[1], costo_ingredientes,ingredientes))
		else:
			messagebox.showerror("Error", "No hay recetas disponibles.")
	except Exception as e:
		messagebox.showerror("Error", f"Error al mostrar recetas con costo: {e}")

def anglosajona():
	def obtener_recetas_con_costo():
		try:
			consulta = "SELECT * FROM RECETAS"
			cursor.execute(consulta)
			recetas = cursor.fetchall()
			return recetas
		except Exception as e:
			raise e

	def obtener_ingredientes_por_receta(id_receta):
		try:
			consulta = """
			SELECT I.Nombre, RI.Cantidad, I.Precio
			FROM INGREDIENTES I
			JOIN RECETAS_INGREDIENTES RI ON I.Codigo_Ingrediente = RI.Codigo_Ingrediente
			WHERE RI.Codigo_Receta = ?
			"""
			cursor.execute(consulta, (id_receta,))
			ingredientes = cursor.fetchall()
			return ingredientes
		except Exception as e:
			raise e

	def calcular_costo_ingredientes(ingredientes):
		costo_total = 0
		for ingrediente in ingredientes:
			nombre, cantidad, precio_unitario = ingrediente
			costo_total += cantidad * precio_unitario
		return costo_total

	def mostrar_recetas_con_costo_en_toplevel(root):
		try:
			recetas = obtener_recetas_con_costo()
			if recetas:
				toplevel = tk.Toplevel(root)

				estilo = ttk.Style()
				estilo.theme_use('clam')
				estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0, background='#FFE3F3', font=('Lucida Console', 9))

				tabla = ttk.Treeview(toplevel, columns=("Código Receta", "Nombre Receta", "Costo Receta", "Ingredientes"), style="mystyle.Treeview")
				tabla.heading("#0", text="Índice")
				tabla.heading("Código Receta", text="Código Receta")
				tabla.heading("Nombre Receta", text="Nombre Receta")
				tabla.heading("Costo Receta", text="Costo Receta")
				tabla.heading("Ingredientes", text="Ingredientes")
				tabla.pack(fill="both", expand=True)

				for index, receta in enumerate(recetas, start=1):
					id_receta = receta[0]
					ingredientes = obtener_ingredientes_por_receta(id_receta)
					costo_ingredientes = calcular_costo_ingredientes(ingredientes)
					ingredientes_str = ', '.join([f"{ing[0]} ({ing[1]} unidades)" for ing in ingredientes])
					tabla.insert('', 'end', text=str(index), values=(receta[0], receta[1], costo_ingredientes, ingredientes_str))
			else:
				messagebox.showinfo("Información", "No hay recetas disponibles.")
		except Exception as e:
			messagebox.showerror("Error", f"Error al mostrar recetas con costo: {e}")
	root = tk.Tk()
	mostrar_recetas_con_costo_en_toplevel(root)
	root.mainloop()

def modificar_receta(frame):
	tk.Label(frame, text="Código de la receta a modificar:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_codigo_modificar = tk.Entry(frame, bg="#FFBFF1", font="Segoe_UI")
	entry_codigo_modificar.pack()
	def mostrar_detalle_modificar():
		codigo_receta = entry_codigo_modificar.get()
		cursor.execute("SELECT * FROM Recetas WHERE Codigo_Receta = ?", (codigo_receta,))
		receta = cursor.fetchone()
		print(f"receta {receta}")
		if receta:
			cursor.execute("SELECT Nombre, Cantidad_De_Cada_Ingrediente FROM Recetas WHERE Codigo_Ingrediente IN (SELECT Codigo_Ingrediente FROM Ingredientes)")
			ingredientes = cursor.fetchall()
			detalle_texto = "Ingredientes:\n"
			for ingrediente in ingredientes:
				detalle_texto += f"{ingrediente[0]} - {ingrediente[1]}\n"
			tk.Label(frame, text=detalle_texto, bg='#FFE3F3', font="Segoe_UI").pack()
			tk.Label(frame, text="Nuevo nombre de la receta:", bg='#FFE3F3', font="Segoe_UI").pack()
			entry_nuevo_nombre = tk.Entry(frame, bg="#FFBFF1", font="Segoe_UI")
			entry_nuevo_nombre.pack()
			tk.Label(frame, text="Nuevo costo de la receta:", bg='#FFE3F3', font="Segoe_UI").pack()
			entry_nuevo_costo = tk.Entry(frame, bg="#FFBFF1", font="Segoe_UI")
			entry_nuevo_costo.pack()
			tk.Label(frame, text="Nuevo código de ingrediente:", bg='#FFE3F3', font="Segoe_UI").pack()
			entry_nuevo_codigo_ingrediente = tk.Entry(frame, bg="#FFBFF1", font="Segoe_UI")
			entry_nuevo_codigo_ingrediente.pack()
			tk.Label(frame, text="Nueva cantidad de cada ingrediente:", bg='#FFE3F3', font="Segoe_UI").pack()
			entry_nueva_cantidad_ingrediente = tk.Entry(frame, bg="#FFBFF1", font="Segoe_UI")
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
			tk.Button(frame, text="Confirmar", command=confirmar_modificacion, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
		else:
			tk.messagebox.showerror("Error", "La receta especificada no existe.")
	tk.Button(frame, text="Mostrar Detalle", command=mostrar_detalle_modificar, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
	tk.Button(frame, text="        Ver        ",command=anglosajona, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()

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

	tk.Label(frame, text="Código de la receta a eliminar:", bg='#FFE3F3', font="Segoe_UI").pack()
	entry_codigo_eliminar = tk.Entry(frame, bg="#FFBFF1", font="Segoe_UI")
	entry_codigo_eliminar.pack()

	tk.Button(frame, text="Confirmar", command=confirmar_eliminacion, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
	tk.Button(frame, text="        Ver        ",command=anglosajona, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()

#..................
def ingresar_plato(frame):
	implementado_menu = tk.BooleanVar()
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
				
	def guardar_plato(entry_nombre, entry_ganancia, implementar_menu_check, entry_precio, detalles):
		nombre = entry_nombre.get()
		ganancia_porcentaje = float(entry_ganancia.get())
		precio_final = entry_precio.get()
		detalles_plato = detalles.get()
		if nombre and ganancia_porcentaje and precio_final:
			implementado_menu_value = implementado_menu.get()
			if implementado_menu_value == 1:
				implementado_menu_value = "Si"
			else:
				implementado_menu_value = "No"

			cursor.execute("INSERT INTO PLATOS (Nombre, Ganancia, Precio_Final, Implementado_Menu, Especificaciones) VALUES (?, ?, ?, ?, ?)",(nombre, ganancia_porcentaje, precio_final, implementado_menu_value, detalles_plato))
			base.commit()
			messagebox.showinfo("Éxito", "Plato ingresado correctamente.")
		else:
			messagebox.showinfo("Error", "Por favor completa todos los campos obligatorios.")
	nombre_label = tk.Label(frame, text="Nombre del Plato:",bg='#FFE3F3', font="Segoe_UI")
	nombre_label.grid(row=0, column=0, padx=10, pady=10 )

	nombre_entry = tk.Entry(frame,bg="#FFBFF1", justify="center", font="Segoe_UI")
	nombre_entry.grid(row=0, column=1, padx=10, pady=10 )

	ganancia_label = tk.Label(frame, text="Ganancia:",bg='#FFE3F3', font="Segoe_UI")
	ganancia_label.grid(row=1, column=0, padx=10, pady=10 )

	ganancia_entry = tk.Entry(frame,bg="#FFBFF1", justify="center", font="Segoe_UI")
	ganancia_entry.grid(row=1, column=1, padx=10, pady=10)

	precio_label = tk.Label(frame, text="Precio del Plato:",bg='#FFE3F3', font="Segoe_UI")
	precio_label.grid(row=2, column=0, padx=10, pady=10)

	precio_entry = tk.Entry(frame,bg="#FFBFF1", justify="center", font="Segoe_UI")
	precio_entry.grid(row=2, column=1, padx=10, pady=10 )

	detalles_lab = tk.Label(frame, text="Detalles del plato",bg='#FFE3F3', font="Segoe_UI")
	detalles_lab.grid(row=3, column=0, padx=10, pady=10)

	detalles = tk.Entry(frame,bg="#FFBFF1", justify="center", font="Segoe_UI")
	detalles.grid(row=3, column=1, padx=10, pady=10)

	implementar_menu_lab = tk.Label(frame, text= "Implementar al menu",bg='#FFE3F3', font="Segoe_UI").grid(row=4, column=0, padx=10, pady=10)

	implementar_menu_check = tk.Checkbutton(frame, text="Implementar menu", offvalue="No", onvalue="Si", variable=implementado_menu,bg='#FFE3F3', font="Segoe_UI")
	implementar_menu_check.grid(row=4, column=1, padx=10, pady=10)

	guardar_button = tk.Button(frame, text="Guardar",bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4", command=lambda: guardar_plato(nombre_entry, ganancia_entry, implementar_menu_check, precio_entry, detalles))
	guardar_button.grid(row=5, column=0, padx=10, pady=10)
	implementar_menu_button = tk.Button(frame, text="Verificar si esta en el Menú",bg='#FFE3F3', font="Segoe_UI_Black",activebackground="#F0A7C4",command=implementar_en_menu)
	implementar_menu_button.grid(row=5, column=1, padx=10, pady=10)

def mostrar_platos_menu(frame):
    cursor.execute("SELECT * FROM Platos")
    platos = cursor.fetchall()
    tabla = ttk.Treeview(frame, columns=("Nombre", "Ganancia", "Precio Final", "Implementado en Menú", "Especificaciones"))
    tabla.heading("#0", text="Índice")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Ganancia", text="Ganancia")
    tabla.heading("Precio Final", text="Precio Final")
    tabla.heading("Implementado en Menú", text="Implementado en Menú")
    tabla.heading("Especificaciones", text="Especificaciones")
    for index, plato in enumerate(platos, start=1):
        tabla.insert('', 'end', text=str(index), values=(plato[1], plato[2], plato[3], plato[4], plato[5]))
    tabla.pack(fill="both", expand=True)
	



def mostrar_platos_menus():
	rootT = tk.Tk()
	rootT.title("Aplicación CRUD")
	rootT.geometry("900x800")
	cursor.execute("SELECT * FROM Platos")
	platos = cursor.fetchall()
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

def mostrar_detalle_modificar(frame):
    tk.Label(frame, text="Nombre del plato a modificar:", bg='#FFE3F3', font="Segoe_UI").pack()
    entry_nombre_modificar = tk.Entry(frame, bg="#FFBFF1", justify="center", font="Segoe_UI")
    entry_nombre_modificar.pack()
    implementado_menu = tk.StringVar()
    implementado_menu.set("No")  # Por defecto se establece en No
    def obtener_datos_modificar():
        nombre_plato = entry_nombre_modificar.get()
        cursor.execute("SELECT * FROM Platos WHERE Nombre = ?", (nombre_plato,))
        plato = cursor.fetchone()
        if plato:
            tk.Label(frame, text=f"Nombre: {plato[1]}", bg='#FFE3F3', font="Segoe_UI").pack()
            tk.Label(frame, text=f"Ganancia: {plato[2]}", bg='#FFE3F3', font="Segoe_UI").pack()
            tk.Label(frame, text=f"Precio Final: {plato[3]}", bg='#FFE3F3', font="Segoe_UI").pack()
            def modificar_plato():
                tk.Label(frame, text="Nuevo valor para Ganancia:", bg='#FFE3F3', font="Segoe_UI").pack()
                entry_ganancia = tk.Entry(frame, bg="#FFBFF1", justify="center", font="Segoe_UI")
                entry_ganancia.pack()
                tk.Label(frame, text="Nuevo valor para Precio Final:", bg='#FFE3F3', font="Segoe_UI").pack()
                entry_precio = tk.Entry(frame, bg="#FFBFF1", justify="center", font="Segoe_UI")
                entry_precio.pack()
                tk.Label(frame, text="¿Modificar implementación en menú?", bg='#FFE3F3', font="Segoe_UI").pack()
                tk.Radiobutton(frame, text="Sí", variable=implementado_menu, value="Si", bg='#FFE3F3', font="Segoe_UI").pack()
                tk.Radiobutton(frame, text="No", variable=implementado_menu, value="No", bg='#FFE3F3', font="Segoe_UI").pack()
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
                tk.Button(frame, text="Guardar Modificación", command=guardar_modificacion, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
            tk.Button(frame, text="Modificar", command=modificar_plato, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
        else:
            tk.messagebox.showerror("Error", "El plato especificado no existe.")
    tk.Button(frame, text="Obtener Detalle", command=obtener_datos_modificar, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
    tk.Button(frame, text="Ver", command=mostrar_platos_menus, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()

def eliminar_plato(frame):
    tk.Label(frame, text="Nombre del plato a eliminar:", bg='#FFE3F3', font="Segoe_UI").pack()
    entry_nombre_eliminar = tk.Entry(frame, bg="#FFBFF1", justify="center", font="Segoe_UI")
    entry_nombre_eliminar.pack()

    def confirmar_eliminacion():
        nombre_plato = entry_nombre_eliminar.get()
        confirmacion = tk.messagebox.askyesno("Confirmación", f"¿Está seguro de querer eliminar el plato '{nombre_plato}'?")
        if confirmacion:
            cursor.execute("DELETE FROM Platos WHERE Nombre = ?", (nombre_plato,))
            base.commit()
            tk.messagebox.showinfo("Éxito", "Plato eliminado correctamente.")

    tk.Button(frame, text="Confirmar", command=confirmar_eliminacion, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()
    tk.Button(frame, text="        Ver        ", command=mostrar_platos_menus, bg='#FFE3F3', font="Segoe_UI_Black", activebackground="#F0A7C4").pack()

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
	btn_cargar = tk.Button(frame, text="Cargar Carta", command=cargar_carta) 
	btn_cargar.pack(pady=10)

def menu_modificar_precios(frame):
	def modificar_precio_plato_individual():
		def guardar_modificacion():
			nombre_plato = entry_nombre_plato.get()
			nuevo_precio = float(entry_nuevo_precio.get())
			cursor.execute("UPDATE Platos SET Precio_Final = ? WHERE Nombre = ?", (nuevo_precio, nombre_plato))
			base.commit()
			tk.messagebox.showinfo("Exito", f"Se ha modificado el precio del plato '{nombre_plato}' correctamente.")

		tk.Label(frame, text="Nombre del plato:").pack()
		entry_nombre_plato = tk.Entry(frame)
		entry_nombre_plato.pack()
		tk.Label(frame, text="Nuevo precio:").pack()
		entry_nuevo_precio = tk.Entry(frame)
		entry_nuevo_precio.pack()
		tk.Button(frame, text="Guardar", command=guardar_modificacion).pack()
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
		tk.Label(frame, text="Porcentaje de aumento para todos los platos (%):").pack()
		entry_porcentaje = tk.Entry(frame)
		entry_porcentaje.pack()
		tk.Button(frame, text="Guardar", command=guardar_modificacion).pack()

	tk.Button(frame, text="Modificar Precio de Plato Individual", command=modificar_precio_plato_individual).pack(pady=10)
	tk.Button(frame, text="Modificar Precio de Todos los Platos", command=modificar_precio_todos).pack(pady=10)
	tk.Button(frame, text="        Ver        ").pack()


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
	current_frame.config(bg="#FFE3F3")
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
			mostrar_recetas_con_costo(current_frame)
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
	root.title("Aplicación CRUD")
	root.geometry("900x800")
		
	global current_frame
	current_frame = None

	menu = tk.Menu(root, bg="#FFBFF1")
	root.config(bg="#FFBFF1", menu=menu)

	opciones_menu = ["Ingresar", "Ver", "Modificar", "Eliminar"]
	opc_menu_carta = ["Ver", "Modificar"]
	menus = [("Ingredientes", opciones_menu), ("Recetas", opciones_menu), ("Platos", opciones_menu), ("Carta", opc_menu_carta)]

	for nombre_menu, opciones in menus:
		crear_menu(menu, nombre_menu, opciones, root)
	root.mainloop()



if __name__ == "__main__":
	main()