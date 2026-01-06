import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- CONFIGURACIÓN PÁGINA ---
st.set_page_config(
    page_title="Finanzas Proactivas €", 
    layout="wide", 
    page_icon="💶",
    initial_sidebar_state="expanded"
)

# --- TRADUCCIÓN FORZADA (Diccionarios) ---
MESES_ES_DICT = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

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
    nombre_mes = MESES_ES_DICT[fecha_dt.month]
    return f"{nombre_mes} {fecha_dt.year}"

# --- ESTADO SESIÓN (MODIFICADO PARA LISTA) ---
if 'simulacion' not in st.session_state:
    st.session_state.simulacion = [] # Ahora es una lista vacía, no None

# --- CARGA DATOS ---
df = load_data()
lista_cats = load_categories()

# --- SIDEBAR: REGISTRO Y SIMULACIÓN MULTI-ITEM ---
st.sidebar.header("📝 Gestión de Movimientos")
modo_simulacion = st.sidebar.checkbox("🧪 Modo Simulación", help="Acumula varios gastos sin guardar")

color_estado = "orange" if modo_simulacion else "green"
txt_estado = "MODO ESCENARIO (Hipotético)" if modo_simulacion else "MODO REGISTRO (Real)"
st.sidebar.markdown(f":{color_estado}[**{txt_estado}**]")

if modo_simulacion:
    st.sidebar.info(f"Items en simulación: **{len(st.session_state.simulacion)}**")

with st.sidebar.form("form_reg", clear_on_submit=True): # clear_on_submit siempre True para agilizar
    tipo = st.radio("Tipo", ["Ingreso", "Gasto"], index=1, horizontal=True)
    fecha = st.date_input("Fecha", datetime.now(), format="DD/MM/YYYY")
    cat = st.selectbox("Categoría", lista_cats)
    con = st.text_input("Concepto")
    imp = st.number_input("Importe (€)", min_value=0.0, step=10.0, format="%.2f")
    fre = st.selectbox("Frecuencia", ["Mensual", "Anual", "Puntual"])
    
    btn_txt = "➕ Añadir a Simulación" if modo_simulacion else "💾 Guardar Definitivamente"
    
    if st.form_submit_button(btn_txt, use_container_width=True):
        if imp > 0 and con:
            impacto = imp / 12 if fre == "Anual" else imp
            
            if modo_simulacion:
                # AÑADIMOS A LA LISTA en lugar de sobrescribir
                item_sim = {
                    "Fecha": fecha.strftime("%d/%m/%Y"), # Solo visual
                    "Tipo": tipo,
                    "Concepto": con,
                    "Importe": imp,
                    "Frecuencia": fre,
                    "Impacto_Mensual": impacto
                }
                st.session_state.simulacion.append(item_sim)
                st.success(f"Añadido: {con}")
                st.rerun()
            else:
                # GUARDADO REAL
                fecha_dt = pd.to_datetime(fecha)
                new_row = pd.DataFrame([[fecha_dt, tipo, cat, con, imp, fre, impacto]], columns=COLUMNS)
                df = pd.concat([df, new_row], ignore_index=True)
                save_all_data(df)
                st.success("Guardado en CSV")
                st.rerun()
        else:
            st.error("Faltan datos (Importe o Concepto)")

# --- DASHBOARD ---
st.title("🚀 Finanzas Personales (€)")

if df.empty:
    st.info("Añade movimientos para empezar.")
