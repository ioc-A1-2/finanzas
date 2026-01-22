# 📋 Especificación Completa de la Aplicación de Finanzas Personales

## 🎯 Concepto General

**"Finanzas Proactivas €"** es una aplicación web de gestión financiera personal desarrollada con Streamlit que permite a los usuarios:

- Registrar ingresos y gastos de forma intuitiva
- Visualizar sus finanzas con gráficos avanzados
- Recibir recomendaciones inteligentes basadas en patrones
- Consultar un asistente IA (Gemini) sobre sus finanzas
- Simular escenarios financieros sin afectar datos reales
- Gestionar presupuestos por categorías
- Exportar/importar datos
- Gestionar gastos recurrentes

---

## 📱 Características de Diseño y UX

### **Responsive Design - Prioridad Móvil**
- La aplicación está optimizada principalmente para móviles (Google Chrome en Android)
- Diseño adaptativo que aprovecha al máximo el espacio disponible
- Sidebar nativa de Streamlit completamente oculta en móvil
- Todos los elementos se adaptan al tamaño de pantalla

### **Header Superior (Siempre Visible)**
- **Posición**: Sticky (fijo en la parte superior al hacer scroll)
- **Contenido**:
  - **Izquierda (3/5 del ancho)**: Título dinámico según la sección actual
  - **Centro (1/5 del ancho)**: Botón "➕ Nuevo" (compacto, no ocupa todo el ancho)
  - **Derecha (1/5 del ancho)**: Botón "☰" (menú hamburger)
- **Comportamiento**: El header permanece visible en todas las secciones

### **Menú de Navegación (Hamburger)**
- **Ubicación**: Botón en la esquina superior derecha del header
- **Comportamiento**: 
  - Al hacer clic, se desliza un menú desde el lado derecho de la pantalla
  - El menú cubre aproximadamente 280px de ancho
  - Animación de deslizamiento suave (slideInRight)
  - Al seleccionar una opción, el menú se cierra automáticamente
- **Opciones del Menú**:
  1. 🤖 Asesor
  2. 📊 Gráficos
  3. 🔍 Tabla
  4. 🔄 Recurrentes
  5. 📝 Editar
  6. 📤 Exportar/Importar
  7. 💰 Presupuestos
  8. ⚙️ Config

### **Modal de Nuevo Movimiento**
- **Trigger**: Botón "➕ Nuevo" en el header
- **Diseño**:
  - Modal centrado en pantalla
  - Fondo oscuro semitransparente (overlay)
  - Contenido con fondo del tema, bordes redondeados
  - **NO tiene título ni botón X** - comienza directamente con los campos del formulario
- **Formulario Inteligente**:
  - **Fila 1**: Checkbox "🧪 Simulación" (izquierda) + Radio buttons "Tipo" (Ingreso/Gasto) (derecha)
  - **Fila 2**: Checkbox "👥 Gasto Conjunto (Dividir entre 2)"
  - **Fila 3**: Campo "📅 Fecha" (izquierda) + Selectbox "Categoría" (derecha)
  - **Fila 4**: Campo "Concepto" (ancho completo)
  - **Fila 5**: Campo "Importe Total (€)" (izquierda, 2/3) + Selectbox "Frecuencia" (derecha, 1/3)
  - **Fila 6**: Botones "Guardar/Añadir a Simulación" (izquierda) + "Cancelar" (derecha)
  - **Fuera del formulario**: Botón "❌ Cerrar" (abajo del formulario)
- **Características Especiales**:
  - El campo de fecha NO debe abrir el teclado en móvil (solo calendario)
  - El calendario debe aparecer centrado y no ocultar el formulario
  - Si es "Gasto Conjunto", muestra un mensaje informativo con el importe dividido
  - El dropdown "Frecuencia" es visible antes del botón de guardar

---

## 🏗️ Estructura de Secciones

### 1. 🤖 ASESOR (Sección Principal)

