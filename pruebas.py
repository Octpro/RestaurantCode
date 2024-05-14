import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()

# Crear un estilo personalizado
estilo = ttk.Style()
estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0, background='light blue', font=('Lucida Console', 9))

# Crear un Treeview con el estilo personalizado
tree = ttk.Treeview(ventana, columns=("Nombres", "Apellidos"), selectmode='browse', style="mystyle.Treeview")
tree.insert('', 'end', text="Esteban", values="Quito")
tree.heading("#0", text="Nombre")
tree.heading("#1", text="Apellido")
tree.pack()

# Botón para cambiar el fondo a blanco
tk.Button(ventana, text="Cambiar fondo blanco", command=lambda: estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0, background='white', font=('Lucida Console', 9))).pack(side=tk.LEFT)

# Botón para cambiar el fondo a azul claro
tk.Button(ventana, text="Cambiar fondo azul claro", command=lambda: estilo.configure("mystyle.Treeview", highlightthickness=0, bd=0, background='light blue', font=('Lucida Console', 9))).pack(side=tk.RIGHT)

ventana.geometry("400x400")
ventana.mainloop()
