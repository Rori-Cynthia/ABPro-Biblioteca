from excepciones import LibroNoDisponibleError,LibroNoPrestadoError, LibroNoEnPrestamoError, FechaPrestamoNoValidaError
from datetime import date, datetime, timedelta

class Usuario:
    _numero_usuarios = 0
    _usuarios = set()

    def __init__(self, nombre: str, id: str, raise_on_existing: bool = True):
        self._nombre = nombre
        self._id = id

        if self.id_es_valido(self._id):
            Usuario._numero_usuarios += 1
            Usuario._usuarios.add(self._id)
        else:
            if raise_on_existing:
                raise ValueError(f'El ID "{self._id}" no es alfanumérico o ya existe.')
            
    def obtener_nombre(self):
        return self._nombre
    
    def obtener_id(self):
        return self._id
    
    @staticmethod
    def id_es_valido(id):
        return id.isalnum() and id not in Usuario._usuarios

    @classmethod
    def contar_usuarios(cls):
        return cls._numero_usuarios
    
    def __str__(self):
        return f'Usuario: nombre: {self._nombre}, id: {self._id}'
    
    def __repr__(self):
        return f"{self._nombre}, {self._id})"
    
    def __len__(self):
        return self.contar_usuarios()


class Lector(Usuario):
    def __init__(self, nombre: str, id: str):
        super().__init__(nombre, id)
        self._libros_en_prestamo = []

    @property
    def mostrar_libros_en_prestamo(self):
        return self._libros_en_prestamo
    
    def pedir_libro(self, libro):
        self._libros_en_prestamo.append(libro)

    def devolver_libro(self, libro):
        if libro in self._libros_en_prestamo:
            self._libros_en_prestamo.remove(libro)
        else:
            raise LibroNoEnPrestamoError


class Administrador(Usuario):
    def __init__(self, nombre: str, id: str):
        super().__init__(nombre, id)

    @staticmethod
    def agregar_libro(libro):
        Libro._catalogo.append(libro)
    
    @staticmethod
    def eliminar_libro(libro):      
        if libro in Libro._catalogo:
            Libro._catalogo.remove(libro)
            Libro._cantidad_de_libros -= 1

    @classmethod
    def contar_libros_disponibles(cls):
        return len([libro for libro in Libro._catalogo if libro.estado == "disponible"])


class LectorAdministrador(Lector, Administrador):
    def __init__(self, nombre: str, id: str):
        super().__init__(nombre, id)