#### **Parte Superior: Métricas Financieras**
- **3 columnas con métricas**:
  - **Columna 1**: 
    - Ingresos del Mes
    - Gasto Promedio
    - Capacidad de Ahorro
  - **Columna 2**:
    - 🐷 Hucha Anuales (Mes) - Ahorro mensual recomendado
    - 📊 Promedio Mensual (histórico)
  - **Columna 3**:
    - 👥 Acumulado Conjunto (gastos compartidos)

#### **Recomendaciones Inteligentes**
- Sección con título "💡 Recomendaciones Inteligentes"
- Muestra hasta 5 recomendaciones basadas en:
  - Comparación con presupuestos (warnings/errors si se excede)
  - Gastos inusuales detectados
  - Alertas de sobrepaso de presupuesto
- Cada recomendación tiene un tipo visual (error/warning/info)

#### **Análisis de Patrones**
- Sección con título "📈 Análisis de Patrones"
- **2 columnas**:
  - **Izquierda**: "🏆 Top 5 Categorías con Más Gasto" (lista)
  - **Derecha**: "📅 Gastos por Día de la Semana" (lista con días en español)

#### **Asistente IA con Gemini**
- Sección con título "🤖 Asistente IA con Gemini"
- **Historial de Chat**:
  - Muestra los últimos 10 mensajes
  - Mensajes del usuario con avatar "user"
  - Mensajes del asistente con avatar "assistant"
- **Campo de Entrada**:
  - Text input con placeholder con ejemplos de preguntas
  - Se limpia automáticamente después de enviar
- **Botones**:
  - "💬 Enviar Pregunta" (principal, 3/4 del ancho)
  - "🗑️ Limpiar Chat" (1/4 del ancho)
- **Preguntas Sugeridas** (Expandible):
  - Lista de 8 preguntas predefinidas en 2 columnas
  - Cada pregunta es un botón clickeable que envía la pregunta directamente
- **Estado**: Si Gemini no está configurado, muestra instrucciones de configuración

#### **Zona de Simulación**
- Solo visible si hay elementos en simulación
- Título: "🧪 Análisis de Escenario Simulado"
- **2 columnas**:
  - **Izquierda (2/3)**: Tabla con los movimientos simulados (Tipo, Concepto, Importe, Frecuencia)
  - **Derecha (1/3)**: 
    - Métrica: "Nuevo Ahorro Proyectado" con delta
    - Indicadores visuales: ⛔ Peligro (déficit), 📉 Ahorro reducido, 🚀 Ahorro mejorado
    - Botón "🗑️ Borrar Simulación"
- Si no hay simulación, muestra un mensaje informativo sobre el modo simulación

---

### 2. 📊 GRÁFICOS

- Título: "📊 Visualizaciones Avanzadas"
- **Selector de Visualización** (dropdown):
  1. **Evolución Temporal**: Gráfico de barras agrupadas (Ingresos vs Gastos por mes)
  2. **Distribución por Categorías**: 
     - 2 columnas: Gráfico de pastel (izquierda) + Gráfico de barras (derecha)
  3. **Gráfico de Sankey (Flujo)**: 
     - Visualización de flujo: Ingresos → Categorías → Ahorro
     - Colores: Verde (Ingresos), Rojo (Gastos), Naranja (Ahorro)
  4. **Gráfico de Burbujas**: 
     - Scatter plot: Mes vs Categoría
     - Tamaño de burbuja = Importe
     - Color = Importe (escala roja)
  5. **Calendario de Gastos**: 
     - Scatter plot: Día del mes vs Mes
     - Tamaño = Importe del día
  6. **Heatmap por Día de Semana**: 
     - Heatmap: Día de semana (filas) vs Mes (columnas)
     - Intensidad de color = Importe total

---

### 3. 🔍 TABLA

- Muestra todos los movimientos en formato tabla (DataFrame de Streamlit)
- Columnas: Fecha, Tipo, Categoría, Concepto, Importe, Frecuencia, Impacto_Mensual, Es_Conjunto
- Formato: Fecha en DD/MM/YYYY, Importe con 2 decimales y símbolo €

