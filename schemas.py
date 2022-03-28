from pydantic import BaseModel, Field

class Usuario(BaseModel):
    id_usuario: int = Field(...)
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    class Config:
        orm_mode = True

class Colores(BaseModel):
    id_color: int = Field(...)
    nombre_color: str = Field(
        ...,
        min_length=1,
        max_length=40
    )
    color: str = Field(
        ...,
        min_length=6,
        max_length=6
    )
    pantone_color: str = Field(
        ...,
        min_length=7,
        max_length=7
    )
    anio_color: str = Field(
        ...,
        min_length=4,
        max_length=4
    )
    class Config:
        orm_mode = True