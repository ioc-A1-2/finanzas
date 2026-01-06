import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import calendar # Necesario para calcular los días de cada mes

# --- CONFIGURACIÓN PÁGINA ---
st.set_page_config(
    page_title="Finanzas Proactivas €", 
    layout="wide", 
    page_icon="💶",
    initial_sidebar_state="expanded"
)

# --- TRADUCCIÓN FORZADA (Diccionarios) ---
MESES_ES_LISTA = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
# Mapeo inverso para guardar en base de datos
MESES_ES_DICT = {nombre: i+1 for i, nombre in enumerate(MESES_ES_LISTA)}
MESES_NUM_DICT = {i+1: nombre for i, nombre in enumerate(MESES_ES_LISTA)}

# --- ARCHIVOS ---
FILE_NAME = "finanzas.csv"
CAT_FILE_NAME = "categorias.csv"
COLUMNS = ["Fecha", "Tipo", "Categoría", "Concepto", "Importe", "Frecuencia", "Impacto_Mensual"]

# --- FUNCIONES ---
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_csv(FILE_NAME)
            df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
            df = df.dropna(subset=['Fecha'])
            return df
        except Exception:
            return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(columns=COLUMNS)

def save_all_data(df):
    df_to_save = df.copy()
    df_to_save['Fecha'] = df_to_save['Fecha'].dt.strftime("%d/%m/%Y")
    df_to_save.to_csv(FILE_NAME, index=False)

def load_categories():
    default_cats = ["Vivienda", "Transporte", "Comida", "Seguros", "Ahorro", "Ingresos", "Otros"]
    if os.path.exists(CAT_FILE_NAME):
        try:
            df_cat = pd.read_csv(CAT_FILE_NAME)
            if not df_cat.empty: return df_cat['Categoría'].tolist()
        except: pass
    return default_cats

def save_categories(lista):
    lista = list(dict.fromkeys(lista)) 
    pd.DataFrame({"Categoría": lista}).to_csv(CAT_FILE_NAME, index=False)

def formatear_periodo_es(fecha_dt):
    if isinstance(fecha_dt, str):
        try: fecha_dt = datetime.strptime(fecha_dt, "%Y-%m")
        except: return fecha_dt
    nombre_mes = MESES_NUM_DICT[fecha_dt.month]
    return f"{nombre_mes} {fecha_dt.year}"

# --- ESTADO SESIÓN ---
if 'simulacion' not in st.session_state:
    st.session_state.simulacion = None

# --- CARGA DATOS ---
df = load_data()
lista_cats = load_categories()

# --- SIDEBAR: REGISTRO CON FECHA EN CASTELLANO FORZADO ---
st.sidebar.header("📝 Gestión de Movimientos")
modo_simulacion = st.sidebar.checkbox("🧪 Modo Simulación", help="Prueba gastos sin guardar")

color_estado = "red" if modo_simulacion else "green"
st.sidebar.markdown(f":{color_estado}[**ESTADO: {'SIMULANDO' if modo_simulacion else 'REAL'}**]")

with st.sidebar.form("form_reg", clear_on_submit=not modo_simulacion):
    tipo = st.radio("Tipo", ["Ingreso", "Gasto"], index=1, horizontal=True)
    
    # --- SELECTOR DE FECHA PERSONALIZADO (FUERZA CASTELLANO) ---
    st.write("Fecha:")
    col_d, col_m, col_y = st.columns([1, 2, 1.5])
    
    hoy = datetime.now()
    
    with col_y:
        # Años: del actual hacia atrás y adelante
        anos = list(range(hoy.year - 5, hoy.year + 6))
        anio_sel = st.selectbox("Año", anos, index=anos.index(hoy.year), label_visibility="collapsed")
    
    with col_m:
        # Meses: Siempre en Español
        mes_sel_nombre = st.selectbox("Mes", MESES_ES_LISTA, index=hoy.month - 1, label_visibility="collapsed")
        mes_sel_num = MESES_ES_DICT[mes_sel_nombre]
    
    with col_d:
        # Días: Calculamos cuántos días tiene el mes/año seleccionado (ej. bisiestos)
        _, num_dias = calendar.monthrange(anio_sel, mes_sel_num)
        dias = list(range(1, num_dias + 1))
        # Intentamos mantener el día actual, si no existe (ej: 31 feb), ponemos el último posible
        idx_dia = hoy.day - 1 if hoy.day <= num_dias else num_dias - 1
        dia_sel = st.selectbox("Día", dias, index=idx_dia, label_visibility="collapsed")
    
    # Reconstruimos la fecha
    fecha_construida = datetime(anio_sel, mes_sel_num, dia_sel)
    # -------------------------------------------------------------

    cat = st.selectbox("Categoría", lista_cats)
    con = st.text_input("Concepto")
    imp = st.number_input("Importe (€)", min_value=0.0, step=10.0, format="%.2f")
    fre = st.selectbox("Frecuencia", ["Mensual", "Anual", "Puntual"])
    
    btn_txt = "🧪 Simular" if modo_simulacion else "💾 Guardar"
    
    if st.form_submit_button(btn_txt, use_container_width=True):
        if imp > 0 and con:
            impacto = imp / 12 if fre == "Anual" else imp
            if modo_simulacion:
                st.session_state.simulacion = {"Concepto": con, "Importe": imp, "Impacto_Mensual": impacto, "Tipo": tipo}
                st.success("Simulando...")
                # Forzamos recarga para que se note en la UI
                st.rerun() 
            else:
                new_row = pd.DataFrame([[fecha_construida, tipo, cat, con, imp, fre, impacto]], columns=COLUMNS)
                df = pd.concat([df, new_row], ignore_index=True)
                save_all_data(df)
                st.session_state.simulacion = None
                st.success("Guardado")
                st.rerun()
        else:
            st.error("Faltan datos")

