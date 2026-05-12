from abc import ABC, abstractmethod
import logging
# Sistema desarrollado para Software FJ
# ==========================================
# Configuración del sistema de logs
# ==========================================

logging.basicConfig(
    filename='logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================

class ClienteError(Exception):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


# ==========================================
# CLASE ABSTRACTA ENTIDAD
# ==========================================

class Entidad(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


# ==========================================
# CLASE CLIENTE
# ==========================================

class Cliente(Entidad):

    def __init__(self, nombre, correo, telefono):

        try:

            if not nombre.strip():
                raise ClienteError("El nombre no puede estar vacío")

            if "@" not in correo:
                raise ClienteError("Correo inválido")

            if len(telefono) < 7:
                raise ClienteError("Teléfono inválido")

            self.__nombre = nombre
            self.__correo = correo
            self.__telefono = telefono

            logging.info(f"Cliente creado correctamente: {nombre}")

        except ClienteError as e:
            logging.error(f"Error al crear cliente: {e}")
            raise

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} | Correo: {self.__correo}"


# ==========================================
# # Clase abstracta de servicios
# ==========================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa_base):

        if tarifa_base <= 0:
            raise ServicioError("La tarifa debe ser mayor que cero")

        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# ==========================================
# SERVICIO 1 - RESERVA DE SALA
# ==========================================

class ReservaSala(Servicio):

    def __init__(self, capacidad):
        super().__init__("Reserva Sala", 50000)
        self.capacidad = capacidad

    def calcular_costo(self, horas, impuesto=0, descuento=0):

        if horas <= 0:
            raise ServicioError("Las horas deben ser mayores que cero")

        costo = self.tarifa_base * horas
        costo += costo * impuesto
        costo -= descuento

        return costo

    def descripcion(self):
        return f"Servicio de reserva de sala para {self.capacidad} personas"


# ==========================================
# SERVICIO 2 - ALQUILER DE EQUIPOS
# ==========================================

class AlquilerEquipo(Servicio):

    def __init__(self, tipo_equipo):
        super().__init__("Alquiler Equipo", 80000)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, horas, impuesto=0, descuento=0):

        if horas <= 0:
            raise ServicioError("Horas inválidas")

        costo = self.tarifa_base * horas
        costo += costo * impuesto
        costo -= descuento

        return costo

    def descripcion(self):
        return f"Alquiler de equipo tipo {self.tipo_equipo}"


# ==========================================
# SERVICIO 3 - ASESORÍA ESPECIALIZADA
# ==========================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, area):
        super().__init__("Asesoría Especializada", 120000)
        self.area = area

    def calcular_costo(self, horas, impuesto=0, descuento=0):

        if horas <= 0:
            raise ServicioError("Cantidad de horas inválida")

        costo = self.tarifa_base * horas
        costo += costo * impuesto
        costo -= descuento

        return costo

    def descripcion(self):
        return f"Asesoría especializada en {self.area}"


# ==========================================
# Clase encargada de gestionar reservas
# ==========================================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        try:

            if not isinstance(cliente, Cliente):
                raise ReservaError("Cliente inválido")

            if not isinstance(servicio, Servicio):
                raise ReservaError("Servicio inválido")

            if horas <= 0:
                raise ReservaError("La duración debe ser mayor que cero")

            self.cliente = cliente
            self.servicio = servicio
            self.horas = horas
            self.estado = "Pendiente"

            logging.info(
                f"Reserva creada para {cliente.nombre}"
            )

        except Exception as e:
            logging.error(f"Error creando reserva: {e}")
            raise ReservaError("No se pudo crear la reserva") from e

    def confirmar(self):

        try:
            self.estado = "Confirmada"

            logging.info(
                f"Reserva confirmada para {self.cliente.nombre}"
            )

        except Exception as e:
            logging.error(f"Error confirmando reserva: {e}")

    def cancelar(self):

        try:
            self.estado = "Cancelada"

            logging.info(
                f"Reserva cancelada para {self.cliente.nombre}"
            )

        except Exception as e:
            logging.error(f"Error cancelando reserva: {e}")

    def procesar_pago(self, impuesto=0.19, descuento=0):

        try:

            costo = self.servicio.calcular_costo(
                self.horas,
                impuesto,
                descuento
            )

        except ServicioError as e:

            logging.error(f"Error calculando costo: {e}")
            raise

        else:

            logging.info(f"Pago procesado correctamente: {costo}")
            return costo

        finally:

            logging.info("Finalizó proceso de pago")

    def mostrar_reserva(self):

        return (
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Estado: {self.estado}"
        )

