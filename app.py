import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Finanzas Proactivas €", layout="wide", page_icon="💶")

# --- LÓGICA DE DATOS (BACKEND) ---
FILE_NAME = "finanzas.csv"
COLUMNS = ["Fecha", "Tipo", "Categoría", "Concepto", "Importe", "Frecuencia", "Impacto_Mensual"]

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_csv(FILE_NAME)
            # errors='coerce' evita que la app se rompa si hay fechas con formato antiguo
            df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
            # Limpiamos filas que no tengan fecha válida tras la conversión
            df = df.dropna(subset=['Fecha'])
            return df
        except Exception:
            return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(columns=COLUMNS)

def save_all_data(df):
    """Guarda el DataFrame completo asegurando el formato de fecha europeo."""
    df_to_save = df.copy()
    df_to_save['Fecha'] = df_to_save['Fecha'].dt.strftime("%d/%m/%Y")
    df_to_save.to_csv(FILE_NAME, index=False)

def calculate_impact(importe, frecuencia):
    """Calcula el coste prorrateado mensual."""
    return importe / 12 if frecuencia == "Anual" else importe

# --- CARGA DE DATOS ---
df = load_data()

# --- SIDEBAR: REGISTRO ---
st.sidebar.header("📥 Registrar Transacción")

with st.sidebar.form("transaccion_form", clear_on_submit=True):
    # Por defecto 'Gasto' (index=1)
    tipo = st.radio("Tipo", ["Ingreso", "Gasto"], index=1, horizontal=True)
    fecha = st.date_input("Fecha", datetime.now())
    categoria = st.selectbox("Categoría", 
                             ["Vivienda", "Transporte", "Comida", "Seguros", "Ahorro", "Ingresos", "Otros"])
    concepto = st.text_input("Concepto", placeholder="Ej: Supermercado, Nómina...")
    importe = st.number_input("Importe (€)", min_value=0.0, step=10.0)
    frecuencia = st.selectbox("Frecuencia", ["Mensual", "Anual", "Puntual"])
    
    submit = st.form_submit_button("Guardar Transacción")
    
    if submit:
        if importe > 0 and concepto:
            impacto = calculate_impact(importe, frecuencia)
            # Creamos la nueva fila asegurando que la fecha es datetime
            new_row = pd.DataFrame([[pd.to_datetime(fecha), tipo, categoria, concepto, importe, frecuencia, impacto]], 
                                   columns=COLUMNS)
            df = pd.concat([df, new_row], ignore_index=True)
            save_all_data(df)
            st.sidebar.success("¡Transacción guardada!")
            st.rerun()
        else:
            st.sidebar.warning("Faltan datos por rellenar.")

# --- PANEL PRINCIPAL ---
st.title("🚀 Gestión de Finanzas Personales (€)")

if df.empty:
    st.info("No hay datos registrados aún. Utiliza el panel lateral para empezar.")
else:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Historial", "🤖 Asesor Proactivo", "⚙️ Gestionar Datos"])

    # Cálculos globales
    month_now, year_now = datetime.now().month, datetime.now().year
    df_mes = df[(df['Fecha'].dt.month == month_now) & (df['Fecha'].dt.year == year_now)]
    
    ingresos_mes = df_mes[df_mes['Tipo'] == "Ingreso"]['Importe'].sum()
    gastos_reales_mes = df_mes[df_mes['Tipo'] == "Gasto"]['Importe'].sum()
    
    # Prorrateo basado en el impacto mensual de todos los registros
    num_meses_total = max(len(df['Fecha'].dt.to_period('M').unique()), 1)
    gasto_total_impacto = df[df['Tipo'] == "Gasto"]['Impacto_Mensual'].sum()
    gasto_prorrateado_medio = gasto_total_impacto / num_meses_total

    with tab1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Ingresos (Mes Actual)", f"{ingresos_mes:,.2f} €")
        c2.metric("Salida Caja (Mes Actual)", f"{gastos_reales_mes:,.2f} €")
        c3.metric("Gasto Real Prorrateado", f"{gasto_prorrateado_medio:,.2f} €", 
                  help="Suma de gastos mensuales + (gastos anuales / 12)")

        # Gráfico de barras apiladas
        df_ev = df.groupby([df['Fecha'].dt.to_period('M'), 'Tipo'])['Importe'].sum().reset_index()
        df_ev['Fecha'] = df_ev['Fecha'].astype(str)
        fig_evolucion = px.bar(df_ev, x='Fecha', y='Importe', color='Tipo', barmode='group',
                               title="Comparativa Mensual Ingresos vs Gastos",
                               labels={'Importe': 'Euros (€)', 'Fecha': 'Mes'},
                               color_discrete_map={'Ingreso': '#00CC96', 'Gasto': '#EF553B'})
        st.plotly_chart(fig_evolucion, use_container_width=True)

    with tab2:
        st.subheader("Historial Completo")
        df_historial = df.sort_values(by="Fecha", ascending=False).copy()
        df_historial['Fecha'] = df_historial['Fecha'].dt.strftime('%d/%m/%Y')
        df_historial['Importe'] = df_historial['Importe'].map('{:,.2f} €'.format)
        st.dataframe(df_historial, use_container_width=True)

    with tab3:
        st.subheader("Análisis de Salud Financiera")
        if ingresos_mes > 0:
            ahorro_real = ingresos_mes - gasto_prorrateado_medio
            pct_ahorro = (ahorro_real / ingresos_mes)
            
            if pct_ahorro < 0.10:
                st.error(f"⚠️ **Atención:** Tu ahorro real ({pct_ahorro:.1%}) está por debajo del 10% de tus ingresos.")
            else:
                st.success(f"✅ **¡Muy bien!** Tu ahorro real es del {pct_ahorro:.1%} ({ahorro_real:,.2f} €).")
            
            proyeccion_anual = gasto_prorrateado_medio * 12
            st.info(f"📅 **Proyección:** Al ritmo actual, gastarás **{proyeccion_anual:,.2f} €** al año.")
        else:
            st.warning("Registra ingresos este mes para activar el asesoramiento.")

    with tab4:
        st.subheader("Editar o Eliminar Movimientos")
        st.write("Selecciona el número de índice de la izquierda para realizar cambios.")
        
        # Mostramos el DF crudo para ver los índices
        st.dataframe(df)
        
        idx = st.number_input("Índice de la fila:", min_value=0, max_value=len(df)-1, step=1)
        
        if len(df) > 0:
            row = df.iloc[idx]
            with st.expander(f"Modificar: {row['Concepto']} ({row['Importe']} €)"):
                e_tipo = st.radio("Tipo", ["Ingreso", "Gasto"], index=0 if row['Tipo']=="Ingreso" else 1)
                e_fecha = st.date_input("Fecha", row['Fecha'])
                e_cat = st.selectbox("Categoría", ["Vivienda", "Transporte", "Comida", "Seguros", "Ahorro", "Ingresos", "Otros"], 
                                    index=["Vivienda", "Transporte", "Comida", "Seguros", "Ahorro", "Ingresos", "Otros"].index(row['Categoría']))
                e_con = st.text_input("Concepto", row['Concepto'])
                e_imp = st.number_input("Importe (€)", value=float(row['Importe']))
                e_fre = st.selectbox("Frecuencia", ["Mensual", "Anual", "Puntual"], 
                                    index=["Mensual", "Anual", "Puntual"].index(row['Frecuencia']))
                
                c_btn1, c_btn2 = st.columns(2)
                
                if c_btn1.button("Guardar Cambios"):
                    df.at[idx, 'Tipo'] = e_tipo
                    df.at[idx, 'Fecha'] = pd.to_datetime(e_fecha)
                    df.at[idx, 'Categoría'] = e_cat
                    df.at[idx, 'Concepto'] = e_con
                    df.at[idx, 'Importe'] = e_imp
                    df.at[idx, 'Frecuencia'] = e_fre
                    df.at[idx, 'Impacto_Mensual'] = calculate_impact(e_imp, e_fre)
                    save_all_data(df)
                    st.success("Registro actualizado correctamente.")
                    st.rerun()
                
                if c_btn2.button("Eliminar permanentemente", type="primary"):
                    df = df.drop(df.index[idx])
                    save_all_data(df)
                    st.warning("Registro eliminado.")
                    st.rerun()

# --- RECOMENDACIÓN FINAL ---
# Si el error persiste, borra el archivo finanzas.csv manualmente una vez.
