# app/services/gemini_service.py
from fastapi import HTTPException
import google.generativeai as genai
import os
from textblob import TextBlob

# Configuración de la API Key de Gemini
genai.configure(api_key="AIzaSyAZFTPJwJxvUBxdiQV0zectkmoO66-_RX4")

# Diccionario de contexto para cada usuario
user_contexts = {
    1: {
        "ID_Cliente": 1,
        "Nombre_Cliente": "Juan Perez",
        "Fecha_Nacimiento": "1985-07-23",
        "Número_Documento": "12345678",
        "Teléfono_Contacto": "123-456-789",
        "Correo_Electrónico": "juan.perez@email.com",
        "Monto_Deuda": 5000,
        "Fecha_Vencimiento": "2024-12-01",
        "Estado_Cuenta": "En mora",
        "Historial_Pagos": [
            {"fecha": "2024-01-15", "monto": 500},
            {"fecha": "2024-05-20", "monto": 700},
        ]
    },
    2: {
        "ID_Cliente": 2,
        "Nombre_Cliente": "María Rodríguez",
        "Fecha_Nacimiento": "1992-11-10",
        "Número_Documento": "87654321",
        "Teléfono_Contacto": "987-654-321",
        "Correo_Electrónico": "maria.rodriguez@example.com",
        "Monto_Deuda": 3000,
        "Fecha_Vencimiento": "2025-03-15",
        "Estado_Cuenta": "Pendiente",
        "Historial_Pagos": [
            {"fecha": "2024-09-05", "monto": 1000},
        ]
    },
    3: {
        "ID_Cliente": 3,
        "Nombre_Cliente": "Carlos López",
        "Fecha_Nacimiento": "1978-04-25",
        "Número_Documento": "54321678",
        "Teléfono_Contacto": "789-456-123",
        "Correo_Electrónico": "carlos.lopez@gmail.com",
        "Monto_Deuda": 800,
        "Fecha_Vencimiento": "2024-12-31",
        "Estado_Cuenta": "Pagada",
        "Historial_Pagos": [
            {"fecha": "2024-11-20", "monto": 800},
        ]
    }
}

def update_context(user_id: int, key: str, value):
    """Actualiza el contexto de un usuario."""
    if user_id not in user_contexts:
        user_contexts[user_id] = {}
    user_contexts[user_id][key] = value

def get_context(user_id: int, key: str):
    """Obtiene un valor del contexto de un usuario."""
    return user_contexts.get(user_id, {}).get(key)

def build_prompt(user_id: int, user_message: str) -> str:
    """
    Construye dinámicamente un prompt para la API de Gemini basado en el contexto del usuario
    y el mensaje recibido desde el frontend.
    """
    context = user_contexts.get(user_id, {})
    # Construcción dinámica del prompt
    prompt = (
        f"Eres un asistente de cobros interactivo. Estás ayudando al usuario con el ID {user_id}. "
        f"Es importante resaltar que si en la informacion que te paso del usuario, pregunta de un tema que no tenga que ver con este contexto de cobros, vas a decir que no tienes permitido hablar de otros temas fuera de dicho contexto y que si hay algo en que le pueda ayudar con respecto a su cuenta"
        f"otro punto importante es que trata de buscar siempre una negociacion y si el cliente no esta conforme con algo, trata de buscar opciones y negociar una opcion con el cliente"
        f"Estos son algunos datos del usuario: "
        f"- Estado de cuenta: {context}. "
        f"El usuario dijo: '{user_message}'. "
        f"Con base en esta información, responde de manera clara y útil para ayudar al usuario a resolver su consulta."
    )
    return prompt

def generate_gemini_response(user_id: int, user_message: str) -> dict:
    try:
        # Registro para depuración
        print("Generando prompt...")
        prompt = build_prompt(user_id, user_message)
        print("Prompt generado:", prompt)

        # Registro antes de llamar a Gemini
        print("Llamando a la API de Gemini...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        gemini_response = model.generate_content(prompt)
        print("Respuesta de Gemini recibida:", gemini_response)

        response_text = gemini_response.text

        # Actualizar el contexto con la última respuesta
        update_context(user_id, "Ultima_Respuesta", response_text)
        emotion = "neutral"  # Placeholder para la emoción
        update_context(user_id, "Emocion", emotion)

        return {"text": response_text, "emotion": emotion}

    except Exception as e:
        print("Error al generar respuesta:", str(e))
        raise HTTPException(status_code=500, detail=f"Error al generar respuesta: {str(e)}")

from textblob import TextBlob

def analyze_emotions_and_cost(conversation: str) -> dict:
    # Análisis de sentimientos usando TextBlob (como ejemplo, puedes integrar otras librerías o servicios)
    sentiment_analysis = TextBlob(conversation).sentiment
    sentiment = sentiment_analysis.polarity  # Sentimiento de la conversación (-1 a 1)
    
    # Simulación de la emoción dominante basada en el sentimiento
    if sentiment > 0.1:
        emotion = "Positiva"
    elif sentiment < -0.1:
        emotion = "Negativa"
    else:
        emotion = "Neutral"
    
    # Calcular el indicador de negociación (simulado entre 0 a 100)
    negotiation_score = max(0, min(100, 50 + sentiment * 50))
    
    # Calcular el costo estimado basado en tokens (suponiendo 0.02 USD por 1000 tokens)
    tokens_used = len(conversation.split())  # Contamos las palabras como tokens
    estimated_cost = max(0.01, tokens_used / 1000 * 0.02)  # Costo mínimo de 0.01 USD
    
    return {
        "emotion": emotion,
        "sentiment": sentiment,
        "negotiationScore": round(negotiation_score, 2),
        "tokensUsed": tokens_used,
        "estimatedCost": round(estimated_cost, 2),
    }
