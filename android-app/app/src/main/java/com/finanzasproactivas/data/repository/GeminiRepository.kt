package com.finanzasproactivas.data.repository

import com.google.ai.client.generativeai.GenerativeModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class GeminiRepository {
    // API Key de Gemini - Configurada aquí
    // Si quieres cambiarla, modifica esta variable o pasa una diferente al inicializar
    private val defaultApiKey = "AIzaSyC9H41PE78zHcjuk_8RoC0BafHT67CUusw"
    
    private var model: GenerativeModel? = null
    
    /**
     * Inicializa el modelo de Gemini con la API key proporcionada o usa la predeterminada
     * 
     * @param apiKey API key de Gemini. Si es null o vacía, usa la predeterminada configurada arriba
     */
    fun initialize(apiKey: String? = null) {
        val key = apiKey?.takeIf { it.isNotEmpty() } ?: defaultApiKey
        try {
            // Usar el constructor directo de GenerativeModel
            model = GenerativeModel(
                modelName = "gemini-pro",
                apiKey = key
            )
        } catch (e: Exception) {
            // Si falla la inicialización, el modelo quedará null
            // Se manejará en el método chat()
        }
    }
    
    /**
     * Envía una pregunta a Gemini con el contexto de los datos financieros
     * 
     * @param pregunta La pregunta del usuario
     * @param contexto Los datos financieros formateados como texto
     * @return La respuesta de Gemini o un mensaje de error
     */
    suspend fun chat(pregunta: String, contexto: String): String = withContext(Dispatchers.IO) {
        try {
            // Inicializar si no está inicializado
            if (model == null) {
                initialize()
            }
            
            // Si aún no hay modelo, retornar error
            val currentModel = model ?: return@withContext "Error: No se pudo inicializar el modelo de Gemini. Verifica tu API key."
            
            // Crear el prompt con el contexto financiero
            val prompt = """
                Eres un asistente financiero inteligente y experto. Analiza los siguientes datos financieros del usuario y responde su pregunta de manera clara, útil y profesional.
                
                DATOS FINANCIEROS DEL USUARIO:
                $contexto
                
                PREGUNTA DEL USUARIO:
                $pregunta
                
                INSTRUCCIONES:
                - Responde de forma clara y concisa
                - Proporciona información útil basada en los datos proporcionados
                - Si no hay suficientes datos, indícalo amablemente
                - Usa un tono profesional pero amigable
                - Si es relevante, proporciona recomendaciones prácticas
            """.trimIndent()
            
            // Generar contenido con Gemini
            val response = currentModel.generateContent(prompt)
            response.text ?: "Lo siento, no pude generar una respuesta. Por favor, intenta de nuevo."
            
        } catch (e: Exception) {
            "Error al comunicarse con Gemini: ${e.message ?: "Error desconocido"}"
        }
    }
}