# --- DASHBOARD ---
st.title("🚀 Finanzas Personales (€)")

if df.empty:
    st.info("Añade movimientos para empezar.")
else:
    m, y = datetime.now().month, datetime.now().year
    df_mes = df[(df['Fecha'].dt.month == m) & (df['Fecha'].dt.year == y)]
    ingresos = df_mes[df_mes['Tipo'] == "Ingreso"]['Importe'].sum()
    gastos = df_mes[df_mes['Tipo'] == "Gasto"]['Importe'].sum()
    
    # Prorrateo Global
    n_meses = max(len(df['Fecha'].dt.to_period('M').unique()), 1)
    gasto_pro = df[df['Tipo'] == "Gasto"]['Impacto_Mensual'].sum() / n_meses

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 Asesor", "📊 Gráficos", "🔍 Tabla", "📝 Editar", "⚙️ Config"])

    # 1. ASESOR
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📅 Situación Real")
            ahorro = ingresos - gasto_pro
            cap_ahorro = (ahorro / ingresos) if ingresos > 0 else 0
            st.metric("Ingresos Mes", f"{ingresos:,.2f} €")
            st.metric("Gasto Promedio", f"{gasto_pro:,.2f} €")
            st.metric("Ahorro", f"{ahorro:,.2f} €", delta=f"{cap_ahorro:.1%}")
            
        with c2:
            st.markdown("### 🧪 Simulación")
            sim = st.session_state.simulacion
            if sim:
                nuevo_gasto = gasto_pro + sim['Impacto_Mensual'] if sim['Tipo']=="Gasto" else gasto_pro
                nuevo_ahorro = ingresos - nuevo_gasto
                nueva_cap = (nuevo_ahorro / ingresos) if ingresos > 0 else 0
                st.metric("Gasto Simulado", f"{nuevo_gasto:,.2f} €", delta=f"-{sim['Impacto_Mensual']:,.2f} €", delta_color="inverse")
                st.metric("Ahorro Simulado", f"{nuevo_ahorro:,.2f} €", delta=f"{(nueva_cap - cap_ahorro):.1%}")
                
                if nueva_cap < 0: st.error("⛔ Déficit")
                elif nueva_cap < 0.1: st.warning("⚠️ Ahorro bajo")
                else: st.success("🟢 Viable")
                if st.button("Borrar Simulación"):
                    st.session_state.simulacion = None
                    st.rerun()
            else:
                st.info("Activa el modo simulación en la barra lateral.")

    # 2. GRÁFICOS
    with tab2:
        st.subheader("Evolución Mensual")
        df_ev = df.groupby([df['Fecha'].dt.to_period('M'), 'Tipo'])['Importe'].sum().reset_index()
        df_ev['Fecha_dt'] = df_ev['Fecha'].dt.to_timestamp()
        df_ev['Mes_Castellano'] = df_ev['Fecha_dt'].apply(formatear_periodo_es)
        df_ev = df_ev.sort_values("Fecha")

        fig = px.bar(df_ev, x='Mes_Castellano', y='Importe', color='Tipo', barmode='group',
                     color_discrete_map={'Ingreso': '#00CC96', 'Gasto': '#EF553B'})
        fig.update_layout(xaxis_title="", yaxis_title="Euros (€)", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

    # 3. TABLA
    with tab3:
        st.dataframe(df.style.format({"Fecha": lambda t: t.strftime("%d/%m/%Y"), "Importe": "{:,.2f} €"}), use_container_width=True)

    # 4. EDITAR
    with tab4:
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True,
                                   column_config={"Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY")})
        if st.button("Guardar Cambios Tabla", use_container_width=True):
            edited_df['Impacto_Mensual'] = edited_df.apply(lambda x: x['Importe']/12 if x['Frecuencia']=="Anual" else x['Importe'], axis=1)
            save_all_data(edited_df)
            st.rerun()

    # 5. CONFIG
    with tab5:
        new_cats = st.data_editor(pd.DataFrame({"Categoría": lista_cats}), num_rows="dynamic", use_container_width=True)
        if st.button("Guardar Categorías", use_container_width=True):
            save_categories([c for c in new_cats["Categoría"].tolist() if c])
            st.rerun()
