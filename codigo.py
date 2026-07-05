"""
Sistema de gestión de préstamos y devoluciones de una biblioteca.
Trabajo Final Integrador - Algoritmos y Estructuras de Datos - ISI

import datetime

# =========================================================
# CONSTANTES GLOBALES
# =========================================================
PLAZO_MAXIMO_DIAS = 7       # días permitidos antes de generar multa
MULTA_POR_DIA = 100         # valor de la multa por cada día de atraso

# =========================================================
# ESTRUCTURAS DE DATOS PRINCIPALES
# =========================================================
# libros: diccionario -> clave = ISBN, valor = datos del libro
# ejemplo: {"111": {"titulo": "Python", "autor": "Juan", "total": 3, "disponibles": 2}}
libros = {}

# usuarios: diccionario -> clave = DNI, valor = nombre del usuario
usuarios = {}

# prestamos: lista de diccionarios con cada préstamo realizado
# ejemplo: {"dni": "123", "isbn": "111", "dia_prestamo": 5, "dia_devolucion": None}
prestamos = []

# ACUMULADORES / CONTADORES (se piden explícitamente en la consigna)
contador_prestamos_totales = 0        # cuenta cuántos préstamos se hicieron en total
contador_devoluciones_totales = 0     # cuenta cuántas devoluciones se hicieron
contador_por_libro = {}               # cuántas veces se prestó cada libro (isbn -> cantidad)
total_recaudado_multas = 0            # acumulador de dinero recaudado por multas


# =========================================================
# FUNCIONES DE VALIDACIÓN (manejo de errores)
# =========================================================

def leer_entero(mensaje, minimo=None):
    """
    Pide un número entero por teclado y NO deja avanzar hasta que
    el dato sea válido. Maneja el error si el usuario ingresa texto.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"⚠ El valor debe ser mayor o igual a {minimo}. Intente nuevamente.")
                continue
            return valor
        except ValueError:
            print("⚠ Error: debe ingresar un número entero válido.")


def leer_texto_no_vacio(mensaje):
    """
    Pide un texto por teclado y valida que no esté vacío.
    """
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            print("⚠ Error: el campo no puede estar vacío.")
        else:
            return valor


def leer_opcion_menu(minimo, maximo):
    """
    Valida que la opción elegida en un menú esté dentro del rango permitido.
    """
    return leer_entero(f"Ingrese una opción ({minimo} a {maximo}): ", minimo)


# =========================================================
# FUNCIONES DEL SISTEMA
# =========================================================

def registrar_usuario():
    """Registra un nuevo usuario en el diccionario 'usuarios'."""
    print("\n--- Registro de usuario ---")
    dni = leer_texto_no_vacio("Ingrese DNI del usuario: ")

    # Validación: evitar usuarios duplicados
    if dni in usuarios:
        print("⚠ Ya existe un usuario registrado con ese DNI.")
        return

    nombre = leer_texto_no_vacio("Ingrese nombre y apellido: ")
    usuarios[dni] = {"nombre": nombre}
    print(f"✔ Usuario '{nombre}' registrado correctamente.")


def registrar_libro():
    """Registra un nuevo libro (o suma ejemplares si el ISBN ya existe)."""
    print("\n--- Registro de libro ---")
    isbn = leer_texto_no_vacio("Ingrese ISBN o código del libro: ")

    if isbn in libros:
        # Si el libro ya existe, se pueden sumar más ejemplares
        cantidad_extra = leer_entero("El libro ya existe. ¿Cuántos ejemplares desea agregar?: ", 1)
        libros[isbn]["total"] += cantidad_extra
        libros[isbn]["disponibles"] += cantidad_extra
        print("✔ Ejemplares agregados correctamente.")
        return

    titulo = leer_texto_no_vacio("Ingrese título: ")
    autor = leer_texto_no_vacio("Ingrese autor: ")
    cantidad = leer_entero("Ingrese cantidad de ejemplares: ", 1)

    libros[isbn] = {
        "titulo": titulo,
        "autor": autor,
        "total": cantidad,
        "disponibles": cantidad
    }
    contador_por_libro[isbn] = 0
    print(f"✔ Libro '{titulo}' registrado correctamente.")


