# API de Microservicio de Productos e Inventario

# 1. Crear Producto
- **Ruta:** /productos
- **Método:** POST
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
```json
201 Created
{
  "mensaje": "Producto creado",
  "id": "integer"  // ID del producto creado
}
400 Bad Request - Si el cuerpo de la solicitud está incompleto.

```
# 2. Obtener Todos los Productos
- **Ruta:** /productos
- **Método:** GET
- **Descripción:** Devuelve una lista de todos los productos almacenados en la base de datos.
- **Respuestas:**
```json
200 OK

[
  {
    "id": "integer",
    "nombre": "string",
    "precio": "integer",
    "descripcion": "string"
  },
]

```
# 3. Obtener Producto por ID
- **Ruta:** /productos/<id>
- **Método:** GET
- **Descripción:** Devuelve los detalles de un producto específico según su ID.
- **Path Parameter:**
 **id (integer):** ID del producto que se desea obtener.
**Respuestas:**
```json
200 OK:

{
  "id": "integer",
  "nombre": "string",
  "precio": "integer",
  "descripcion": "string"
}

404 Not Found:
{
  "mensaje": "Producto no encontrado"
}

```
# 4. Actualizar Producto
- **Ruta:** /productos/<id>
- **Método:** PUT
- **Descripción:** Actualiza el nombre, precio y descripción de un producto específico.
- **Path Parameter:**
 **id (integer):** ID del producto que se desea actualizar.
**Request Body:**
```json
{
  "nombre": "string",
  "precio": "integer",
  "descripcion": "string"
}
```
**Respuestas:**
```json

200 Ok:
{
  "mensaje": "Producto actualizado"
}

404 Not Found:
{
  "mensaje": "Producto no encontrado"
}

```
# 5. Eliminar Producto
- **Ruta:** /productos/<id>
- **Método:** DELETE
- **Descripción:** Elimina un producto de la base de datos según su ID.
- **Path Parameter:**
**id (integer):** ID del producto que se desea eliminar.
**Respuestas:**
```json
204 No Content:- El producto fue eliminado exitosamente.
404 Not Found: 
{
  "mensaje": "Producto no encontrado"
}
