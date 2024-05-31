from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import shutil

app = FastAPI()

# Directorio base para los archivos PDF
BASE_DIR = Path("static")
# Crear el directorio si no existe
BASE_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Go to /pdf?filename=sample.pdf to view the PDF"}


@app.get("/pdf")
async def get_pdf(filename: str):
    # Construir la ruta completa al archivo de manera segura
    pdf_path = Path('.') / 'static' / filename

    # Verificar que el archivo existe y es un archivo regular
    if not pdf_path.exists() or not pdf_path.is_file():
        raise HTTPException(status_code=404, detail="PDF file not found")

    # Devolver el archivo PDF
    return FileResponse(pdf_path, media_type='application/pdf')


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Verificar que el archivo tiene la extensión .pdf
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Only PDF files are allowed/Solo archivos PDF son permitidos")

    # Construir la ruta completa al archivo donde se guardará
    file_path = BASE_DIR / file.filename

    # Guardar el archivo en el directorio especificado
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, 
            "message": "File uploaded successfully/Archivo Subido exitosamente", 
            "link": f"https://pdf.luque.site/pdf?filename={file.filename}"
            }


@app.get("/list-pdfs")
async def list_pdfs():
    # Listar todos los archivos PDF en el directorio especificado
    pdf_files = [str(file.name) for file in BASE_DIR.glob("*.pdf")]

    return {"pdf_files": pdf_files}


@app.delete("/delete-pdf")
async def delete_pdf(filename: str):
    # Construir la ruta completa al archivo de manera segura
    pdf_path = BASE_DIR / filename

    # Verificar que el archivo existe y es un archivo regular
    if not pdf_path.exists() or not pdf_path.is_file():
        raise HTTPException(status_code=404, detail="PDF file not found")

    # Eliminar el archivo
    pdf_path.unlink()

    return {"message": f"File '{filename}' deleted successfully/Archivo '{filename}' eliminado exitosamente"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
