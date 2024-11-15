# app/routers/gemini.py
from fastapi import APIRouter, HTTPException, Request
from app.services import gemini_service

router = APIRouter()

@router.post("/gemini/generate")
async def generate_content(request: Request):
    data = await request.json()
    print("Datos recibidos en el backend:", data)
    user_message = data.get("message")
    customer_id = data.get("customer_id", 1)  # ID del cliente, por defecto 1
    if not user_message:
        raise HTTPException(status_code=400, detail="El mensaje del usuario es obligatorio.")
    try:
        # Generar respuesta basada en el mensaje y contexto
        gemini_response = gemini_service.generate_gemini_response(customer_id, user_message)
        return {
            "response": gemini_response["text"],
            "emotion": gemini_response["emotion"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/analyze_emotion")
async def analyze_emotion(request: Request):
    data = await request.json()
    conversation = data.get("conversation")
    
    if not conversation:
        raise HTTPException(status_code=400, detail="La conversación es obligatoria.")
    try:
        # Llamar al servicio de análisis de emociones y cálculo de costos
        analysis_result = gemini_service.analyze_emotions_and_cost(conversation)
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar emociones y costos: {str(e)}")

