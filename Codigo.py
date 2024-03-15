from sqlite3 import * 
import tkinter as tk
from tkinter import ttk

#TODOS LOS PRINTS SE PUEDEN CAMBIAR PARA QUE SE VEA MAS PROFESIONAL
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


	#Conectar Base de datos
base = connect('sistema.db')
cursor = base.cursor()

import tkinter as tk
from tkinter import ttk
import sqlite3

# Conectar a la base de datos
base = sqlite3.connect('sistema.db')
cursor = base.cursor()

#---------------------------- I n g r e d i e n t e s 
def ingresar_ingredientes():
	while True:
		nombre_ingrediente = input("Ingrese el nombre del ingrediente: ")
		cantidad = float(input("Ingrese la cantidad que tiene de {}: ".format(nombre_ingrediente)))
		unidad_medida = input("Ingrese la unidad de medida : ")
		precio = float(input("Ingrese el precio por cada unidad : "))
		print("\nNombre: {}\nUnidad de medida: {}\nPrecio: {}".format(nombre_ingrediente, unidad_medida, precio))
		op = input("¿Está seguro de todos estos datos ingresados? (S/N): ").lower()
		if op == "s":
			cursor.execute("INSERT INTO Ingredientes (Nombre, Unidad_Medida, Cantidad, Precio) VALUES (?, ?, ?, ?)", (nombre_ingrediente, unidad_medida, cantidad, precio))
			base.commit()
			print("¡Ingrediente ingresado correctamente!")
			break
		elif op == "n":
			print("Volver a ingresar.\n")
		else:
			print("Opción no válida, por favor ingrese 'S' o 'N'.\n")
def obtener_ingredientes():
	cursor.execute("SELECT * FROM Ingredientes")
	ingredientes = cursor.fetchall()
	return ingredientes

def actualizar_tabla(tabla):
	tabla.delete(*tabla.get_children())
	ingredientes = obtener_ingredientes()
	for ingrediente in ingredientes:
		tabla.insert('', 'end', values=ingrediente)
def mostrar_ingredientes():
	cursor.execute("SELECT Codigo_Ingrediente, Nombre, Cantidad, Unidad_Medida FROM Ingredientes")
	ingredientes = cursor.fetchall()
	# Crear ventana y tabla para mostrar los ingredientes
	ventana = tk.Tk()
	ventana.title("Lista de Ingredientes")
	tabla = ttk.Treeview(ventana, columns=("Código", "Nombre", "Cantidad", "Unidad de Medida"), show="headings")
	tabla.heading("Código", text="Código")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Cantidad", text="Cantidad")
	tabla.heading("Unidad de Medida", text="Unidad de Medida")
	for ingrediente in ingredientes:
		tabla.insert("", "end", values=ingrediente)
	tabla.pack(padx=20, pady=20)
	ventana.mainloop()

