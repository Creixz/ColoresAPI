# ColoresAPI
Esta aplicación construida con Python permite realizar un CRUD completo de colores y usuarios, además toda la información se guarda en una base de datos. Por otro lado, cuentan con validaciones y una documentación en Swagger.

![](https://fv9-4.failiem.lv/thumb_show.php?i=3djtscddm&view)
#Tecnologías y Frameworks utilizados
Para este proyecto se utilizó:
- Lenguaje de programación: **Python**
- Framework de Python: **FastAPI**
- Base de datos: **MySQL**
- Emulador de terminal: **Cmder**
- Editor de código: **VSCode**
- Servidor virtual: **WAMP**

#Instalación de dependencias y despliegue del proyecto
- Importamos nuestra base de datos a **MySQL**
- Nos aseguramos de tener instalado **Cmder**, **Python** y **VSCode**
- Abrimos **Cmder** y por medio del comando **cd** a la carpeta donde está el proyecto
- Una vez dentro de la carpeta del proyecto, crearemos el entorno virtual con el comando:
 - **py -m venv venv**
- Entramos al entorno virtual con el comando:
  - .\venv\Scripts\activate
- Dentro del entorno virtual, instalamos las siguientes dependencias:
  - **pip install fastapi**
  - **pip install sqlalchemy**
  - **pip install mysql**
  - **pip install mysql-connector**
  - **pip install uvicorn**
- Con las dependencias instaladas abrimos el **VSCode** con el comando:
  - **code .**
- Verificamos que todo este correcto con el entorno virtual y volvemos a **Cmder** para iniciar la aplicación(**API**) con el comando:
  -  **uvicorn app.main:app --reload**
- Nos dirigimos a la dirección que nos indica y **está listo**.

#Poblar la base de datos
- Corremos nuestro servidor virtual **WampServer**
- Entramos a **localhost** en el navegador
- En Tools le damos click a **phpmyadmin**
- Creamos una base de datos llamada **colores_api**
- Le damos click a **importar** y seleccionamos el archivo **colores_api.sql** que esta en la carpeta **DataBase** del proyecto.
- Se cargará la base de datos con toda la información previa.