# Simulación de operaciones válidas e inválidas
# ==========================================
# SIMULACIONES
# ==========================================

print("\n========== SOFTWARE FJ ==========")
print("SISTEMA DE GESTIÓN DE RESERVAS\n")

reservas = []

# ------------------------------------------
# SIMULACIÓN 1
# Cliente válido
# ------------------------------------------

try:

    cliente1 = Cliente(
        "Carlos Pérez",
        "carlos@gmail.com",
        "3124567890"
    )

    print(cliente1.mostrar_info())

except Exception as e:
    print(e)


# ------------------------------------------
# SIMULACIÓN 2
# Cliente inválido
# ------------------------------------------

try:

    cliente2 = Cliente(
        "",
        "correo_malo",
        "123"
    )

except Exception as e:
    print(f"Error detectado: {e}")


# ------------------------------------------
# SIMULACIÓN 3
# Servicio válido
# ------------------------------------------

try:

    sala = ReservaSala(20)

    print(sala.descripcion())

except Exception as e:
    print(e)


# ------------------------------------------
# SIMULACIÓN 4
# Servicio inválido
# ------------------------------------------

try:

    servicio_error = AlquilerEquipo("Laptop")

    servicio_error.tarifa_base = -500

    servicio_error.calcular_costo(2)

except Exception as e:
    print(f"Error servicio: {e}")


# ------------------------------------------
# SIMULACIÓN 5
# Reserva válida
# ------------------------------------------

try:

    reserva1 = Reserva(cliente1, sala, 3)

    reserva1.confirmar()

    valor = reserva1.procesar_pago()

    print(reserva1.mostrar_reserva())
    print(f"Costo total: {valor}")

    reservas.append(reserva1)

except Exception as e:
    print(e)


# ------------------------------------------
# SIMULACIÓN 6
# Reserva inválida
# ------------------------------------------

try:

    reserva2 = Reserva(cliente1, sala, -2)

except Exception as e:
    print(f"Error reserva: {e}")


# ------------------------------------------
# SIMULACIÓN 7
# Asesoría válida
# ------------------------------------------

try:

    asesoria = AsesoriaEspecializada("Ciberseguridad")

    reserva3 = Reserva(cliente1, asesoria, 5)

    reserva3.confirmar()

    total = reserva3.procesar_pago(
        impuesto=0.19,
        descuento=50000
    )

    print(reserva3.mostrar_reserva())
    print(f"Costo asesoría: {total}")

except Exception as e:
    print(e)


# ------------------------------------------
# SIMULACIÓN 8
# Error de cálculo
# ------------------------------------------

try:

    alquiler = AlquilerEquipo("VideoBeam")

    alquiler.calcular_costo(0)

except Exception as e:
    print(f"Error cálculo: {e}")


# ------------------------------------------
# SIMULACIÓN 9
# Cancelación de reserva
# ------------------------------------------

try:

    reserva1.cancelar()

    print(reserva1.mostrar_reserva())

except Exception as e:
    print(e)


# ------------------------------------------
# SIMULACIÓN 10
# Cliente inválido en reserva
# ------------------------------------------

try:

    reserva_invalida = Reserva(
        "cliente falso",
        sala,
        2
    )

except Exception as e:
    print(f"Error final detectado: {e}")


print("\n========== SISTEMA FINALIZADO ==========")
print("El sistema continuó funcionando correctamente")
