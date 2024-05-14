import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

base = sqlite3.connect('sistemaa.db')
cursor = base.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS INGREDIENTES  ( Codigo_Ingrediente INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Unidad_Medida VARCHAR(50), Cantidad NUMBER, Precio NUMBER, Detalles TEXT )')
cursor.execute('CREATE TABLE IF NOT EXISTS RECETAS (Codigo_Receta INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Costo NUMBER, Codigo_Ingrediente INT, Cantidad_De_Cada_Ingrediente NUMBER, FOREIGN KEY (Codigo_Ingrediente) REFERENCES INGREDIENTES(Codigo_Ingrediente))')
cursor.execute('CREATE TABLE IF NOT EXISTS PLATOS ( Nombre VARCHAR(100) PRIMARY KEY, Ganancia NUMBER, Precio_Final NUMBER, Implementado_Menu BOOLEAN , Apto_Veganos BOOLEAN, Apto_Vegetarianos BOOLEAN, Apto_Celiacos BOOLEAN)')
cursor.execute("CREATE TABLE IF NOT EXISTS Menu (Nombre_Plato VARCHAR(100), FOREIGN KEY (Nombre_Plato) REFERENCES Platos(Nombre) ON DELETE CASCADE)")

def ingresar_ingrediente(frame):
	opciones_unidades = ["Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)",
						"Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
						"Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
						"Cucharaditas (tsp)", "Tazas (cup)"]
	tk.Label(frame, text="Nombre del ingrediente:").pack()
	entry_nombre = tk.Entry(frame)
	entry_nombre.pack()
	tk.Label(frame, text="Cantidad:").pack()
	entry_cantidad = tk.Entry(frame)
	entry_cantidad.pack()
	tk.Label(frame, text="Unidad de medida:").pack()
	variable_unidad = tk.StringVar(frame)
	variable_unidad.set(opciones_unidades[0])
	menu_unidad = tk.OptionMenu(frame, variable_unidad, *opciones_unidades)
	menu_unidad.pack()
	tk.Label(frame, text="Precio por unidad:").pack()
	entry_precio = tk.Entry(frame)
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
	tk.Button(frame, text="Guardar", command=guardar_ingrediente).pack()

def ver_ingrediente(frame):
	cursor.execute("SELECT Codigo_Ingrediente, Nombre, Cantidad, Unidad_Medida, Precio FROM Ingredientes")
	ingredientes = cursor.fetchall()
	if not ingredientes:
		print("No hay ingredientes para mostrar.")
		return
	tabla = ttk.Treeview(frame, columns=("Código", "Nombre", "Cantidad", "Unidad de Medida", "Precio por Unidad"), show="headings")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Cantidad", text="Cantidad")
	tabla.heading("Unidad de Medida", text="Unidad de Medida")
	tabla.heading("Precio por Unidad", text="Precio por Unidad")
	for ingrediente in ingredientes:
		codigo, nombre, cantidad, unidad, precio = ingrediente
		precio_por_unidad = precio / cantidad
		tabla.insert("", "end", values=(codigo, nombre, cantidad, unidad, precio_por_unidad))
	tabla.pack(padx=20, pady=20)

def ver_ingredientes():
	# Crear una nueva ventana de nivel superior
	top = tk.Toplevel()
	top.title("Ingredientes")    
	# Conectar a la base de datos (asumiendo que ya tienes una conexión)
	# cursor = sqlite3.connect('tu_base_de_datos.db').cursor()
	# Ejecutar la consulta SQL para obtener los ingredientes
	cursor.execute("SELECT Codigo_Ingrediente, Nombre, Cantidad, Unidad_Medida, Precio FROM Ingredientes")
	ingredientes = cursor.fetchall()
	if not ingredientes:
		tk.Label(top, text="No hay ingredientes para mostrar.").pack()
		return
	# Crear el widget Treeview
	tabla = ttk.Treeview(top, columns=("Código", "Nombre", "Cantidad", "Unidad de Medida", "Precio por Unidad"), show="headings")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Cantidad", text="Cantidad")
	tabla.heading("Unidad de Medida", text="Unidad de Medida")
	tabla.heading("Precio por Unidad", text="Precio por Unidad")
	# Insertar los ingredientes en el Treeview
	for ingrediente in ingredientes:
		codigo, nombre, cantidad, unidad, precio = ingrediente
		precio_por_unidad = precio / cantidad
		tabla.insert("", "end", values=(codigo, nombre, cantidad, unidad, precio_por_unidad))
	
	# Empaquetar el Treeview en la ventana de nivel superior
	tabla.pack(padx=20, pady=20)
	
