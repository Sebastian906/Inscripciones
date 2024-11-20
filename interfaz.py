from inscripciones import ProcesadorInscripciones
from consultas_db import ConsultasDB
from base_datos import BaseDatos

class InterfazConsola:
    def __init__(self):
        self.procesador = ProcesadorInscripciones()
        self.consultas = ConsultasDB()
        self.base_datos = BaseDatos()

    def mostrar_menu(self):
        while True:
            print("\n=== SISTEMA DE INSCRIPCIONES ===")
            print("1. Cargar archivo de inscripciones")
            print("2. Mostrar total de materias por estudiante")
            print("3. Filtrar estudiantes por materia")
            print("4. Exportar datos")
            print("5. Mostrar consultas avanzadas")
            print("6. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.cargar_archivo()
            elif opcion == "2":
                self.mostrar_totales()
            elif opcion == "3":
                self.filtrar_estudiantes()
            elif opcion == "4":
                self.exportar_datos()
            elif opcion == "5":
                self.menu_consultas()
            elif opcion == "6":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, intente nuevamente.")

    def cargar_archivo(self):
        ruta = input("Ingrese la ruta del archivo de inscripciones: ")
        self.procesador.procesar_archivo(ruta)  

    def mostrar_totales(self):
        totales = self.procesador.db.obtener_materias_por_estudiante()
        print("\nTotal de materias por estudiante:")
        for estudiante, total in totales.items():
            print(f"{estudiante}: {total} materias")

    def filtrar_estudiantes(self):
        codigo = input("Ingrese el código de la materia: ")
        estudiantes = self.procesador.db.obtener_estudiantes_por_materia(codigo)
        if estudiantes:
            print("\nEstudiantes inscritos:")
            for estudiante in estudiantes:
                print(f"- {estudiante}")
        else:
            print("No se encontraron estudiantes inscritos en esta materia.")

    def exportar_datos(self):
        print("\nFormato de exportación:")
        print("1. JSON")
        print("2. CSV")

        opcion = input("Seleccione el formato: ")
        ruta = input("Ingrese la ruta de salida: ")

        if opcion == "1":
            self.procesador.exportar_json(ruta)
        elif opcion == "2":
            self.procesador.exportar_csv(ruta)
        else:
            print("Opción inválida.")

    def menu_consultas(self):
        while True:
            print("\n=== CONSULTAS AVANZADAS ===")
            print("1. Buscar estudiante por cédula")
            print("2. Ver estadísticas generales")
            print("3. Insertar nuevo registro")
            print("4. Ver todos los registros")
            print("5. Volver al menú principal")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                cedula = input("Ingrese la cédula del estudiante: ")
                estudiante = self.consultas.consultar_estudiante(cedula)
                if estudiante:
                    print(f"\nNombre: {estudiante['nombre']}")
                    print(f"Materias: {', '.join(estudiante['materias'])}")
                else:
                    print("Estudiante no encontrado")
            elif opcion == "2":
                stats = self.consultas.obtener_estadisticas_inscripciones()
                for key, value in stats.items():
                    print(f"{key}: {value}")
            elif opcion == "3":
                self.insertar_nuevo_registro()
            elif opcion == "4":
                self.mostrar_todos_registros()
            elif opcion == "5":
                break
            else:
                print("Opción inválida. Por favor, intente nuevamente.")

    def insertar_nuevo_registro(self):
        print("\n=== INSERTAR NUEVO REGISTRO ===")
        cedula = input("Ingrese la cédula del estudiante: ")
        nombre = input("Ingrese el nombre del estudiante: ")
        codigo = input("Ingrese el código de la materia: ")
        materia = input("Ingrese el nombre de la materia: ")

        if self.consultas.insertar_nuevo_registro(cedula, nombre, codigo, materia):
            print("\n¡Registro insertado exitosamente!")
        else:
            print("\nHubo un error al insertar el registro. Por favor, intente nuevamente.")

    def mostrar_todos_registros(self):
        print("\n=== TODOS LOS REGISTROS EN LA BASE DE DATOS ===")
        registros = self.consultas.ver_todos_registros()
        if registros:
            print("\nCédula      | Estudiante          | Código | Materia")
            print("-" * 60)
            for reg in registros:
                print(f"{reg['cedula']:<11} | {reg['estudiante']:<18} | {reg['codigo']:<6} | {reg['materia']}")
        else:
            print("No hay registros en la base de datos.")

if __name__ == "__main__":
    interfaz = InterfazConsola()
    interfaz.mostrar_menu()