else:
    # CÁLCULOS REALES
    m, y = datetime.now().month, datetime.now().year
    df_mes = df[(df['Fecha'].dt.month == m) & (df['Fecha'].dt.year == y)]
    ingresos_reales = df_mes[df_mes['Tipo'] == "Ingreso"]['Importe'].sum()
    
    # Prorrateo Global Real
    n_meses = max(len(df['Fecha'].dt.to_period('M').unique()), 1)
    gasto_pro_real = df[df['Tipo'] == "Gasto"]['Impacto_Mensual'].sum() / n_meses

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 Asesor & Escenarios", "📊 Gráficos", "🔍 Tabla", "📝 Editar", "⚙️ Config"])

    # 1. ASESOR CON SIMULACIÓN MÚLTIPLE
    with tab1:
        c1, c2 = st.columns(2)
        
        # COLUMNA IZQUIERDA: REALIDAD
        with c1:
            st.markdown("### 📅 Situación Actual")
            ahorro_real = ingresos_reales - gasto_pro_real
            cap_ahorro_real = (ahorro_real / ingresos_reales) if ingresos_reales > 0 else 0
            
            st.metric("Ingresos Reales (Mes)", f"{ingresos_reales:,.2f} €")
            st.metric("Gasto Promedio Real", f"{gasto_pro_real:,.2f} €")
            st.metric("Ahorro Actual", f"{ahorro_real:,.2f} €", delta=f"{cap_ahorro_real:.1%}")

        # COLUMNA DERECHA: ESCENARIO WHAT-IF
        with c2:
            st.markdown("### 🧪 Escenario Simulado")
            
            lista_sim = st.session_state.simulacion
            
            if len(lista_sim) > 0:
                # Convertimos lista a DF para cálculos fáciles
                df_sim = pd.DataFrame(lista_sim)
                
                # Mostramos la "Cesta de Simulación"
                st.caption("Items en este escenario:")
                st.dataframe(df_sim[['Tipo', 'Concepto', 'Importe', 'Frecuencia']], 
                             use_container_width=True, hide_index=True)
                
                # Cálculos del impacto de la simulación
                sim_gastos_extra = df_sim[df_sim['Tipo'] == "Gasto"]['Impacto_Mensual'].sum()
                sim_ingresos_extra = df_sim[df_sim['Tipo'] == "Ingreso"]['Impacto_Mensual'].sum()
                
                # Proyección Combinada
                nuevo_ingreso_total = ingresos_reales + sim_ingresos_extra
                nuevo_gasto_total = gasto_pro_real + sim_gastos_extra
                nuevo_ahorro = nuevo_ingreso_total - nuevo_gasto_total
                nueva_capacidad = (nuevo_ahorro / nuevo_ingreso_total) if nuevo_ingreso_total > 0 else 0
                
                st.markdown("---")
                # Métricas Comparativas
                st.metric("Nuevo Gasto Promedio", f"{nuevo_gasto_total:,.2f} €", 
                          delta=f"+{sim_gastos_extra:,.2f} €", delta_color="inverse")
                
                st.metric("Nuevo Ahorro Potencial", f"{nuevo_ahorro:,.2f} €", 
                          delta=f"{(nueva_capacidad - cap_ahorro_real):.1%}")
                
                # Veredicto
                if nuevo_ahorro < 0:
                    st.error(f"⛔ **PELIGRO:** Este escenario genera un déficit de {nuevo_ahorro:,.2f} €/mes.")
                elif nueva_capacidad < 0.10:
                    st.warning(f"⚠️ **PRECAUCIÓN:** Tu ahorro bajaría al {nueva_capacidad:.1%}. Es arriesgado.")
                elif nueva_capacidad < cap_ahorro_real:
                    st.info(f"📉 **ASUMIBLE:** Reduces ahorro, pero sigues en verde ({nueva_capacidad:.1%}).")
                else:
                    st.success(f"🚀 **MEJORA:** Este escenario mejora tu situación financiera.")
                
                if st.button("🗑️ Limpiar Escenario", type="primary", use_container_width=True):
                    st.session_state.simulacion = []
                    st.rerun()
            else:
                st.info("La cesta de simulación está vacía.")
                st.markdown("""
                **Cómo usar:**
                1. Activa **'Modo Simulación'** en la barra lateral.
                2. Añade varios gastos (ej: Coche + Seguro + Gimnasio).
                3. Mira aquí el impacto total combinado.
                """)

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
