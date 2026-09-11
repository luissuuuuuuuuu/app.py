import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="HydroCheck IA", page_icon="🧪", layout="centered")

st.title("🧪 HydroCheck IA")
st.subheader("Análisis Cromático de pH por Inteligencia Artificial")
st.write("Captura una foto al tubo de ensayo con extracto de col morada para diagnosticar el pH y la presencia de CO₂.")

# Entrada de imagen mediante cámara o archivo
img_file = st.camera_input("Capturar muestra de agua") or st.file_uploader("O sube una imagen de la muestra", type=["jpg", "png", "jpeg"])

if img_file is not None:
    image = Image.open(img_file)
    st.image(image, caption="Muestra analizada", use_container_width=True)
    
    img_array = np.array(image)
    h, w, _ = img_array.shape
    
    # Análisis cromático central de la imagen
    center_region = img_array[int(h*0.4):int(h*0.6), int(w*0.4):int(w*0.6)]
    avg_color = np.average(np.average(center_region, axis=0), axis=0)
    
    r, g, b = int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
    st.markdown(f"**Matriz Cromática Detectada (RGB):** R={r}, G={g}, B={b}")
    
    # Lógica de diagnóstico según el espectro de color de las antocianinas
    if r > g and r > b:
        if r - b > 40:
            ph_estimado = "4.0 - 5.0 (Ácido)"
            estado = "🔴 ÁCIDO ALTO - Disolución de CO₂ detectada"
            diagnostico = "Muestra saturada con CO₂. Requiere neutralización con Bicarbonato de Sodio (NaHCO₃)."
        else:
            ph_estimado = "5.5 - 6.5 (Ligeramente Ácido)"
            estado = "🟠 ÁCIDO LEVE - Agua de contenedor destapado"
            diagnostico = "Muestra con acidificación por exposición prolongada al aire ambiental."
    elif b > r and b > g:
        ph_estimado = "7.0 - 7.5 (Neutro)"
        estado = "🟣 NEUTRO - Agua Potable / Segura"
        diagnostico = "El nivel de pH cumple con los límites de la norma sanitaria (NOM-127-SSA1)."
    else:
        ph_estimado = "8.0 - 9.0 (Alcalino)"
        estado = "🟢 BÁSICO / ALCALINO"
        diagnostico = "Muestra con presencia de sales o proceso de neutralización completado."

    st.success(f"**Nivel de pH Estimado:** {ph_estimado}")
    st.info(f"**Diagnóstico:** {estado}")
    st.write(diagnostico)
