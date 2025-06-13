# 🛍️ Product Service

**Product Service** es una API REST desarrollada con Flask que implementa un microservicio para la gestión de productos, siguiendo los principios de arquitectura hexagonal.

## 🚀 Tecnologías Utilizadas

- **Python 3.9+**
- **Flask 2.3.2** - Framework web
- **PostgreSQL 13** - Base de datos
- **SQLAlchemy** - ORM para Python
- **Docker & Docker Compose** - Contenedorización
- **psycopg2-binary** - Adaptador PostgreSQL para Python

## 📁 Estructura del Proyecto

```
ProductService/
├── app/                           # Código de la aplicación
│   ├── adapters/                 # Capa de adaptadores
│   │   ├── controller/           # Controladores HTTP (Flask)
│   │   │   └── product_controller.py
│   │   └── repository/           # Repositorios de datos
│   ├── domain/                   # Lógica de negocio y entidades
│   │   └── product.py           # Entidad Product
│   ├── ports/                    # Interfaces/Puertos
│   ├── use_cases/               # Casos de uso de la aplicación
│   ├── config/                  # Configuración de la aplicación
│   └── docs/                    # Documentación
│       └── swagger/             # Especificaciones Swagger/OpenAPI
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias de Python
├── Dockerfile                   # Configuración de Docker
├── docker-compose.yml          # Orquestación de contenedores
├── .dockerignore               # Archivos excluidos de Docker
├── .gitignore                  # Archivos excluidos de Git
├── CHANGELOG.md                # Registro de cambios
├── LICENSE                     # Licencia del proyecto
└── README.md                   # Este archivo
```

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (versión 4.0 o superior)
- **[Docker Compose](https://docs.docker.com/compose/install/)** (incluido con Docker Desktop)

### Verificar Instalación

```bash
# Verificar Docker
docker --version

# Verificar Docker Compose
docker-compose --version
```

## ⚡ Instalación y Ejecución

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd ProductService
```

### 2. Configurar Variables de Entorno (Opcional)

Crea un archivo `.env` si necesitas personalizar la configuración:

```env
# Base de datos
DATABASE_URL=postgresql://postgres:postgres@db:5432/productdb

# Flask
FLASK_APP=main.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=productdb
```

### 3. Ejecutar la Aplicación

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Para ejecutar en segundo plano
docker-compose up -d --build
```

### 4. Verificar que Funciona

La aplicación estará disponible en:

- **API**: http://localhost:5000
- **Base de datos**: localhost:5432

## 📡 Endpoints de la API

La API está disponible en: **http://localhost:5000**  
Documentación Swagger: **http://localhost:5000/swagger/**

### Productos

| Método   | Endpoint                | Descripción                 |
| -------- | ----------------------- | --------------------------- |
| `GET`    | `/api/v1/products`      | Obtener todos los productos |
| `GET`    | `/api/v1/products/{id}` | Obtener producto por ID     |
| `POST`   | `/api/v1/products`      | Crear nuevo producto        |
| `PUT`    | `/api/v1/products/{id}` | Actualizar producto         |
| `DELETE` | `/api/v1/products/{id}` | Eliminar producto           |

### Estructura del Producto

```json
{
  "name": "Tomates Cherry",
  "farm_id": 1,
  "type": "Vegetal",
  "quantity": 100,
  "price_per_unit": 2.5,
  "description": "Tomates cherry frescos de temporada",
  "harvest_date": "2023-12-01T10:00:00Z",
  "created_at": "2023-12-01T08:00:00Z"
}
```

### Ejemplos de Uso

#### 1. Obtener todos los productos

```bash
curl http://localhost:5000/api/v1/products
```

**Respuesta:**

```json
[
  {
    "product_id": 1,
    "name": "Tomates Cherry",
    "farm_id": 1,
    "type": "Vegetal",
    "quantity": 100,
    "price_per_unit": 2.5,
    "description": "Tomates cherry frescos de temporada",
    "harvest_date": "2023-12-01T10:00:00Z",
    "created_at": "2023-12-01T08:00:00Z"
  }
]
```

#### 2. Obtener producto por ID

```bash
curl http://localhost:5000/api/v1/products/1
```

#### 3. Crear un producto

```bash
curl -X POST http://localhost:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu-token-jwt" \
  -d '{
    "name": "Tomates Cherry",
    "type": "Vegetal",
    "quantity": 100,
    "price_per_unit": 2.50,
    "description": "Tomates cherry frescos de temporada",
    "harvest_date": "2023-12-01T10:00:00Z"
  }'
```

**Campos requeridos:**

- `name` (string): Nombre del producto
- `type` (string): Tipo de producto
- `quantity` (integer): Cantidad disponible
- `price_per_unit` (float): Precio por unidad
- `description` (string): Descripción del producto

**Campos opcionales:**

- `harvest_date` (string, ISO format): Fecha de cosecha (por defecto: fecha actual)


#### 4. Actualizar un producto

```bash
curl -X PUT http://localhost:5000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tomates Cherry Orgánicos",
    "price_per_unit": 3.00,
    "quantity": 150
  }'
```

**Nota:** Todos los campos son opcionales en la actualización. Solo se actualizarán los campos proporcionados.

#### 5. Eliminar un producto

```bash
curl -X DELETE http://localhost:5000/api/v1/products/1
```

### Códigos de Respuesta

| Código | Descripción                 |
| ------ | --------------------------- |
| `200`  | Operación exitosa           |
| `201`  | Recurso creado exitosamente |
| `400`  | Datos de entrada inválidos  |
| `404`  | Recurso no encontrado       |
| `500`  | Error interno del servidor  |

## 🗄️ Base de Datos

### Estructura de la Arquitectura Hexagonal

```
app/
├── adapters/           # Capa de adaptadores (infraestructura)
│   ├── controller/    # Controladores HTTP (entrada)
│   └── repository/    # Repositorios de datos (salida)
├── domain/            # Lógica de negocio y entidades
├── ports/             # Interfaces/Puertos (contratos)
├── use_cases/         # Casos de uso (lógica de aplicación)
├── config/            # Configuración de la aplicación
└── docs/              # Documentación API (Swagger)
```

**Principios implementados:**

- **Separación de responsabilidades**: Cada capa tiene una responsabilidad específica
- **Inversión de dependencias**: El dominio no depende de la infraestructura
- **Puertos y adaptadores**: Interfaces claras entre capas
- **Testabilidad**: Arquitectura que facilita las pruebas unitarias
