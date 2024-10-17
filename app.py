import threading
import time
import random
import math

# Clase que representa el sistema de reserva de boletos
class TicketBookingSystem:
    def __init__(self, size, total_seats):
        self.size = size  # Tamaño de la matriz (filas y columnas)
        self.total_seats = total_seats  # Total de asientos disponibles
        self.available_seats = total_seats  # Contador de asientos disponibles
        self.seats = [['[O]' for _ in range(size)] for _ in range(size)]  # O = Asiento disponible
        self.lock = threading.Lock()  # Mutex para proteger el acceso a asientos

        # Marcar los asientos sobrantes como no disponibles
        extra_seats = size * size - total_seats
        for i in range(extra_seats):
            row = (total_seats + i) // size
            col = (total_seats + i) % size
            self.seats[row][col] = '[-]'  # Asiento no disponible

        # Crear una lista de asientos disponibles
        self.available_seats_list = [(i, j) for i in range(size) for j in range(size) if self.seats[i][j] == '[O]']

    def display_seats(self):
        print("Estado de los asientos:")
        print("    " + "   ".join(str(j) for j in range(self.size)))  # Encabezado de columnas
        for i, row in enumerate(self.seats):
            print(f"{i} | " + ' '.join(row))  # Indicar índice de fila
        print("\n")

    def reserve_ticket(self, user_id):
        with self.lock:  # Adquirir el bloqueo antes de acceder a los asientos
            if self.available_seats <= 0:
                print(f"Usuario {user_id} no pudo reservar. No hay asientos disponibles.")
                return
            
            # Seleccionar aleatoriamente un asiento de la lista de asientos disponibles
            i, j = random.choice(self.available_seats_list)
            print(f"Usuario {user_id} reservando asiento en ({i}, {j})...")
            time.sleep(random.uniform(0.1, 0.5))  # Simula el tiempo de reserva
            self.seats[i][j] = '[X]'  # X = Asiento reservado
            self.available_seats -= 1  # Decrementar el contador de asientos disponibles
            self.available_seats_list.remove((i, j))  # Remover el asiento reservado de la lista
            print(f"Asiento reservado para el usuario {user_id} en ({i}, {j}).")
            self.display_seats()  # Mostrar estado actualizado

# Función que representa la acción de un usuario que intenta reservar un boleto
def user_action(user_id, booking_system):
    booking_system.reserve_ticket(user_id)

# Solicitar al usuario la cantidad total de asientos
total_seats = int(input("Ingrese la cantidad total de asientos: "))

# Calcular el tamaño de la matriz cuadrada
size = math.ceil(math.sqrt(total_seats))

# Crear el sistema de reserva de boletos
booking_system = TicketBookingSystem(size, total_seats)

# Mostrar el estado inicial de los asientos
booking_system.display_seats()

# Crear múltiples hilos para simular usuarios
threads = []
for user_id in range(10):  # 10 usuarios intentando reservar
    thread = threading.Thread(target=user_action, args=(user_id, booking_system))
    threads.append(thread)
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

print("Reserva de boletos finalizada.")
