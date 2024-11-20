import sqlite3
from typing import List, Dict
from modelo import Estudiante, Materia

class ConsultasDB:
    def __init__(self, db_name: str = "inscripciones.db"):
        self.db_name = db_name

    def consultar_estudiante(self, cedula: str) -> Dict[str, str]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT e.nombre, GROUP_CONCAT(m.nombre) AS materias
                FROM estudiantes e
                JOIN inscripciones i ON e.cedula = i.cedula_estudiante
                JOIN materias m ON i.codigo_materia = m.codigo
                WHERE e.cedula = ?
                GROUP BY e.nombre
            """, (cedula,))
            result = cursor.fetchone()
            if result:
                return {'nombre': result[0], 'materias': result[1].split(',')}
            else:
                return {}
        finally:
            conn.close()

    def obtener_estadisticas_inscripciones(self) -> Dict[str, int]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM estudiantes) AS total_estudiantes,
                    (SELECT COUNT(*) FROM materias) AS total_materias,
                    (SELECT COUNT(*) FROM inscripciones) AS total_inscripciones
            """)
            result = cursor.fetchone()
            return {
                'Total de estudiantes': result[0],
                'Total de materias': result[1],
                'Total de inscripciones': result[2]
            }
        finally:
            conn.close()

    def insertar_nuevo_registro(self, cedula: str, nombre: str, codigo: str, materia: str) -> bool:
        """
        Inserta un nuevo registro en las tablas correspondientes.
        Retorna True si la inserción fue exitosa, False en caso contrario.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            # Comenzar transacción
            conn.execute("BEGIN TRANSACTION")
            
            # Insertar estudiante si no existe
            cursor.execute(
                "INSERT OR IGNORE INTO estudiantes (cedula, nombre) VALUES (?, ?)",
                (cedula, nombre)
            )
            
            # Insertar materia si no existe
            cursor.execute(
                "INSERT OR IGNORE INTO materias (codigo, nombre) VALUES (?, ?)",
                (codigo, materia)
            )
            
            # Insertar inscripción
            cursor.execute(
                "INSERT OR IGNORE INTO inscripciones (cedula_estudiante, codigo_materia) VALUES (?, ?)",
                (cedula, codigo)
            )
            
            # Confirmar transacción
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            # Si hay error, deshacer cambios
            conn.rollback()
            print(f"Error en la base de datos: {e}")
            return False
        finally:
            conn.close()

    def ver_todos_registros(self) -> List[Dict[str, str]]:
        """
        Obtiene todos los registros de inscripciones con la información completa.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT e.cedula, e.nombre, m.codigo, m.nombre
                FROM estudiantes e
                JOIN inscripciones i ON e.cedula = i.cedula_estudiante
                JOIN materias m ON i.codigo_materia = m.codigo
                ORDER BY e.nombre, m.nombre
            """)
            
            registros = []
            for row in cursor.fetchall():
                registros.append({
                    'cedula': row[0],
                    'estudiante': row[1],
                    'codigo': row[2],
                    'materia': row[3]
                })
            return registros
        finally:
            conn.close()