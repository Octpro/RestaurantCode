from sqlite3 import * 

#TODOS LOS PRINTS SE PUEDEN CAMBIAR PARA QUE SE VEA MAS PROFESIONAL

def validar_opcion(opcion_n): #Funcion que valida las opciones
	try:

		if opcion_n < 0 or opcion_n > 4:
			print("El valor ingresado no es valido. ","\n","-"*15)
	
	except:
		print("Valor incorrecto, Ingrese nuevamente...", "\n", "-"*15)


	#Conectar Base de datos
	
#----------------------------

base = connect('sistema.db')
cursor = base.cursor()

#----------------------------

				#Crear TABLAS

#-----------------------------------------------------------------------

cursor.execute('CREATE TABLE IF NOT EXISTS INGREDIENTES(Nombre, Unidad_Medida ,Cantidad, Precio, Detalle )')

cursor.execute('CREATE TABLE IF NOT EXISTS RECETAS(Nombre)')

cursor.execute('CREATE TABLE IF NOT EXISTS PLATOS(Nombre, Ganancia, Precio_Final )')

#-----------------------------------------------------------------------

				#PRINTS DE MENUS
#-----------------------------------------------
menu = '''
---- MENU ----
1= Ingredientes
2= Ver
3= Modificar
5= Carta
0= Salir
'''

menu_ingredientes = '''
---- INGREDIENTES ----
1= Ingresar
2= Ver
3= Modificar
4= Volver
'''

menu_recetas = '''
---- RECETAS ----
1= Ingresar
2= Ver
3= Modificar
4= Volver
'''

menu_platos = '''
---- PLATOS ----
1= Ingresar
2= Ver
3= Modificar
4= Volver
'''

menu_carta = '''
---- CARTA ----
1= Cargar Platos
2= Ver Carta
3= Modificar Carta
'''
#-----------------------------------------------

while True: #Bucle Principal

	print(menu) #Imprimo el menu principal

	try:
		opcion = int(input("Ingrese la opcion: ")) #Ingreso a las opciones del menu principal
	
		if opcion < 0 or opcion > 4:
			print("La opcion ingresada debe ser mayor a 0 y menor que 4", "\n", "-"*15)
	
	except:
		print("Valor incorrecto. Reintente...")

	
	if opcion == 1: #Menu de Ingredientes
		while True:
			
			print(menu_ingredientes) #Imprimo el menu de agregar

			opcion_n = int(input('Ingrese la opcion deseada: '))
			validar_opcion(opcion_n)

			if opcion_n == 1: #Ingreso datos ingredientes

				print("\n","Esta ingresando ingredientes", "\n")

				nombre = input('Nombre del ingrediente: ')
				cantidad = int(input('Cantidad del ingrediente: '))
				precio = int(input('Precio del ingrediente: ')) 

			if opcion_n == 2: #Ver Ingredientes
				
				print('Leyendo Ingredientes')

				cursor.execute('SELECT * FROM INGREDIENTES')
				
				registros = cursor.fetchall()
				total_registros = len(registros)
				indice = 0

				while True:
					registro = registros[indice]
					print(f"""
Ingrediente: {registro[0]}
Un. Medida: {registro[1]}
Cantidad: {registro[2]}
Precio: {registro[3]}

""")

			if opcion_n == 3: #Modificar
				pass


			if opcion_n == 4: #Volver 
				break
	
	if opcion == 2: # Menu de Recetas
		while True:

			if opcion_n == 1: #Ingreso datos recetas
				
				print("\n","Esta ingresando recetas", "\n")

				nombre = input('Nombre de la receta: ')
				ingredientes = input('Ingredientes (separados por coma): ') # Vamos a usar un split para cargar a la base de datos.

				cargar_ingredientes = ingredientes.split(", ")

				cursor.executemany("INSERT INTO RECETAS VALUES (?)",cargar_ingredientes) #Para cargar todo, por ahora puse solamente la lista de ingredientes.
						   
			if opcion_n == 2: #Ver Recetas

				print('Leyendo Recetas')

				cursor.execute('SELECT * FROM RECETAS') #consigo los datos de recetas
				
				registros = cursor.fetchall()
				total_registros = len(registros)
				indice = 0

				while True:
					registro = registros[indice]
					print(f"""
Ingrediente: {registro[0]}
Un. Medida: {registro[1]}
Cantidad: {registro[2]}
Precio: {registro[3]}
""") #CAMBIAR