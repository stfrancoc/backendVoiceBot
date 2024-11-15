# main.py
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from app.routers import gemini
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen (para pruebas). En producción, especifica tu frontend.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gemini.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API en FastAPI"}


# @app.post("/gemini/generate")
# async def generate_content(request: Request):
#     data = await request.json()
#     prompt = data.get("prompt")
    
#     try:
#         model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#         response = model.generate_content(prompt)
#         return {"response": response.text}
#     except Exception as e:
#         print("Error:", e)  # Registro del error en la terminal
#         raise HTTPException(status_code=500, detail="Error al generar contenido con Gemini API.")
