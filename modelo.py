from dataclasses import dataclass

@dataclass
class Estudiante:
    cedula: str
    nombre: str

@dataclass
class Materia:
    codigo: str
    nombre: str

@dataclass
class Inscripcion:
    estudiante: Estudiante
    materia: Materia