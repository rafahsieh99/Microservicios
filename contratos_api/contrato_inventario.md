# API de Microservicio de Inventario

# 1. Agregar Inventario
- **Ruta:** `/inventario`
- **Método:** `POST`
- **Descripción:** Agrega un nuevo producto al inventario.

**Request Body**
```json
{
  "producto_id": "integer",
  "cantidad": "integer"
}
```
**Respuestas**
```json
201 Creado
{
  "mensaje": "Inventario agregado",
  "id": "integer"  // ID del inventario creado
}

404 Not Found
{
  "mensaje": "Producto no encontrado"
}

```
# 2. Obtener Todo el Inventario
- **Ruta:** `/inventario`
- **Método:** `GET`
- **Descripción:** Devuelve una lista de todos los inventarios almacenados en la base de datos

**Respuestas**
```json
220 OK
[
  {
    "id": "integer",
    "producto_id": "integer",
    "cantidad": "integer"
  },
]

```
# 3. Obtener Inventario por ID
- **Ruta:** /inventario/<id>
- **Metodo:** `GET`
- **Descripción:** Devuelve los detalles de un invenatario especifico segun su ID
- **Path Parameter:**
**id(integer):** ID del inventario que se desea obtener

**Respuestas**
```json
200 OK
{
  "id": "integer",
  "producto_id": "integer",
  "cantidad": "integer"
}

404 Not Found
{
  "mensaje": "Inventario no encontrado"
}
