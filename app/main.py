from fastapi import FastAPI
from .routers import clients, purchases

app = FastAPI(title="VISE Payments API", version="1.0.0")

# Incluimos los routers
app.include_router(clients.router)
app.include_router(purchases.router)
