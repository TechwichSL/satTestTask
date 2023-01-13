import uuid
from typing import Union
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response, FileResponse, JSONResponse
import rasterio
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os

app = FastAPI()

IMAGEDIR = "uploaded/"
THUMBDIR = "thumbnail/"
NDVIDIR = "ndvi/"


def checkDirs():
    if not os.path.exists(IMAGEDIR):
        os.makedirs(IMAGEDIR)
    if not os.path.exists(THUMBDIR):
        os.makedirs(THUMBDIR)
    if not os.path.exists(NDVIDIR):
        os.makedirs(NDVIDIR)


@app.post("/attributes")
async def attributes(file: UploadFile = File(...)):
    try:
        checkDirs()
        file.filename = f"{uuid.uuid4()}.tif"
        contents = await file.read()
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
        dataset = rasterio.open(f"{IMAGEDIR}{file.filename}")
        return {"imageSize": {"height": dataset.height, "width": dataset.width}, "bandsCount": dataset.count,
                "boundingBox": dataset.bounds, "crs": str(dataset.crs)}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@app.post("/thumbnail")
async def thumbnail(width: int = Form(100), height: int = Form(100), file: UploadFile = File(...)):
    try:
        checkDirs()
        file.filename = f"{uuid.uuid4()}.PNG"
        contents = await file.read()
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
        image = Image.open(f"{IMAGEDIR}{file.filename}").convert('RGB')
        image.thumbnail((width, height))
        image.save(f"{THUMBDIR}{file.filename}")

        return FileResponse(f"{THUMBDIR}{file.filename}")
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@app.post("/ndvi")
async def ndvi(palette: str = Form("summer"), file: UploadFile = File(...)):
    try:
        checkDirs()
        file.filename = f"{uuid.uuid4()}.png"
        contents = await file.read()
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
        image = rasterio.open(f"{IMAGEDIR}{file.filename}")
        # Calculate NDVI
        np.seterr(divide='ignore', invalid='ignore')
        band_red = image.read(3)
        band_nir = image.read(4)
        ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

        plt.imsave(f"{NDVIDIR}{file.filename}", ndvi, cmap=palette)
        return FileResponse(f"{NDVIDIR}{file.filename}")

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
