# Guía Detallada: Obtener Credenciales de Service Account para Google Sheets

## Paso 1: Crear un Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Si no tienes cuenta, créala (es gratuita)
3. Haz clic en el selector de proyectos (arriba a la izquierda)
4. Haz clic en **"Nuevo Proyecto"**
5. Ingresa un nombre para el proyecto (ej: "Finanzas Proactivas")
6. Haz clic en **"Crear"**
7. Espera unos segundos y selecciona el proyecto recién creado

## Paso 2: Habilitar Google Sheets API

1. En el menú lateral izquierdo, ve a **"APIs y servicios" > "Biblioteca"**
2. En el buscador, escribe **"Google Sheets API"**
3. Haz clic en **"Google Sheets API"**
4. Haz clic en el botón **"HABILITAR"**
5. Espera a que se habilite (puede tardar unos segundos)

## Paso 3: Crear Service Account

1. En el menú lateral, ve a **"APIs y servicios" > "Credenciales"**
2. Haz clic en **"+ CREAR CREDENCIALES"** (arriba)
3. Selecciona **"Cuenta de servicio"**
4. Completa el formulario:
   - **Nombre de la cuenta de servicio**: `finanzas-proactivas` (o el que prefieras)
   - **ID de la cuenta de servicio**: Se genera automáticamente
   - **Descripción**: `Service Account para Finanzas Proactivas`
5. Haz clic en **"Crear y continuar"**
6. En **"Otorgar a esta cuenta de servicio acceso al proyecto"**, selecciona el rol **"Editor"** (o deja en blanco si no aparece)
7. Haz clic en **"Continuar"**
8. Haz clic en **"Listo"** (puedes saltar el paso de usuarios)

## Paso 4: Descargar Credenciales JSON

1. En la lista de cuentas de servicio, busca la que acabas de crear
2. Haz clic en el email de la cuenta de servicio (termina en `@...iam.gserviceaccount.com`)
3. Ve a la pestaña **"Claves"**
4. Haz clic en **"Agregar clave" > "Crear nueva clave"**
5. Selecciona **"JSON"**
6. Haz clic en **"Crear"**
7. **Se descargará automáticamente un archivo JSON** - ¡Guárdalo en un lugar seguro!

## Paso 5: Compartir la Hoja de Google Sheets con el Service Account

1. Abre el archivo JSON que descargaste
2. Busca el campo **"client_email"** (algo como `finanzas-proactivas@...iam.gserviceaccount.com`)
3. Copia ese email
4. Abre tu hoja de Google Sheets: https://docs.google.com/spreadsheets/d/17EBvx8s1IsxcV9-RigMxYvUxgz15ZA6yIuHyY9f8xGk/edit
5. Haz clic en el botón **"Compartir"** (arriba a la derecha)
6. Pega el email del Service Account
7. Asegúrate de que tenga permisos de **"Editor"**
8. **Desmarca** la casilla "Notificar a las personas" (no es necesario)
9. Haz clic en **"Compartir"**

## Paso 6: Colocar el Archivo JSON en la App

1. El archivo JSON descargado tiene un nombre como `tu-proyecto-xxxxx-xxxxx.json`
2. **Renómbralo** a `credentials.json`
3. Copia el archivo `credentials.json` a la carpeta:
   ```
   android-app/app/src/main/assets/
   ```
4. Si la carpeta `assets` no existe, créala

## Verificación

Una vez completados todos los pasos:
- ✅ El archivo `credentials.json` está en `android-app/app/src/main/assets/`
- ✅ La hoja de Google Sheets está compartida con el email del Service Account
- ✅ El Service Account tiene permisos de Editor en la hoja

## Solución de Problemas

### Error: "FileNotFoundException: credentials.json"
- Verifica que el archivo esté exactamente en `android-app/app/src/main/assets/credentials.json`
- Verifica que el nombre del archivo sea exactamente `credentials.json` (sin espacios, todo en minúsculas)

### Error: "403 Forbidden" al acceder a Sheets
- Verifica que hayas compartido la hoja con el email del Service Account
- Verifica que el Service Account tenga permisos de **Editor** (no solo Lector)
- Espera unos minutos después de compartir (puede tardar en propagarse)

### Error: "API not enabled"
- Verifica que hayas habilitado la **Google Sheets API** en Google Cloud Console
- Ve a "APIs y servicios" > "Biblioteca" y busca "Google Sheets API" para verificar que esté habilitada

## Nota de Seguridad

⚠️ **IMPORTANTE**: El archivo `credentials.json` contiene información sensible. No lo subas a repositorios públicos de GitHub. Si ya lo hiciste, ve a Google Cloud Console y elimina esa clave, luego crea una nueva.
