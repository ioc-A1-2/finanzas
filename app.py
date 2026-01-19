import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
from io import BytesIO
import json

# Intentar importar gspread para Google Sheets
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

# --- CONFIGURACIÓN PÁGINA ---
st.set_page_config(
    page_title="Finanzas Proactivas €", 
    layout="wide", 
    page_icon="💶",
    initial_sidebar_state="expanded"
)

# --- CONSTANTES ---
FILE_NAME = "finanzas.csv"
CAT_FILE_NAME = "categorias.csv"
REC_FILE_NAME = "recurrentes.csv"

# Configuración de Google Sheets (usar variables de entorno en Streamlit Cloud)
GOOGLE_SHEETS_ENABLED = os.getenv('GOOGLE_SHEETS_ENABLED', 'false').lower() == 'true'
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON', '')

# Nombres de las hojas en Google Sheets
SHEET_FINANZAS = "Finanzas"
SHEET_CATEGORIAS = "Categorias"
SHEET_RECURRENTES = "Recurrentes"

MESES_ES_DICT = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

COLUMNS = ["Fecha", "Tipo", "Categoría", "Concepto", "Importe", "Frecuencia", "Impacto_Mensual", "Es_Conjunto"]
COLUMNS_REC = ["Tipo", "Categoría", "Concepto", "Importe", "Frecuencia", "Es_Conjunto"]

# --- FUNCIONES DE GOOGLE SHEETS ---
@st.cache_resource
def get_google_sheet():
    """Inicializa y retorna la conexión a Google Sheets"""
    if not GSPREAD_AVAILABLE or not GOOGLE_SHEETS_ENABLED:
        return None
    
    try:
        if GOOGLE_CREDENTIALS_JSON and GOOGLE_SHEET_ID:
            # Parsear credenciales desde JSON string
            creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            client = gspread.authorize(creds)
            return client.open_by_key(GOOGLE_SHEET_ID)
        elif os.path.exists('credentials.json') and GOOGLE_SHEET_ID:
            # Fallback: usar archivo de credenciales local (útil para desarrollo)
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
            client = gspread.authorize(creds)
            return client.open_by_key(GOOGLE_SHEET_ID)
    except Exception as e:
        st.error(f"Error conectando a Google Sheets: {str(e)}")
        return None
    
    return None

def get_or_create_worksheet(sheet, sheet_name, headers):
    """Obtiene o crea una hoja de cálculo con los encabezados"""
    try:
        worksheet = sheet.worksheet(sheet_name)
        return worksheet
    except gspread.exceptions.WorksheetNotFound:
        # Crear nueva hoja
        worksheet = sheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
        if headers:
            worksheet.append_row(headers)
        return worksheet
    except Exception as e:
        st.error(f"Error obteniendo hoja {sheet_name}: {str(e)}")
        return None

# --- FUNCIONES DE DATOS ---
@st.cache_data
def load_data():
    """Carga datos desde Google Sheets o archivo local"""
    # Intentar cargar desde Google Sheets primero
    if GOOGLE_SHEETS_ENABLED and GSPREAD_AVAILABLE:
        sheet = get_google_sheet()
        if sheet:
            try:
                worksheet = get_or_create_worksheet(sheet, SHEET_FINANZAS, COLUMNS)
                if worksheet:
                    records = worksheet.get_all_records()
                    if records:
                        df = pd.DataFrame(records)
                        df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
                        if "Es_Conjunto" not in df.columns: 
                            df["Es_Conjunto"] = False
                        return df.dropna(subset=['Fecha']).copy()
                    else:
                        # Si está vacía, retornar DataFrame vacío
                        return pd.DataFrame(columns=COLUMNS)
            except Exception as e:
                st.warning(f"Error cargando desde Google Sheets: {str(e)}. Usando archivo local.")
    
    # Fallback: cargar desde archivo local
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_csv(FILE_NAME)
            df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
            if "Es_Conjunto" not in df.columns: df["Es_Conjunto"] = False
            return df.dropna(subset=['Fecha'])
        except: pass
    return pd.DataFrame(columns=COLUMNS)

