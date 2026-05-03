import os
import io
import base64
import re
import random
from datetime import datetime
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__, static_folder='static')

# --- CONFIGURACIÓN DE ESTILO ---
COLOR_NEGRO = (0, 0, 0)
# --- CODIGO NUEVO (CORREGIDO) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_FUENTES = os.path.join(BASE_DIR, "fuentes")
FUENTE_GENERAL = os.path.join(BASE_DIR, "fuentes", "helvetica.ttf")
FUENTE_BOLD = os.path.join(BASE_DIR, "fuentes", "helvetica-bold.ttf")

# Diccionario Maestro de Configuraciones
CONFIG_TIPOS = {
    "1_propietario": {
        "archivo": "boleta_1.png",
        "campos": {
            "placa": (203, 678, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "tipo_uso": (203, 710, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "categoria": (203, 742, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "carroceria": (203, 774, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "marca": (203, 806, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "modelo": (203, 838, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "año_mod": (203, 870, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "año_fab": (203, 902, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_version": (203, 934, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_serie": (203, 966, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_vin": (203, 998, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_1": (203, 1030, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_2": (203, 1062, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_3": (658, 744, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_motor": (658, 776, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "tipo_combus": (658, 808, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "pot_motor": (658, 840, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_cilindros": (658, 872, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "cilindrada": (658, 904, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "peso_neto": (658, 936, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "peso_bruto": (658, 968, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "carga_util": (658, 1001, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_asientos": (658, 1033, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_pasaj": (658, 1066, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_partida": (1130, 711, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_ejes": (1130, 777, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_ruedas": (1130, 809, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "longitud": (1130, 841, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "ancho": (1130, 873, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "altura": (1130, 906, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "form_rodan": (1130, 938, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "inmatriculac": (1130, 970, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "fec_prop": (1130, 1003, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "oficina": (504, 678, 21, FUENTE_BOLD, COLOR_NEGRO),
            "condicion": (1130, 1035, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_propietario_1": (180, 481, 21, FUENTE_BOLD, COLOR_NEGRO),
            "d_propietario_1": (180, 530, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "dni_1": (1197, 536, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "usuario": (473, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_trans": (678, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "pagado": (898, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "f_sunarp": (1105, 143, 21, FUENTE_GENERAL, COLOR_NEGRO)
        }
    },
    "2_propietarios": {
        "archivo": "boleta_2.png",
        "campos": {
            "placa": (203, 766, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "tipo_uso": (203, 798, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "categoria": (203, 830, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "carroceria": (203, 862, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "marca": (203, 894, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "modelo": (203, 926, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "año_mod": (203, 958, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "año_fab": (203, 990, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_version": (203, 1022, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_serie": (203, 1054, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_vin": (203, 1086, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_1": (203, 1118, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_2": (203, 1150, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_3": (658, 834, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_motor": (658, 864, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "tipo_combus": (658, 896, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "pot_motor": (658, 929, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_cilindros": (658, 961, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "cilindrada": (658, 993, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "peso_neto": (658, 1025, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "peso_bruto": (658, 1057, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "carga_util": (658, 1089, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_asientos": (658, 1121, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_pasaj": (658, 1154, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_partida": (1130, 800, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_ejes": (1130, 865, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_ruedas": (1130, 898, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "longitud": (1130, 930, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "ancho": (1130, 962, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "altura": (1130, 994, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "form_rodan": (1130, 1026, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "inmatriculac": (1130, 1059, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "fec_prop": (1130, 1090, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "oficina": (504, 767, 21, FUENTE_BOLD, COLOR_NEGRO),
            "condicion": (1130, 1123, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_propietario_1": (180, 481, 21, FUENTE_BOLD, COLOR_NEGRO),
            "d_propietario_1": (180, 530, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "dni_1": (1197, 536, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_propietario_2": (180, 576, 21, FUENTE_BOLD, COLOR_NEGRO),
            "d_propietario_2": (180, 624, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "dni_2": (1197, 627, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "usuario": (473, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_trans": (678, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "pagado": (898, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "f_sunarp": (1105, 143, 21, FUENTE_GENERAL, COLOR_NEGRO)
        }
    },
    "empresa": {
        "archivo": "boleta_3.png",
        "campos": {
            "placa": (203, 678, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "tipo_uso": (203, 710, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "categoria": (203, 742, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "carroceria": (203, 774, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "marca": (203, 806, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "modelo": (203, 838, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "año_mod": (203, 870, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "año_fab": (203, 902, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_version": (203, 934, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_serie": (203, 966, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_vin": (203, 998, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_1": (203, 1030, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_2": (203, 1062, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "color_3": (658, 744, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_motor": (658, 776, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "tipo_combus": (658, 808, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "pot_motor": (658, 840, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_cilindros": (658, 872, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "cilindrada": (658, 904, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "peso_neto": (658, 936, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "peso_bruto": (658, 968, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "carga_util": (658, 1001, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_asientos": (658, 1033, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_pasaj": (658, 1066, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_partida": (1130, 711, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_ejes": (1130, 777, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_ruedas": (1130, 809, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "longitud": (1130, 841, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "ancho": (1130, 873, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "altura": (1130, 906, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "form_rodan": (1130, 938, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "inmatriculac": (1130, 970, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "fec_prop": (1130, 1003, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "oficina": (504, 678, 21, FUENTE_BOLD, COLOR_NEGRO),
            "condicion": (1130, 1035, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_juridico_1": (180, 481, 21, FUENTE_BOLD, COLOR_NEGRO),
            "d_juridico_1": (180, 530, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "partida_juridica": (1190, 536, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "usuario": (473, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "n_trans": (678, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "pagado": (898, 362, 21, FUENTE_GENERAL, COLOR_NEGRO),
            "f_sunarp": (1105, 143, 21, FUENTE_GENERAL, COLOR_NEGRO)
        }
    }
}

def generar_documento(texto_input, tipo_boleta):
    # --- NUEVA LÍNEA PARA LIMPIEZA ---
    # Elimina cualquier cosa que esté entre corchetes, incluyendo los corchetes:[cite: 1, 2], etc.
    texto_input = re.sub(r'\[.*?\]', '', texto_input)
    config = CONFIG_TIPOS.get(tipo_boleta, CONFIG_TIPOS["empresa"])
    base_dir = os.path.dirname(__file__)
    # --- CODIGO NUEVO (CORREGIDO) ---
    ruta_fondo = os.path.join(BASE_DIR, "imagenes", config["archivo"])
    
    if not os.path.exists(ruta_fondo):
        return None

    img = Image.open(ruta_fondo).convert("RGB")
    draw = ImageDraw.Draw(img)
    campos_coord = config["campos"]
    valores_imprimir = {}

    lineas = texto_input.split('\n')
    for linea in lineas:
        if ":" in linea:
            partes = linea.split(':', 1)
            etiqueta = partes[0].strip().lower()
            valor_original = partes[1].strip()

            if etiqueta == "tipo_uso":
                # Si no hay paréntesis, aplicamos el formato especial
                if "(" not in valor_original:
                    # Dividimos por guiones para capitalizar después de cada uno
                    partes_guion = valor_original.split('-')
                    resultado_partes = []
                    
                    for parte in partes_guion:
                        parte = parte.strip()
                        if parte:
                            # Primera letra mayúscula, demás minúsculas para cada segmento
                            formateado = parte[0].upper() + parte[1:].lower()
                            resultado_partes.append(formateado)
                    
                    # Unimos con el guion y espacios correspondientes
                    valores_imprimir[etiqueta] = "-".join(resultado_partes)
                else:
                    # Si hay paréntesis, mantenemos tu lógica actual de conectores o mayúsculas
                    conectores = ["y", "en", "de", "con", "o"]
                    palabras = valor_original.split()
                    resultado = []
                    for p in palabras:
                        if any(char.isdigit() for char in p):
                            resultado.append(p.upper())
                        else:
                            p_limpia = re.sub(r'[^\wáéíóúñÁÉÍÓÚÑ]', '', p).lower()
                            if p_limpia in conectores:
                                resultado.append(p.lower())
                            else:
                                p_formateada = re.sub(r'[a-zA-ZáéíóúñÁÉÍÓÚÑ]+', lambda m: m.group(0).capitalize(), p.lower())
                                resultado.append(p_formateada)
                    valores_imprimir[etiqueta] = " ".join(resultado)
            elif etiqueta in ["peso_neto", "peso_bruto", "carga_util", "longitud", "ancho", "altura"]:
                valores_imprimir[etiqueta] = valor_original.lower()
            else:
                valores_imprimir[etiqueta] = valor_original.upper()

    for etiqueta, valor in valores_imprimir.items():
        if etiqueta in campos_coord and valor != "":
            x, y, tam, fuente_path, color = campos_coord[etiqueta]
            try:
                fuente = ImageFont.truetype(fuente_path, tam)
                draw.text((x, y), valor, font=fuente, fill=color)
            except:
                draw.text((x, y), valor, fill=color)
    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    imagen_base64, texto_final, tipo_previo = None, "", "empresa"
    oficina_previa = "" # Variable nueva
    
    if request.method == 'POST':
        texto_recibido = request.form.get('texto_datos', '')
        oficina_previa = request.form.get('oficina_valor', '') # Capturamos la oficina

        # Detección automática del tipo de boleta basada en el texto
        if "n_juridico_1:" in texto_recibido:
            tipo_previo = "empresa"
        elif "n_propietario_2:" in texto_recibido:
            tipo_previo = "2_propietarios"
        elif "n_propietario_1:" in texto_recibido:
            tipo_previo = "1_propietario"
        else:
            tipo_previo = request.form.get('tipo_boleta', 'empresa')

        # --- LÓGICA DE ACTUALIZACIÓN EN CADA CLIC ---
        n_trans_nuevo = "25" + "".join([str(random.randint(0, 9)) for _ in range(7)])
        fecha_nueva = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # 1. Reemplazar o añadir N_TRANS
        if re.search(r'(?i)n_trans:.*', texto_recibido):
            texto_recibido = re.sub(r'(?i)n_trans:.*', f'n_trans: {n_trans_nuevo}', texto_recibido)
        else:
            texto_recibido += f"\nn_trans: {n_trans_nuevo}"
            
        # 2. Reemplazar o añadir FECHA
        if re.search(r'(?i)f_sunarp:.*', texto_recibido):
            texto_recibido = re.sub(r'(?i)f_sunarp:.*', f'f_sunarp: {fecha_nueva}', texto_recibido)
        else:
            texto_recibido += f"\nf_sunarp: {fecha_nueva}"

        # 3. Asegurar Usuario y Pagado (si no están)
        if not re.search(r'(?i)usuario:.*', texto_recibido):
            texto_recibido += "\nusuario: MANNY132"
        if not re.search(r'(?i)pagado:.*', texto_recibido):
            texto_recibido += "\npagado: 6.60"

        texto_final = texto_recibido.strip()
        img = generar_documento(texto_final, tipo_previo)
        
        if img:
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=95)
            imagen_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
    return render_template('index.html', imagen_preview=imagen_base64, texto=texto_final, tipo_boleta=tipo_previo,oficina_seleccionada=oficina_previa)

@app.route('/descargar', methods=['POST'])
def descargar():
    texto = request.form.get('texto_datos', '')
    tipo = request.form.get('tipo_boleta', 'empresa')
    match_placa = re.search(r'placa:\s*([^\n\r]*)', texto, re.IGNORECASE)
    placa_valor = match_placa.group(1).strip().upper() if match_placa else "BOLETA"
    img = generar_documento(texto, tipo)
    if img:
        img_io = io.BytesIO()
        img.save(img_io, 'PDF', resolution=300.0)
        img_io.seek(0)
        return send_file(img_io, mimetype='application/pdf', as_attachment=True, download_name=f"BOLETA_{placa_valor}.pdf")
    return "Error", 400

if __name__ == '__main__':
    app.run(debug=True)
