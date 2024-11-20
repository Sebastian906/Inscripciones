import logging
import sqlite3
import json
import csv
from typing import List, Dict
from base_datos import BaseDatos
from modelo import Estudiante, Materia

class ProcesadorInscripciones:
    def __init__(self):
        self.db = BaseDatos()
        
    def procesar_archivo(self, ruta_archivo: str):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    try:
                        cedula, nombre, codigo, materia = linea.strip().split(',')
                        estudiante = Estudiante(cedula=cedula, nombre=nombre)
                        materia_obj = Materia(codigo=codigo, nombre=materia)
                        self.db.insertar_estudiante(estudiante)
                        self.db.insertar_materia(materia_obj)
                        self.db.insertar_inscripcion(cedula, codigo)
                    except ValueError as e:
                        logging.error(f"Error al procesar línea: {linea.strip()}. Error: {str(e)}")
                        continue
            logging.info("Archivo procesado exitosamente")
        except FileNotFoundError:
            logging.error(f"No se encontró el archivo: {ruta_archivo}")
        except Exception as e:
            logging.error(f"Error al procesar el archivo: {str(e)}")

    def exportar_json(self, ruta_salida: str):
        """Exporta los datos a un archivo JSON."""
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT e.cedula, e.nombre, m.codigo, m.nombre
                FROM estudiantes e
                JOIN inscripciones i ON e.cedula = i.cedula_estudiante
                JOIN materias m ON i.codigo_materia = m.codigo
            ''')
            
            datos = []
            for row in cursor.fetchall():
                datos.append({
                    "cedula": row[0],
                    "estudiante": row[1],
                    "codigo_materia": row[2],
                    "materia": row[3]
                })
            
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
                
            logging.info(f"Datos exportados exitosamente a {ruta_salida}")
        finally:
            conn.close()
    
    def exportar_csv(self, ruta_salida: str):
        """Exporta los datos a un archivo CSV."""
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT e.cedula, e.nombre, m.codigo, m.nombre
                FROM estudiantes e
                JOIN inscripciones i ON e.cedula = i.cedula_estudiante
                JOIN materias m ON i.codigo_materia = m.codigo
            ''')
            
            with open(ruta_salida, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Cédula', 'Estudiante', 'Código Materia', 'Materia'])
                writer.writerows(cursor.fetchall())
                
            logging.info(f"Datos exportados exitosamente a {ruta_salida}")
        finally:
            conn.close()