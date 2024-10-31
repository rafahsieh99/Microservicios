# API de Microservicio de Productos 

### 1. Crear Producto
- **Ruta:** `/productos`
- **Método:** `POST`
- **Descripción:** Crea un nuevo producto con nombre, precio y descripción.

#### Request Body
```json
{
  "nombre": "string",
  "precio": "integer",
  "descripcion": "string"
}

Respuestas:
201 Created
{
  "mensaje": "Producto creado",
  "id": "integer"  // ID del producto creado
}
400 Bad Request - Si el cuerpo de la solicitud está incompleto.

# Obtener Todos los Productos

- **Ruta:** `/productos`
- **Método:** `GET`
- **Descripción:** Devuelve una lista de todos los productos almacenados en la base de datos.

## Respuestas

### 200 OK
Devuelve un array de objetos, cada uno representando un producto.

```json
[
  {
    "id": "integer",
    "nombre": "string",
    "precio": "integer",
    "descripcion": "string"
  },

]


# Obtener Producto por ID

- **Ruta:** `/productos/<id>`
- **Método:** `GET`
- **Descripción:** Devuelve los detalles de un producto específico según su ID.

## Path Parameter
- **id** (`integer`): ID del producto que se desea obtener.

## Respuestas

### 200 OK
Devuelve los detalles del producto solicitado.

```json
{
  "id": "integer",
  "nombre": "string",
  "precio": "integer",
  "descripcion": "string"
}

### 404 Not Found
Devuelve un mensaje de error si el producto no se encuentra
{
  "mensaje": "Producto no encontrado"
}


# Actualizar Producto

- **Ruta:** `/productos/<id>`
- **Método:** `PUT`
- **Descripción:** Actualiza el nombre, precio y descripción de un producto específico.

## Path Parameter
- **id** (`integer`): ID del producto que se desea actualizar.

## Request Body
El cuerpo de la solicitud debe contener los siguientes parámetros:

```json
{
  "nombre": "string",
  "precio": "integer",
  "descripcion": "string"
}

## Respuestas

### 200 OK
Devuelve un mensaje de éxito si el producto fue actualizado correctamente
{
  "mensaje": "Producto actualizado"
}

### 404 Not Found
Devuelve un mensaje de error si el producto no se encuentra
{
  "mensaje": "Producto no encontrado"
}


# Eliminar Producto

- **Ruta:** `/productos/<id>`
- **Método:** `DELETE`
- **Descripción:** Elimina un producto de la base de datos según su ID.

## Path Parameter
- **id** (`integer`): ID del producto que se desea eliminar.

## Respuestas

### 204 No Content
Devuelve este código de estado si el producto fue eliminado exitosamente.

### 404 Not Found
Devuelve un mensaje de error si el producto no se encuentra.

```json
{
  "mensaje": "Producto no encontrado"
}
