# Proyecto de Microservicios de Gestión de Productos e Inventario

Este proyecto consiste en un conjunto de microservicios diseñados para gestionar productos e inventarios. Utiliza Flask como framework web y PostgreSQL como base de datos.

## Descripción de los Microservicios

### Microservicio de Productos

El microservicio de productos permite realizar operaciones CRUD sobre productos. Las rutas disponibles son:

1. **Crear Producto**
   - **Ruta:** `/productos`
   - **Método:** `POST`
   - **Descripción:** Crea un nuevo producto con nombre, precio y descripción.
   - **Request Body:**
     ```json
     {
       "nombre": "string",
       "precio": "integer",
       "descripcion": "string"
     }
     ```
   - **Respuestas:**
     - **201 Created**
     ```json
     {
       "mensaje": "Producto creado",
       "id": "integer"
     }
     ```
     - **400 Bad Request** (si el cuerpo de la solicitud está incompleto)

2. **Obtener Todos los Productos**
   - **Ruta:** `/productos`
   - **Método:** `GET`
   - **Descripción:** Devuelve una lista de todos los productos almacenados en la base de datos.
   - **Respuestas:**
     - **200 OK**
     ```json
     [
       {
         "id": "integer",
         "nombre": "string",
         "precio": "integer",
         "descripcion": "string"
       },
     ]
     ```

3. **Obtener Producto por ID**
   - **Ruta:** `/productos/<id>`
   - **Método:** `GET`
   - **Descripción:** Devuelve los detalles de un producto específico según su ID.
   - **Respuestas:**
     - **200 OK**
     ```json
     {
       "id": "integer",
       "nombre": "string",
       "precio": "integer",
       "descripcion": "string"
     }
     ```
     - **404 Not Found**
     ```json
     {
       "mensaje": "Producto no encontrado"
     }
     ```

4. **Actualizar Producto**
   - **Ruta:** `/productos/<id>`
   - **Método:** `PUT`
   - **Descripción:** Actualiza el nombre, precio y descripción de un producto específico.
   - **Request Body:**
     ```json
     {
       "nombre": "string",
       "precio": "integer",
       "descripcion": "string"
     }
     ```
   - **Respuestas:**
     - **200 OK**
     ```json
     {
       "mensaje": "Producto actualizado"
     }
     ```
     - **404 Not Found**
     ```json
     {
       "mensaje": "Producto no encontrado"
     }
     ```

5. **Eliminar Producto**
   - **Ruta:** `/productos/<id>`
   - **Método:** `DELETE`
   - **Descripción:** Elimina un producto de la base de datos según su ID.
   - **Respuestas:**
     - **204 No Content**
     - **404 Not Found**
     ```json
     {
       "mensaje": "Producto no encontrado"
     }
     ```

---

### Microservicio de Inventario

El microservicio de inventario permite gestionar la cantidad de productos disponibles en el inventario. Las rutas disponibles son:

1. **Agregar Inventario**
   - **Ruta:** `/inventario`
   - **Método:** `POST`
   - **Descripción:** Agrega un nuevo producto al inventario.
   - **Request Body:**
     ```json
     {
       "producto_id": "integer",
       "cantidad": "integer"
     }
     ```
   - **Respuestas:**
     - **201 Created**
     ```json
     {
       "mensaje": "Inventario agregado",
       "id": "integer"
     }
     ```
     - **404 Not Found** (si el producto no existe)
     ```json
     {
       "mensaje": "Producto no encontrado"
     }
     ```

2. **Obtener Todo el Inventario**
   - **Ruta:** `/inventario`
   - **Método:** `GET`
   - **Descripción:** Devuelve una lista de todos los inventarios almacenados en la base de datos.
   - **Respuestas:**
     - **200 OK**
     ```json
     [
       {
         "id": "integer",
         "producto_id": "integer",
         "cantidad": "integer"
       },
     ]
     ```

3. **Obtener Inventario por ID**
   - **Ruta:** `/inventario/<id>`
   - **Método:** `GET`
   - **Descripción:** Devuelve los detalles de un inventario específico según su ID.
   - **Respuestas:**
     - **200 OK**
     ```json
     {
       "id": "integer",
       "producto_id": "integer",
       "cantidad": "integer"
     }
     ```
     - **404 Not Found**
     ```json
     {
       "mensaje": "Inventario no encontrado"
     }
     ```

## Requisitos

- Python 3.x
- Flask
- psycopg2
- PostgreSQL

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>

2. Crea y activa un entorno virtual: 
python -m venv venv
source venv/bin/activate  # Para Linux o Mac
venv\Scripts\activate  # Para Windows

3. Instala las dependecias:
pip install -r requirements.txt

4. Configura la base de datos en db.py y ajusta cualquier otra configuracion necesaria.

## Ejecucion
1. Para iniciar el microservicio de productos
- python app.py

2. Para iniciar el microservicio de inventario
- python app.py

## Contribuciones
Las contribuciones son bienvenidas, sientete libre de enviar un pull request o abrir un problema :)


