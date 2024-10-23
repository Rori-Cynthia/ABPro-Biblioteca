class LibroNoDisponibleError(Exception):
    def __init__(self, mensaje="El libro no se encuentra disponible en el inventario."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class LibroNoPrestadoError(Exception):
    def __init__(self, mensaje="El libro ya se encuentra en el inventario y no puede ser devuelto."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class LibroNoEncontradoError(Exception):
    def __init__(self, mensaje="El libro no se encuentra registrado en el sistema."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class LibroNoEnPrestamoError(Exception):
    def __init__(self, mensaje="El libro no se encuentra en la lista de prestamos de este usuario."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class FechaPrestamoNoValidaError(Exception):
    def __init__(self, mensaje="La fecha de devolución es mayor a la fecha de prestamo."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)