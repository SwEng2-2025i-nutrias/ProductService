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
├── app/                     # Código de la aplicación
│   ├── adapters/           # Adaptadores (controladores, repositorios)
│   └── config/             # Configuración de la aplicación
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias de Python
├── Dockerfile             # Configuración de Docker
├── docker-compose.yml     # Orquestación de contenedores
├── .dockerignore          # Archivos excluidos de Docker
└── README.md              # Este archivo
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

### Productos

| Método   | Endpoint         | Descripción                 |
| -------- | ---------------- | --------------------------- |
| `GET`    | `/products`      | Obtener todos los productos |
| `GET`    | `/products/{id}` | Obtener producto por ID     |
| `POST`   | `/products`      | Crear nuevo producto        |
| `PUT`    | `/products/{id}` | Actualizar producto         |
| `DELETE` | `/products/{id}` | Eliminar producto           |

### Ejemplos de Uso

```bash
# Obtener todos los productos
curl http://localhost:5000/products

# Crear un producto
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Producto Test", "price": 99.99}'
```

## 🗄️ Base de Datos

### Acceso Directo a PostgreSQL

```bash
# Conectar a la base de datos
docker-compose exec db psql -U postgres -d productdb

# Comandos SQL útiles
\dt          # Listar tablas
\d products  # Describir tabla products
SELECT * FROM products;  # Ver todos los productos
```

### Credenciales por Defecto

- **Usuario**: postgres
- **Contraseña**: postgres
- **Base de datos**: productdb
- **Puerto**: 5432




### Ejemplo de Configuración de Producción

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    build: .
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
```



### Estructura de la Arquitectura Hexagonal

```
app/
├── adapters/           # Capa de adaptadores
│   ├── controller/    # Controladores HTTP
│   └── repository/    # Repositorios de datos
├── domain/            # Lógica de negocio
└── config/            # Configuración
```

