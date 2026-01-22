# 🔑 Configuración de la API Key de Gemini

## 📍 Ubicación de la API Key

La API key de Gemini está configurada en el siguiente archivo:

**Archivo:** `app/src/main/java/com/finanzasproactivas/data/repository/GeminiRepository.kt`

**Línea:** 11

```kotlin
private val defaultApiKey = "AIzaSyC9H41PE78zHcjuk_8RoC0BafHT67CUusw"
```

## 🔧 Cómo Cambiar la API Key

### Opción 1: Modificar directamente en el código (Actual)

1. Abre el archivo: `android-app/app/src/main/java/com/finanzasproactivas/data/repository/GeminiRepository.kt`
2. Busca la línea 11: `private val defaultApiKey = "TU_API_KEY_AQUI"`
3. Reemplaza `"TU_API_KEY_AQUI"` con tu nueva API key
4. Recompila la aplicación

### Opción 2: Pasar la API key al inicializar (Recomendado para producción)

El método `initialize()` acepta una API key como parámetro:

```kotlin
val geminiRepo = GeminiRepository()
geminiRepo.initialize("TU_NUEVA_API_KEY_AQUI")
```

Si no pasas ninguna API key, usará la predeterminada configurada en el código.

## ✅ API Key Actual Configurada

La API key actualmente configurada es:
```
AIzaSyC9H41PE78zHcjuk_8RoC0BafHT67CUusw
```

Esta API key ya está funcionando y lista para usar.

## 🔒 Seguridad

⚠️ **IMPORTANTE**: 
- La API key está hardcodeada en el código fuente
- Si planeas hacer público el código, considera usar variables de entorno o un archivo de configuración local
- El archivo `.gitignore` ya está configurado para evitar subir credenciales accidentalmente

## 🧪 Verificar que Funciona

1. Abre la app en tu dispositivo Android
2. Ve a la sección **"Asesor"**
3. Desplázate hasta **"Asistente IA con Gemini"**
4. Escribe una pregunta (ej: "¿Cuánto he gastado este mes?")
5. Presiona enviar
6. Deberías recibir una respuesta de Gemini

## ❌ Solución de Problemas

### Error: "No se pudo inicializar el modelo de Gemini"
- Verifica que la API key sea correcta
- Asegúrate de que tu dispositivo tenga conexión a internet
- Verifica que la API key tenga permisos para usar Gemini API

### Error: "API key not valid"
- Obtén una nueva API key desde: https://makersuite.google.com/app/apikey
- Reemplaza la API key en `GeminiRepository.kt`
- Recompila la aplicación

### La app no responde
- Verifica que tengas conexión a internet
- Revisa los logs de Android Studio (Logcat) para ver errores específicos

## 📝 Notas

- El modelo usado es `gemini-pro`
- La API key se inicializa automáticamente cuando se crea el `GeminiRepository`
- Si necesitas cambiar el modelo, modifica `modelName` en la línea 24 de `GeminiRepository.kt`