def save_all_data(df):
    """Guarda datos en Google Sheets o archivo local"""
    df_to_save = df.copy()
    df_to_save['Fecha'] = df_to_save['Fecha'].dt.strftime("%d/%m/%Y")
    
    # Intentar guardar en Google Sheets primero
    if GOOGLE_SHEETS_ENABLED and GSPREAD_AVAILABLE:
        sheet = get_google_sheet()
        if sheet:
            try:
                worksheet = get_or_create_worksheet(sheet, SHEET_FINANZAS, COLUMNS)
                if worksheet:
                    # Limpiar hoja y escribir nuevos datos
                    worksheet.clear()
                    worksheet.append_row(COLUMNS)
                    
                    # Convertir DataFrame a lista de listas
                    for _, row in df_to_save.iterrows():
                        worksheet.append_row(row.tolist())
                    
                    st.cache_data.clear()
                    return
            except Exception as e:
                st.warning(f"Error guardando en Google Sheets: {str(e)}. Guardando en archivo local.")
    
    # Fallback: guardar en archivo local
    df_to_save.to_csv(FILE_NAME, index=False)

def load_recurrentes():
    """Carga gastos recurrentes desde Google Sheets o archivo local"""
    if GOOGLE_SHEETS_ENABLED and GSPREAD_AVAILABLE:
        sheet = get_google_sheet()
        if sheet:
            try:
                worksheet = get_or_create_worksheet(sheet, SHEET_RECURRENTES, COLUMNS_REC)
                if worksheet:
                    records = worksheet.get_all_records()
                    if records:
                        return pd.DataFrame(records)
                    else:
                        worksheet.append_row(COLUMNS_REC)
            except Exception as e:
                st.warning(f"Error cargando recurrentes desde Google Sheets: {str(e)}")
    
    if os.path.exists(REC_FILE_NAME):
        try: return pd.read_csv(REC_FILE_NAME)
        except: pass
    return pd.DataFrame(columns=COLUMNS_REC)

def save_recurrentes(df):
    """Guarda gastos recurrentes en Google Sheets o archivo local"""
    if GOOGLE_SHEETS_ENABLED and GSPREAD_AVAILABLE:
        sheet = get_google_sheet()
        if sheet:
            try:
                worksheet = get_or_create_worksheet(sheet, SHEET_RECURRENTES, COLUMNS_REC)
                if worksheet:
                    worksheet.clear()
                    worksheet.append_row(COLUMNS_REC)
                    for _, row in df.iterrows():
                        worksheet.append_row(row.tolist())
                    return
            except Exception as e:
                st.warning(f"Error guardando recurrentes en Google Sheets: {str(e)}")
    
    df.to_csv(REC_FILE_NAME, index=False)

def load_categories():
    """Carga categorías desde Google Sheets o archivo local"""
    default = ["Vivienda", "Transporte", "Comida", "Seguros", "Ahorro", "Ingresos", "Otros"]
    
    if GOOGLE_SHEETS_ENABLED and GSPREAD_AVAILABLE:
        sheet = get_google_sheet()
        if sheet:
            try:
                worksheet = get_or_create_worksheet(sheet, SHEET_CATEGORIAS, ["Categoría"])
                if worksheet:
                    records = worksheet.get_all_records()
                    if records:
                        return [r['Categoría'] for r in records if r.get('Categoría')]
                    else:
                        # Inicializar con categorías por defecto
                        for cat in default:
                            worksheet.append_row([cat])
                        return default
            except Exception as e:
                st.warning(f"Error cargando categorías desde Google Sheets: {str(e)}")
    
    if os.path.exists(CAT_FILE_NAME):
        try:
            df = pd.read_csv(CAT_FILE_NAME)
            if not df.empty: return df['Categoría'].tolist()
        except: pass
    return default

def save_categories(lista):
<<<<<<< HEAD
    """Guarda categorías en Google Sheets o archivo local"""
    lista = list(dict.fromkeys(lista))
    
    if GOOGLE_SHEETS_ENABLED and GSPREAD_AVAILABLE:
        sheet = get_google_sheet()
        if sheet:
            try:
                worksheet = get_or_create_worksheet(sheet, SHEET_CATEGORIAS, ["Categoría"])
                if worksheet:
                    worksheet.clear()
                    worksheet.append_row(["Categoría"])
                    for cat in lista:
                        worksheet.append_row([cat])
                    st.cache_data.clear()
                    return
            except Exception as e:
                st.warning(f"Error guardando categorías en Google Sheets: {str(e)}")
    
    lista = list(dict.fromkeys(lista))
    pd.DataFrame({"Categoría": lista}).to_csv(CAT_FILE_NAME, index=False)

def formatear_periodo_es(fecha_dt):
    if isinstance(fecha_dt, str):
        try: fecha_dt = datetime.strptime(fecha_dt, "%Y-%m")
        except: return fecha_dt
    return f"{MESES_ES_DICT[fecha_dt.month]} {fecha_dt.year}"