---

### 4. 🔄 RECURRENTES

- Título: "🔄 Generador de Gastos Fijos"
- **2 columnas**:
  - **Izquierda (2/3)**: 
    - Editor de datos (data_editor) para gestionar plantillas de gastos recurrentes
    - Botón "💾 Guardar Plantillas"
  - **Derecha (1/3)**:
    - Date input: "Generar para fecha:"
    - Botón "🚀 Cargar Fijos" (principal)
    - Al hacer clic, genera movimientos para todas las plantillas en la fecha seleccionada

---

### 5. 📝 EDITAR

- Título: "📝 Editar Movimientos"
- Subtítulo: "Edita los movimientos directamente en la tabla y haz clic en 'Guardar Cambios'"
- **Editor de Datos**:
  - Permite editar todos los campos directamente en la tabla
  - Configuración de columnas:
    - Fecha: DateColumn (formato DD/MM/YYYY)
    - Tipo: SelectboxColumn (Ingreso/Gasto)
    - Categoría: SelectboxColumn (opciones dinámicas)
    - Concepto: TextColumn
    - Importe: NumberColumn
    - Frecuencia: SelectboxColumn (Puntual/Mensual/Anual)
    - Es_Conjunto: CheckboxColumn
  - Permite agregar nuevas filas y eliminar existentes
- **Botón "💾 Guardar Cambios"**: Guarda todas las modificaciones

---

### 6. 📤 EXPORTAR/IMPORTAR

- Título: "📤 Exportar / Importar"
- **2 columnas**:
  - **Exportar**:
    - Botón "📥 Descargar CSV" (descarga el DataFrame completo)
    - Botón "📥 Descargar Excel" (descarga como archivo Excel)
  - **Importar**:
    - File uploader para CSV o Excel
    - Botón "📤 Cargar Datos" para procesar el archivo
    - Validación y merge con datos existentes

---

### 7. 💰 PRESUPUESTOS

- Título: "💰 Presupuestos"
- **Editor de Presupuestos**:
  - Tabla editable con columnas: Categoría, Presupuesto_Mensual
  - Permite agregar/editar/eliminar presupuestos
- **Visualización de Estado**:
  - Muestra el estado de cada presupuesto (dentro/sobrepasado)
  - Comparación visual del gasto vs presupuesto

---

### 8. ⚙️ CONFIG

- Título: "⚙️ Configuración"
- **Gestión de Categorías**:
  - Editor para agregar/editar/eliminar categorías
- **Configuración de Google Sheets** (si está habilitado):
  - Información sobre el estado de la conexión
- **Configuración de Gemini** (si está habilitado):
  - Estado de la API key
  - Información del modelo en uso

---

## 🎨 Paleta de Colores y Estilo

