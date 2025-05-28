import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# ============================
# ENTRADA SEGURA DE API KEY
# ============================
st.title("🤖 Chatbot sobre Base de datos de desplazamiento de personas")
api_key = st.text_input("🔑 Ingresa tu OpenAI API Key:", type="password")

if not api_key:
    st.warning("Por favor ingresa tu clave de API para continuar.")
    st.stop()

# Configura el cliente con la API Key ingresada
os.environ['OPENAI_API_KEY'] = api_key
client = OpenAI()

# ====================
# CARGA DEL ARCHIVO
# ====================
st.subheader("📊 Tabla de Datos")

xlsx_path = "df_final.xlsx"
try:
    df = pd.read_excel(xlsx_path).head(100)  # Limita a 100 filas para evitar exceso de tokens
    st.dataframe(df)
except FileNotFoundError:
    st.error(f"No se encontró el archivo Excel en la ruta: {xlsx_path}")
    st.stop()
except Exception as e:
    st.error(f"Ocurrió un error al cargar el archivo: {e}")
    st.stop()

# ==========================
# CHAT CON LA TABLA
# ==========================
st.subheader("💬 Pregúntale algo a la tabla")
user_question = st.chat_input("Haz una pregunta sobre la tabla...")

if user_question:
    # Convertimos el DataFrame en texto para el modelo
    df_string = df.to_csv(index=False, sep='|')

    # Instrucciones para el modelo
    system_prompt = (
        "Eres un asistente experto en análisis de datos. Solo puedes responder preguntas "
        "basándote en la siguiente tabla de datos (formato delimitado por '|'). "
        "Si la pregunta no está relacionada con la tabla, responde educadamente que no puedes responderla."
        "\n\n"
        "Datos:\n" + df_string
    )

    try:
        with st.spinner("Pensando..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content
            st.chat_message("assistant").write(answer)
    except Exception as e:
        st.error(f"Ocurrió un error al contactar con la API: {e}")