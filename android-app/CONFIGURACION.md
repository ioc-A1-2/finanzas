# Configuración de la Aplicación Android Nativa

## 1. Google Sheets API

### Paso 1: Crear credenciales
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **Google Sheets API**
4. Ve a **APIs & Services > Credentials**
5. Crea credenciales de tipo **Service Account**
6. Descarga el archivo JSON de credenciales

### Paso 2: Configurar en la app
1. Coloca el archivo JSON en: `app/src/main/assets/credentials.json`
2. Abre `GoogleSheetsRepository.kt`
3. Cambia `SPREADSHEET_ID` por el ID de tu hoja de cálculo
   - El ID está en la URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

### Paso 3: Compartir hoja con Service Account
1. Abre tu hoja de Google Sheets
2. Haz clic en **Compartir**
3. Agrega el email del Service Account (está en el JSON)
4. Dale permisos de **Editor**

## 2. Gemini API

### Opción A: Desde la app (Recomendado)
1. Abre la app
2. Ve a **⚙️ Config**
3. Ingresa tu API key de Gemini
4. Se guardará automáticamente

### Opción B: Hardcodear temporalmente
1. Abre `GeminiRepository.kt`
2. En el método `initialize()`, puedes hardcodear la API key temporalmente:
   ```kotlin
   fun initialize(apiKey: String = "TU_API_KEY_AQUI") {
       model = generativeModel(
           modelName = "gemini-pro",
           apiKey = apiKey.ifEmpty { "TU_API_KEY_AQUI" }
       )
   }
   ```

## 3. Compilar la APK

### En Android Studio:
1. Abre el proyecto
2. **File > Sync Project with Gradle Files**
3. **Build > Build Bundle(s) / APK(s) > Build APK(s)**
4. El APK estará en: `app/build/outputs/apk/debug/app-debug.apk`

### Desde línea de comandos (si tienes Gradle):
```bash
cd android-app
./gradlew assembleDebug
```

## Estructura de Datos en Google Sheets

La hoja debe tener estas columnas:
- A: ID (opcional)
- B: Fecha (formato: dd/MM/yyyy)
- C: Tipo (Ingreso o Gasto)
- D: Categoría
- E: Concepto
- F: Importe
- G: Frecuencia (Puntual, Mensual, Anual)
- H: Impacto_Mensual
- I: Es_Conjunto (TRUE o FALSE)

## Solución de Problemas

### Error: "FileNotFoundException: credentials.json"
- Asegúrate de que el archivo esté en `app/src/main/assets/`
- Verifica que el archivo se llame exactamente `credentials.json`

### Error: "403 Forbidden" al acceder a Sheets
- Verifica que hayas compartido la hoja con el email del Service Account
- Verifica que el Service Account tenga permisos de Editor

### Error: "API key not valid" en Gemini
- Verifica que la API key sea correcta
- Asegúrate de que la API key tenga permisos para usar Gemini
