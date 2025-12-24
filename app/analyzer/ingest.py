import tarfile
import zipfile
import tempfile
import os
import shutil
import aiofiles
from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)

def verify_file_type(file: UploadFile):
    if not (file.filename.endswith(".tar.gz") or file.filename.endswith(".tgz") or file.filename.endswith(".zip")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .tar.gz, .tgz, or .zip allowed.")

async def save_and_extract(file: UploadFile) -> str:
    """
    Saves the uploaded file to a temp dir and extracts it.
    Returns the path to the extracted directory.
    """
    verify_file_type(file)
    
    # Create a temp dir for this analysis session
    temp_dir = tempfile.mkdtemp(prefix="mke_analysis_")
    
    # Determine extension for saving
    ext = ".zip" if file.filename.endswith(".zip") else ".tar.gz"
    archive_path = os.path.join(temp_dir, f"dump{ext}")
    
    try:
        async with aiofiles.open(archive_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # Read in 1MB chunks
                await out_file.write(content)
                
        # Extract based on type
        if ext == ".tar.gz":
            if not tarfile.is_tarfile(archive_path):
                 raise HTTPException(status_code=400, detail="File is not a valid tar archive.")
                 
            with tarfile.open(archive_path, "r:gz") as tar:
                # Security check for Zip Slip
                for member in tar.getmembers():
                    if os.path.isabs(member.name) or ".." in member.name:
                        raise HTTPException(status_code=400, detail="Malicious file path detected in archive.")
                tar.extractall(path=temp_dir)
        
        elif ext == ".zip":
            if not zipfile.is_zipfile(archive_path):
                 raise HTTPException(status_code=400, detail="File is not a valid zip archive.")
            
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                # Security check for Zip Slip
                for member in zip_ref.namelist():
                    if os.path.isabs(member) or ".." in member:
                        raise HTTPException(status_code=400, detail="Malicious file path detected in archive.")
                zip_ref.extractall(temp_dir)
            
        # Debug: list extracted files
        print(f"DEBUG: Extracted to {temp_dir}")
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                print(f"DEBUG: Found file: {os.path.join(root, file)}")
                
        return temp_dir
        
    except Exception as e:
        shutil.rmtree(temp_dir)
        logger.error(f"Extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

def find_dump_root(temp_dir: str) -> str:
    """
    Locates the actual root of the dump.
    If the dump contains a single top-level directory, returns that.
    Otherwise checks for common markers like 'nodes' or 'info.json'.
    """
    # 1. Check if we have 'nodes' directly
    if os.path.exists(os.path.join(temp_dir, "nodes")):
        return temp_dir
        
    # 2. Check if single top-level dir
    items = os.listdir(temp_dir)
    if len(items) == 1:
        single_item = os.path.join(temp_dir, items[0])
        if os.path.isdir(single_item):
            # Check if this new root looks promising?
            # Or just assume it wraps the dump.
            return single_item
            
    # 3. Recursive search for 'nodes' dir? 
    # Might be too aggressive and pick up unrelated nodes dir.
    # For now, just stick to the single-folder unwrap pattern which is standard.
    
    return temp_dir

def cleanup_temp_dir(path: str):
    if os.path.exists(path) and "mke_analysis_" in path:
        shutil.rmtree(path)