class Libro():
    _catalogo = []
    _cantidad_de_libros = 0
    
    def __init__(self, titulo: str, autor: str, codigo: str, estado = "disponible"):
        self.titulo = titulo
        self.autor = autor
        self.codigo = codigo
        self._estado = "disponible"

        Libro._cantidad_de_libros += 1

    @property
    def estado(self):
        return self._estado
    
    def prestar(self):
        if self._estado == "disponible":
            self._estado = "prestado"
        else:
            raise LibroNoDisponibleError
        
    def devolver(self):
        if self._estado == "prestado":
            self._estado = "disponible"
        else:
            raise LibroNoPrestadoError

    @classmethod
    def contar_libros(cls):
        return cls._cantidad_de_libros
    
    @classmethod
    def guardar_catalogo(cls, archivo = "catalogo.txt"):
        with open(archivo, "w", encoding="utf-8") as archivo:
            for libro in cls._catalogo:
                archivo.write(repr(libro) + "\n")


    @classmethod
    def cargar_catalogo(cls, archivo = "catalogo.txt"):
        try:
            with open(archivo, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    titulo, autor, codigo, estado = linea.strip().split(', ')
                    libro = Libro(titulo, autor, codigo, estado)
                    Libro._catalogo.append(libro)
        except FileNotFoundError:
            with open(archivo, "w", encoding="utf-8") as archivo:
                pass

    def __str__(self):
        return f"titulo: {self.titulo}, autor: {self.autor}, codigo {self.codigo}, estado: {self._estado}"

    def __repr__(self):
        return f"{self.titulo}, {self.autor}, {self.codigo}, {self._estado}"

    def __len__(self):
        return self.contar_libros()


class Prestamo():
    _prestamos = []

    def __init__(self, libro: Libro, usuario: Usuario, fecha_prestamo = date.today(), fecha_devolucion = (date.today() + timedelta(weeks=2))):
        self._libro = libro
        self._usuario = usuario
        self._fecha_prestamo = self.convertir_fecha(fecha_prestamo)
        self._fecha_devolucion = self.convertir_fecha(fecha_devolucion)

        if not self.fecha_es_valida:
            raise FechaPrestamoNoValidaError

    @property
    def fecha_es_valida(self):
        return self._fecha_devolucion >= self._fecha_prestamo
    
    @staticmethod
    def convertir_fecha(fecha_usuario):
        return datetime.strptime(fecha_usuario, "%Y-%m-%d").date()
    
    def registrar_prestamo(self):
        if self._libro.estado == "disponible":
            self._usuario.pedir_libro(self._libro)
            self._libro.prestar()
            Prestamo._prestamos.append(self)


    def devolver_libro(self):
        if self._libro.estado == "prestado":
            self._usuario.devolver_libro(self._libro)
            self._libro.devolver()
            Prestamo._prestamos.remove(self)

    @classmethod
    def guardar_prestamos(cls, archivo = "prestamos.txt"):
        with open(archivo, "w", encoding="utf-8") as archivo:
            for prestamo in cls._prestamos:
                archivo.write(repr(prestamo) + "\n")

    @classmethod
    def cargar_prestamos(cls, archivo = "prestamos.txt"):
        try:
            with open(archivo, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    titulo_libro, autor_libro, codigo_libro, estado_libro, nombre_usuario, id_usuario, fecha_prestamo, fecha_devolucion = linea.strip().split(', ')
                    prestamo = Prestamo(Libro(titulo_libro, autor_libro, codigo_libro, estado_libro), Usuario(nombre_usuario, id_usuario, False), fecha_prestamo, fecha_devolucion)
                    prestamo._libro._estado = estado_libro
                    Prestamo._prestamos.append(prestamo)
        except FileNotFoundError:
            with open(archivo, "w", encoding="utf-8") as archivo:
                pass


    def __str__(self):
        return f"Prestamo: [libro: {self._libro}], autor: [{self._usuario}], fecha de prestamo {self._fecha_prestamo}, fecha de devolucion: {self._fecha_devolucion}"

    def __repr__(self):
        return f"{self._libro.titulo}, {self._libro.autor}, {self._libro.codigo}, {self._libro.estado}, {self._usuario._nombre}, {self._usuario._id}, {self._fecha_prestamo}, {self._fecha_devolucion}"
        

#bloque de pruebas
usuario1 = Usuario("Juan", "ABPRO1")
print((usuario1))
lector = Lector("Cynthia", "ABPRO3")
admin = Administrador("Roberto", "ABPRO2")
libro1 = Libro("El grabado en la casa", "H.P. Lovecraft", "ABP001")
admin.agregar_libro(libro1)
Libro.guardar_catalogo()
print(Libro._catalogo)
libro2 = Libro("El modelo de Pickman", "H.P. Lovecraft", "ABP002")
admin.agregar_libro(libro2)
Libro.guardar_catalogo()
Libro._catalogo.clear()
print(Libro._catalogo)
Libro.cargar_catalogo()
print(Libro._catalogo)
print(Libro.contar_libros())
print(Prestamo._prestamos)
prestamo = Prestamo(libro1, lector, "2024-10-01", "2024-10-07")
print(prestamo)
Prestamo.registrar_prestamo(prestamo)
print(Prestamo._prestamos)
Prestamo.guardar_prestamos()
Prestamo._prestamos.clear()
print(Prestamo._prestamos)
Prestamo.cargar_prestamos()
print(Prestamo._prestamos)