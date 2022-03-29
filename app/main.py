import re
from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status
from starlette.responses import RedirectResponse
from . import models, schemas
from .conexion import SessionLocal, engine
from sqlalchemy.orm import Session

# Se obtiene la información de los modelos y objetos mapeados.
models.Base.metadata.create_all(bind=engine)

# Definición de la aplicación.
app = FastAPI()

# Obtener la conexion y la sesión de la base de datos.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Path Operations

## Home
@app.get(path="/")
def main():
    """
    Redirección a la documentación de Swagger

    """
    return RedirectResponse(url="/docs/")

### Mostrar los usuarios
@app.get(
    path="/users",
    response_model=List[schemas.Usuario],
    status_code=status.HTTP_200_OK,
    summary="Mostrar usuarios",
    tags = ["Usuarios"]
)
def show_all_users(db: Session = Depends(get_db)):
    """
    Mostrar todos los usuarios

    Esta path operation muestra a todos los usuarios de la base de datos.

    Parametros:
    -db: Session

    Regresa una lista con la información de cada usuario:
    - usuario_id: int
    - nombre: str
    """
    usuarios = db.query(models.Usuario).all()
    return usuarios

### Crear un usuario
@app.post(
    path="/users/create",
    response_model=schemas.Usuario,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un usuario",
    tags = ["Usuarios"]
)
def create_user(entrada: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    """
    Crear un usuario

    Esta path operation crea un usuario en la base de datos.

    Parametros:
    - entrada: UsuarioCrear
    - db: Session

    Regresa el usuario creado:
    - usuario_id: int
    - nombre: str
    """
    usuario = models.Usuario(nombre = entrada.nombre)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

### Actualizar un usuario
@app.put(
    path="/users/update/{usuario_id}",
    response_model=schemas.Usuario,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un usuario",
    tags = ["Usuarios"]
)
def update_user(usuario_id: int, entrada: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    """
    Actualizar un usuario

    Esta path operation actualiza los datos de un usuario existente en la bd.

    Parametros:
    - usuario_id: int
    - entrada: UsuarioCrear
    - db: Session

    Regresa el usuario modificado:
    - usuario_id: int
    - nombre: str
    
    """
    usuario = db.query(models.Usuario).filter_by(id_usuario=usuario_id).first()
    usuario.nombre = entrada.nombre
    db.commit()
    db.refresh(usuario)
    return usuario

### Borrar un usuario
@app.delete(
    path="/users/delete/{usuario_id}",
    response_model=schemas.Respuesta,
    status_code=status.HTTP_200_OK,
    summary="Borrar un usuario",
    tags = ["Usuarios"]
)
def delete_user(usuario_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un usuario

    Esta path operation elimina un usuario existente en la bd.

    Parametros:
    - usuario_id: int
    - db: Session

    Regresa un mensaje indicando que el usuario se eliminó correctamente.
    
    """
    usuario = db.query(models.Usuario).filter_by(id_usuario=usuario_id).first()
    db.delete(usuario)
    db.commit()
    respuesta = schemas.Respuesta(mensaje = "Usuario eliminado exitosamente")
    return respuesta

### Mostrar los colores
@app.get(
    path="/colors",
    status_code=status.HTTP_200_OK,
    summary="Mostrar colores",
    tags = ["Colors"]
)
def show_all_colors(db: Session = Depends(get_db), page: int = 1, page_size: int = 4):
    """
    Mostrar todos los colores

    Esta path operation muestra a todos los colores de la base de datos.

    Parametros:
    - db: Session

    Regresa una lista con la información de cada color:
    - color_id: int
    - nombre_color: str
    - Color: str
    - pantone_color: str
    - año_color: str
    """
    colores = db.query(models.Colores).all()

    # Agregamos en "#" para que aparezca en el JSON, más no se guarda en la base de datos.
    for m in colores:
        m.color = "#"+m.color

    # Aparecerá primero los colores que fueron creados últimos
    colores.reverse()

    # Paginación
    start = (page - 1) * page_size
    end = start + page_size

    response = {
        "Colors": colores[start:end],
        "pages": (len(colores) // page_size) + 1,
        "pagination": {}
    }

    if end >= len(colores):
        response["pagination"]["next"] = None

        if page > 1:
            response["pagination"]["previous"] = f"/colors?page={page-1}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page > 1:
            response["pagination"]["previous"] = f"/colors?page={page-1}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"]["next"] = f"/colors?page={page+1}"

    return response

### Crear un color
@app.post(
    path="/colors/create",
    response_model=schemas.Colores,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un color",
    tags = ["Colors"]
)
def create_color(entrada: schemas.ColoresCrear, response: Response, db: Session = Depends(get_db)):
    """
    Crear un color

    Esta path operation crea un color en la base de datos.

    Parametros:
    - entrada: ColoresCrear
    - response: Response
    - db: Session

    Regresa el color creado indicando su información:
    - color_id: int
    - nombre_color: str
    - Color: str
    - pantone_color: str
    - año_color: str
    
    """
    def ValidarHexadecimal(numeroHexa):
        """
        Verifica si el color ingresado es un hexadecimal

        Parametros:
        - numeroHexa: str

        Regresa un valor booleano true si es hexadecimal y false si no lo es
        
        """
        regex = "^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

        p = re.compile(regex)

        if(str == None):
            return False

        if(re.search(p, numeroHexa)):
            return True
        else:
            return False
    
    if len(entrada.color) == 6 and ValidarHexadecimal(entrada.color):
        color = models.Colores(nombre_color = entrada.nombre_color, color = entrada.color, pantone_color = entrada.pantone_color, año_color = entrada.año_color)
        db.add(color)
        db.commit()
        db.refresh(color)
        color.color = "#"+color.color
        return color
    else:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    

### Mostrar un color
@app.get(
    path="/colors/show/{color_id}",
    response_model=schemas.Colores,
    status_code=status.HTTP_200_OK,
    summary="Mostrar un color",
    tags = ["Colors"]
)
def show_color(color_id: int, db: Session = Depends(get_db)):
    """
    Mostrar un color

    Esta path operation muestra un color existente en la bd.

    Parametros: 
    - color_id: int
    - db: Session

    Regresa el color solicitado mediante el id_color:
    - color_id: int
    - nombre_color: str
    - Color: str
    - pantone_color: str
    - año_color: str
    
    """
    color = db.query(models.Colores).filter_by(id_color=color_id).first()
    db.commit()
    db.refresh(color)
    color.color = "#"+color.color
    return color

### Actualizar un color
@app.put(
    path="/colors/update/{color_id}",
    response_model=schemas.Colores,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un color",
    tags = ["Colors"]
)
def update_color(color_id: int, entrada: schemas.ColoresCrear, db: Session = Depends(get_db)):
    """
    Actualizar un color

    Esta path operation actualiza los datos de un color existente en la bd.

    Parametros: None

    Regresa el color actualizado indicando su información final:
    - color_id: int
    - nombre_color: str
    - Color: str
    - pantone_color: str
    - año_color: str
    
    """
    color = db.query(models.Colores).filter_by(id_color=color_id).first()
    color.nombre_color = entrada.nombre_color
    color.color = entrada.color
    color.pantone_color = entrada.pantone_color
    color.año_color = entrada.año_color
    db.commit()
    db.refresh(color)
    color.color = "#"+color.color
    
    return color
    
### Borrar un color
@app.delete(
    path="/colors/delete/{color_id}",
    response_model=schemas.Respuesta,
    status_code=status.HTTP_200_OK,
    summary="Borrar un color",
    tags = ["Colors"]
)
def delete_color(color_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un color

    Esta path operation elimina un color existente en la bd.

    Parametros: 
    - color_id: int
    - db: Session

    Regresa un mensaje indicando que el usuario se eliminó correctamente.
    - Mensaje: str
    
    """
    color = db.query(models.Colores).filter_by(id_color=color_id).first()
    db.delete(color)
    db.commit()
    respuesta = schemas.Respuesta(mensaje = "Color eliminado exitosamente")
    return respuesta