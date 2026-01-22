# Guía Rápida para Compilar la APK

## Opción 1: Usar Android Studio (Recomendado)

### Paso 1: Instalar Android Studio
1. Descarga desde: https://developer.android.com/studio
2. Instala siguiendo el asistente
3. Acepta las licencias del SDK

### Paso 2: Configurar la URL
Ejecuta este comando en PowerShell desde la carpeta `android-app`:
```powershell
.\configurar_url.ps1 -StreamlitURL "https://tu-url-streamlit.streamlit.app"
```

O edita manualmente el archivo:
`app/src/main/java/com/finanzasproactivas/MainActivity.kt`
y cambia la línea:
```kotlin
private val STREAMLIT_URL = "https://tu-app.streamlit.app"
```

### Paso 3: Compilar
1. Abre Android Studio
2. File > Open > Selecciona la carpeta `android-app`
3. Build > Build Bundle(s) / APK(s) > Build APK(s)
4. El APK estará en: `app/build/outputs/apk/debug/app-debug.apk`

## Opción 2: Usar GitHub Actions (Automático)

He creado un workflow de GitHub Actions que compilará la APK automáticamente cuando hagas push.

**Requisitos:**
1. Tener la aplicación en GitHub (ya la tienes)
2. Configurar la URL en el archivo de configuración
3. El workflow compilará la APK automáticamente

## Opción 3: Usar servicios online

Puedes usar servicios como:
- **Appetize.io** - Para probar sin instalar
- **BuildBox** - Para compilar online
- **GitHub Actions** - Para compilar automáticamente

## ¿Necesitas ayuda?

Si me proporcionas la URL de tu aplicación Streamlit, puedo:
1. Configurarla automáticamente
2. Crear un script de compilación automatizado
3. Configurar GitHub Actions para compilar automáticamente
