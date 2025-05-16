# --- CÓDIGO PARA dashboard_tarea_grupo_X.py ---
# (Este bloque NO se ejecuta directamente en Jupyter)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Supermarket Sales", layout="wide")

# --- Cargar datos ---
@st.cache_data
def cargar_datos():
    df = pd.read_csv("data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = cargar_datos()

# --- Título ---
st.title("📊 Dashboard Interactivo - Supermarket Sales")

# --- Filtros ---
st.sidebar.header("Filtros")
branch = st.sidebar.multiselect("Sucursal", options=df["Branch"].unique(), default=df["Branch"].unique())
product_lines = st.sidebar.multiselect("Línea de producto", options=df["Product line"].unique(), default=df["Product line"].unique())

df_filtrado = df[df["Branch"].isin(branch) & df["Product line"].isin(product_lines)]

# --- Evolución de Ventas Totales ---
st.subheader("🗓️ Evolución de Ventas Totales")
ventas_diarias = df_filtrado.groupby("Date")["Total"].sum().reset_index()
fig1, ax1 = plt.subplots()
sns.lineplot(data=ventas_diarias, x="Date", y="Total", ax=ax1)
ax1.set_title("Ventas Totales por Fecha")
ax1.set_ylabel("Total ($)")
st.pyplot(fig1)

# --- Ingresos por Línea de Producto ---
st.subheader("📦 Ingresos por Línea de Producto")
ingresos_product_line = df_filtrado.groupby("Product line")["Total"].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots()
sns.barplot(x=ingresos_product_line.values, y=ingresos_product_line.index, ax=ax2)
ax2.set_xlabel("Total ($)")
ax2.set_title("Ingresos por Línea de Producto")
st.pyplot(fig2)

# --- Distribución de Calificación de Clientes ---
st.subheader("⭐ Distribución de Calificación de Clientes")
fig3, ax3 = plt.subplots()
sns.histplot(df_filtrado["Rating"], bins=20, kde=True, ax=ax3)
ax3.set_title("Distribución de Ratings de Clientes")
ax3.set_xlabel("Rating")
st.pyplot(fig3)

# --- Gasto por Tipo de Cliente ---
st.subheader("👥 Comparación de Gasto por Tipo de Cliente")
fig4, ax4 = plt.subplots()
sns.boxplot(data=df_filtrado, x="Customer type", y="Total", ax=ax4)
ax4.set_title("Distribución del Gasto Total por Tipo de Cliente")
ax4.set_ylabel("Total ($)")
st.pyplot(fig4)

# --- Relación entre Costo y Ganancia Bruta ---
st.subheader("💰 Relación entre Costo (cogs) y Ganancia Bruta (gross income)")
fig5, ax5 = plt.subplots()
sns.scatterplot(data=df_filtrado, x="cogs", y="gross income", hue="Branch", ax=ax5)
ax5.set_title("Relación entre Costo y Ganancia Bruta")
st.pyplot(fig5)

# --- Métodos de Pago Preferidos ---
st.subheader("💳 Métodos de Pago Preferidos")
metodos_pago = df_filtrado["Payment"].value_counts()
fig6, ax6 = plt.subplots()
metodos_pago.plot.pie(autopct='%1.1f%%', ax=ax6)
ax6.set_ylabel("")
ax6.set_title("Distribución de Métodos de Pago")
st.pyplot(fig6)

# --- Análisis de Correlación Numérica ---
st.subheader("📈 Correlación entre Variables Numéricas")
variables = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]
correlacion = df_filtrado[variables].corr()
fig7, ax7 = plt.subplots()
sns.heatmap(correlacion, annot=True, cmap="coolwarm", fmt=".2f", ax=ax7)
ax7.set_title("Matriz de Correlación")
st.pyplot(fig7)

# --- Ingreso Bruto por Sucursal y Línea de Producto ---
st.subheader("🏬 Composición del Ingreso Bruto por Sucursal y Línea de Producto")
pivot = df_filtrado.pivot_table(values="gross income", index="Product line", columns="Branch", aggfunc="sum", fill_value=0)
fig8, ax8 = plt.subplots()
pivot.plot(kind="bar", stacked=True, ax=ax8)
ax8.set_title("Ingreso Bruto por Línea de Producto y Sucursal")
ax8.set_ylabel("Gross Income ($)")
st.pyplot(fig8)

# --- Reflexión Final ---
st.markdown("---")
st.markdown("✅ **Reflexión:** La interactividad del dashboard permite filtrar por sucursal y producto para explorar patrones de comportamiento y ventas. Esto facilita identificar qué líneas de producto son más rentables, cómo se distribuyen las calificaciones de los clientes y qué métodos de pago son más utilizados, lo que es clave para decisiones de marketing y operación.")
