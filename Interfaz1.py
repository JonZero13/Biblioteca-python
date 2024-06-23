import tkinter as tk
from tkinter import ttk

class Libro:
    def __init__(self, titulo, isbn, autor, categoria):
        self.titulo = titulo
        self.isbn = isbn
        self.autor = autor
        self.categoria = categoria

    def mostrar_info(self):
        return f"Título: {self.titulo}\nISBN: {self.isbn}\nAutor: {self.autor.nombre} {self.autor.apellido}\nCategoría: {self.categoria.nombre}"

class Autor:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

class Usuario:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.prestamos = []

class Prestamo:
    def __init__(self, libro, usuario):
        self.libro = libro
        self.usuario = usuario

class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre

class Biblioteca:
    def __init__(self, info_text):
        self.libros = []
        self.autores = []
        self.usuarios = []
        self.prestamos = []
        self.categorias = []
        self.info_text = info_text

    def agregar_libro(self, titulo, isbn, autor, categoria):
        autor_existente = next((a for a in self.autores if a.nombre == autor.nombre and a.apellido == autor.apellido), None)
        if not autor_existente:
            self.autores.append(autor)
        categoria_existente = next((c for c in self.categorias if c.nombre == categoria.nombre), None)
        if not categoria_existente:
            self.categorias.append(categoria)
        libro = Libro(titulo, isbn, autor_existente or autor, categoria_existente or categoria)
        self.libros.append(libro)
        self.mostrar_informacion()

    def agregar_usuario(self, nombre, apellido):
        usuario = Usuario(nombre, apellido)
        self.usuarios.append(usuario)
        self.mostrar_informacion()

    def prestar_libro(self, titulo_libro, nombre_usuario, apellido_usuario):
        libro = next((lib for lib in self.libros if lib.titulo == titulo_libro), None)
        usuario = next((user for user in self.usuarios if user.nombre == nombre_usuario and user.apellido == apellido_usuario), None)
        if libro and usuario:
            prestamo = Prestamo(libro, usuario)
            self.prestamos.append(prestamo)
            usuario.prestamos.append(prestamo)
            self.mostrar_informacion()

    def eliminar_libro(self, libro):
        self.libros.remove(libro)
        self.mostrar_informacion()

    def eliminar_usuario(self, usuario):
        self.usuarios.remove(usuario)
        for prestamo in list(usuario.prestamos):
            self.prestamos.remove(prestamo)
        usuario.prestamos.clear()
        self.mostrar_informacion()

    def mostrar_informacion(self):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert(tk.END, "Libros:\n")
        for libro in self.libros:
            self.info_text.insert(tk.END, libro.mostrar_info() + "\n\n")
        self.info_text.insert(tk.END, "Usuarios:\n")
        for usuario in self.usuarios:
            self.info_text.insert(tk.END, usuario.nombre + " " + usuario.apellido + "\n")
            self.info_text.insert(tk.END, "Préstamos:\n")
            for prestamo in usuario.prestamos:
                self.info_text.insert(tk.END, prestamo.libro.titulo + "\n")
            self.info_text.insert(tk.END, "\n")
        self.info_text.config(state=tk.DISABLED)

def crear_entrada(parent, texto, fila, columna):
    label = tk.Label(parent, text=texto)
    label.grid(row=fila, column=columna, sticky="w", padx=5, pady=5)
    entry = tk.Entry(parent)
    entry.grid(row=fila, column=columna+1, sticky="w", padx=5, pady=5)
    return entry

def agregar_libro_callback():
    titulo = titulo_entry.get()
    isbn = isbn_entry.get()
    autor_nombre = autor_nombre_entry.get()
    autor_apellido = autor_apellido_entry.get()
    categoria_nombre = categoria_entry.get()
    autor = Autor(autor_nombre, autor_apellido)
    categoria = Categoria(categoria_nombre)
    biblioteca.agregar_libro(titulo, isbn, autor, categoria)
    for entry in [titulo_entry, isbn_entry, autor_nombre_entry, autor_apellido_entry, categoria_entry]:
        entry.delete(0, tk.END)

