# Script para configurar automáticamente la URL de Streamlit en la aplicación Android
param(
    [Parameter(Mandatory=$true)]
    [string]$StreamlitURL
)

$mainActivityPath = "app\src\main\java\com\finanzasproactivas\MainActivity.kt"

if (Test-Path $mainActivityPath) {
    $content = Get-Content $mainActivityPath -Raw
    $content = $content -replace 'private val STREAMLIT_URL = ".*"', "private val STREAMLIT_URL = `"$StreamlitURL`""
    Set-Content $mainActivityPath $content
    Write-Host "✅ URL configurada correctamente: $StreamlitURL" -ForegroundColor Green
} else {
    Write-Host "❌ No se encontró el archivo MainActivity.kt" -ForegroundColor Red
    exit 1
}