def buscar_prestamo_activo(dni, isbn):
    """
    Función auxiliar: recorre la lista de préstamos y busca uno activo
    (sin devolver) que coincida con el dni y el isbn indicados.
    Devuelve el diccionario del préstamo o None si no lo encuentra.
    """
    for prestamo in prestamos:
        if (prestamo["dni"] == dni and prestamo["isbn"] == isbn
                and prestamo["dia_devolucion"] is None):
            return prestamo
    return None


def prestar_libro():
    """Gestiona el préstamo de un libro a un usuario, con validaciones."""
    global contador_prestamos_totales

    print("\n--- Préstamo de libro ---")

    if not usuarios:
        print("⚠ No hay usuarios registrados. Registre uno primero.")
        return
    if not libros:
        print("⚠ No hay libros registrados. Registre uno primero.")
        return

    dni = leer_texto_no_vacio("DNI del usuario: ")
    if dni not in usuarios:
        print("⚠ Error: no existe un usuario con ese DNI.")
        return

    isbn = leer_texto_no_vacio("ISBN del libro solicitado: ")
    if isbn not in libros:
        print("⚠ Error: no existe un libro con ese ISBN.")
        return

    # Validación de disponibilidad
    if libros[isbn]["disponibles"] <= 0:
        print(f"⚠ No hay ejemplares disponibles de '{libros[isbn]['titulo']}' en este momento.")
        return

    dia_prestamo = leer_entero("Ingrese el día actual (número de día, ej: 1, 2, 3...): ", 0)

    # Se registra el préstamo
    nuevo_prestamo = {
        "dni": dni,
        "isbn": isbn,
        "dia_prestamo": dia_prestamo,
        "dia_devolucion": None
    }
    prestamos.append(nuevo_prestamo)

    # Actualización de disponibilidad y acumuladores/contadores
    libros[isbn]["disponibles"] -= 1
    contador_prestamos_totales += 1
    contador_por_libro[isbn] = contador_por_libro.get(isbn, 0) + 1

    print(f"✔ Préstamo registrado: '{libros[isbn]['titulo']}' a {usuarios[dni]['nombre']}.")
    print(f"  Debe devolverlo antes del día {dia_prestamo + PLAZO_MAXIMO_DIAS} para evitar multas.")


def devolver_libro():
    """Gestiona la devolución de un libro y calcula multa si corresponde."""
    global contador_devoluciones_totales, total_recaudado_multas

    print("\n--- Devolución de libro ---")
    dni = leer_texto_no_vacio("DNI del usuario: ")
    isbn = leer_texto_no_vacio("ISBN del libro a devolver: ")

    prestamo = buscar_prestamo_activo(dni, isbn)

    if prestamo is None:
        print("⚠ Error: no se encontró un préstamo activo con esos datos.")
        return

    dia_devolucion = leer_entero("Ingrese el día actual de la devolución: ", 0)

    dias_transcurridos = dia_devolucion - prestamo["dia_prestamo"]
    multa = 0

    # Estructura condicional: se calcula multa solo si se excedió el plazo
    if dias_transcurridos > PLAZO_MAXIMO_DIAS:
        dias_atraso = dias_transcurridos - PLAZO_MAXIMO_DIAS
        multa = dias_atraso * MULTA_POR_DIA
        total_recaudado_multas += multa
        print(f"⚠ Devolución fuera de término ({dias_atraso} día/s de atraso).")
        print(f"  Multa a pagar: ${multa}")
    else:
        print("✔ Devolución realizada en tiempo y forma. Sin multa.")

    # Se actualiza el préstamo y la disponibilidad del libro
    prestamo["dia_devolucion"] = dia_devolucion
    libros[isbn]["disponibles"] += 1
    contador_devoluciones_totales += 1

    print(f"✔ Libro '{libros[isbn]['titulo']}' devuelto correctamente.")


