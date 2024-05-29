from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Directorio base para los archivos PDF
BASE_DIR = Path("static")

@app.get("/")
def read_root():
    return {"message": "Go to /pdf?filename=sample.pdf to view the PDF"}

@app.get("/pdf")
async def get_pdf(filename:str):
    # Construir la ruta completa al archivo de manera segura
    pdf_path = Path('.') / 'static' / filename

    # Verificar que el archivo existe y es un archivo regular
    if not pdf_path.exists() or not pdf_path.is_file():
        raise HTTPException(status_code=404, detail="PDF file not found")

    # Devolver el archivo PDF
    return FileResponse(pdf_path, media_type='application/pdf')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