def sisisi(frame):
	tk.Label(frame, text="Código del ingrediente a modificar:").pack()
	entry_codigo_modificar = tk.Entry(frame)
	entry_codigo_modificar.pack()

	def mostrar_detalle_modificar():
		codigo_modificar = int(entry_codigo_modificar.get())
		cursor.execute("SELECT * FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_modificar,))
		resultado_verificacion = cursor.fetchone()
		if not resultado_verificacion:
			tk.messagebox.showerror("Error", "No se encontró ningún ingrediente con ese código.")
		else:
			tk.Label(frame, text=f"Nombre: {resultado_verificacion[1]}").pack()
			tk.Label(frame, text=f"Cantidad: {resultado_verificacion[3]}").pack()
			tk.Label(frame, text=f"Unidad de Medida: {resultado_verificacion[2]}").pack()
			tk.Label(frame, text=f"Precio: {resultado_verificacion[4]}").pack()
			opciones_modificar = ["Nombre", "Cantidad", "Unidad de Medida", "Precio", "Todos"]
			variable_opcion_modificar = tk.StringVar(frame)
			variable_opcion_modificar.set(opciones_modificar[0])  # Valor predeterminado
			option_menu_modificar = tk.OptionMenu(frame, variable_opcion_modificar, *opciones_modificar)
			option_menu_modificar.pack()
			entry_nuevo_valor = tk.Entry(frame)
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

				boton_confirmar = tk.Button(frame, text="Confirmar", command=guardar_modificacion)
				boton_confirmar.pack()

			boton_guardar_cambios = tk.Button(frame, text="Guardar Cambios", command=confirmar_modificacion)
			boton_guardar_cambios.pack()
	tk.Button(frame, text="Mostrar Detalle", command=mostrar_detalle_modificar).pack()
	tk.Button(frame, text="        Ver        ",command=ver_ingredientes).pack()

def eliminar_ingredientes(frame):
	tk.Label(frame, text="Código del ingrediente a eliminar:").pack()
	entry_codigo_eliminar = tk.Entry(frame)
	entry_codigo_eliminar.pack()
	def confirmar_eliminacion():
		codigo_eliminar = int(entry_codigo_eliminar.get())
		cursor.execute("DELETE FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_eliminar,))
		base.commit()
		tk.messagebox.showinfo("Éxito", "El ingrediente ha sido eliminado correctamente.")
		frame.destroy()
	boton_confirmar_eliminacion = tk.Button(frame, text="Confirmar Eliminación", command=confirmar_eliminacion)
	boton_confirmar_eliminacion.pack()
	tk.Button(frame, text="        Ver        ",command=ver_ingredientes).pack()

#-----------------------------------------------------------------------------------------------------------------------------

def ingresar_receta(frame):
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

	tk.Label(frame, text="Nombre de la receta:").pack()
	entry_nombre_receta = tk.Entry(frame)
	entry_nombre_receta.pack()
	tk.Label(frame, text="Código del ingrediente:").pack()
	entry_codigo = tk.Entry(frame)
	entry_codigo.pack()
	tk.Label(frame, text="Cantidad del ingrediente:").pack()
	entry_cantidad = tk.Entry(frame)
	entry_cantidad.pack()
	unidad = tk.StringVar(frame)
	unidades = [
		"Gramos (g)", "Kilogramos (kg)", "Miligramos (mg)", "Libras (lb)", "Onzas (oz)",
		"Mililitros (ml)", "Litros (l)", "Centilitros (cl)", "Onzas fluidas (fl oz)",
		"Pintas (pt)", "Cuartos de galón (qt)", "Galones (gal)", "Cucharadas (tbsp)",
		"Cucharaditas (tsp)", "Tazas (cup)"
	]
	unidad.set(unidades[0])
	tk.OptionMenu(frame, unidad, *unidades).pack()
	tk.Button(frame, text="Agregar Ingrediente", command=agregar_ingrediente).pack()
	listbox_ingredientes = tk.Listbox(frame)
	listbox_ingredientes.pack()
	tk.Button(frame, text="Guardar Receta", command=guardar_receta).pack()

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
		SELECT I.Nombre, R.Cantidad_De_Cada_Ingrediente, I.Precio
		FROM INGREDIENTES I
		JOIN RECETAS R ON I.Codigo_Ingrediente = R.Codigo_Ingrediente
		WHERE R.Codigo_Receta = ?
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

def mostrar_recetas_con_costo(frame):
	try:
		recetas = obtener_recetas_con_costo()
		if recetas:
			# Crear un frame dentro del frame principal para contener la tabla y la barra de desplazamiento
			inner_frame = tk.Frame(frame)
			inner_frame.pack(fill="both", expand=True)

			# Crear un canvas para la tabla y la barra de desplazamiento
			canvas = tk.Canvas(inner_frame)
			canvas.pack(side="left", fill="both", expand=True)

			# Agregar una barra de desplazamiento al canvas
			scrollbar = ttk.Scrollbar(inner_frame, orient="vertical", command=canvas.yview)
			scrollbar.pack(side="right", fill="y")

			# Configurar el canvas para que funcione con la barra de desplazamiento
			canvas.configure(yscrollcommand=scrollbar.set)
			canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

			# Crear un nuevo frame interior para contener la tabla
			inner_canvas = tk.Frame(canvas)
			canvas.create_window((0, 0), window=inner_canvas, anchor="nw")

			# Crear la tabla dentro del frame interior
			tabla = ttk.Treeview(inner_canvas, columns=("Código Receta", "Nombre Receta", "Costo Receta" ,"Ingredientes"))
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
				tabla.insert('', 'end', text=str(index), values=(receta[0], receta[1], costo_ingredientes, ', '.join([f"{ing[0]} ({ing[1]} unidades)" for ing in ingredientes])))

			# Configurar el tamaño del canvas
			canvas.config(scrollregion=canvas.bbox("all"))

			# Agregar el canvas a la barra de desplazamiento
			canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

		else:
			print("No hay recetas disponibles.")
	except Exception as e:
		print("Error al mostrar recetas con costo:", e)

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
			SELECT I.Nombre, RI.Cantidad, I.PrecioUnitario
			FROM INGREDIENTES I
			JOIN RECETAS_INGREDIENTES RI ON I.ID_Ingrediente = RI.ID_Ingrediente
			WHERE RI.ID_Receta = ?
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
				tabla = ttk.Treeview(toplevel, columns=("Código Receta", "Nombre Receta", "Costo Receta" ,"Ingredientes"))
				tabla.heading("#0", text="Índice")
				tabla.heading("Código Receta", text="Código Receta")
				tabla.heading("Nombre Receta", text="Nombre Receta")
				tabla.heading("Costo Receta", text="Costo Receta")
				tabla.heading("Ingredientes", text="Ingredientes")            
				tabla.pack(fill="both", expand=True)
				for index, receta in enumerate(recetas, start=1):
					id_receta = receta[0] # Suponiendo que el ID de la receta es el primer elemento
					ingredientes = obtener_ingredientes_por_receta(id_receta)
					costo_ingredientes = calcular_costo_ingredientes(ingredientes)
					tabla.insert('', 'end', text=str(index), values=(receta[0], receta[1], costo_ingredientes, ', '.join([f"{ing[0]} ({ing[1]} unidades)" for ing in ingredientes])))
			else:
				print("No hay recetas disponibles.")
		except Exception as e:
			print("Error al mostrar recetas con costo:", e)
	# Ejemplo de uso
	root = tk.Tk()
	mostrar_recetas_con_costo_en_toplevel(root)
	root.mainloop()

def modificar_receta(frame):
	tk.Label(frame, text="Código de la receta a modificar:").pack()
	entry_codigo_modificar = tk.Entry(frame)
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
			tk.Label(frame, text=detalle_texto).pack()
			tk.Label(frame, text="Nuevo nombre de la receta:").pack()
			entry_nuevo_nombre = tk.Entry(frame)
			entry_nuevo_nombre.pack()
			tk.Label(frame, text="Nuevo costo de la receta:").pack()
			entry_nuevo_costo = tk.Entry(frame)
			entry_nuevo_costo.pack()
			tk.Label(frame, text="Nuevo código de ingrediente:").pack()
			entry_nuevo_codigo_ingrediente = tk.Entry(frame)
			entry_nuevo_codigo_ingrediente.pack()
			tk.Label(frame, text="Nueva cantidad de cada ingrediente:").pack()
			entry_nueva_cantidad_ingrediente = tk.Entry(frame)
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
			tk.Button(frame, text="Confirmar", command=confirmar_modificacion).pack()
		else:
			tk.messagebox.showerror("Error", "La receta especificada no existe.")
	tk.Button(frame, text="Mostrar Detalle", command=mostrar_detalle_modificar).pack()
	tk.Button(frame, text="        Ver        ",command=anglosajona).pack()

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

	tk.Label(frame, text="Código de la receta a eliminar:").pack()
	entry_codigo_eliminar = tk.Entry(frame)
	entry_codigo_eliminar.pack()

	tk.Button(frame, text="Confirmar", command=confirmar_eliminacion).pack()
	tk.Button(frame, text="        Ver        ",command=anglosajona).pack()

#..................

def ingresar_plato(frame):
	# Función para calcular el precio de la receta asociada
	def calcular_receta(nombre_receta):
		cursor.execute("SELECT Codigo_Ingrediente, Cantidad_De_Cada_Ingrediente FROM Recetas WHERE Nombre = ?", (nombre_receta,))
		ingredientes_receta = cursor.fetchall()
		costo_total = 0
		for codigo_ingrediente, cantidad_ingrediente in ingredientes_receta:
			cursor.execute("SELECT Precio FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_ingrediente,))
			precio_ingrediente = cursor.fetchone()[0]
			costo_total += precio_ingrediente * cantidad_ingrediente
		return costo_total

	# Función para confirmar el nombre de la receta y calcular el precio del plato
	def confirmar_nombre_receta(entry_nombre_receta, entry_precio_manual):
		nombre_receta = entry_nombre_receta.get()
		precio_manual = entry_precio_manual.get()
		if precio_manual:
			precio_final = float(precio_manual)
		else:
			precio_final = calcular_receta(nombre_receta)
		return precio_final

	# Función para guardar el plato
	def guardar_plato(entry_nombre, entry_ganancia, implementado_var, veganos_var, vegetarianos_var, celiacos_var, entry_nombre_receta, entry_precio_manual):
		nombre = entry_nombre.get()
		ganancia_porcentaje = float(entry_ganancia.get())
		implementado_menu = implementado_var.get()
		apto_veganos = veganos_var.get()
		apto_vegetarianos = vegetarianos_var.get()
		apto_celiacos = celiacos_var.get()

		precio_final = confirmar_nombre_receta(entry_nombre_receta, entry_precio_manual)

		cursor.execute("INSERT INTO Platos (Nombre, Ganancia, Precio_Final, Implementado_Menu, Apto_Veganos, Apto_Vegetarianos, Apto_Celiacos) VALUES (?, ?, ?, ?, ?, ?, ?)",
					(nombre, ganancia_porcentaje, precio_final, implementado_menu, apto_veganos, apto_vegetarianos, apto_celiacos))
		base.commit()
		messagebox.showinfo("Éxito", "Plato ingresado correctamente.")

	# Función para implementar el plato en el menú
	def implementar_en_menu():
		nombre_plato = entry_nombre.get()
		cursor.execute("SELECT Nombre FROM Carta WHERE Nombre = ?", (nombre_plato,))
		plato_existente = cursor.fetchone()
		if plato_existente:
			messagebox.showwarning("Advertencia", f"El plato '{nombre_plato}' ya está en la carta.")
		else:
			cursor.execute("INSERT INTO Carta (Nombre) VALUES (?)", (nombre_plato,))
			base.commit()
			messagebox.showinfo("Éxito", f"El plato '{nombre_plato}' ha sido implementado en el menú.")
	# Crear la ventana principal
	# Widgets para ingresar los datos del plato
	tk.Label(frame, text="Nombre del plato:").pack()
	entry_nombre = tk.Entry(frame)
	entry_nombre.pack()
	tk.Label(frame, text="% Ganancia del plato:").pack()
	entry_ganancia = tk.Entry(frame)
	entry_ganancia.pack()
	implementado_var = tk.BooleanVar()
	tk.Checkbutton(frame, text="¿Está implementado en el menú?", variable=implementado_var).pack()
	veganos_var = tk.BooleanVar()
	tk.Checkbutton(frame, text="¿Es apto para veganos?", variable=veganos_var).pack()
	vegetarianos_var = tk.BooleanVar()
	tk.Checkbutton(frame, text="¿Es apto para vegetarianos?", variable=vegetarianos_var).pack()
	celiacos_var = tk.BooleanVar()
	tk.Checkbutton(frame, text="¿Es apto para celiacos?", variable=celiacos_var).pack()
	tk.Label(frame, text="Nombre de la receta asociada:").pack()
	entry_nombre_receta = tk.Entry(frame)
	entry_nombre_receta.pack()
	tk.Label(frame, text="Precio manual (opcional):").pack()
	entry_precio_manual = tk.Entry(frame)
	entry_precio_manual.pack()
	# Botón para guardar el plato
	tk.Button(frame, text="Guardar", command=lambda: guardar_plato(entry_nombre, entry_ganancia, implementado_var, veganos_var, vegetarianos_var, celiacos_var, entry_nombre_receta, entry_precio_manual)).pack()
	# Botón para implementar el plato en el menú
	tk.Button(frame, text="IMPLEMENTAR EN EL MENÚ", command=implementar_en_menu).pack()

def mostrar_platos_menu(frame):
	cursor.execute("SELECT * FROM Platos")
	platos = cursor.fetchall()

	tabla = ttk.Treeview(frame, columns=("Nombre", "Ganancia", "Precio Final", "Implementado en Menú", "Apto Veganos", "Apto Vegetarianos", "Apto Celiacos"))
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
def mostrar_platos_menu_en_toplevel(root):
	try:
		cursor.execute("SELECT * FROM Platos")
		platos = cursor.fetchall()

		toplevel = tk.Toplevel(root)
		tabla = ttk.Treeview(toplevel, columns=("Nombre", "Ganancia", "Precio Final", "Implementado en Menú", "Apto Veganos", "Apto Vegetarianos", "Apto Celiacos"))
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
	except Exception as e:
		print("Error al mostrar platos en el menú:", e)

def modificar_plato(frame):
	tk.Label(frame, text="ID del plato a modificar:").pack()
	entry_id_modificar = tk.Entry(frame)
	entry_id_modificar.pack()
	
	def obtener_y_modificar_datos(frame):
		id_plato = entry_id_modificar.get()
		cursor.execute("SELECT * FROM Platos WHERE ID =?", (id_plato,))
		plato = cursor.fetchone()
		if plato:
			frame = tk.Toplevel()
			frame.title("Detalle del Plato")
			tk.Label(frame, text=f"Nombre: {plato[0]}").pack()
			tk.Label(frame, text=f"Ganancia: {plato[1]}").pack()
			tk.Label(frame, text=f"Precio Final: {plato[2]}").pack()
			tk.Label(frame, text=f"Implementado en Menú: {'Sí' if plato[3] else 'No'}").pack()
			tk.Label(frame, text=f"Apto Veganos: {'Sí' if plato[4] else 'No'}").pack()
			tk.Label(frame, text=f"Apto Vegetarianos: {'Sí' if plato[5] else 'No'}").pack()
			tk.Label(frame, text=f"Apto Celiacos: {'Sí' if plato[6] else 'No'}").pack()
			def confirmar_plato(frame):
				tk.Label(frame, text="Nuevo valor para Ganancia:").pack()
				entry_ganancia = tk.Entry(frame)
				entry_ganancia.pack()
				tk.Label(frame, text="Nuevo valor para Precio Final:").pack()
				entry_precio = tk.Entry(frame)
				entry_precio.pack()
				tk.Label(frame, text="¿Modificar implementación en menú? (S/N):").pack()
				entry_implementado = tk.Entry(frame)
				entry_implementado.pack()
				tk.Label(frame, text="¿Modificar apto para veganos? (S/N):").pack()
				entry_veganos = tk.Entry(frame)
				entry_veganos.pack()
				tk.Label(frame, text="¿Modificar apto para vegetarianos? (S/N):").pack()
				entry_vegetarianos = tk.Entry(frame)
				entry_vegetarianos.pack()
				tk.Label(frame, text="¿Modificar apto para celiacos? (S/N):").pack()
				entry_celiacos = tk.Entry(frame)
				entry_celiacos.pack()
				def guardar_modificacion():
					nueva_ganancia = float(entry_ganancia.get())
					nuevo_precio = float(entry_precio.get())
					nueva_implementacion = entry_implementado.get().upper() == "S"
					nuevo_veganos = entry_veganos.get().upper() == "S"
					nuevo_vegetarianos = entry_vegetarianos.get().upper() == "S"
					nuevo_celiacos = entry_celiacos.get().upper() == "S"
					cursor.execute("UPDATE Platos SET Ganancia = ?, Precio_Final = ?, Implementado_Menu = ?, Apto_Veganos = ?, Apto_Vegetarianos = ?, Apto_Celiacos = ? WHERE ID = ?",
									(nueva_ganancia, nuevo_precio, nueva_implementacion, nuevo_veganos, nuevo_vegetarianos, nuevo_celiacos, id_plato))
					base.commit()
					messagebox.showinfo("Éxito", "Plato modificado correctamente.")
				tk.Button(frame, text="Guardar Modificación", command=guardar_modificacion).pack()
			tk.Button(frame, text="Modificar", command=confirmar_plato).pack()
		else:
			messagebox.showerror("Error", "El plato especificado no existe.")
	tk.Button(frame, text="Obtener Detalle", command=obtener_y_modificar_datos).pack()
	tk.Button(frame, text="        Ver        ",command=mostrar_platos_menu_en_toplevel).pack()


def eliminar_plato(frame):

	tk.Label(frame, text="Nombre del plato a eliminar:").pack()
	entry_nombre_eliminar = tk.Entry(frame)
	entry_nombre_eliminar.pack()

	def confirmar_eliminacion():
		nombre_plato = entry_nombre_eliminar.get()
		confirmacion = tk.messagebox.askyesno("Confirmación", f"¿Está seguro de querer eliminar el plato '{nombre_plato}'?")
		if confirmacion:
			cursor.execute("DELETE FROM Platos WHERE Nombre = ?", (nombre_plato,))
			base.commit()
			tk.messagebox.showinfo("Éxito", "Plato eliminado correctamente.")

	tk.Button(frame, text="Confirmar", command=confirmar_eliminacion).pack()
	tk.Button(frame, text="        Ver        ",command=mostrar_platos_menu_en_toplevel).pack()

#_________________________________ M e n u 
def ver_carta(frame):
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

	table = ttk.Treeview(frame)
	table['columns'] = ('Precio Final', 'Vegano', 'Vegetariano', 'Celiaco')
	table.heading('#0', text='Plato')
	table.heading('Precio Final', text='Precio Final')
	table.heading('Vegano', text='Vegano')
	table.heading('Vegetariano', text='Vegetariano')
	table.heading('Celiaco', text='Celiaco')
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
			tk.messagebox.showinfo("Éxito", f"Se ha modificado el precio del plato '{nombre_plato}' correctamente.")

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
	current_frame = ttk.Frame(root)
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
			modificar_plato(current_frame)
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

	menu = tk.Menu(root)
	root.config(menu=menu)

	opciones_menu = ["Ingresar", "Ver", "Modificar", "Eliminar"]
	opc_menu_carta = ["Ver", "Modificar"]
	menus = [("Ingredientes", opciones_menu), ("Recetas", opciones_menu), ("Platos", opciones_menu), ("Carta", opc_menu_carta)]

	for nombre_menu, opciones in menus:
		crear_menu(menu, nombre_menu, opciones, root)

	root.mainloop()

if __name__ == "__main__":
	main()