# --- ESTADO SESIÓN ---
if 'simulacion' not in st.session_state: 
    st.session_state.simulacion = []

# --- CARGA ---
df = load_data()
df_rec = load_recurrentes()
lista_cats = load_categories()

# --- SIDEBAR ---
st.sidebar.header("📝 Gestión de Movimientos")
modo_simulacion = st.sidebar.checkbox("🧪 Modo Simulación", help="Prueba gastos sin guardar")

color = "orange" if modo_simulacion else "green"
txt = "MODO ESCENARIO" if modo_simulacion else "MODO REGISTRO"
st.sidebar.markdown(f":{color}[**{txt}**]")

if modo_simulacion and len(st.session_state.simulacion) > 0:
    st.sidebar.info(f"Items simulados: {len(st.session_state.simulacion)}")

with st.sidebar.form("form_reg", clear_on_submit=True):
    tipo = st.radio("Tipo", ["Ingreso", "Gasto"], index=1, horizontal=True)
    es_conjunto = st.checkbox("👥 Gasto Conjunto (Div / 2)")
    fecha = st.date_input("Fecha", datetime.now(), format="DD/MM/YYYY")
    cat = st.selectbox("Categoría", lista_cats)
    con = st.text_input("Concepto")
    imp_input = st.number_input("Importe Total (€)", min_value=0.0, step=10.0, format="%.2f")
    fre = st.selectbox("Frecuencia", ["Mensual", "Anual", "Puntual"])
    
    imp_real = imp_input / 2 if es_conjunto and tipo == "Gasto" else imp_input
    if es_conjunto and tipo == "Gasto" and imp_input > 0:
        st.sidebar.caption(f"ℹ️ Se registrarán **{imp_real:.2f} €**")

    btn = "➕ Añadir a Simulación" if modo_simulacion else "💾 Guardar"
    
    if st.form_submit_button(btn, use_container_width=True):
        if imp_input > 0 and con:
            impacto = imp_real / 12 if fre == "Anual" else imp_real
            
            if modo_simulacion:
                # LÓGICA DE SIMULACIÓN CORREGIDA
                st.session_state.simulacion.append({
                    "Fecha": fecha.strftime("%d/%m/%Y"), 
                    "Tipo": tipo, 
                    "Concepto": f"{con} (Sim)",
                    "Importe": imp_real, 
                    "Frecuencia": fre, 
                    "Impacto_Mensual": impacto, 
                    "Es_Conjunto": es_conjunto
                })
                st.success("Añadido a simulación")
                st.rerun()
            else:
                # LÓGICA DE GUARDADO REAL
                new_row = pd.DataFrame([[pd.to_datetime(fecha), tipo, cat, con, imp_real, fre, impacto, es_conjunto]], columns=COLUMNS)
                df = pd.concat([df, new_row], ignore_index=True)
                save_all_data(df)
                st.success("Guardado")
                st.rerun()
        else: st.error("Faltan datos")

# --- DASHBOARD ---
st.title("🚀 Finanzas Personales (€)")

