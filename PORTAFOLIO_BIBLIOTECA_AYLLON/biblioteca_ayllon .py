from datetime import date


ARCHIVO_LIBROS = "libros.txt"
ARCHIVO_PRESTAMOS = "prestamos.txt"

LIBROS_INICIALES = [
    {"codigo": 1, "titulo": "Python para todos", "autor": "Charles Severance", "estado": "Disponible"},
    {"codigo": 2, "titulo": "Aprende Java", "autor": "Ana Torres", "estado": "Disponible"},
    {"codigo": 3, "titulo": "Bases de datos", "autor": "Carlos Mora", "estado": "Disponible"},
]


def guardar_libros(libros):
    with open(ARCHIVO_LIBROS, "w", encoding="utf-8") as archivo:
        for libro in libros:
            linea = f"{libro['codigo']},{libro['titulo']},"
            linea += f"{libro['autor']},{libro['estado']}\n"
            archivo.write(linea)


def cargar_libros():
    libros = []

    try:
        with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")

                libros.append({
                    "codigo": int(datos[0]),
                    "titulo": datos[1],
                    "autor": datos[2],
                    "estado": datos[3]
                })

    except FileNotFoundError:
        print("No se encontró libros.txt: se usan los libros iniciales.")

        for libro in LIBROS_INICIALES:
            libros.append(dict(libro))

        guardar_libros(libros)

    return libros


def guardar_prestamos(prestamos):
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
        for prestamo in prestamos:
            linea = f"{prestamo['numero']},{prestamo['codigo_libro']},"
            linea += f"{prestamo['estudiante']},{prestamo['fecha']},"
            linea += f"{prestamo['estado']}\n"
            archivo.write(linea)


def cargar_prestamos():
    prestamos = []

    try:
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")

                prestamos.append({
                    "numero": int(datos[0]),
                    "codigo_libro": int(datos[1]),
                    "estudiante": datos[2],
                    "fecha": datos[3],
                    "estado": datos[4]
                })

    except FileNotFoundError:
        print("No se encontró prestamos.txt: se inicia sin préstamos.")
        guardar_prestamos(prestamos)

    return prestamos


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe escribir un número entero.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto == "":
            print("Error: este campo no puede estar vacío.")

        elif "," in texto:
            print("Error: no use comas en este campo.")

        else:
            return texto


def buscar_por_codigo(libros, codigo):
    for libro in libros:
        if libro["codigo"] == codigo:
            return libro

    return None


def registrar_libro(libros):
    titulo = leer_texto("Título del libro: ")
    autor = leer_texto("Autor del libro: ")

    codigo_siguiente = 1

    for libro in libros:
        if libro["codigo"] >= codigo_siguiente:
            codigo_siguiente = libro["codigo"] + 1

    libro_nuevo = {
        "codigo": codigo_siguiente,
        "titulo": titulo,
        "autor": autor,
        "estado": "Disponible"
    }

    libros.append(libro_nuevo)
    guardar_libros(libros)

    print(f"Libro registrado con el código {codigo_siguiente}.")
    return libro_nuevo


def mostrar_libros(libros):
    print(f"\n{'CÓDIGO':<8} {'TÍTULO':<30} {'AUTOR':<25} ESTADO")
    print("-" * 78)

    for libro in libros:
        print(f"{libro['codigo']:<8} {libro['titulo']:<30} "
              f"{libro['autor']:<25} {libro['estado']}")

    print(f"Total de libros: {len(libros)}")
    return len(libros)


def buscar_libro(libros):
    palabra = leer_texto("Palabra a buscar en el título: ")
    encontrados = 0

    for libro in libros:
        if palabra.lower() in libro["titulo"].lower():
            print(f"{libro['codigo']}: {libro['titulo']} - "
                  f"{libro['autor']} ({libro['estado']})")
            encontrados += 1

    if encontrados == 0:
        print("No se encontraron libros con esa palabra.")

    return encontrados


