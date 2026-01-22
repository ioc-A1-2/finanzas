# Instrucciones para Compilar la APK

## Paso 1: Instalar Android Studio

1. Descarga Android Studio desde: https://developer.android.com/studio
2. Instálalo siguiendo el asistente
3. Acepta las licencias del SDK

## Paso 2: Abrir el Proyecto

1. Abre Android Studio
2. Selecciona "Open an Existing Project"
3. Navega a la carpeta `android-app` y selecciónala
4. Espera a que Android Studio sincronice el proyecto (puede tardar varios minutos la primera vez)
   - Android Studio descargará automáticamente las dependencias necesarias
   - La primera vez puede tardar 5-10 minutos

## Paso 3: Verificar Configuración (Opcional)

La aplicación ya está configurada con:
- ✅ API key de Gemini
- ✅ ID de Google Sheets
- ✅ Credenciales de Service Account (si colocaste el archivo `credentials.json`)

**Importante**: Asegúrate de que:
- El archivo `credentials.json` esté en `app/src/main/assets/`
- Tu hoja de Google Sheets esté compartida con el Service Account (ver `VERIFICACION_FINAL.md`)

## Paso 4: Compilar la APK

### Opción A: APK de Debug (para pruebas)

1. En Android Studio, ve a: **Build > Build Bundle(s) / APK(s) > Build APK(s)**
2. Espera a que termine la compilación
3. Cuando termine, haz clic en "locate" en la notificación
4. El APK estará en: `app/build/outputs/apk/debug/app-debug.apk`

### Opción B: APK de Release (para distribución)

1. Ve a: **Build > Generate Signed Bundle / APK**
2. Selecciona "APK"
3. Si no tienes un keystore, crea uno nuevo:
   - Haz clic en "Create new..."
   - Completa el formulario (guarda bien la contraseña)
4. Selecciona "release" como build variant
5. Marca "V1 (Jar Signature)" y "V2 (Full APK Signature)"
6. Haz clic en "Finish"
7. El APK estará en: `app/build/outputs/apk/release/app-release.apk`

## Paso 5: Instalar en tu Dispositivo

1. Transfiere el APK a tu dispositivo Android (por USB, email, etc.)
2. En tu dispositivo, ve a **Configuración > Seguridad**
3. Habilita **"Instalar desde fuentes desconocidas"** o **"Instalar aplicaciones desconocidas"**
4. Abre el archivo APK desde el administrador de archivos
5. Sigue las instrucciones de instalación

## Solución de Problemas

### Error: "SDK not found"
- Ve a **File > Settings > Appearance & Behavior > System Settings > Android SDK**
- Instala el SDK Platform para API 34 y las herramientas de compilación

### Error: "Gradle sync failed"
- Ve a **File > Settings > Build, Execution, Deployment > Gradle**
- Asegúrate de que "Use Gradle from" esté configurado correctamente
- Intenta hacer clic en "Sync Project with Gradle Files" de nuevo

### Error: "403 Forbidden" al acceder a Google Sheets
- Verifica que hayas compartido la hoja con el Service Account
- El email del Service Account está en `credentials.json` (campo `client_email`)
- Asegúrate de dar permisos de **Editor** al Service Account

### Error: "FileNotFoundException: credentials.json"
- Verifica que el archivo esté en `app/src/main/assets/credentials.json`
- El nombre debe ser exactamente `credentials.json` (sin espacios, todo minúsculas)

### La app se cierra al abrirla
- Verifica los logs en Android Studio: **View > Tool Windows > Logcat**
- Asegúrate de que el dispositivo tenga Android 5.0 (API 21) o superior

## Notas Importantes

- La aplicación requiere conexión a internet para funcionar
- Todos los datos se almacenan en Google Sheets (online)
- La IA (Gemini) funciona completamente online
- Esta es una aplicación **nativa de Android** (no usa Streamlit)
- Los datos y la IA están completamente integrados en la app nativa