def sisisi():
	def modificar_ingrediente():
		def modificar_cantidad(codigo_modificar):
			cursor.execute("SELECT Cantidad FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_modificar,))
			cantidad_actual = cursor.fetchone()[0]
			print("Cantidad actual del ingrediente:", cantidad_actual)
			print("Seleccione la operación a realizar:")
			print("1- Cambiar cantidad directamente")
			print("2- Sumar cantidad")
			print("3- Restar cantidad")

			opcion = int(input("Elija una opción: "))
			if opcion == 1:
				nueva_cantidad = float(input("Ingrese la nueva cantidad: "))
			elif opcion == 2:
				suma = float(input("Ingrese la cantidad a sumar: "))
				nueva_cantidad = cantidad_actual + suma
			elif opcion == 3:
				resta = float(input("Ingrese la cantidad a restar: "))
				nueva_cantidad = cantidad_actual - resta
			else:
				print("Opción inválida.")
				return

			cursor.execute("UPDATE Ingredientes SET Cantidad = ? WHERE Codigo_Ingrediente = ?", (nueva_cantidad, codigo_modificar))
			base.commit()
			print("Cantidad actualizada correctamente.")

		codigo_modificar = int(input("Ingrese el código del ingrediente que desea modificar (0 para mostrar la lista de ingredientes): "))
		if codigo_modificar == 0:
			mostrar_ingredientes(cursor)
		else:
			cursor.execute("SELECT * FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_modificar,))
			resultado_verificacion = cursor.fetchone()
			if not resultado_verificacion:
				print("No se encontró ningún ingrediente con ese código.")
			else:
				print("Ingrediente encontrado.")
				print("Seleccione el detalle a modificar:")
				print("1- Nombre")
				print("2- Cantidad")
				print("3- Unidad de Medida")
				print("4- Precio")
				print("5- Todos")
				opcion_modificar = int(input("Elija una opción: "))
				if opcion_modificar in range(1, 6):
					nuevo_valor = input(f"Ingrese el nuevo valor para {resultado_verificacion[opcion_modificar - 1]}: ")
					confirmacion = input("¿Está seguro de realizar la modificación? (s/n): ")
					if confirmacion.lower() == 's':
						campos = ["Nombre", "Cantidad", "Unidad_Medida", "Precio"]
						campo_mod = campos[opcion_modificar - 1]
						consulta_modificar = f"UPDATE Ingredientes SET {campo_mod} = ? WHERE Codigo_Ingrediente = ?"
						cursor.execute(consulta_modificar, (nuevo_valor, codigo_modificar))
						base.commit()
						print(f"Se ha modificado el valor del campo {campo_mod}.")
					else:
						print("Modificación cancelada.")
				elif opcion_modificar == 0:
					print("Saliendo...")
				else:
					print("Opción invslida.")
	modificar_ingrediente()

def eliminar_ingredientes():
					mostrar_ingredientes()
					codigo_eliminar = int(input("Ingrese el código del ingrediente que desea eliminar: "))
					confirmacion = input("¿Está seguro de eliminar este ingrediente? (s/n): ")
					if confirmacion.lower() == 's':
						cursor.execute("DELETE FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_eliminar,))
						base.commit()
						print("El ingrediente ha sido eliminado correctamente.")
					else:
						print("Eliminación cancelada.")

#----------------------------- R e c e t a s 
def ingresar_receta():
	print("\nEstás ingresando una nueva receta\n")
	nombre_receta = input("Ingrese el nombre de la receta: ")
	ingredientes_receta = []
	while True:
		codigo_ingrediente = int(input("Ingrese el código del ingrediente (0 para terminar): "))
		if codigo_ingrediente == 0:
			break
		cantidad_ingrediente = float(input("Ingrese la cantidad del ingrediente: "))

		cursor.execute("SELECT Nombre FROM INGREDIENTES WHERE Codigo_Ingrediente = ?",(codigo_ingrediente,))
		nombre_ing = cursor.fetchone()
		
		ingredientes_receta.append((nombre_ing, cantidad_ingrediente))
	
	# Convertir ingredientes a strings separados por coma
	nombre_ingredientes = ", ".join(ingrediente[0][0] for ingrediente in ingredientes_receta)
	cantidades_ingredientes = ",".join(str(ingrediente[1]) for ingrediente in ingredientes_receta) 

	costo_total = 0
	for codigo_ingrediente, cantidad_ingrediente in ingredientes_receta:
		cursor.execute("SELECT Precio FROM Ingredientes WHERE Nombre = ?", (codigo_ingrediente))
		precio_ingrediente = cursor.fetchone()[0]
		costo_ingrediente = precio_ingrediente * cantidad_ingrediente
		costo_total += costo_ingrediente
	
	cursor.execute("INSERT INTO Recetas (Nombre, Costo, Codigo_Ingrediente, Cantidad_De_Cada_Ingrediente) VALUES (?, ?, ?, ?)",
				   (nombre_receta, costo_total, nombre_ingredientes, cantidades_ingredientes))
	base.commit()
	print("Receta ingresada correctamente.")

def obtener_recetas_con_costo():
	consulta = """SELECT Recetas.Codigo_Receta, 
	   				Recetas.Nombre AS Nombre_Receta, 
	   				GROUP_CONCAT(Ingredientes.Nombre) AS Ingredientes, 
	   				SUM(Ingredientes.Precio * Recetas.Cantidad_De_Cada_Ingrediente) AS Costo_Receta
					FROM Recetas
					INNER JOIN Ingredientes ON Recetas.Codigo_Ingrediente = Ingredientes.Codigo_Ingrediente
					GROUP BY Recetas.Codigo_Receta, Recetas.Nombre"""
	
	cursor.execute(consulta)
	recetas = cursor.fetchall()
	print(recetas)
	return recetas

def mostrar_recetas_con_costo():
	recetas = obtener_recetas_con_costo()
	ventana = tk.Tk()
	ventana.title("Recetas y Costo")
	tabla = ttk.Treeview(ventana, columns=("Código Receta", "Nombre Receta", "Ingredientes", "Costo Receta"))
	tabla.heading("#0", text="Índice")
	tabla.heading("Código Receta", text="Código Receta")
	tabla.heading("Nombre Receta", text="Nombre Receta")
	tabla.heading("Ingredientes", text="Ingredientes")
	tabla.heading("Costo Receta", text="Costo Receta")
	tabla.pack(fill="both", expand=True)
	for index, receta in enumerate(recetas, start=1):
		tabla.insert('', 'end', text=str(index), values=receta)
	ventana.mainloop()

def modificar_receta():
	opcion = input("¿Cómo desea buscar la receta? (1 - Por código, 2 - Por nombre): ")
	if opcion == '1':
		codigo_receta = input("Ingrese el código de la receta que desea modificar: ")
		cursor.execute("SELECT * FROM Recetas WHERE Codigo_Receta = ?", (codigo_receta,))
	elif opcion == '2':
		nombre_receta = input("Ingrese el nombre de la receta que desea modificar: ")
		cursor.execute("SELECT * FROM Recetas WHERE Nombre = ?", (nombre_receta,))
	else:
		print("Opción no válida.")
		return
	receta = cursor.fetchone()
	
	if receta:
		print("\nDatos de la receta:")
		print(f"Código: {receta[0]}")
		print(f"Nombre: {receta[1]}")
		print(f"Costo: {receta[2]}")
		print(f"Código de Ingrediente: {receta[3]}")
		print(f"Cantidad de cada Ingrediente: {receta[4]}")
		nuevo_nombre = input("Ingrese el nuevo nombre de la receta (deje en blanco para mantener el mismo): ")
		nuevo_costo = float(input("Ingrese el nuevo costo de la receta (deje en blanco para mantener el mismo): "))
		nuevo_codigo_ingrediente = input("Ingrese el nuevo código de ingrediente (deje en blanco para mantener el mismo): ")
		nueva_cantidad_ingrediente = float(input("Ingrese la nueva cantidad de cada ingrediente (deje en blanco para mantener la misma): "))
		if nuevo_nombre.strip():
			cursor.execute("UPDATE Recetas SET Nombre = ? WHERE Codigo_Receta = ?", (nuevo_nombre, receta[0]))
		if nuevo_costo:
			cursor.execute("UPDATE Recetas SET Costo = ? WHERE Codigo_Receta = ?", (nuevo_costo, receta[0]))
		if nuevo_codigo_ingrediente.strip():
			cursor.execute("UPDATE Recetas SET Codigo_Ingrediente = ? WHERE Codigo_Receta = ?", (nuevo_codigo_ingrediente, receta[0]))
		if nueva_cantidad_ingrediente:
			cursor.execute("UPDATE Recetas SET Cantidad_De_Cada_Ingrediente = ? WHERE Codigo_Receta = ?", (nueva_cantidad_ingrediente, receta[0]))        
		print("Receta modificada correctamente.")
	else:
		print("La receta especificada no existe.")

def eliminar_receta():
	opcion = input("¿Cómo desea eliminar la receta? (1 - Por código, 2 - Por nombre): ")
	if opcion == '1':
		codigo_receta = input("Ingrese el código de la receta que desea eliminar: ")
		cursor.execute("SELECT * FROM Recetas WHERE Codigo_Receta = ?", (codigo_receta,))
	elif opcion == '2':
		nombre_receta = input("Ingrese el nombre de la receta que desea eliminar: ")
		cursor.execute("SELECT * FROM Recetas WHERE Nombre = ?", (nombre_receta,))
	else:
		print("Opción no válida.")
		return
	receta = cursor.fetchone()    
	if receta:
		print("\nDatos de la receta:")
		print(f"Código: {receta[0]}")
		print(f"Nombre: {receta[1]}")
		print(f"Costo: {receta[2]}")
		print(f"Código de Ingrediente: {receta[3]}")
		print(f"Cantidad de cada Ingrediente: {receta[4]}")
		confirmacion = input("¿Está seguro de querer eliminar esta receta? (S/N): ").upper()
		
		if confirmacion == 'S':
			if opcion == '1':
				cursor.execute("DELETE FROM Recetas WHERE Codigo_Receta = ?", (codigo_receta,))
				
			elif opcion == '2':
				cursor.execute("DELETE FROM Recetas WHERE Nombre = ?", (nombre_receta,))
			print("Receta eliminada correctamente.")
			base.commit()
		else:
			print("Operación cancelada.")
	else:
		print("La receta especificada no existe.")



#----------------------------- P l a t o s			
def calcular_receta(nombre_receta):
	cursor.execute("SELECT Ingredientes FROM Recetas WHERE Nombre = ?", (nombre_receta,))
	ingredientes_receta = cursor.fetchone()[0]
	costo_total = 0
	for codigo_ingrediente, cantidad_ingrediente in ingredientes_receta:
		cursor.execute("SELECT Precio FROM Ingredientes WHERE Codigo_Ingrediente = ?", (codigo_ingrediente,))
		precio_ingrediente = cursor.fetchone()[0]
		costo_total += precio_ingrediente * cantidad_ingrediente
	return costo_total
def ingresar_plato():
	nombre = input("Ingrese el nombre del plato: ")
	ganancia_porcentaje = float(input("Ingrese el % ganancia del plato: "))
	implementado_menu = input("¿Está implementado en la carta/menu? (S/N): ").upper()
	implementado_menu_boolean = implementado_menu == "S"
	
	confirmacion_calculo = input("¿Desea calcular automáticamente el precio final? (S/N): ").upper()
	
	if confirmacion_calculo == 'S':
		nombre_receta = input("Ingrese el nombre de la receta asociada al plato: ")
		cursor.execute("SELECT Costo FROM RECETAS WHERE Nombre = ?", (nombre_receta,))
		costo_receta = cursor.fetchone()
		print(costo_receta)
		precio_final_calculado = costo_receta[0] * (1 + ganancia_porcentaje / 100)
		print(f"El precio final calculado para el plato '{nombre}' es: {precio_final_calculado}")
		confirmacion = input("¿Está de acuerdo con este precio? (S/N): ").upper()
		if confirmacion == 'S':
			precio_final = precio_final_calculado
		else:
			precio_final = float(input("Ingrese el precio final del plato: "))
	else:
		precio_final = float(input("Ingrese el precio final del plato: "))
	apto_veganos = input("¿Es apto para veganos? (S/N): ").upper()
	apto_veganos_boolean = apto_veganos
	apto_vegetarianos = input("¿Es apto para vegetarianos? (S/N): ").upper()
	apto_vegetarianos_boolean = apto_vegetarianos
	apto_celiacos = input("¿Es apto para celiacos? (S/N): ").upper()
	apto_celiacos_boolean = apto_celiacos
	cursor.execute("INSERT INTO Platos (Nombre, Ganancia, Precio_Final, Implementado_Menu, Apto_Veganos, Apto_Vegetarianos, Apto_Celiacos) VALUES (?, ?, ?, ?, ?, ?, ?)",
				   (nombre, ganancia_porcentaje, precio_final, implementado_menu_boolean, apto_veganos_boolean, apto_vegetarianos_boolean, apto_celiacos_boolean))
	base.commit()
	print("Plato ingresado correctamente.")
	if implementado_menu_boolean == False :  
		cursor.execute("INSERT INTO Menu (Nombre_Plato) VALUES (?)", (nombre,))
		base.commit()
		print("Plato agregado al menú.")
	
def mostrar_platos():
	cursor.execute("SELECT * FROM Platos")
	platos = cursor.fetchall()
	ventana = tk.Tk()
	ventana.title("Platos")
	tabla = ttk.Treeview(ventana, columns=("Nombre", "Ganancia", "Precio Final", "Implementado en Menú", "Apto Veganos", "Apto Vegetarianos", "Apto Celiacos"))
	tabla.heading("#0", text="Índice")
	tabla.heading("Nombre", text="Nombre")
	tabla.heading("Ganancia", text="Ganancia")
	tabla.heading("Precio Final", text="Precio Final")
	tabla.heading("Implementado en Menú", text="Implementado en Menú")
	tabla.heading("Apto Veganos", text= "Apto Veganos")
	tabla.heading("Apto Vegetarianos", text= "Apto Vegetarianos")
	tabla.heading("Apto Celiacos", text="Apto Celiacos")
	tabla.pack(fill="both", expand=True)
	for index, plato in enumerate(platos, start=1):
		implementado = "Sí" if plato[3] else "No"  # Convertir el valor booleano a texto
		tabla.insert('', 'end', text=str(index), values=(plato[0], plato[1], plato[2], implementado, plato[4], plato[5], plato[6]))
	ventana.mainloop()
	
def modificar_plato():
	nombre_plato = input("Ingrese el nombre del plato que desea modificar: ")
	cursor.execute("SELECT Nombre FROM Platos WHERE Nombre = ?", (nombre_plato,))
	plato_existente = cursor.fetchone()

	for i in plato_existente:
		print("{:<20} ".format(i[0]))

	if plato_existente:
		cursor.execute("SELECT Ganancia, Precio_Final, Apto_Veganos, Apto_Vegetarianos, Apto_Celiacos FROM PLATOS WHERE Nombre = ?",(nombre_plato,))
		registros = cursor.fetchall()

		for i in registros:					
			print("\n",f"Estos son los registros de la tabla:", "\n")
			lista = ["Ganancia", "Precio Final", "Apto Vegano", "Apto Vegetariano", "Apto Celiaco"]
			for j in range(len(i)):	
				
				print(f"""	{j})_ {i[j]} {lista[j]}""")
		
		print('\n')
		
		while True:
			cambiar = input("Cual desea cambiar? (x para salir): ")

			if cambiar == "0":
				ganancia_nueva = float(input("Nueva Ganancia del plato: "))
				cursor.execute("UPDATE PLATOS SET Ganancia = ? WHERE Nombre = ? ",(ganancia_nueva, nombre_plato))
				cambiar_otro(Cambot=input("Desea modificar otro dato?(S/Si o N/No): "))
			if cambiar == "1":
				precio_final_nueva = input("Nuevo Precio Final : ")
				cursor.execute("UPDATE PLATOS SET Precio_Final = ? WHERE Nombre = ? ", (precio_final_nueva, nombre_plato))
				cambiar_otro(Cambot=input("Desea modificar otro dato?(S/Si o N/No): "))
			if cambiar == "2":
				Apto_vegano_nuevo = input("Nuevo Apto para vegano: ")
				cursor.execute("UPDATE PLATOS SET Apto_Veganos = ? WHERE Nombre = ? ", (Apto_vegano_nuevo, nombre_plato))
				cambiar_otro(Cambot=input("Desea modificar otro dato?(S/Si o N/No): "))
			if cambiar == "3":
				Apto_vegetariano_nuevo = input("Nuevo apto para vegetariano: ")
				cursor.execute("UPDATE PLATOS SET Apto_Vegetarianos = ? WHERE Nombre = ? ", (Apto_vegetariano_nuevo, nombre_plato))
				cambiar_otro(Cambot=input("Desea modificar otro dato?(S/Si o N/No): "))
			if cambiar == "4":
				apto_celiaco_nuevo = input("Nuevo apto para celiaco: ")
				cursor.execute("UPDATE PLATOS SET Apto_Celiacos = ? WHERE Nombre = ? ", (apto_celiaco_nuevo,nombre_plato))
				cambiar_otro(Cambot=input("Desea modificar otro dato?(S/Si o N/No): "))
			if cambiar == 'x':
				break	

		base.commit()
		print("Plato modificado correctamente.")
	else:
		print("El plato ingresado no existe.")

def eliminar_plato():
	nombre_plato = input("Ingrese el nombre del plato que desea eliminar: ")
	confirmacion = input("¿Está seguro? (S/N): ").upper()
	if confirmacion == "S":
		cursor.execute("DELETE FROM Platos WHERE Nombre = ?", (nombre_plato,))
		base.commit()
		print("Plato eliminado correctamente.")
	else:
		print("Operación cancelada.")

#----------------------------- M e n u
def ver_carta():
	root = tk.Tk()
	root.title("Ver Carta")

	# Crear tabla en la ventana
	table = ttk.Treeview(root)
	table['columns'] = ('Precio Final', 'Vegano', 'Vegetariano', 'Celiaco')
	table.heading('#0', text='Plato')
	table.heading('Precio Final', text='Precio Final')
	table.heading('Vegano', text='Vegano')
	table.heading('Vegetariano', text='Vegetariano')
	table.heading('Celiaco', text='Celiaco')
	table.pack(padx=10, pady=10)
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
	# Botón para cargar la carta
	btn_cargar = tk.Button(root, text="Cargar Carta", command=cargar_carta)
	btn_cargar.pack(pady=10)


def modificar_carta():
	print("Modificar Carta")
	nombre_plato = input("Ingrese el nombre del plato que desea modificar: ")
	nuevo_precio = float(input("Ingrese el nuevo precio final del plato: "))
	cursor.execute("UPDATE Platos SET Precio_Final = ? WHERE Nombre = ?", (nuevo_precio, nombre_plato))
	base.commit()
	print("Cambios guardados correctamente.")

cursor.execute('CREATE TABLE IF NOT EXISTS INGREDIENTES  ( Codigo_Ingrediente INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Unidad_Medida VARCHAR(50), Cantidad NUMBER, Precio NUMBER, Detalles TEXT )')
cursor.execute('CREATE TABLE IF NOT EXISTS RECETAS (Codigo_Receta INTEGER PRIMARY KEY AUTOINCREMENT, Nombre VARCHAR(100), Costo NUMBER, Codigo_Ingrediente INT, Cantidad_De_Cada_Ingrediente NUMBER, FOREIGN KEY (Codigo_Ingrediente) REFERENCES INGREDIENTES(Codigo_Ingrediente))')
cursor.execute('CREATE TABLE IF NOT EXISTS PLATOS ( Nombre VARCHAR(100) PRIMARY KEY, Ganancia NUMBER, Precio_Final NUMBER, Implementado_Menu BOOLEAN , Apto_Veganos BOOLEAN, Apto_Vegetarianos BOOLEAN, Apto_Celiacos BOOLEAN)')
cursor.execute("CREATE TABLE IF NOT EXISTS Menu (Nombre_Plato VARCHAR(100), FOREIGN KEY (Nombre_Plato) REFERENCES Platos(Nombre) ON DELETE CASCADE)")

while True:
	print("\n \n ---- MENU ----")
	print("1= Ingredientes")
	print("2= Recetas")
	print("3= Platos")
	print("4= Carta")
	print("0= Salir")
	o = input("Ingrese una opción: ")
	print("\n \n")
	if o == "1": # ingredientwees
		while True:
			print("---- Ingredientes ----")
			print("1= Ingresar")
			print("2= Ver")
			print("3= Modificar")
			print("4= Eliminar")
			print("5= Volver")
			oi = input("Ingrese una opcion: ")
			if oi == "1":
				ingresar_ingredientes()

			elif oi == "2":
				mostrar_ingredientes()

			elif oi == "3":
				sisisi()
			
			elif oi == "4":	
				eliminar_ingredientes()
			
			elif oi=="5":
				break			
			else:
				print("Opción inválida.")

	elif o == "2": # recetrass
		while True:
			print("---- Recetas ----")
			print("1= Ingresar")
			print("2= Ver")
			print("3= Modificar")
			print("4= Volver")
			print("5= Eliminar")
			orr = input("Ingrese una opción: ")
			if orr == "1":
				ingresar_receta()
						   
			elif orr == "2":
				mostrar_recetas_con_costo()

			elif orr == "3":
				print(" ---- Modificar Recetas ---- ")
				modificar_receta()
			elif orr == "4":
				eliminar_receta()
			elif orr == "5":
				break
			else:
				print("Opción no válida, seleccione una opción válida.")

	elif o == "3": # platos
		while True:
			print("---- Platos ----")
			print("1= Ingresar")
			print("2= Ver")
			print("3= Modificar")
			print("4= Eliminar")
			print("5= Volver")
			opcion_plato = input("Ingrese una opción: ")

			if opcion_plato == "1":
				ingresar_plato()
				#  ingresar platos
			elif opcion_plato == "2":
				mostrar_platos()
				#  ver platos
			elif opcion_plato == "3":
				modificar_plato()
				#  modificar platos
			elif opcion_plato == "4":
				eliminar_plato()
			elif opcion_plato == "5":
				break
			else:
				print("Opción no válida. Por favor, seleccione una opción válida.")

	elif o == "4":
		while True:
			print("---- Carta ----")
			print("1= Ver Carta")
			print("2= Modificar Carta")
			print("3= Volver")

			opcion_carta = input("Ingrese una opción: ")

			if opcion_carta == "1":
				ver_carta()

			elif opcion_carta == "2":
				modificar_carta()
				#  ver la carta
			elif opcion_carta == "3":
				break
				
			else:
				print("Opción no válida. Por favor, seleccione una opción válida.")

	elif o == "0":
		print("Saliendo del programa.")
		break
	else:
		print("Opción no válida. Por favor, seleccione una opción válida.")