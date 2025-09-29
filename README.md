# VISE Payments API 💳

API REST construida con *FastAPI* que implementa las restricciones y beneficios descritos en la actividad VISE.  
Permite registrar clientes con diferentes tipos de tarjeta (Classic, Gold, Platinum, Black, White) y realizar compras aplicando beneficios o rechazándolas según las reglas de negocio.

---

## 🚀 Características

- *Registro de clientes* (POST /client):
  - Valida ingresos mínimos por tipo de tarjeta.
  - Requiere membresía *VISE Club* para Platinum, Black y White.
  - Black/White: no se permite residencia en {China, Vietnam, India, Irán}.

- *Compras* (POST /purchase):
  - Aplica *solo un beneficio (el mejor)* según día, monto y país.
  - Black/White: se rechazan compras hechas *desde países restringidos*.
  - Respuesta incluye: monto original, descuento aplicado, monto final y detalle del beneficio.

- *Swagger UI* automático en:  
  👉 http://localhost:8000/docs

---

## 📂 Estructura del proyecto

vise_api/
│
├── app/
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── models.py            # Schemas Pydantic
│   ├── rules.py             # Reglas de negocio
│   └── routers/             # Endpoints
│       ├── clients.py       # /client
│       └── purchases.py     # /purchase
│
├── tests/                   # Pruebas con pytest
│   ├── conftest.py
│   ├── test_clients.py
│   └── test_purchases.py
│
├── requirements.txt         # Dependencias principales
├── requirements-dev.txt     # Dependencias de desarrollo (pytest, httpx, etc.)
├── pytest.ini               # Configuración pytest
│
├── Dockerfile               # Imagen de producción
├── docker-compose.yml       # Orquestación para dev (hot reload)
├── Dockerfile.test          # Imagen para ejecutar tests en Docker
└── README.md                # Este archivo

---

## 🔧 Instalación y ejecución

### 1) Local (sin Docker)

Instalar dependencias principales:
bash
pip install -r requirements.txt


Levantar el servidor en modo desarrollo:
bash
python -m uvicorn app.main:app --reload


Abrir en el navegador: http://127.0.0.1:8000/docs

---

### 2) Docker (producción simple)

Construir la imagen:
bash
docker build -t vise-api:latest .


Ejecutar el contenedor:
bash
docker run --name vise_api -p 8000:8000 vise-api:latest


---

### 3) Docker Compose (modo desarrollo con autoreload)

bash
docker compose up --build


Esto monta la carpeta ./app dentro del contenedor y permite hot reload.

---

### 4) Pruebas automatizadas

#### Local
Instalar dependencias de desarrollo (incluye pytest y httpx):
bash
pip install -r requirements-dev.txt


Ejecutar tests:
bash
python -m pytest


#### Docker
Construir imagen de pruebas:
bash
docker build -f Dockerfile.test -t vise-api-tests .


Ejecutar pruebas dentro del contenedor:
bash
docker run --rm vise-api-tests


---

## 🛠 Tecnologías utilizadas
- [FastAPI](https://fastapi.tiangolo.com/) 🚀
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- [Pydantic](https://docs.pydantic.dev/) (validación de datos)
- [Pytest](https://docs.pytest.org/) (testing)
- [Docker](https://www.docker.com/)