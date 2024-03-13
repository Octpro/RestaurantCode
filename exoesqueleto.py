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

cursor.execute(' CREATE TABLE INGREDIENTES ( Codigo_Ingrediente INT PRIMARY KEY AUTO_INCREMENT, Nombre VARCHAR(100), Unidad_Medida VARCHAR(50), Cantidad NUMBER, Precio NUMBER, Detalles TEXT )')

cursor.execute('CREATE TABLE RECETAS (Nombre VARCHAR(100) PRIMARY KEY, Costo NUMBER, Codigo_Ingrediente INT, Cantidad_De_Cada_Ingrediente NUMBER, FOREIGN KEY (Codigo_Ingrediente) REFERENCES INGREDIENTES(Codigo_Ingrediente));')

cursor.execute('CREATE TABLE PLATOS ( Nombre VARCHAR(100) PRIMARY KEY, Ganancia NUMBER, Precio_Final NUMBER)')

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
            print("4= Volver")

            oi = input("Ingrese una opcion: ")

            if oi == "1":
                print("asd")
                # ingresar ingredientes
            elif oi == "2":
                print("asda.")
                # ver ingredientes
            elif oi == "3":
                print("asdasd.")
                # modificar ingredientes
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
                print("qwer.")
                #  ingresar recetas
            elif orr == "2":
                print("qwer.")
                #  ver recetas
            elif orr == "3":
                print("qwer.")
                #  modificar recetas
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
