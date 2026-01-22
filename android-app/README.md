# Finanzas Proactivas - Aplicación Android

Esta es una aplicación Android nativa que carga la aplicación Streamlit en un WebView, manteniendo todos los datos y la IA funcionando online.

## Requisitos

- Android Studio (última versión)
- Android SDK mínimo: API 21 (Android 5.0)
- Android SDK objetivo: API 34 (Android 14)

## Configuración

1. Abre el proyecto en Android Studio
2. Edita `app/src/main/java/com/finanzasproactivas/MainActivity.kt` y cambia la URL de Streamlit en la línea que dice:
   ```kotlin
   private val STREAMLIT_URL = "TU_URL_AQUI"
   ```
   Reemplaza `TU_URL_AQUI` con la URL de tu aplicación Streamlit (por ejemplo: `https://tu-app.streamlit.app`)

3. Sincroniza el proyecto (Sync Project with Gradle Files)

## Compilar APK

1. Build > Build Bundle(s) / APK(s) > Build APK(s)
2. El APK se generará en `app/build/outputs/apk/debug/app-debug.apk`

## Instalación

1. Transfiere el APK a tu dispositivo Android
2. Habilita "Instalar desde fuentes desconocidas" en la configuración de seguridad
3. Abre el APK e instálalo

## Características

- ✅ Carga la aplicación Streamlit completa
- ✅ Mantiene sesiones y cookies
- ✅ Soporte para JavaScript
- ✅ Permisos de internet
- ✅ Interfaz optimizada para móvil
- ✅ Botón de recarga
- ✅ Indicador de carga