def mostrar_disponibilidad():
    """Muestra el listado completo de libros y su disponibilidad."""
    print("\n--- Disponibilidad de libros ---")
    if not libros:
        print("No hay libros cargados en el sistema.")
        return

    # Estructura repetitiva: recorre todos los libros del diccionario
    for isbn, datos in libros.items():
        print(f"ISBN: {isbn} | '{datos['titulo']}' - {datos['autor']} "
              f"| Disponibles: {datos['disponibles']}/{datos['total']}")


def mostrar_prestamos_activos():
    """Muestra los préstamos que todavía no fueron devueltos."""
    print("\n--- Préstamos activos ---")
    hay_activos = False

    for prestamo in prestamos:
        if prestamo["dia_devolucion"] is None:
            hay_activos = True
            nombre_usuario = usuarios[prestamo["dni"]]["nombre"]
            titulo_libro = libros[prestamo["isbn"]]["titulo"]
            print(f"- {nombre_usuario} tiene '{titulo_libro}' "
                  f"(prestado el día {prestamo['dia_prestamo']})")

    if not hay_activos:
        print("No hay préstamos activos en este momento.")


def mostrar_estadisticas():
    """Muestra estadísticas generales del sistema."""
    print("\n--- Estadísticas de la biblioteca ---")
    print(f"Total de préstamos realizados: {contador_prestamos_totales}")
    print(f"Total de devoluciones realizadas: {contador_devoluciones_totales}")
    print(f"Total recaudado en multas: ${total_recaudado_multas}")

    if not contador_por_libro:
        print("Aún no hay datos suficientes sobre libros más solicitados.")
        return

    # Se busca el libro más solicitado recorriendo el diccionario acumulador
    isbn_mas_solicitado = None
    cantidad_maxima = -1

    for isbn, cantidad in contador_por_libro.items():
        if cantidad > cantidad_maxima:
            cantidad_maxima = cantidad
            isbn_mas_solicitado = isbn

    if isbn_mas_solicitado is not None and cantidad_maxima > 0:
        titulo = libros[isbn_mas_solicitado]["titulo"]
        print(f"Libro más solicitado: '{titulo}' ({cantidad_maxima} préstamos)")
    else:
        print("Todavía no se registraron préstamos.")


# =========================================================
# MENÚ PRINCIPAL
# =========================================================

def mostrar_menu():
    print("\n============ BIBLIOTECA ============")
    print("1. Registrar usuario")
    print("2. Registrar libro")
    print("3. Prestar libro")
    print("4. Devolver libro")
    print("5. Ver disponibilidad de libros")
    print("6. Ver préstamos activos")
    print("7. Ver estadísticas")
    print("8. Salir")
    print("=====================================")


def main():
    """Función principal: controla el ciclo de ejecución del programa."""
    print("Bienvenido/a al Sistema de Gestión de Biblioteca")

    opcion = 0
    # Estructura repetitiva principal: se repite hasta que el usuario elige salir
    while opcion != 8:
        mostrar_menu()
        opcion = leer_opcion_menu(1, 8)

        # Estructura condicional: deriva a la función correspondiente
        if opcion == 1:
            registrar_usuario()
        elif opcion == 2:
            registrar_libro()
        elif opcion == 3:
            prestar_libro()
        elif opcion == 4:
            devolver_libro()
        elif opcion == 5:
            mostrar_disponibilidad()
        elif opcion == 6:
            mostrar_prestamos_activos()
        elif opcion == 7:
            mostrar_estadisticas()
        elif opcion == 8:
            print("\nGracias por usar el sistema. ¡Hasta luego!")
        else:
            print("⚠ Opción inválida.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
