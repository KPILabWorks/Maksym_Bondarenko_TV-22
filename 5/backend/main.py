from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
import sqlite3
import io
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df = df.dropna(how='all')
    df.columns = df.columns.str.lower().str.strip()
    return df

def process_csv(file: UploadFile) -> pd.DataFrame:
    content = file.file.read().decode("utf-8")
    df = pd.read_csv(io.StringIO(content))
    return clean_df(df)

def process_json(file: UploadFile) -> pd.DataFrame:
    content = file.file.read().decode("utf-8")
    df = pd.read_json(io.StringIO(content))
    return clean_df(df)

def process_sqlite(file: UploadFile) -> List[pd.DataFrame]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    conn = sqlite3.connect(tmp_path)
    try:
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        dfs = []
        for table_name, in tables:
            try:
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                dfs.append(clean_df(df))
            except Exception as e:
                continue
        return dfs
    finally:
        conn.close()

@app.post("/")
async def merge_data(files: List[UploadFile] = File(...)):
    try:
        dataframes = []

        for file in files:
            ext = Path(file.filename).suffix

            if ext == '.csv':
                dataframes.append(process_csv(file))
            elif ext == '.json':
                dataframes.append(process_json(file))
            elif ext == '.db':
                dataframes.extend(process_sqlite(file))
            else:
                raise f'Unsupported file extension {ext}'

        merged_df = pd.concat(dataframes, ignore_index=True, sort=False)
        return JSONResponse(content=merged_df.to_dict(orient="records"))

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
