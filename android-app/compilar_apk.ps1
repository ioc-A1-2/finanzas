# Script para compilar la APK automáticamente
param(
    [string]$StreamlitURL = ""
)

Write-Host "🚀 Iniciando compilación de APK..." -ForegroundColor Cyan

# Verificar si se proporcionó URL
if ($StreamlitURL -ne "") {
    Write-Host "📝 Configurando URL: $StreamlitURL" -ForegroundColor Yellow
    & .\configurar_url.ps1 -StreamlitURL $StreamlitURL
}

# Verificar si Gradle está disponible
$gradlePath = Get-Command gradle -ErrorAction SilentlyContinue
if (-not $gradlePath) {
    Write-Host "❌ Gradle no encontrado. Instalando Android Studio o configurando Gradle..." -ForegroundColor Red
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Yellow
    Write-Host "1. Instalar Android Studio desde: https://developer.android.com/studio" -ForegroundColor White
    Write-Host "2. Usar GitHub Actions para compilar automáticamente (ver .github/workflows/build-apk.yml)" -ForegroundColor White
    Write-Host "3. Usar el script configurar_url.ps1 para configurar la URL y luego compilar manualmente en Android Studio" -ForegroundColor White
    exit 1
}

# Compilar APK
Write-Host "🔨 Compilando APK..." -ForegroundColor Cyan
try {
    if (Test-Path "gradlew.bat") {
        & .\gradlew.bat assembleDebug
    } else {
        gradle assembleDebug
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ APK compilada exitosamente!" -ForegroundColor Green
        Write-Host "📍 Ubicación: app\build\outputs\apk\debug\app-debug.apk" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al compilar la APK" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Sugerencia: Abre el proyecto en Android Studio y compila desde allí" -ForegroundColor Yellow
    exit 1
}