if df.empty: st.info("Empieza añadiendo movimientos.")
else:
    # CÁLCULOS REALES
    now = datetime.now()
    df_mes = df[(df['Fecha'].dt.month == now.month) & (df['Fecha'].dt.year == now.year)]
    
    ingresos = df_mes[df_mes['Tipo'] == "Ingreso"]['Importe'].sum()
    n_meses = max(len(df['Fecha'].dt.to_period('M').unique()), 1)
    gasto_pro = df[df['Tipo'] == "Gasto"]['Impacto_Mensual'].sum() / n_meses
    
    df_anuales = df[(df['Tipo'] == "Gasto") & (df['Frecuencia'] == "Anual")]
    prov_anual = df_anuales['Impacto_Mensual'].sum() if not df_anuales.empty else 0
    total_conjunto = df[df['Es_Conjunto'] == True]['Importe'].sum()

    # PESTAÑAS
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["🤖 Asesor", "📊 Gráficos", "🔍 Tabla", "🔄 Recurrentes", "📝 Editar", "⚙️ Config"]
    )

    # --- TAB 1: ASESOR & SIMULACIÓN (RESTAURADO) ---
    with tab1:
        # 1. PARTE SUPERIOR: DATOS REALES
        c1, c2, c3 = st.columns(3)
        ahorro_real = ingresos - gasto_pro
        with c1:
            st.metric("Ingresos Mes", f"{ingresos:,.2f} €")
            st.metric("Gasto Promedio", f"{gasto_pro:,.2f} €")
            st.metric("Capacidad Ahorro", f"{ahorro_real:,.2f} €")
        with c2:
            st.metric("🐷 Hucha Anuales (Mes)", f"{prov_anual:,.2f} €", help="Ahorra esto cada mes")
        with c3:
            st.metric("👥 Acumulado Conjunto", f"{total_conjunto:,.2f} €")
        
        # 2. PARTE INFERIOR: ZONA DE SIMULACIÓN
        st.markdown("---")
        if len(st.session_state.simulacion) > 0:
            st.subheader("🧪 Análisis de Escenario Simulado")
            st.caption("Estos son los gastos/ingresos que estás probando (NO se han guardado):")
            
            # Recuperamos la lista y creamos DF temporal
            lista_sim = st.session_state.simulacion
            df_sim = pd.DataFrame(lista_sim)
            
            # Mostramos tabla de items simulados
            col_tabla, col_metrics = st.columns([2, 1])
            
            with col_tabla:
                st.dataframe(df_sim[['Tipo', 'Concepto', 'Importe', 'Frecuencia']], use_container_width=True, hide_index=True)
            
            # Cálculos del impacto simulado
            with col_metrics:
                sim_gastos = df_sim[df_sim['Tipo'] == "Gasto"]['Impacto_Mensual'].sum()
                sim_ingresos = df_sim[df_sim['Tipo'] == "Ingreso"]['Impacto_Mensual'].sum()
                
                nuevo_ingreso_total = ingresos + sim_ingresos
                nuevo_gasto_total = gasto_pro + sim_gastos
                nuevo_ahorro = nuevo_ingreso_total - nuevo_gasto_total
                
                st.metric("Nuevo Ahorro Proyectado", f"{nuevo_ahorro:,.2f} €", 
                          delta=f"{(nuevo_ahorro - ahorro_real):,.2f} €")
                
                if nuevo_ahorro < 0:
                    st.error("⛔ Peligro: Déficit")
                elif nuevo_ahorro < ahorro_real:
                    st.warning("📉 Ahorro reducido")
                else:
                    st.success("🚀 Ahorro mejorado")

                if st.button("🗑️ Borrar Simulación", type="primary", use_container_width=True):
                    st.session_state.simulacion = []
                    st.rerun()
        else:
            st.info("💡 Consejo: Activa el 'Modo Simulación' en la barra lateral para probar gastos sin ensuciar tus datos.")

    with tab2:
        df_ev = df.groupby([df['Fecha'].dt.to_period('M'), 'Tipo'])['Importe'].sum().reset_index()
        df_ev['Mes'] = df_ev['Fecha'].dt.to_timestamp().apply(formatear_periodo_es)
        fig = px.bar(df_ev.sort_values("Fecha"), x='Mes', y='Importe', color='Tipo', barmode='group',
                     color_discrete_map={'Ingreso': '#00CC96', 'Gasto': '#EF553B'})
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.dataframe(df.style.format({"Fecha": lambda t: t.strftime("%d/%m/%Y"), "Importe": "{:,.2f} €"}), use_container_width=True)

    # --- RECURRENTES ---
    with tab4:
        st.subheader("🔄 Generador de Gastos Fijos")
        col_list, col_action = st.columns([2, 1])
        
        with col_list:
            edited_rec = st.data_editor(df_rec, num_rows="dynamic", use_container_width=True, key="editor_rec")
            if st.button("💾 Guardar Plantillas"):
                save_recurrentes(edited_rec)
                st.success("Guardado"); st.rerun()

        with col_action:
            fecha_gen = st.date_input("Generar para fecha:", datetime.now(), format="DD/MM/YYYY")
            if st.button("🚀 Cargar Fijos", type="primary", use_container_width=True):
                if not df_rec.empty:
                    nuevos_movs = []
                    for _, row in df_rec.iterrows():
                        imp_base = row['Importe']
                        imp_final = imp_base / 2 if row['Es_Conjunto'] and row['Tipo'] == "Gasto" else imp_base
                        impacto = imp_final / 12 if row['Frecuencia'] == "Anual" else imp_final
                        nuevos_movs.append([pd.to_datetime(fecha_gen), row['Tipo'], row['Categoría'], row['Concepto'], imp_final, row['Frecuencia'], impacto, row['Es_Conjunto']])
                    
                    df = pd.concat([df, pd.DataFrame(nuevos_movs, columns=COLUMNS)], ignore_index=True)
                    save_all_data(df)
                    st.success(f"Generados {len(nuevos_movs)} movimientos"); st.rerun()

    with tab5:
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True,
                                   column_config={"Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY")})
        if st.button("Guardar Tabla"):
            edited_df['Impacto_Mensual'] = edited_df.apply(lambda x: x['Importe']/12 if x['Frecuencia']=="Anual" else x['Importe'], axis=1)
            save_all_data(edited_df); st.rerun()

    with tab6:
