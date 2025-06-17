# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

## [0.3.0] - 2025-06-15

### Agregado

- Adición de test para el controlador del producto

### Cambiado

- Se hace modificaciones a README.md

## [0.2.0] - 2025-06-12

### Agregado

- Documentación completa de la API con Swagger/Flasgger
- Configuración automática de Swagger UI en `/swagger/`

### Cambiado

- Refactorización del método `create_product` para simplificar parámetros
- Rutas de productos con prefijo de versión (`/api/v1/products`)

## [0.1.1] - 2025-06-11

### Agregado

- CRUD completo de productos con SQLAlchemy
- Entidad `Product` con campos extendidos (farm_id, type, quantity, price_per_unit, etc.)
- Arquitectura hexagonal (dominio, puertos, adaptadores, casos de uso)

## [0.1.0] - 2025-06-11

### Agregado

- Primera versión funcional del servicio de productos con Flask
- Configuración de Docker y base de datos
