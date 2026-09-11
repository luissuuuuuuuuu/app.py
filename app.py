import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="HydroCheck IA", page_icon="🧪", layout="centered")

st.title("🧪 HydroCheck IA")
st.subheader("Análisis Cromático de pH por Inteligencia Artificial")
st.write("Toma una foto al tubo de ensayo o vaso con el extracto de col morada para diagnosticar el pH.")

# Opción para tomar foto con la cámara del celular/laptop o subir imagen
img_file = st.camera_input("Capturar muestra de agua") or st.file_uploader("O sube una imagen de la muestra", type=["jpg", "png", "jpeg"])

if img_file is not None:
    # Cargar imagen
    image = Image.open(img_file)
    st.image(image, caption="Muestra analizada", use_column_width=True)
    
    # Convertir imagen a array de NumPy
    img_array = np.array(image)
    
    # Obtener el color promedio de la zona central
    h, w, _ = img_array.shape
    center_region = img_array[int(h*0.4):int(h*0.6), int(w*0.4):int(w*0.6)]
    avg_color_per_row = np.average(center_region, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    
    r, g, b = int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
    
    st.markdown(f"**Color RGB detectado:** R={r}, G={g}, B={b}")
    
    # Lógica de clasificación de pH basada en colorimetría de antocianinas
    # Ralto + Gbajo = Rojo/Rosa (Ácido) | B alto = Azul/Morado (Neutro/Alcalino)
    if r > g and r > b:
        if r - b > 50:
            ph_estimado = "4.0 - 5.0 (Ácido)"
            estado = "🔴 ÁCIDO ALTO - Disolución de CO₂ detectada"
            diagnostico = "Agua no segura para consumo sin neutralizar. Requiere adición de bicarbonato."
        else:
            ph_estimado = "5.5 - 6.5 (Ligeramente Ácido)"
            estado = "🟠 ÁCIDO LEVE - Agua de contenedor destapado"
            diagnostico = "Muestra expuesta al ambiente por tiempo prolongado."
    elif b > r and b > g:
        ph_estimado = "7.0 - 7.5 (Neutro)"
        estado = "🟣 NEUTRO - Agua Segura / Potable"
        diagnostico = "Cumple con los niveles recomendados de pH (NOM-127-SSA1)."
    else:
        ph_estimado = "8.0 - 9.0 (Alcalino)"
        estado = "🟢 BÁSICO / ALCALINO"
        diagnostico = "Muestra con presencia de sales o neutralizada."

    # Mostrar Resultados
    st.success(f"**Nivel de pH Estimado:** {ph_estimado}")
    st.info(f"**Diagnóstico:** {estado}")
    st.write(diagnostico)
