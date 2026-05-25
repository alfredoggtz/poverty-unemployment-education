"""
main.py
-------
FastAPI backend for the poverty indicators data pipeline.

Exposes endpoints to:
    - Execute the three Python pipeline scripts
    - Stream their output in real time via Server-Sent Events (SSE)
    - Read and update config.txt
    - Query data from MySQL and MongoDB

Dependencies: fastapi, uvicorn, pymongo, mysql-connector-python
Run with:
    uvicorn main:app --reload --port 8000
"""

import os
import subprocess
import asyncio
from pathlib import Path
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from mysql.connector import connect, Error as MySQLError
from pymongo import MongoClient
from pymongo.errors import PyMongoError


# ── App setup ────────────────────────────────────────────────────────────────

app = FastAPI(title="Poverty Indicators API", version="1.0.0")

# Allow requests from the React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve paths relative to this file
BASE_DIR    = Path(__file__).parent
CONFIG_PATH = BASE_DIR.parent / "config.txt"
SCRIPTS     = {
    "extraction": BASE_DIR.parent / "DataExtraction" / "DataExtraction.py",
    "mysql":      BASE_DIR.parent / "MySQL"          / "InsertMySQL.py",
    "mongodb":    BASE_DIR.parent / "MongoBD"        / "ExportMongoDB.py",
}


# ── Config helpers ───────────────────────────────────────────────────────────

