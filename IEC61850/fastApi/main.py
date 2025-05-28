from fastapi import FastAPI, HTTPException, Query
from typing import List
import os
from fastapi.responses import FileResponse
import time
import shutil
import zipfile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app = FastAPI()

HTDOCS_DIR = "/var/www/html/dms_setting/assets/api/file_dr/"

# Allowed file extensions for Comtrade files
ALLOWED_EXTENSIONS = {".cfg", ".dat", ".hdr"}

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/device/{device_id}")
def get_zip_items(device_id: str):
    """
    Get a list of file or folder names in the specified directory under HTDOCS_DIR that end with '.zip'.
    """
    target_dir = os.path.join(HTDOCS_DIR, device_id)
    
    if not os.path.exists(target_dir):
        raise HTTPException(status_code=404, detail=f"Directory not found: {target_dir}")
    
    try:
        all_items = [entry.name for entry in os.scandir(target_dir) if entry.is_file()]
        zip_items = [
            os.path.splitext(item)[0]  # Remove the extension
            for item in all_items
            if item.lower().endswith(".zip")
        ]
        return zip_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/getzip")
def get_zip_file(
    device_id: str = Query(..., description="Subdirectory under HTDOCS_DIR"),
    filename: str = Query(..., description="Name of the zip file (without .zip extension) to return")
):
    """
    Returns the ZIP file that matches the requested filename located in the specified subdirectory.
    """
    file_path = os.path.join(HTDOCS_DIR, device_id, f"{filename}.zip")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    
    return FileResponse(
        file_path,
        media_type="application/zip",
        filename=f"{filename}.zip"
    )

@app.get("/getdevicezip")
def get_device_zip(device_id: str = Query(..., description="Device ID corresponding to the folder")):
    """
    Finds `.zip` files in the given device folder inside HTDOCS_DIR, 
    compresses them into a single ZIP archive, and returns the file.
    """
    device_folder = os.path.join(HTDOCS_DIR, device_id)
    
    if not os.path.exists(device_folder) or not os.path.isdir(device_folder):
        raise HTTPException(status_code=404, detail=f"Directory not found: {device_folder}")
    
    output_zip_path = os.path.join(HTDOCS_DIR, f"{device_id}.zip")

    try:
        with zipfile.ZipFile(output_zip_path, 'w') as zipf:
            for file in os.listdir(device_folder):
                file_path = os.path.join(device_folder, file)
                if os.path.isfile(file_path) and file.endswith('.zip'):
                    zipf.write(file_path, arcname=file)  # Only include the file name, not full path

        if not os.path.exists(output_zip_path) or os.path.getsize(output_zip_path) == 0:
            raise HTTPException(status_code=404, detail="No .zip files found to compress.")

        return FileResponse(output_zip_path, media_type="application/zip", filename=f"{device_id}.zip")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getlatestzip")
def get_latest_zip(device_id: str = Query(..., description="Device ID corresponding to the folder")):
    """
    Returns the latest ZIP file in the specified device folder.
    """
    device_folder = os.path.join(HTDOCS_DIR, device_id)
    
    if not os.path.exists(device_folder) or not os.path.isdir(device_folder):
        raise HTTPException(status_code=404, detail=f"Directory not found: {device_folder}")
    
    try:
        time.sleep(1)  # Ensure file system updates are reflected
        zip_files = [
            entry.path for entry in os.scandir(device_folder)
            if entry.is_file() and entry.name.lower().endswith(".zip")
        ]
        if not zip_files:
            raise HTTPException(status_code=404, detail="No ZIP files found in the directory")
        latest_zip = max(zip_files, key=lambda f: os.stat(f).st_mtime)
        return FileResponse(latest_zip, filename=os.path.basename(latest_zip))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
