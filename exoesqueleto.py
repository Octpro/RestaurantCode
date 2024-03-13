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
		break


	#Conectar Base de datos
	
#----------------------------

base = connect('sistema.db')
cursor = base.cursor()

cursor.execute(' CREATE TABLE IF NOT EXISTS INGREDIENTES  ( Codigo_Ingrediente INT PRIMARY KEY AUTO_INCREMENT, Nombre VARCHAR(100), Unidad_Medida VARCHAR(50), Cantidad NUMBER, Precio NUMBER, Detalles TEXT )')
cursor.execute('CREATE TABLE IF NOT EXISTS RECETAS (Codigo_Receta INT PRIMARY KEY AUTO_INCREMENT, Nombre VARCHAR(100) PRIMARY KEY, Costo NUMBER, Codigo_Ingrediente INT, Cantidad_De_Cada_Ingrediente NUMBER, FOREIGN KEY (Codigo_Ingrediente) REFERENCES INGREDIENTES(Codigo_Ingrediente));')
cursor.execute('CREATE TABLE IF NOT EXISTS PLATOS ( Nombre VARCHAR(100) PRIMARY KEY, Ganancia NUMBER, Precio_Final NUMBER)')

while True:
	print("---- MENU ----")
	print("1= Ingredientes")
	print("2= Recetas")
	print("3= Platos")
	print("4= Carta")
	print("0= Salir")
	o = input("Ingrese una opción: ")
	if o == "1":
		while True:
			print("---- Ingredientes ----")
			print("1= Ingresar")
			print("2= Ver")
			print("3= Modificar")
			print("4= Eliminar")
			print("5= Volver")
			oi = input("Ingrese una opcion: ")
			if oi == "1":
				while True:
					print('\n \n')
					# ingresar ingredientes
					nombre_ingrediente = input("Ingrese el nombre del ingrediente: ")
					cantidad = float(input("Ingrese la cantidad que tiene de {}: ".format(nombre_ingrediente)))
					unidad_medida = input("Ingrese la unidad de medida : ")
					precio=float(input("ingrese el precio por cada unidad : "))
					print("\n","{}","\n","{}","\n","{}").format(nombre_ingrediente,unidad_medida,precio)
					op=input("esta seguro de todos estos datos ingresados? (S/N):").lower()
					if op == "s":
						cursor.execute("INSERT INTO Ingredientes (Nombre, Unidad_Medida, Cantidad, Precio) VALUES (?, ?, ?, ?)",)
						(nombre, unidad_medida, cantidad, precio)
						cursor.commit()
						break
					if op == "n":
						print("va devuelta","\n")
					

			elif oi == "2":
				ventana = tk.Tk()
				ventana.title("Lista de Ingredientes")
			
				# Crear tabla
				tabla = ttk.Treeview(ventana, columns=("Nombre", "Cantidad", "Unidad de Medida", "Precio"))
				tabla.heading("#0", text="Código")
				tabla.heading("Nombre", text="Nombre")
				tabla.heading("Cantidad", text="Cantidad")
				tabla.heading("Unidad de Medida", text="Unidad de Medida")
				tabla.heading("Precio", text="Precio")
				tabla.pack()
			
			# # Botón para actualizar la tabla
			# btn_actualizar = ttk.Button(ventana, text="Actualizar", command=actualizar_tabla)
			# btn_actualizar.pack()
			# 
			# # Mostrar la tabla inicialmente
			# actualizar_tabla()
			# 
				ventana.mainloop()
				print("asda.")
				# ver ingredientes

			elif oi == "3":
				# modificar ingredientes modificar todos los ingredientes y/o 
				print("")


			elif oi == "4":
				break
			else:
				print("Opción no válida, seleccione una opción válida.")

	elif o == "2":
		while True:
			print("---- Recetas ----")
			print("1= Ingresar")
			print("2= Ver")
			print("3= Modificar")
			print("4= Volver")

			orr = input("Ingrese una opción: ")

			if orr == "1":
				print("\n","Esta ingresando recetas", "\n")

				nombre = input('Nombre de la receta: ')
				costo = int(input('Ingrese el costo: '))
				ingredientes = input('Codigo _ Ingredientes (separados por coma): ') # Vamos a usar un split para cargar a la base de datos.
				cant_ingrediente = int(input('Ingrese la cantidad a usar: '))

				cod_ingrediente = ingredientes.split(", ")

				cursor.executemany("INSERT INTO RECETAS VALUES (?,?,?)",nombre,costo,cant_ingrediente) #Para cargar todo, por ahora puse solamente la lista de ingredientes.
				cursor.executemany('INSERT INTO RECETAS VALUES (?)',cod_ingrediente)
						   
			elif orr == "2":
				print('Leyendo Recetas')

				cursor.execute('SELECT * FROM RECETAS') #consigo los datos de recetas
				
				registros = cursor.fetchall()
				total_registros = len(registros)
				indice = 0

				while True:
					registro = registros[indice]
					print(f"""
					Nombre: {registro[0]}
					Costo: {registro[1]}
					Cod_Ingrediente: {registro[2]}
					Cant_Ingrediente: {registro[3]}
					""") #CAMBIAR
					

			elif orr == "3":
				print(" ---- Modificar Recetas ---- ")

				cursor.execute("SELECT Codigo_Receta FROM RECETAS")
				registro = cursor.fetchall()
				for i in registro:
					print(f"Las recetas disponibles son: {i}")

				B_Cod_Receta = input("Ingrese la receta que quiere modificar: ")
				print("x para volver")

				if B_Cod_Receta.lower() == 'x':
					continue
					
				cursor.execute("SELECT Nombre,Codigo_Ingrediente, Cantidad_De_Cada_Ingrediente FROM RECETAS WHERE Codigo_Receta = ?",(B_Cod_Receta))
				registros = cursor.fetchall()

				for i in registros:
					print("\n",f"Estos son los registros de la tabla:", "\n")
					for j in range(len(i)):						
						print(f"""	{j}.{i[j]}""")

				print("\n")

				while True:
					cambiar = input("Que dato desea cambiar?: ")
					print('x para volver')

					if cambiar.lower() == 'x':
						break
					if cambiar == '0':
						mod_nombre = input('Ingrese el nombre nuevo: ')
						cursor.execute("UPDATE RECETAS SET Nombre = ? WHERE Codigo_Receta = ?", (mod_nombre, B_Cod_Receta))
						cambiar_otro(Cambot=input("Desea modificar otro dato?(S/Si o N/No): "))
					if cambiar == '1':
						while True:
						
							cursor.execute('SELECT Codigo_Ingrediente FROM RECETAS WHERE Codigo_Receta = ?',(B_Cod_Receta))
							registro = cursor.fetchall()

							ingrediente = registro.split(', ')

							print(f'Los codigo de ingrediente son: {ingrediente}')

							mod_ingrediente = int(input('Ingrese el ingrediente viejo: '))

							

							

			elif orr == "4":
				break
			else:
				print("Opción no válida, seleccione una opción válida.")

	elif o == "3":
		while True:
			print("---- Platos ----")
			print("1= Ingresar")
			print("2= Ver")
			print("3= Modificar")
			print("4= Volver")

			opcion_plato = input("Ingrese una opción: ")

			if opcion_plato == "1":
				print("ytr.")
				#  ingresar platos
			elif opcion_plato == "2":
				print("ytr.")
				#  ver platos
			elif opcion_plato == "3":
				print("ytr.")
				#  modificar platos
			elif opcion_plato == "4":
				break
			else:
				print("Opción no válida. Por favor, seleccione una opción válida.")

	elif o == "4":
		while True:
			print("---- Carta ----")
			print("1= Cargar Platos")
			print("2= Ver Carta")
			print("3= Modificar Carta")
			print("4= Volver")

			opcion_carta = input("Ingrese una opción: ")

			if opcion_carta == "1":
				print("wer.")
				#  cargar platos en la carta
			elif opcion_carta == "2":
				print("wer.")
				#  ver la carta
			elif opcion_carta == "3":
				print("wer.")
				#  modificar la carta
			elif opcion_carta == "4":
				break
			else:
				print("Opción no válida. Por favor, seleccione una opción válida.")

	elif o == "0":
		print("Saliendo del programa...")
		break

	else:
		print("Opción no válida. Por favor, seleccione una opción válida.")
