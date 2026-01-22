package com.finanzasproactivas.data.repository

import com.google.ai.client.generativeai.GenerativeModel
import com.google.ai.client.generativeai.generativeModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class GeminiRepository {
    private var model: GenerativeModel? = null
    
    // API Key configurada
    private val defaultApiKey = "AIzaSyC9H41PE78zHcjuk_8RoC0BafHT67CUusw"
    
    fun initialize(apiKey: String? = null) {
        val key = apiKey?.ifEmpty { null } ?: defaultApiKey
        model = generativeModel(
            modelName = "gemini-pro",
            apiKey = key
        )
    }
    
    suspend fun chat(pregunta: String, contexto: String): String = withContext(Dispatchers.IO) {
        try {
            val prompt = """
                Eres un asistente financiero inteligente. Analiza los siguientes datos financieros y responde la pregunta del usuario de manera clara y útil.
                
                Datos financieros:
                $contexto
                
                Pregunta del usuario: $pregunta
                
                Responde de forma clara, concisa y útil.
            """.trimIndent()
            
            val response = model?.generateContent(prompt)
            response?.text ?: "Lo siento, no pude generar una respuesta."
        } catch (e: Exception) {
            "Error al comunicarse con Gemini: ${e.message}"
        }
    }
}
