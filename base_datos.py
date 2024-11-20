import sqlite3
from typing import Dict, List
from modelo import Estudiante, Materia

class BaseDatos:
    def __init__(self, db_name: str = "inscripciones.db"):
        self.db_name = db_name
        self.crear_tablas()
    
    def crear_tablas(self):
        """Crea las tablas necesarias en la base de datos."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            cedula TEXT PRIMARY KEY,
            nombre TEXT NOT NULL
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL
        )''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscripciones (
            cedula_estudiante TEXT,
            codigo_materia TEXT,
            PRIMARY KEY (cedula_estudiante, codigo_materia),
            FOREIGN KEY (cedula_estudiante) REFERENCES estudiantes(cedula),
            FOREIGN KEY (codigo_materia) REFERENCES materias(codigo)
        )''')
        
        conn.commit()
        conn.close()
    
    def insertar_estudiante(self, estudiante: Estudiante):
        """Inserta un estudiante en la base de datos."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO estudiantes (cedula, nombre) VALUES (?, ?)",
                (estudiante.cedula, estudiante.nombre)
            )
            conn.commit()
        finally:
            conn.close()
    
    def insertar_materia(self, materia: Materia):
        """Inserta una materia en la base de datos."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO materias (codigo, nombre) VALUES (?, ?)",
                (materia.codigo, materia.nombre)
            )
            conn.commit()
        finally:
            conn.close()
    
    def insertar_inscripcion(self, cedula: str, codigo_materia: str):
        """Inserta una inscripción en la base de datos."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO inscripciones (cedula_estudiante, codigo_materia) VALUES (?, ?)",
                (cedula, codigo_materia)
            )
            conn.commit()
        finally:
            conn.close()
    
    def obtener_materias_por_estudiante(self) -> Dict[str, int]:
        """Retorna un diccionario con el total de materias por estudiante."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT e.nombre, COUNT(i.codigo_materia) as total_materias
                FROM estudiantes e
                LEFT JOIN inscripciones i ON e.cedula = i.cedula_estudiante
                GROUP BY e.cedula, e.nombre
            ''')
            return {row[0]: row[1] for row in cursor.fetchall()}
        finally:
            conn.close()
    
    def obtener_estudiantes_por_materia(self, codigo_materia: str) -> List[str]:
        """Retorna una lista de estudiantes inscritos en una materia específica."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT e.nombre
                FROM estudiantes e
                JOIN inscripciones i ON e.cedula = i.cedula_estudiante
                WHERE i.codigo_materia = ?
            ''', (codigo_materia,))
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()