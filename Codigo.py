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

cursor.execute('CREATE TABLE IF NOT EXISTS INGREDIENTES( )')

cursor.execute('CREATE TABLE IF NOT EXISTS RECETAS( )')

cursor.execute('CREATE TABLE IF NOT EXISTS PLATOS( )')

#-----------------------------------------------------------------------

                #PRINTS DE MENUS
#-----------------------------------------------
menu = '''
1= Agregar
2= Ver
3= Carta
4= Salir
'''

menu_agregar = '''
---- AGREGAR ----
1= Ingredientes
2= Recetas
3= Platos
4= Volver
'''

menu_ver = '''
---- VER ----
1= Ingredientes
2= Recetas
3= Platos
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

    
    if opcion == 1: #Menu de agregar datos
        while True:
            
            print(menu_agregar) #Imprimo el menu de agregar

            opcion_n = int(input('Ingrese la opcion deseada: '))
            validar_opcion(opcion_n)

            if opcion_n == 1: #Ingreso datos ingredientes

                print("\n","Esta ingresando ingredientes", "\n")

                nombre = input('Nombre del ingrediente: ')
                cantidad = int(input('Cantidad del ingrediente: '))
                precio = int(input('Precio del ingrediente: ')) 
            
            if opcion_n == 2: #Ingreso datos recetas
                
                print("\n","Esta ingresando recetas", "\n")

                nombre = input('Nombre de la receta: ')
                ingredientes = input('Ingredientes (separados por coma): ') # Vamos a usar un split para cargar a la base de datos.
                           
            if opcion_n == 3: #Ingreso Datos Platos
                
                print("\n","Esta ingresando platos", "\n")

                nombre = input('Nombre del plato: ')
                precio = int(input('Precio del plato: ')) 

            if opcion_n == 4: #Volver 
                break


        