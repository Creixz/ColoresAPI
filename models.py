from sqlalchemy import Column, Integer, String
from .conexion import Base

class Usuario(Base):

    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(50))

class Colores(Base):
    
    __tablename__ = "colores"

    id_color = Column(Integer, primary_key=True, index=True)

    nombre_color = Column(String(40))

    color = Column(String(6))

    pantone_color = Column(String(7))

    año_color = Column(String(4))