def prestar_libro(libros, prestamos):
    codigo = leer_entero("Código del libro a prestar: ")
    libro = buscar_por_codigo(libros, codigo)

    if libro is None:
        print("Error: no existe un libro con ese código.")
        return False

    if libro["estado"] == "Prestado":
        print("Error: el libro ya está prestado.")
        return False

    estudiante = leer_texto("Nombre del estudiante: ")

    numero_siguiente = 1

    for prestamo in prestamos:
        if prestamo["numero"] >= numero_siguiente:
            numero_siguiente = prestamo["numero"] + 1

    prestamo_nuevo = {
        "numero": numero_siguiente,
        "codigo_libro": codigo,
        "estudiante": estudiante,
        "fecha": str(date.today()),
        "estado": "Activo"
    }

    prestamos.append(prestamo_nuevo)
    libro["estado"] = "Prestado"

    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print(f"Préstamo #{numero_siguiente} registrado correctamente.")
    return True


def devolver_libro(libros, prestamos):
    codigo = leer_entero("Código del libro a devolver: ")
    libro = buscar_por_codigo(libros, codigo)

    if libro is None:
        print("Error: no existe un libro con ese código.")
        return False

    if libro["estado"] == "Disponible":
        print("Error: el libro no está prestado.")
        return False

    for prestamo in prestamos:
        if prestamo["codigo_libro"] == codigo and prestamo["estado"] == "Activo":
            libro["estado"] = "Disponible"
            prestamo["estado"] = "Devuelto"

            guardar_libros(libros)
            guardar_prestamos(prestamos)

            print("Libro devuelto correctamente.")
            return True

    return False


def mostrar_prestamos(prestamos, libros):
    print(f"\n{'NÚMERO':<8} {'LIBRO':<30} {'ESTUDIANTE':<24} "
          f"{'FECHA':<12} ESTADO")
    print("-" * 92)

    for prestamo in prestamos:
        libro = buscar_por_codigo(libros, prestamo["codigo_libro"])

        print(f"{prestamo['numero']:<8} {libro['titulo']:<30} "
              f"{prestamo['estudiante']:<24} {prestamo['fecha']:<12} "
              f"{prestamo['estado']}")

    return len(prestamos)


def reporte_general(libros, prestamos):
    disponibles = 0
    prestados = 0
    activos = 0

    for libro in libros:
        if libro["estado"] == "Disponible":
            disponibles += 1
        else:
            prestados += 1

    for prestamo in prestamos:
        if prestamo["estado"] == "Activo":
            activos += 1

    try:
        porcentaje = prestados * 100 / len(libros)

    except ZeroDivisionError:
        porcentaje = 0

    print("\n========== REPORTE GENERAL ==========")
    print(f"Total de libros:          {len(libros)}")
    print(f"Libros disponibles:       {disponibles}")
    print(f"Libros prestados:         {prestados}")
    print(f"Préstamos registrados:    {len(prestamos)}")
    print(f"Préstamos activos:        {activos}")
    print(f"Porcentaje prestado:      {porcentaje:.1f}%")

    return porcentaje


def main():
    libros = cargar_libros()
    prestamos = cargar_prestamos()
    opcion = 0

    while opcion != 8:
        print("""
==================================
   BIBLIOTECA DIGITAL TEC AZUAY
==================================
1. Registrar libro      5. Devolver libro
2. Mostrar libros       6. Mostrar préstamos
3. Buscar libro         7. Reporte general
4. Prestar libro        8. Salir""")

        opcion = leer_entero("Elija una opción: ")

        if opcion == 1:
            registrar_libro(libros)

        elif opcion == 2:
            mostrar_libros(libros)

        elif opcion == 3:
            buscar_libro(libros)

        elif opcion == 4:
            prestar_libro(libros, prestamos)

        elif opcion == 5:
            devolver_libro(libros, prestamos)

        elif opcion == 6:
            mostrar_prestamos(prestamos, libros)

        elif opcion == 7:
            reporte_general(libros, prestamos)

        elif opcion == 8:
            guardar_libros(libros)
            guardar_prestamos(prestamos)
            print("Datos guardados. ¡Hasta pronto!")

        else:
            print("Opción no válida: elija un número del 1 al 8.")


main()