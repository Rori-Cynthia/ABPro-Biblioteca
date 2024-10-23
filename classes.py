from excepciones import LibroNoDisponibleError,LibroNoPrestadoError, LibroNoEnPrestamoError

class Usuario:
    _numero_usuarios = 0
    _usuarios = {}

    def __init__(self, nombre: str, id: str):
        self._nombre = nombre
        self._id = id

        if self.id_es_valido(self._id):
            Usuario._numero_usuarios += 1
            Usuario._usuarios[self._nombre] = self._id
        else:
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
        return f'Usuario({self._nombre!r}, {self._id!r})'
    

class Lector(Usuario):
    def __init__(self):
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
    def agregar_libro(self, libro):
        pass
        

class Libro():
    _cantidad_de_libros = 0
    
    def __init__(self, titulo: str, autor: str, codigo: str):
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
    def contar_usuarios(cls):
        return cls._cantidad_de_libros

    def __str__(self):
        return f"Libro: titulo: {self.titulo}, autor: {self.autor}, codigo {self.codigo}, estado: {self._estado}"

    def __repr__(self):
        return f'Usuario({self.titulo!r}, {self.autor!r}), {self.codigo!r}, {self._estado}'


usuario1 = Usuario("Juan", "ABPRO1")
print(str(usuario1))
libro1 = Libro("El grabado en la casa", "H.P. Lovecraft", "ABP001")
print(str(libro1))
libro1.prestar()
print(str(libro1))
libro1.devolver()
print(str(libro1))
print(Libro._cantidad_de_libros)
libro2 = Libro("El modelo de Pickman", "H.P. Lovecraft", "ABP002")
print(Libro._cantidad_de_libros)