def leer_config() -> dict:
    """Parses config.txt into a dictionary."""
    config = {}
    with open(CONFIG_PATH, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if linea and '=' in linea:
                clave, valor = linea.split('=', 1)
                config[clave.strip()] = valor.strip()
    return config


def escribir_config(data: dict):
    """Writes a dictionary back to config.txt."""
    with open(CONFIG_PATH, 'w') as f:
        for clave, valor in data.items():
            f.write(f"{clave}={valor}\n")


# ── DB helpers ───────────────────────────────────────────────────────────────

def get_mysql_connection():
    """Returns an open MySQL connection using config.txt credentials."""
    cfg = leer_config()
    try:
        return connect(
            host=cfg['host'],
            user=cfg['user'],
            password=cfg['password'],
            database=cfg['database']
        )
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")


def get_mongo_db():
    """Returns the target MongoDB database using config.txt credentials."""
    cfg = leer_config()
    try:
        cliente = MongoClient(
            host=cfg['mongo_host'],
            port=int(cfg['mongo_port']),
            username=cfg.get('mongo_user') or None,
            password=cfg.get('mongo_password') or None
        )
        return cliente[cfg['mongo_database']]
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB error: {e}")


def serializar(obj):
    """Recursively converts non-JSON-serializable types."""
    if isinstance(obj, Decimal):
        return float(obj)
    if hasattr(obj, '__str__'):
        return str(obj)
    return obj


# ── Script execution ─────────────────────────────────────────────────────────

def run_script_sync(script_path: Path):
    """
    Runs a Python script as a subprocess and yields its stdout/stderr
    line by line as Server-Sent Events (SSE).

    Uses synchronous subprocess for Windows compatibility, since
    asyncio.create_subprocess_exec requires ProactorEventLoop on Windows
    which conflicts with uvicorn's default event loop.
    """
    process = subprocess.Popen(
        ["py", str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    for line in process.stdout:
        yield f"data: {line.rstrip()}\n\n"

    process.wait()
    yield f"data: [EXIT:{process.returncode}]\n\n"


@app.post("/run/extraction", summary="Run data extraction script")
async def run_extraction():
    """Executes data_extraction.py and streams its output."""
    return StreamingResponse(
        run_script_sync(SCRIPTS["extraction"]),
        media_type="text/event-stream"
    )


@app.post("/run/mysql", summary="Run MySQL insertion script")
async def run_mysql():
    """Executes InsertMySQL.py and streams its output."""
    return StreamingResponse(
        run_script_sync(SCRIPTS["mysql"]),
        media_type="text/event-stream"
    )


@app.post("/run/mongodb", summary="Run MongoDB export script")
async def run_mongodb():
    """Executes ExportMongoDB.py and streams its output."""
    return StreamingResponse(
        run_script_sync(SCRIPTS["mongodb"]),
        media_type="text/event-stream"
    )


# ── Config endpoints ─────────────────────────────────────────────────────────

@app.get("/config", summary="Read config.txt")
def get_config():
    """Returns the current contents of config.txt as a JSON object."""
    try:
        return leer_config()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="config.txt not found")


class ConfigUpdate(BaseModel):
    data: dict


@app.put("/config", summary="Update config.txt")
def update_config(body: ConfigUpdate):
    """Overwrites config.txt with the provided key-value pairs."""
    try:
        escribir_config(body.data)
        return {"message": "config.txt updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Data endpoints ────────────────────────────────────────────────────────────

MYSQL_TABLES = {
    "period": "sp_get_all_periods",
    "education_indicator": "sp_get_all_education",
    "economy_indicator": "sp_get_all_economy",
    "employment_indicator": "sp_get_all_employment",
}

MONGO_COLLECTIONS = [
    "period",
    "education_indicator",
    "economy_indicator",
    "employment_indicator",
]


@app.get("/data/mysql/{table}", summary="Query MySQL table via stored procedure")
def get_mysql_data(table: str):
    """
    Calls the corresponding stored procedure for the requested table
    and returns all rows as a list of dictionaries.
    """
    if table not in MYSQL_TABLES:
        raise HTTPException(
            status_code=404,
            detail=f"Table '{table}' not found. Valid options: {list(MYSQL_TABLES.keys())}"
        )

    conexion = get_mysql_connection()
    cursor = conexion.cursor()
    cursor.callproc(MYSQL_TABLES[table])

    registros = []
    for resultado in cursor.stored_results():
        columnas = [col[0] for col in resultado.description]
        for fila in resultado.fetchall():
            registros.append({
                col: (float(val) if isinstance(val, Decimal) else val)
                for col, val in zip(columnas, fila)
            })

    cursor.close()
    conexion.close()
    return registros


@app.get("/data/mongodb/{collection}", summary="Query MongoDB collection")
def get_mongo_data(collection: str):
    """
    Returns all documents from the requested MongoDB collection,
    excluding the internal _id field.
    """
    if collection not in MONGO_COLLECTIONS:
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection}' not found. Valid options: {MONGO_COLLECTIONS}"
        )

    db = get_mongo_db()
    # Exclude _id from results as it is not JSON-serializable by default
    documentos = list(db[collection].find({}, {"_id": 0}))
    return documentos


# ── Views endpoints ───────────────────────────────────────────────────────────

MYSQL_VIEWS = [
    "v_full_indicators",
    "v_education_vs_unemployment",
    "v_unemployment_vs_economy",
    "v_poverty_trend",
    "v_audit_activity",
    "v_indicator_averages",
    "v_year_over_year",
    "v_spending_vs_outcomes",
    "v_population_distribution",
]


@app.get("/views", summary="List available MySQL views")
def list_views():
    """Returns the list of available MySQL views."""
    return MYSQL_VIEWS


@app.get("/views/{view_name}", summary="Query a MySQL view")
def get_view_data(view_name: str):
    """
    Executes a SELECT * on the requested MySQL view and returns
    all rows as a list of dictionaries.
    """
    if view_name not in MYSQL_VIEWS:
        raise HTTPException(
            status_code=404,
            detail=f"View '{view_name}' not found. Valid options: {MYSQL_VIEWS}"
        )

    conexion = get_mysql_connection()
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM {view_name}")

    columnas = [col[0] for col in cursor.description]
    registros = []
    for fila in cursor.fetchall():
        registros.append({
            col: (float(val) if isinstance(val, Decimal) else val)
            for col, val in zip(columnas, fila)
        })

    cursor.close()
    conexion.close()
    return registros