def agregar_usuario_callback():
    nombre = usuario_nombre_entry.get()
    apellido = usuario_apellido_entry.get()
    biblioteca.agregar_usuario(nombre, apellido)
    for entry in [usuario_nombre_entry, usuario_apellido_entry]:
        entry.delete(0, tk.END)

def prestar_libro_callback():
    titulo_libro = prestamo_libro_entry.get()
    nombre_usuario = prestamo_usuario_nombre_entry.get()
    apellido_usuario = prestamo_usuario_apellido_entry.get()
    biblioteca.prestar_libro(titulo_libro, nombre_usuario, apellido_usuario)
    for entry in [prestamo_libro_entry, prestamo_usuario_nombre_entry, prestamo_usuario_apellido_entry]:
        entry.delete(0, tk.END)

def eliminar_libro_callback():
    seleccion = biblioteca.info_text.get(tk.SEL_FIRST, tk.SEL_LAST)
    for libro in biblioteca.libros:
        if libro.titulo in seleccion:
            biblioteca.eliminar_libro(libro)
            break

def eliminar_usuario_callback():
    seleccion = biblioteca.info_text.get(tk.SEL_FIRST, tk.SEL_LAST)
    for usuario in biblioteca.usuarios:
        if usuario.nombre in seleccion or usuario.apellido in seleccion:
            biblioteca.eliminar_usuario(usuario)
            break

root = tk.Tk()
root.title("Sistema de Gestión de Bibliotecas")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

libro_tab = ttk.Frame(notebook)
notebook.add(libro_tab, text="Libros")

libro_frame = tk.LabelFrame(libro_tab, text="Agregar Libro", padx=10, pady=10)
libro_frame.pack(fill="x", padx=10, pady=10)

titulo_entry = crear_entrada(libro_frame, "Título:", 0, 0)
isbn_entry = crear_entrada(libro_frame, "ISBN:", 1, 0)
autor_nombre_entry = crear_entrada(libro_frame, "Nombre del Autor:", 2, 0)
autor_apellido_entry = crear_entrada(libro_frame, "Apellido del Autor:", 3, 0)
categoria_entry = crear_entrada(libro_frame, "Categoría:", 4, 0)

tk.Button(libro_frame, text="Agregar Libro", command=agregar_libro_callback).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

usuario_tab = ttk.Frame(notebook)
notebook.add(usuario_tab, text="Usuarios")

usuario_frame = tk.LabelFrame(usuario_tab, text="Agregar Usuario", padx=10, pady=10)
usuario_frame.pack(fill="x", padx=10, pady=10)

usuario_nombre_entry = crear_entrada(usuario_frame, "Nombre:", 0, 0)
usuario_apellido_entry = crear_entrada(usuario_frame, "Apellido:", 1, 0)

tk.Button(usuario_frame, text="Agregar Usuario", command=agregar_usuario_callback).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

prestamo_tab = ttk.Frame(notebook)
notebook.add(prestamo_tab, text="Préstamos")

prestamo_frame = tk.LabelFrame(prestamo_tab, text="Prestar Libro", padx=10, pady=10)
prestamo_frame.pack(fill="x", padx=10, pady=10)

prestamo_libro_entry = crear_entrada(prestamo_frame, "Título del Libro:", 0, 0)
prestamo_usuario_nombre_entry = crear_entrada(prestamo_frame, "Nombre del Usuario:", 1, 0)
prestamo_usuario_apellido_entry = crear_entrada(prestamo_frame, "Apellido del Usuario:", 2, 0)

tk.Button(prestamo_frame, text="Prestar Libro", command=prestar_libro_callback).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

info_tab = ttk.Frame(notebook)
notebook.add(info_tab, text="Información")

info_text = tk.Text(info_tab, height=20, width=50, state=tk.DISABLED)
info_text.pack(fill="both", expand=True, padx=10, pady=10)

eliminar_frame = tk.Frame(info_tab)
eliminar_frame.pack(fill="x", padx=10, pady=10)
tk.Button(eliminar_frame, text="Eliminar Libro", command=eliminar_libro_callback).pack(side="left", padx=5)
tk.Button(eliminar_frame, text="Eliminar Usuario", command=eliminar_usuario_callback).pack(side="left", padx=5)

biblioteca = Biblioteca(info_text)

root.mainloop()