### **Colores Principales**
- **Primario**: Gradiente púrpura/azul (#667eea → #764ba2)
- **Ingresos**: Verde (#00CC96)
- **Gastos**: Rojo (#EF553B)
- **Ahorro**: Naranja (#FFA726)
- **Fondo**: Tema oscuro de Streamlit (var(--background-color))

### **Tipografía**
- **Títulos H1**: Gradiente de texto (púrpura/azul), font-weight: 700
- **Títulos H2/H3**: Color #667eea, font-weight: 600
- **Texto general**: Color del tema de Streamlit

### **Componentes**
- **Botones**: Bordes redondeados (0.5rem), transiciones suaves, hover con elevación
- **Inputs**: Bordes redondeados, focus con borde púrpura y sombra
- **Formularios**: Fondo semitransparente, bordes sutiles, padding generoso
- **Info Boxes**: Borde izquierdo de 4px con color según tipo (azul/verde/naranja/rojo)

---

## 📱 Optimizaciones Móviles Específicas

### **Inputs y Formularios**
- Font-size mínimo de 16px en inputs para evitar zoom automático en iOS
- Altura mínima de 44px en botones e inputs (estándar de accesibilidad)
- Padding reducido pero suficiente para toques precisos

### **Calendario (Date Input)**
- **CRÍTICO**: El input de fecha NO debe abrir el teclado
- Implementación: `readonly`, `inputmode="none"`, JavaScript para prevenir teclado
- Calendario aparece centrado en pantalla con z-index alto
- Tamaño de días del calendario aumentado (2.5rem x 2.5rem)

### **Espaciado**
- Padding reducido en contenedores principales (0.75rem en móvil)
- Headers más pequeños (H1: 1.5rem, H2: 1.25rem, H3: 1.1rem)
- Elementos más compactos pero legibles

### **Gráficos**
- Ancho 100% en móvil
- Altura adaptativa
- Interactividad táctil optimizada

---

## 🔧 Funcionalidades Técnicas

### **Almacenamiento de Datos**
- **Primario**: Google Sheets (si está configurado)
- **Fallback**: Archivo CSV local (`finanzas.csv`)
- Sincronización automática

### **Cálculos Automáticos**
- **Impacto_Mensual**: 
  - Puntual: Importe completo
  - Mensual: Importe completo
  - Anual: Importe / 12
- **Gasto Conjunto**: Si está marcado, el importe se divide entre 2
- **Provisiones Anuales**: Cálculo automático de ahorro mensual necesario para gastos anuales

### **Análisis de Patrones**
- Detección de gastos inusuales
- Cálculo de promedios mensuales
- Análisis por día de la semana
- Top categorías con más gasto

### **Integración con Gemini AI**
- Contexto financiero preparado automáticamente
- Historial de conversación mantenido en sesión
- Respuestas en español
- Análisis proactivo de datos financieros

---

## 🎯 Flujos de Usuario Principales

### **1. Agregar Nuevo Movimiento**
1. Usuario hace clic en "➕ Nuevo" (header)
2. Se abre modal con formulario
3. Usuario completa campos (fecha, tipo, categoría, concepto, importe, frecuencia)
4. Opcional: Marca "Gasto Conjunto" o "Simulación"
5. Hace clic en "Guardar" o "Añadir a Simulación"
6. Modal se cierra, datos se guardan/agregan a simulación
7. App se actualiza automáticamente

### **2. Consultar Asistente IA**
1. Usuario va a sección "🤖 Asesor"
2. Se desplaza hasta "🤖 Asistente IA con Gemini"
3. Escribe pregunta en el campo de texto
4. Hace clic en "💬 Enviar Pregunta"
5. Se muestra respuesta del asistente
6. Puede continuar la conversación o limpiar el chat

### **3. Ver Gráficos**
1. Usuario hace clic en menú hamburger (☰)
2. Selecciona "📊 Gráficos"
3. Elige tipo de visualización del dropdown
4. Ve el gráfico interactivo
5. Puede cambiar el tipo de visualización en cualquier momento

### **4. Simular Escenario**
1. Usuario hace clic en "➕ Nuevo"
2. Marca checkbox "🧪 Simulación"
3. Completa el formulario y guarda
4. El movimiento se agrega a la simulación (no se guarda en datos reales)
5. En la sección "🤖 Asesor", ve el análisis del escenario simulado
6. Puede agregar más movimientos a la simulación
7. Puede borrar toda la simulación cuando termine

---

## 📊 Estructura de Datos

### **Movimientos Financieros**
- **Fecha**: datetime
- **Tipo**: "Ingreso" | "Gasto"
- **Categoría**: string (de lista de categorías)
- **Concepto**: string (descripción)
- **Importe**: float (en euros)
- **Frecuencia**: "Puntual" | "Mensual" | "Anual"
- **Impacto_Mensual**: float (calculado automáticamente)
- **Es_Conjunto**: boolean

### **Gastos Recurrentes (Plantillas)**
- **Tipo**: "Ingreso" | "Gasto"
- **Categoría**: string
- **Concepto**: string
- **Importe**: float
- **Frecuencia**: "Puntual" | "Mensual" | "Anual"
- **Es_Conjunto**: boolean

### **Presupuestos**
- **Categoría**: string
- **Presupuesto_Mensual**: float

---

## 🚀 Características Avanzadas

### **Modo Simulación**
- Permite probar escenarios sin afectar datos reales
- Los movimientos simulados se muestran con "(Sim)" en el concepto
- Análisis separado del escenario simulado
- Se puede borrar toda la simulación con un botón

### **Gastos Conjuntos**
- Opción para dividir gastos entre 2 personas
- El importe se divide automáticamente
- Se muestra el importe real que se registrará
- Útil para parejas o gastos compartidos

### **Análisis Proactivo**
- Recomendaciones automáticas basadas en patrones
- Alertas de presupuestos excedidos
- Detección de gastos inusuales
- Comparación mes actual vs mes anterior

### **Exportación/Importación**
- Exportar datos a CSV o Excel
- Importar datos desde archivos
- Validación y merge inteligente

---

## 🎨 Elementos Visuales Importantes

### **Iconos y Emojis**
- 🤖 Asesor
- 📊 Gráficos
- 🔍 Tabla
- 🔄 Recurrentes
- 📝 Editar
- 📤 Exportar/Importar
- 💰 Presupuestos
- ⚙️ Config
- ➕ Nuevo
- 🧪 Simulación
- 👥 Gasto Conjunto
- 💬 Chat
- 🗑️ Limpiar/Borrar
- ❌ Cerrar/Cancelar
- 💾 Guardar
- 🚀 Acciones principales

### **Estados Visuales**
- **Éxito**: Verde, icono ✓
- **Advertencia**: Naranja, icono ⚠️
- **Error**: Rojo, icono ❌
- **Info**: Azul, icono ℹ️

---

## 📐 Consideraciones de Diseño para el Diseñador

### **Prioridades**
1. **Móvil First**: Diseñar primero para móvil, luego adaptar a desktop
2. **Espacio Eficiente**: Aprovechar cada píxel disponible
3. **Accesibilidad**: Botones e inputs con tamaño mínimo de 44x44px
4. **Claridad**: Información organizada y fácil de escanear
5. **Rapidez**: Interacciones fluidas y sin fricción

### **Elementos Clave a Diseñar**
1. **Header Sticky** con botones compactos
2. **Modal de Nuevo Movimiento** sin título, directo al formulario
3. **Menú Lateral Derecho** con animación de deslizamiento
4. **Cards de Métricas** con información clara
5. **Gráficos Interactivos** responsivos
6. **Chat con IA** con burbujas de conversación
7. **Tablas Editables** con buena UX
8. **Formularios Inteligentes** que se adaptan al espacio

### **Animaciones y Transiciones**
- Menú lateral: Slide in desde la derecha (0.3s ease)
- Modal: Fade in con overlay (0.3s ease)
- Botones: Hover con elevación sutil
- Scroll: Suave y natural

---

## 🔐 Seguridad y Privacidad

- Datos almacenados localmente o en Google Sheets del usuario
- No hay transmisión de datos a terceros (excepto Gemini API si está configurado)
- API keys se almacenan en variables de entorno/secrets
- No se comparten datos financieros con servicios externos

---

## 📝 Notas Finales para el Diseñador

Esta aplicación está diseñada para ser **simple, rápida y eficiente**. El usuario debe poder:

- Agregar un movimiento en menos de 30 segundos
- Ver su situación financiera de un vistazo
- Obtener insights valiosos sin esfuerzo
- Usar la app principalmente desde el móvil

El diseño debe reflejar **profesionalismo, confianza y modernidad**, pero sin ser abrumador. Los colores púrpura/azul dan un toque moderno y tecnológico, mientras que los verdes/rojos para ingresos/gastos son universales y comprensibles.

**El objetivo es hacer que la gestión financiera personal sea tan fácil como enviar un mensaje de texto.**
