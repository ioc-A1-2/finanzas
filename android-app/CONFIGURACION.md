# Configuración de la Aplicación Android Nativa

## ✅ Configuración Automática Completada

Las siguientes configuraciones ya están aplicadas en el código:

### 1. Gemini API ✅
- **API Key configurada**: Ya está configurada en `GeminiRepository.kt`
- **Modelo**: `gemini-pro`
- No necesitas hacer nada adicional para Gemini

### 2. Google Sheets ✅
- **SPREADSHEET_ID configurado**: `17EBvx8s1IsxcV9-RigMxYvUxgz15ZA6yIuHyY9f8xGk`
- **Categorías por defecto**: Vivienda, Transporte, Comida, Seguros, Ahorro, Ingresos, Otros

## 🔧 Solo Falta: Credenciales de Service Account

Para que la app pueda leer y escribir en Google Sheets, necesitas:

### Paso 1: Obtener Credenciales de Service Account

**Sigue la guía detallada**: `OBTENER_CREDENCIALES_SERVICE_ACCOUNT.md`

Resumen rápido:
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto y habilita **Google Sheets API**
3. Crea una **Service Account**
4. Descarga el archivo JSON de credenciales
5. Renómbralo a `credentials.json`
6. Colócalo en: `android-app/app/src/main/assets/credentials.json`

### Paso 2: Compartir la Hoja con el Service Account

1. Abre el archivo JSON descargado
2. Busca el campo **"client_email"** (algo como `...@...iam.gserviceaccount.com`)
3. Copia ese email
4. Abre tu hoja: https://docs.google.com/spreadsheets/d/17EBvx8s1IsxcV9-RigMxYvUxgz15ZA6yIuHyY9f8xGk/edit
5. Haz clic en **"Compartir"**
6. Pega el email del Service Account
7. Dale permisos de **"Editor"**
8. Haz clic en **"Compartir"**

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