<<<<<<< HEAD
        st.subheader("📤 Exportar Datos")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.markdown("**Exportar como CSV**")
            csv = df_filtrado.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name=f"finanzas_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_exp2:
            st.markdown("**Exportar como Excel**")
            try:
                excel_data = export_to_excel(df_filtrado)
                st.download_button(
                    label="📊 Descargar Excel",
                    data=excel_data,
                    file_name=f"finanzas_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except ImportError:
                st.warning("⚠️ Para exportar a Excel, instala: pip install openpyxl")
                st.code("pip install openpyxl")
        
        st.markdown("---")
        st.markdown("**📋 Resumen de Datos Exportados**")
        st.info(f"Se exportarán {len(df_filtrado)} registros filtrados.")
    
    # --- TAB 7: CONFIGURACIÓN MEJORADA ---
    with tab7:
        st.subheader("⚙️ Configuración")
        
        # Gestión de categorías
        st.markdown("### 📁 Gestión de Categorías")
        new_cats = st.data_editor(
            pd.DataFrame({"Categoría": lista_cats}),
            num_rows="dynamic",
            use_container_width=True,
            key="editor_cats"
        )
        
        if st.button("💾 Guardar Categorías", type="primary"):
            categorias_validas = [c for c in new_cats["Categoría"].tolist() if c and pd.notna(c)]
            if categorias_validas:
                save_categories(categorias_validas)
                st.success("✅ Categorías guardadas")
                st.rerun()
            else:
                st.error("❌ Debe haber al menos una categoría")
        
        st.markdown("---")
        
        # Configuración de Google Sheets
        st.markdown("### ☁️ Google Drive / Sheets")
        
        if GOOGLE_SHEETS_ENABLED and GSPREAD_AVAILABLE:
            sheet = get_google_sheet()
            if sheet:
                st.success("✅ Google Sheets conectado correctamente")
                st.info(f"📊 Libro: **{sheet.title}**")
                st.caption("Tus datos se están guardando automáticamente en Google Drive")
            else:
                st.warning("⚠️ Google Sheets no está configurado correctamente")
                st.markdown("""
                **Para configurar Google Sheets:**
                
                1. Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
                2. Habilita la API de Google Sheets y Google Drive
                3. Crea una cuenta de servicio y descarga el archivo JSON de credenciales
                4. Crea una hoja de cálculo en Google Sheets y compártela con el email de la cuenta de servicio
                5. En Streamlit Cloud, agrega estas variables de entorno:
                   - `GOOGLE_SHEETS_ENABLED=true`
                   - `GOOGLE_SHEET_ID=tu_id_de_la_hoja`
                   - `GOOGLE_CREDENTIALS_JSON=contenido_del_json_como_texto`
                """)
        else:
            st.info("💡 **Google Sheets no está habilitado**")
            st.markdown("""
            **Actualmente los datos se guardan solo localmente. Para habilitar Google Sheets:**
            
            1. Instala las dependencias: `pip install gspread google-auth`
            2. Configura las credenciales de Google Cloud
            3. En Streamlit Cloud, configura las variables de entorno:
               - `GOOGLE_SHEETS_ENABLED=true`
               - `GOOGLE_SHEET_ID=tu_id_de_la_hoja`
               - `GOOGLE_CREDENTIALS_JSON=contenido_del_json`
            
            **📝 Estado actual:**
            - Almacenamiento: Archivo local (se pierde al reiniciar Streamlit Cloud)
            - Recomendado: Configurar Google Sheets para persistencia permanente
            """)
        
        st.markdown("---")
        
        # Estadísticas del sistema
        st.markdown("### 📊 Estadísticas del Sistema")
        col_sys1, col_sys2 = st.columns(2)
        with col_sys1:
            st.metric("Total Movimientos", len(df))
            st.metric("Categorías Activas", len(lista_cats))
        with col_sys2:
            st.metric("Plantillas Guardadas", len(df_rec))
            if not df.empty:
                fecha_antigua = df['Fecha'].min()
                fecha_reciente = df['Fecha'].max()
                st.metric("Rango de Datos", f"{fecha_antigua.strftime('%d/%m/%Y')} - {fecha_reciente.strftime('%d/%m/%Y')}")
