import pandas as pd
import streamlit as st
import requests
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import feedparser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import lxml

st.set_page_config(page_title="AgroAppCredicoop",page_icon="🌱",layout="wide") 

arrenda = 0

#OCULTAR FUENTE GITHUB
hide_github_link = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_github_link, unsafe_allow_html=True)

#PARA ABRIR GOOGLEMAPS
def abrir_google_maps():
    # Coordenadas de ejemplo (puedes cambiarlas por las que necesites)
    latitud = -34.62125
    longitud = -58.42810
    url_maps = f"https://www.google.com/maps?q={latitud},{longitud}"

    # Enlace a Google Maps
    st.write(f"[Google Maps]({url_maps})")

#BOTON PARA BAJAR PDF
@st.cache_data
def load_unpkg(src: str) -> str:
    return requests.get(src).text

HTML_2_CANVAS = load_unpkg("https://unpkg.com/html2canvas@1.4.1/dist/html2canvas.js")
JSPDF = load_unpkg("https://unpkg.com/jspdf@latest/dist/jspdf.umd.min.js")
BUTTON_TEXT = "Create PDF"

    
def css():
    # CSS to inject contained in a string
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

#LOTTIE
#def load_lottieurl(url: str):
#    r = requests.get(url)
#    if r.status_code != 200:
#        return None
#    return r.json()

#VALORES DE MANTENIMIENTO
valorminc = 21000 #valor minimo cosecha
valormaxc = 34000 #valor maximo cosecha
valors = 18700 #valor referencia siembra

#CARGA RINDES HISTÓRICOS
url = "https://raw.githubusercontent.com/Jthl1986/T1/main/Estimaciones.csv"
dfr = pd.read_csv(url, encoding='ISO-8859-1', sep=';')


# VALUACION HACIENDA
def app():
    st.title("🐮 Valuación de hacienda")
    left, right = st.columns(2)
    left.write("Completar:")
    form = left.form("template_form")
    tipo = form.selectbox('Ingrese tipo de hacienda: ', ["Ternero             ", "Novillito       ", "Ternera             ", "Vaquillona        ", "Vaca                "])
    cantidad = form.number_input("Ingrese cantidad de cabezas: ", step=1)
    peso = form.number_input("Ingrese peso: ", step=1)
    submit = form.form_submit_button("Ingresar")
    df=pd.read_html('https://www.monasterio-tattersall.com/precios-hacienda') #leo la tabla de la página
    hacienda = df[0] 
    categoria = hacienda.Categoría 
    promedio = hacienda.Promedio
    tabla = pd.DataFrame({'categoria':categoria,'promedio':promedio}) #creo un dataframe con categoria y promedio
    ternero=tabla[0:5] 
    novillito=tabla[5:7]
    ternera=tabla[7:11]
    vaquillona=tabla[11:14]
    vaca=tabla[22:23]  
    fecha=(tabla[25:26].values)[0][0] #el predeterminado es 25:26
    ternero160=int(ternero.promedio[0][2:6])
    ternero180=int(ternero.promedio[1][2:6])
    ternero200=int(ternero.promedio[2][2:6])
    ternero230=int(ternero.promedio[3][2:6])
    novillo260=int(novillito.promedio[5][2:6])
    novillo300=int(novillito.promedio[6][2:6])
    ternera150=int(ternera.promedio[7][2:6])
    ternera170=int(ternera.promedio[8][2:6])
    ternera190=int(ternera.promedio[9][2:6])
    ternera210=int(ternera.promedio[10][2:6])
    vaquillona250=int(vaquillona.promedio[11][2:6])
    vaquillona290=int(vaquillona.promedio[12][2:6])
    vaquillona291=int(vaquillona.promedio[13][2:6])
    vacas=int(vaca.promedio[22][2:8])
    def constructor():
        def valores():
            if tipo == 'Ternero             ' and peso < 160:
                valor = ternero160*cantidad*peso
            elif tipo == 'Ternero             ' and peso < 180:
                valor = ternero180*cantidad*peso
            elif tipo == 'Ternero             ' and peso <= 200:
                valor = ternero200*cantidad*peso
            elif tipo == 'Ternero             ' and peso > 200:
                valor = ternero230*cantidad*peso
            elif tipo == 'Ternero             ' and peso == 0:
                valor = ternero200*cantidad*peso
            elif tipo == 'Novillito       ' and peso < 260:
                valor = novillo260*cantidad*peso
            elif tipo == 'Novillito       ' and peso <= 300:
                valor = novillo300*cantidad*peso
            elif tipo == 'Novillito       ' and peso > 300:
                valor = novillo300*cantidad*peso
            elif tipo == 'Novillito       ' and peso == 0:
                valor = novillo300*cantidad*peso
            elif tipo == 'Ternera             ' and peso < 150:
                valor = ternera150*cantidad*peso
            elif tipo == 'Ternera             ' and peso < 170:
                valor = ternera170*cantidad*peso
            elif tipo == 'Ternera             ' and peso <= 190:
                valor = ternera190*cantidad*peso
            elif tipo == 'Ternera             ' and peso > 190:
                valor = ternera210*cantidad*peso
            elif tipo == 'Ternera             ' and peso == 0:
                valor = ternera190*cantidad*peso
            elif tipo == 'Vaquillona        ' and peso < 250:
                valor = vaquillona250*cantidad*peso
            elif tipo == 'Vaquillona        ' and peso <= 290:
                valor = vaquillona290*cantidad*peso
            elif tipo == 'Vaquillona        ' and peso > 290:
                valor = vaquillona291*cantidad*peso
            elif tipo == 'Vaquillona        ' and peso == 0:
                valor = vaquillona290*cantidad*peso
            elif tipo == 'Vaca                ':
                valor = vacas*cantidad
            valor = int(valor*0.9) #ESTAMOS CASTIGANDO 10% EL VALOR DE ESTIMACIÓN
            return valor #valor de ajuste
        valor=valores()
        d = [tipo, cantidad, peso, valor]
        return d
    metalista=[]
    if "dfa" not in st.session_state:
        st.session_state.dfa = pd.DataFrame(columns=("Categoría", "Cantidad", "Peso", "Valuación"))
    if submit:
        metalista.append(constructor())
        dfb = pd.DataFrame(metalista, columns=("Categoría", "Cantidad", "Peso", "Valuación"))
        st.session_state.dfa = pd.concat([st.session_state.dfa, dfb])
    css()
    valuacion_total = st.session_state.dfa['Valuación'].sum()
    right.metric('La valuación total de hacienda es: ', '${:,}'.format(valuacion_total))

    del_button = right.button("Borrar última fila")
    if del_button and len(st.session_state.dfa) > 0:
        st.session_state.dfa = st.session_state.dfa.iloc[:-1]

    right.write("Tabla para copiar:")
    right.table(st.session_state.dfa.style.format({"Cantidad":"{:.0f}", "Peso":"{:.0f}", "Valuación":"${:,}","RindeProm":"{:.2f}"}))
    right.write(f'Los precios considerados son de la {fecha}')
    promedios = pd.DataFrame(
        {'Categoria': ['Ternero', 'Novillo', 'Ternera', 'Vaquillonas'],
         'Peso': ['180', '260', '170','250']})
    st.write('Pesos promedio para tipo de hacienda (en caso que no se informe el peso). En vacas poner peso cero')
    st.table(promedios.assign(hack='').set_index('hack'))

#COTIZACIONES GRANOS
# URL de la página web que contiene los datos
url = "https://www.ggsa.com.ar/get_pizarra/"

# Realizar la solicitud HTTP para obtener el contenido JSON
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
response = requests.get(url, verify=False)

# Verificar si la solicitud fue exitosa (código 200)
if response.status_code == 200:
    # Obtener el contenido JSON de la respuesta
    data = response.json()

    # Extraer los valores para Rosario y los nombres de los cultivos
    pizarra_data = data["pizarra"][0]
    cultivos = ["trigo", "soja", "maiz", "girasol", "sorgo"]
    valores_rosario = {}

    # Verificar si el valor de Rosario es "0.00" y usar el valor estimativo en su lugar
    for cultivo in cultivos:
        valor_rosario = pizarra_data[cultivo]["rosario"]
        valor_estimativo = pizarra_data[cultivo]["estimativo"]

        if valor_rosario == "0.00":
            valores_rosario["pp" + cultivo] = float(valor_estimativo)
        else:
            valores_rosario["pp" + cultivo] = float(valor_rosario)

    # Extraer la fecha
    fecha1 = pizarra_data["fecha"]

    # Asignar los valores a las variables con los nombres personalizados
    pptrigo = valores_rosario["pptrigo"]
    ppsoja = valores_rosario["ppsoja"]
    ppmaiz = valores_rosario["ppmaiz"]
    ppgirasol = valores_rosario["ppgirasol"]
    ppsorgo = valores_rosario["ppsorgo"]


def app1():
    fecha = fecha1
    st.title("🌾 Valuación de granos")
    st.write(f'Precios de pizarra del Mercado de Rosario al {fecha}')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Soja", '${:,}'.format(int(ppsoja)))
    col2.metric("Trigo", '${:,}'.format(int(pptrigo)))
    col3.metric("Maíz", '${:,}'.format(int(ppmaiz)))
    col4.metric("Sorgo", '${:,}'.format(int(ppsorgo)))
    col5.metric("Girasol",'${:,}'.format(int(ppgirasol)))
    left, right = st.columns(2)
    left.write("Completar:")
    form = left.form("template_form")
    tipo = form.selectbox('Ingrese tipo de grano: ', ["Soja","Trigo","Maíz","Sorgo","Girasol"])
    cantidad = form.number_input("Ingrese toneladas: ", step=1)
    submit = form.form_submit_button("Ingresar")
    def lista():
        def valor():
            if tipo == "Soja":
                precio = ppsoja
            elif tipo == "Trigo":
                precio = pptrigo
            elif tipo == "Maíz":
                precio = ppmaiz
            elif tipo == "Sorgo":
                precio = ppsorgo
            else:
                precio = ppgirasol
            return int(cantidad*precio)
        valor = valor()
        lista = [tipo, cantidad, valor]
        return lista
    cereales=[]
    if "dfs" not in st.session_state:
        st.session_state.dfs = pd.DataFrame(columns=("Tipo grano", "Cantidad (tn)", "Valuación"))
    if submit:
        cereales.append(lista())
        dfd = pd.DataFrame(cereales, columns=("Tipo grano", "Cantidad (tn)", "Valuación"))
        st.session_state.dfs = pd.concat([st.session_state.dfs, dfd])
    css()
    valuacion_total = st.session_state.dfs['Valuación'].sum()
    right.metric('La valuación total de granos es: ', '${:,}'.format(valuacion_total))
    del_button = right.button("Borrar última fila")
    if del_button and len(st.session_state.dfs) > 0:
        st.session_state.dfs = st.session_state.dfs.iloc[:-1]
    right.write("Tabla para copiar:")
    right.table(st.session_state.dfs.style.format({"Cantidad (tn)":"{:.0f}", "Valuación":"${:,}"}))

def app2():
    if "ingresos_totales" not in st.session_state:
        st.session_state["ingresos_totales"] = 0
    st.title("🚜 Servicios agrícolas")
    left, right = st.columns(2)
    left.write("Completar:")
    form = left.form("template_form")
    tipo = form.selectbox('Ingrese tipo de servicio: ', ["Cosecha","Siembra","Pulverización","Laboreos"])
    valormins = valors*0.50 #valor minimo siembra
    valormaxs = valors*1.50 #valor maximo siembra
    cantidad = form.number_input("Ingrese superficie (has): ", step=1)
    precio = form.number_input("Ingrese precio por ha", step=1)
    submit = form.form_submit_button("Ingresar")
    
    def lista():
        def valor():
            return cantidad*precio
        valor = valor()
        lista = [tipo, cantidad, precio, valor]
        return lista
    servagro=[]
    if "dfx" not in st.session_state:
        st.session_state.dfx = pd.DataFrame(columns=("Categoría", "Superficie(ha)", "Precio", "Ingreso estimado"))
    if submit:
        servagro.append(lista())
        st.session_state["ingresos_totales"] += cantidad*precio
        dfy = pd.DataFrame(servagro, columns=("Categoría", "Superficie(ha)", "Precio", "Ingreso estimado"))
        st.session_state.dfx = pd.concat([st.session_state.dfx, dfy])
        if tipo == 'Cosecha' and (precio > valormaxc or precio < valorminc):
            st.warning("ALERTA! El precio por ha de cosecha cargado esta fuera de los promedios de mercado. Ver precios de referencia abajo")
        elif tipo == 'Siembra' and (precio > valormaxs or precio < valormins):
            st.warning("ALERTA! El precio por ha de siembra cargado esta fuera de los promedios de mercado. Ver precios de referencia abajo")
        else:
            pass
    
    right.metric('Los ingresos totales por servicios agrícolas son: ', "${:,}".format(st.session_state["ingresos_totales"]))    

    delete_last_row = right.button("Borrar última fila")
    if delete_last_row:
        if not st.session_state.dfx.empty:
            st.session_state["ingresos_totales"] -= st.session_state.dfx["Ingreso estimado"].iloc[-1]
            st.session_state.dfx = st.session_state.dfx.iloc[:-1]
    css()
    
    right.write("Tabla para copiar:")
    right.table(st.session_state.dfx.style.format({"Superficie(ha)":"{:.0f}", "Precio":"${:,}", "Ingreso estimado":"${:,}"}))
    
    facmalink = "http://www.facma.com.ar"
    st.markdown(f"**[Precios de referencia Cosecha - Siembra]({facmalink})**")
    
    return st.session_state.dfx
    
def app3():
    st.title("⛅️ Estado de los campos")
    with st.expander("Recomendaciones de interpretación"):
     st.write("""
         - Para ver el panorama general de sequía ir a ¿Qué zonas estan en sequía? y buscar en "unidad administrativa de nivel 2" la localidad donde estan los campos
         - En caso de estar en área de sequía ver la sección "Evolución de sequías entre dos períodos" para ver si se registraron mejoras en los ultimos meses.
         - En la sección ¿Hace cuanto que no llueve? se puede ver la última información de precipitaciones
         - Tener en cuenta que el mapa de calor se conforma con la información recolectada de las estaciones por lo que algunas áreas con pocas estaciones (como por ejemplo zona centro este de Santa Fe) pueden verse influenciadas por estaciones más lejanas
     """)
    components.iframe("https://dashboard.crc-sas.org/informes/como-estamos/", height = 1500)
    st.caption("Datos extraidos de https://sissa.crc-sas.org/novedades/publicaciones-y-reportes-tecnicos/")


# Variable global para almacenar departamento_seleccionado
departamento_seleccionado = None

def app4():
    
    # Estilo CSS para ajustar el margen superior de toda la página
    st.markdown(
        """
        <style>
            .block-container {
                margin-top: -80px;
            }
            
            .st-emotion-cache-6qob1r.eczjsme3 {
                padding-top: 80px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Mensajes personalizados
    # URL del archivo JSON
    url_archivo = 'https://raw.githubusercontent.com/Jthl1986/T1/master/mensajes.json'
    
    # Realizar la solicitud HTTP para descargar el archivo
    response = requests.get(url_archivo)
    
    # Verificar si la solicitud fue exitosa (código de respuesta 200)
    if response.status_code == 200:
        # Cargar el contenido JSON desde la respuesta
        contenido_json = response.json()
    
        # Inicializar la cadena HTML una sola vez
        mensajes_html = '<div style="padding-top: 20px;"><marquee behavior="scroll" direction="left" scrollamount="6">'
    
        # Iterar sobre los mensajes en el JSON y agregarlos a la cadena HTML
        for i, mensaje_info in enumerate(contenido_json):
            # Obtener el valor asociado a la clave "mensaje"
            mensaje = mensaje_info.get("mensaje", "")
    
            # Obtener el valor asociado a la clave "enlace" o establecer enlace como None si no existe
            enlace = mensaje_info.get("enlace", None)
    
            # Agregar el mensaje al HTML con o sin enlace y la separación entre mensajes
            if enlace:
                mensajes_html += f'<a href="{enlace}" target="_blank">{mensaje}</a>'
            else:
                mensajes_html += mensaje
    
            # Agregar la separación si no es el último mensaje
            if i < len(contenido_json) - 1:
                mensajes_html += ' - '
    
        # Cerrar la etiqueta marquee y div
        mensajes_html += '</marquee></div>'
    
        # Mostrar el HTML en Streamlit
        st.components.v1.html(mensajes_html, height=50)
    else:
        print(f"No se pudo acceder al archivo JSON. Código de estado: {response.status_code}")
    
    
    st.title("🌽 Planteo productivo")
    left, center, right = st.columns(3)


#API TIPO DE CAMBIO
    #url = "https://www.dolarsi.com/api/api.php?type=dolar"
    #response = requests.get(url)
    #if response.status_code == 200:
    #   api_data = response.json()
    #   value = api_data[2]['casa']['venta']
    #   value2 = value.replace(',', '.')
    #   dol = float(827) #value2
    #else:
    #    print("Failed to retrieve data")
    dol = float(833.9)
    left.metric("Dolar mayorista", '${:,}'.format(float(dol)))
     
#SELECCIÓN DEPARTAMENTE Y PROVINCIA (INICIALIZACION)
    if 'provincia_seleccionada' not in st.session_state:
        st.session_state.provincia_seleccionada = None    
    if 'departamento_seleccionado' not in st.session_state:
        st.session_state.departamento_seleccionado = None    
    url = "https://raw.githubusercontent.com/Jthl1986/T1/main/Estimaciones7.csv"
    dfr = pd.read_csv(url, encoding='ISO-8859-1', sep=',')    
    # Obtener las provincias únicas
    provincias = dfr['Provincia'].unique()    
    # Interfaz de usuario
    st.session_state.provincia_seleccionada = left.selectbox("Provincia", provincias)
    # Filtrar departamentos según la provincia seleccionada
    departamentos_provincia = dfr.loc[dfr['Provincia'] == st.session_state.provincia_seleccionada, 'Departamento'].unique()
    # Si st.session_state.departamento_seleccionado no está en departamentos_provincia, seleccionar el primer elemento por defecto
    if st.session_state.departamento_seleccionado not in departamentos_provincia:
        st.session_state.departamento_seleccionado = departamentos_provincia[0]
    st.session_state.departamento_seleccionado = left.selectbox("Departamento", departamentos_provincia, index=departamentos_provincia.tolist().index(st.session_state.departamento_seleccionado))

#SEGMENTACION DE ZONAS    
    nucleo_norte = ["MARCOS JUAREZ","UNION","DIAMANTE", "VICTORIA", "BELGRANO", "CASEROS", "IRIONDO", "ROSARIO", "SAN JERONIMO", "SAN LORENZO", "SAN MARTIN"]
    nucleo_sur = ["ALBERTI", "ARRECIFES", "BARADERO", "BRAGADO", "CAMPANA", "CAPITAN SARMIENTO", "CARMEN DE ARECO", "CHACABUCO", "CHIVILCOY", "COLON", "EXALTACION DE LA CRUZ", "GENERAL ARENALES", "GENERAL RODRIGUEZ", "JUNIN", "LEANDRO N. ALEM", "LUJAN", "MARCOS PAZ", "MERCEDES", "PERGAMINO", "PILAR", "RAMALLO", "ROJAS", "SALTO", "SAN ANDRES DE GILES", "SAN ANTONIO DE ARECO", "SAN NICOLAS", "SAN PEDRO", "SUIPACHA", "ZARATE", "CONSTITUCION", "GENERAL LOPEZ"]
    oeste_baires = ["9 DE JULIO", "CARLOS CASARES", "CARLOS TEJEDOR", "FLORENTINO AMEGHINO", "GENERAL PINTO", "GENERAL VIAMONTE", "GENERAL VILLEGAS", "LINCOLN", "PEHUAJO", "PELLEGRINI", "RIVADAVIA", "TRENQUE LAUQUEN","CATRILO","CHAPALEUFU", "CONHELO", "MARACO","QUEMU QUEMU","RANCUL","REALICO","TRENEL"]
    so_baires = ["BAHIA BLANCA", "CRNEL DE MARINA L ROSALES", "CORONEL SUAREZ","GENERAL LA MADRID","GUAMINI","PATAGONES","PUAN","SAAVEDRA","SALLIQUELO", "TORNQUIST","TRES LOMAS","VILLARINO","ATREUCO","CALEU CALEU","CAPITAL","GUATRACHE","HUCAL","LIHUEL CALEL","LOVENTUE","TOAY","UTRACAN","ADOLFO ALSINA"]
    se_baires = ["ADOLFO GONZALES CHAVES","BALCARCE","BENITO JUAREZ","CORONEL DORREGO","CORONEL PRINGLES","GENERAL ALVARADO","GENERAL PUEYRREDON","LAPRIDA","LOBERIA","MAR CHIQUITA","MONTE HERMOSO","NECOCHEA","SAN CAYETANO","TANDIL","TRES ARROYOS"]
    centro_baires = ["25 DE MAYO","AYACUCHO","AZUL","BOLIVAR","DAIREAUX","GENERAL ALVEAR","HIPOLITO YRIGOYEN","LAS FLORES","NAVARRO","OLAVARRIA","RAUCH","ROQUE PEREZ","SALADILLO","TAPALQUE"]
    cuenca_salado = ["BRANDSEN","CANUELAS","CASTELLI","CHASCOMUS","DOLORES","GENERAL BELGRANO","GENERAL GUIDO","GENERAL JUAN MADARIAGA","GENERAL LAS HERAS","GENERAL LAVALLE","GENERAL PAZ","LA COSTA","LA PLATA","LEZAMA","LOBOS","MAGDALENA","MAIPU","MONTE","PILA","PUNTA INDIO","SAN VICENTE","TORDILLO","VILLA GESELL"]
    sur_cordoba = ["GENERAL ROCA","JUAREZ CELMAN","PRES. ROQUE SAENZ PENA", "RIO CUARTO"]
    centronorte_cba = ["CALAMUCHITA","CAPITAL","COLON", "CRUZ DEL EJE","GENERAL SAN MARTIN", "ISCHILIN","MINAS","POCHO","PUNILLA","RIO PRIMERO","RIO SECO","RIO SEGUNDO","SAN ALBERTO","SAN JAVIER","SAN JUSTO","SANTA MARIA","SOBREMONTE","TERCERO ARRIBA","TOTORAL","TULUMBA"]
    santafe_centro = ["CASTELLANOS","GARAY","LA CAPITAL","LAS COLONIAS","SAN JUSTO"]
    santafe_norte = ["9 DE JULIO","GENERAL OBLIGADO","SAN CRISTOBAL", "SAN JAVIER", "VERA"]
    nea_oeste=["AGUIRRE","ALBERDI","ATAMISQUI","AVELLANEDA","BELGRANO","COPO","GENERAL TABOADA","JUAN F. IBARRA","MITRE","MORENO","RIVADAVIA"]
    noa = ["AMBASTO","ANCASTI","CAPAYAN","CAPITAL","EL ALTO","FRAY MAMERTO ESQUIU","LA PAZ","PACLIN","SANTA ROSA","VALLE VIEJO","DR. MANUEL BELGRANO","EL CARMEN","HUMAHUACA","LEDESMA","PALPALA","SAN ANTONIO","SAN PEDRO","SANTA BARBARA","TILCARA","TUMBAYA","VALLE GRANDE","GENERAL SAN MARTIN","ANTA","CACHI","CAPITAL","CERRILLOS","CHICOANA","GENERAL GUEMES","GENERAL JOSE DE SAN MARTIN","GUACHIPAS","IRUYA","LA CALDERA","LA CANDELARIA","LA VINA","METAN","ORAN","RIVADAVIA","ROSARIO DE LA FRONTERA","ROSARIO DE LERMA","SANTA VICTORIA","BANDA","CAPITAL","CHOYA","FIGUEROA","GUASAYAN","JIMENEZ","LORETO","OJO DE AGUA","PELLEGRINI","RIO HONDO","ROBLES","SAN MARTIN","SARMIENTO","SILIPICA","BURRUYACU","CAPITAL","CHICLIGASTA","CRUZ ALTA","FAMAILLA","GRANEROS","JUAN B. ALBERDI","LA COCHA","LEALES","LULES","MONTEROS","RIO CHICO","SIMOCA","TAFI DEL VALLE","TAFI VIEJO","TRANCAS","YERBA BUENA"]
    nea_este=["CHACO","FORMOSA"]
    
#AGRUPAMIENTO PROVINCIAS POR ZONA
    nnorte = ["CORDOBA","SANTA FE","ENTRE RIOS"]  
    nsur = ["BUENOS AIRES","SANTA FE"]
    obaires = ["LA PAMPA","BUENOS AIRES"] #Obaires, Sobaires
    baires = ["BUENOS AIRES"] #Sebaires,, Cenbaires, Salado
    cord = ["CORDOBA"] #Sur y Centro Cba
    stafe = ["SANTA FE"]#Santa Fe centro y norte
    neaoeste = ["SANTIAGO DEL ESTERO"]
    noap = ["CATAMARCA","JUJUY","LA RIOJA","SALTA","SANTIAGO DEL ESTERO"]
    
    if st.session_state.provincia_seleccionada in nea_este:
        region = "NEA Este"
    elif st.session_state.provincia_seleccionada == "SAN LUIS":
        region = "San Luis"
    elif st.session_state.provincia_seleccionada == "ENTRE RIOS":
        region = "Centro Este Entre Rios"        
    elif st.session_state.departamento_seleccionado in nucleo_norte and st.session_state.provincia_seleccionada in nnorte:
        region = "Zona Nucleo Norte"
    elif st.session_state.departamento_seleccionado in nucleo_sur and st.session_state.provincia_seleccionada in nsur:
        region = "Zona Nucleo Sur"
    elif st.session_state.departamento_seleccionado in oeste_baires and st.session_state.provincia_seleccionada in obaires:
        region = "Oeste Bs As - N La Pampa"
    elif st.session_state.departamento_seleccionado in so_baires and st.session_state.provincia_seleccionada in obaires:
        region = "SO Bs As - S La Pampa"
    elif st.session_state.departamento_seleccionado in se_baires and st.session_state.provincia_seleccionada in baires:
        region = "SE Bs As"
    elif st.session_state.departamento_seleccionado in centro_baires and st.session_state.provincia_seleccionada in baires:
        region = "Centro Bs As"
    elif st.session_state.departamento_seleccionado in cuenca_salado and st.session_state.provincia_seleccionada in baires:
        region = "Cuenca Salado"
    elif st.session_state.departamento_seleccionado in sur_cordoba and st.session_state.provincia_seleccionada in cord:
            region = "Sur Cordoba"
    elif st.session_state.departamento_seleccionado in centronorte_cba and st.session_state.provincia_seleccionada in cord:
            region = "Centro Norte Cordoba"
    elif st.session_state.departamento_seleccionado in santafe_centro and st.session_state.provincia_seleccionada in stafe:
            region = "Santa Fe Centro"
    elif st.session_state.departamento_seleccionado in santafe_norte and st.session_state.provincia_seleccionada in stafe:
            region = "Santa Fe Norte"
    elif st.session_state.departamento_seleccionado in nea_oeste and st.session_state.provincia_seleccionada in neaoeste:
            region = "NEA Oeste"
    elif st.session_state.departamento_seleccionado in noa and st.session_state.provincia_seleccionada in noap:
            region = "NOA"
        
    left.markdown(f"Corresponde a **{region}**")

    on = left.toggle("Activar rinde automático")

#PRUEBA    
    with left.expander("Análisis de Rendimientos"):
        cultivos = dfr['Cultivo'].unique()
        cultivos_seleccionados = st.selectbox("Cultivos", cultivos)
        
        # Filtrar el DataFrame según las selecciones del usuario
        filtro_provincia = (dfr['Provincia'] == st.session_state.provincia_seleccionada)
        filtro_departamento = (dfr['Departamento'] == st.session_state.departamento_seleccionado)
        filtro_cultivos = dfr['Cultivo'].isin([cultivos_seleccionados])
        
        df_filtrado = dfr[filtro_provincia & filtro_departamento & filtro_cultivos]
        
        # Mostrar los rendimientos en una tabla
        if not df_filtrado.empty:
            df_filtrado['Rendimiento'] /= 1000  # Dividir por 1000
            df_filtrado['Rendimiento'] = df_filtrado['Rendimiento'].apply(lambda x: '{:.2f}'.format(x))  # Formatear a dos decimales
            # Crear checkboxes con etiquetas de campañas
            st.table(df_filtrado[['Campaña', 'Rendimiento']])
            selected_rendimientos = st.checkbox("Seleccionar campañas", df_filtrado['Campaña'].astype(str).tolist(), key="checkboxes")
        
            # Calcular el promedio de los rendimientos seleccionados
            if selected_rendimientos:
                promedio_seleccionado = df_filtrado[df_filtrado['Campaña'].astype(str).isin(st.multiselect("Campañas", df_filtrado['Campaña'].astype(str).unique()))]['Rendimiento'].astype(float).mean()
                st.write(f"Promedio de rendimientos seleccionados: {promedio_seleccionado:.2f} tn/ha")
        else:
            st.warning("No se encontraron datos con las selecciones realizadas.")
            
#RINDE AUTOMATICO
    def rindeautomatico(tipo):
        cultivos_seleccionados = tipo
        # Filtrar el DataFrame según las selecciones del usuario
        filtro_provincia = (dfr['Provincia'] == st.session_state.provincia_seleccionada)
        filtro_departamento = (dfr['Departamento'] == st.session_state.departamento_seleccionado)
        filtro_cultivos = dfr['Cultivo'].isin([cultivos_seleccionados])
        df_filtrado = dfr[filtro_provincia & filtro_departamento & filtro_cultivos]
        # Calcular el promedio de los rendimientos para cada cultivo seleccionado
        promedios_por_cultivo = df_filtrado.groupby('Cultivo')['Rendimiento'].mean().reset_index()
        return round(promedios_por_cultivo.iloc[0,1]/1000,2)
        
#LECTURA VARIABLES
    df = pd.read_csv('https://raw.githubusercontent.com/Jthl1986/T1/main/variables3.csv')

    # Crear un diccionario para almacenar las variables y valores
    variables_dict = {}
    
    # Iterar sobre el DataFrame y llenar el diccionario
    for _, row in df.iterrows():
        variable = row['variable']
        valor = row['valor']
    
        # Almacenar la variable y su valor en el diccionario
        variables_dict[variable] = valor
    
    # Definir cada variable en el espacio de nombres global
    for variable, valor in variables_dict.items():
        globals()[variable] = valor    
                
    # Mapear los nombres de los cultivos a las variables correspondientes
    mapeo_cultivos_variables = {
        "Soja 1ra": "psoja1",
        "Soja 2da": "psoja2",
        "Trigo": "ptrigo",
        "Maíz": "pmaiz",
        "Girasol": "pgirasol",
        "Sorgo": "psorgo",
        "Cebada": "pcebada"}
    
    def obtener_precio(tipo):
        # Obtener el nombre de la variable correspondiente al cultivo
        variable_cultivo = mapeo_cultivos_variables.get(tipo, None)
        if variable_cultivo:
            return variables_dict.get(variable_cultivo, "Cultivo no encontrado en la lista")
        else:
            return "Cultivo no encontrado en la lista"
    
#LECTURA DE RINDES
    rind = {}
    for variable in list(variables_dict.keys())[245:355]:
        rind[variable] = variables_dict[variable]
        
    rind_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": rtrigo1, "Maíz": rmaiz1, "Soja 1ra": rsoja11, "Soja 2da": rsoja21, "Girasol":rgirasol1 , "Cebada": rcebada1, "Sorgo": rsorgo1},
        "Zona Nucleo Sur" : {"Trigo": rtrigo2, "Maíz": rmaiz2, "Soja 1ra": rsoja12, "Soja 2da": rsoja22, "Girasol":rgirasol2 , "Cebada": rcebada2, "Sorgo": rsorgo2},
        "Oeste Bs As - N La Pampa" : {"Trigo": rtrigo3, "Maíz": rmaiz3, "Soja 1ra": rsoja13, "Soja 2da": rsoja23, "Girasol":rgirasol3, "Cebada": rcebada3, "Sorgo": rsorgo3},
        "SO Bs As - S La Pampa" : {"Trigo": rtrigo4, "Maíz": rmaiz4, "Soja 1ra": rsoja14, "Soja 2da": rsoja24, "Girasol":rgirasol4, "Cebada": rcebada4, "Sorgo": rsorgo4},
        "SE Bs As" : {"Trigo": rtrigo5, "Maíz": rmaiz5, "Soja 1ra": rsoja15, "Soja 2da": rsoja25, "Girasol":rgirasol5, "Cebada": rcebada5, "Sorgo": rsorgo5},
        "Centro Bs As" : {"Trigo": rtrigo6, "Maíz": rmaiz6, "Soja 1ra": rsoja16, "Soja 2da": rsoja26, "Girasol":rgirasol6, "Cebada": rcebada6, "Sorgo": rsorgo6},
        "Cuenca Salado" : {"Trigo": rtrigo7, "Maíz": rmaiz7, "Soja 1ra": rsoja17, "Soja 2da": rsoja27, "Girasol":rgirasol7, "Cebada": rcebada7, "Sorgo": rsorgo7},
        "Sur Cordoba" : {"Trigo": rtrigo8, "Maíz": rmaiz8, "Soja 1ra": rsoja18, "Soja 2da": rsoja28, "Girasol":rgirasol8, "Cebada": rcebada8, "Sorgo": rsorgo8},
        "Centro Norte Cordoba" : {"Trigo": rtrigo9, "Maíz": rmaiz9, "Soja 1ra": rsoja19, "Soja 2da": rsoja29, "Girasol":rgirasol9, "Cebada": rcebada9, "Sorgo": rsorgo9},
        "Santa Fe Centro" : {"Trigo": rtrigo10, "Maíz": rmaiz10, "Soja 1ra": rsoja110, "Soja 2da": rsoja210, "Girasol":rgirasol10, "Cebada": rcebada10, "Sorgo": rsorgo11},
        "Santa Fe Norte" : {"Trigo": rtrigo11, "Maíz": rmaiz11, "Soja 1ra": rsoja111, "Soja 2da": rsoja211, "Girasol":rgirasol11, "Sorgo": rsorgo11},
        "Centro Este Entre Rios" : {"Trigo": rtrigo12, "Maíz": rmaiz12, "Soja 1ra": rsoja112, "Soja 2da": rsoja212, "Girasol":rgirasol12, "Cebada": rcebada12, "Sorgo": rsorgo12},
        "NEA Oeste" : {"Trigo": rtrigo13, "Maíz": rmaiz13, "Soja 1ra": rsoja113, "Soja 2da": rsoja213, "Girasol":rgirasol13, "Cebada": rcebada13, "Sorgo": rsorgo13},
        "NEA Este" : {"Trigo": rtrigo14, "Maíz": rmaiz14, "Soja 1ra": rsoja114, "Soja 2da": rsoja214, "Girasol":rgirasol14, "Cebada": rtrigo14, "Sorgo": rsorgo14},
        "NOA" : {"Trigo": rtrigo15, "Maíz": rmaiz15, "Soja 1ra": rsoja115, "Soja 2da": rsoja215, "Girasol":rgirasol15, "Cebada": rcebada15, "Sorgo": rsorgo15},
        "San Luis" : {"Trigo": rtrigo16, "Maíz": rmaiz16, "Soja 1ra": rsoja116, "Soja 2da": rsoja216, "Girasol":rgirasol16, "Cebada": rcebada16, "Sorgo": rsorgo16},
    }
    
    # Función para obtener el gasto estructura para campo arrendado de un cultivo en una región
    def obtener_rind(region, tipo):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in rind_por_region_cultivo and tipo in rind_por_region_cultivo[region]:
            return rind_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
    
#LECTURA DE COSTOS
    costos = {}
    for variable in list(variables_dict.keys())[7:120]:
        costos[variable] = variables_dict[variable]
        
    # Crear un diccionario para almacenar los costos por región y cultivo
        costos_por_region_cultivo = {
            "Zona Nucleo Norte": {"Trigo": ctrigo1, "Maíz": cmaiz1, "Soja 1ra": csoja11, "Soja 2da": csoja21, "Girasol":cgirasol1 , "Cebada": ccebada1, "Sorgo": csorgo1},
            "Zona Nucleo Sur" : {"Trigo": ctrigo2, "Maíz": cmaiz2, "Soja 1ra": csoja12, "Soja 2da": csoja22, "Girasol":cgirasol2 , "Cebada": ccebada2, "Sorgo": csorgo2},
            "Oeste Bs As - N La Pampa" : {"Trigo": ctrigo3, "Maíz": cmaiz3, "Soja 1ra": csoja13, "Soja 2da": csoja23, "Girasol":cgirasol3, "Cebada": ccebada3, "Sorgo": csorgo3},
            "SO Bs As - S La Pampa" : {"Trigo": ctrigo4, "Maíz": cmaiz4, "Soja 1ra": csoja14, "Soja 2da": csoja24, "Girasol":cgirasol4, "Cebada": ccebada4, "Sorgo": csorgo4},
            "SE Bs As" : {"Trigo": ctrigo5, "Maíz": cmaiz5, "Soja 1ra": csoja15, "Soja 2da": csoja25, "Girasol":cgirasol5, "Cebada": ccebada5, "Sorgo": csorgo5},
            "Centro Bs As" : {"Trigo": ctrigo6, "Maíz": cmaiz6, "Soja 1ra": csoja16, "Soja 2da": csoja26, "Girasol":cgirasol6, "Cebada": ccebada6, "Sorgo": csorgo6},
            "Cuenca Salado" : {"Trigo": ctrigo7, "Maíz": cmaiz7, "Soja 1ra": csoja17, "Soja 2da": csoja27, "Girasol":cgirasol7, "Cebada": ccebada7, "Sorgo": csorgo7},
            "Sur Cordoba" : {"Trigo": ctrigo8, "Maíz": cmaiz8, "Soja 1ra": csoja18, "Soja 2da": csoja28, "Girasol":cgirasol8, "Cebada": ccebada8, "Sorgo": csorgo8},
            "Centro Norte Cordoba" : {"Trigo": ctrigo9, "Maíz": cmaiz9, "Soja 1ra": csoja19, "Soja 2da": csoja29, "Girasol":cgirasol9, "Cebada": ccebada9, "Sorgo": csorgo9},
            "Santa Fe Centro" : {"Trigo": ctrigo10, "Maíz": cmaiz10, "Soja 1ra": csoja110, "Soja 2da": csoja210, "Girasol":cgirasol10, "Cebada": ccebada10, "Sorgo": csorgo11},
            "Santa Fe Norte" : {"Trigo": ctrigo11, "Maíz": cmaiz11, "Soja 1ra": csoja111, "Soja 2da": csoja211, "Girasol":cgirasol11, "Cebada": ccebada11, "Sorgo": csorgo11},
            "Centro Este Entre Rios" : {"Trigo": ctrigo12, "Maíz": cmaiz12, "Soja 1ra": csoja112, "Soja 2da": csoja212, "Girasol":cgirasol12, "Cebada": ccebada12, "Sorgo": csorgo12},
            "NEA Oeste" : {"Trigo": ctrigo13, "Maíz": cmaiz13, "Soja 1ra": csoja113, "Soja 2da": csoja213, "Girasol":cgirasol13, "Cebada": ccebada13, "Sorgo": csorgo13},
            "NEA Este" : {"Trigo": ctrigo14, "Maíz": cmaiz14, "Soja 1ra": csoja114, "Soja 2da": csoja214, "Girasol":cgirasol14, "Cebada": notuse14, "Sorgo": csorgo14},
            "NOA" : {"Trigo": ctrigo15, "Maíz": cmaiz15, "Soja 1ra": csoja115, "Soja 2da": csoja215, "Girasol":cgirasol15, "Cebada": ccebada15, "Sorgo": csorgo15},
            "San Luis" : {"Trigo": ctrigo16, "Maíz": cmaiz16, "Soja 1ra": csoja116, "Soja 2da": csoja216, "Girasol":cgirasol16, "Cebada": ccebada16, "Sorgo": csorgo16},
            } #No hay  cebada en zona 14 se asignó notuse14
    
    # Función para obtener el costo de un cultivo en una región
    def obtener_costo(region, tipo):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in costos_por_region_cultivo and tipo in costos_por_region_cultivo[region]:
            return costos_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
        
    gasvar = {}
    for variable in list(variables_dict.keys())[355:467]:
        gasvar[variable] = variables_dict[variable]
    
    gasvar_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": gasvartrigo1, "Maíz": gasvarmaiz1, "Soja 1ra": gasvarsoja11, "Soja 2da": gasvarsoja21, "Girasol":gasvargirasol1 , "Cebada": gasvarcebada1, "Sorgo": gasvarsorgo1},
        "Zona Nucleo Sur" : {"Trigo": gasvartrigo2, "Maíz": gasvarmaiz2, "Soja 1ra": gasvarsoja12, "Soja 2da": gasvarsoja22, "Girasol":gasvargirasol2 , "Cebada": gasvarcebada2, "Sorgo": gasvarsorgo2},
        "Oeste Bs As - N La Pampa" : {"Trigo": gasvartrigo3, "Maíz": gasvarmaiz3, "Soja 1ra": gasvarsoja13, "Soja 2da": gasvarsoja23, "Girasol":gasvargirasol3, "Cebada": gasvarcebada3, "Sorgo": gasvarsorgo3},
        "SO Bs As - S La Pampa" : {"Trigo": gasvartrigo4, "Maíz": gasvarmaiz4, "Soja 1ra": gasvarsoja14, "Soja 2da": gasvarsoja24, "Girasol":gasvargirasol4, "Cebada": gasvarcebada4, "Sorgo": gasvarsorgo4},
        "SE Bs As" : {"Trigo": gasvartrigo5, "Maíz": gasvarmaiz5, "Soja 1ra": gasvarsoja15, "Soja 2da": gasvarsoja25, "Girasol":gasvargirasol5, "Cebada": gasvarcebada5, "Sorgo": gasvarsorgo5},
        "Centro Bs As" : {"Trigo": gasvartrigo6, "Maíz": gasvarmaiz6, "Soja 1ra": gasvarsoja16, "Soja 2da": gasvarsoja26, "Girasol":gasvargirasol6, "Cebada": gasvarcebada6, "Sorgo": gasvarsorgo6},
        "Cuenca Salado" : {"Trigo": gasvartrigo7, "Maíz": gasvarmaiz7, "Soja 1ra": gasvarsoja17, "Soja 2da": gasvarsoja27, "Girasol":gasvargirasol7, "Cebada": gasvarcebada7, "Sorgo": gasvarsorgo7},
        "Sur Cordoba" : {"Trigo": gasvartrigo8, "Maíz": gasvarmaiz8, "Soja 1ra": gasvarsoja18, "Soja 2da": gasvarsoja28, "Girasol":gasvargirasol8, "Cebada": gasvarcebada8, "Sorgo": gasvarsorgo8},
        "Centro Norte Cordoba" : {"Trigo": gasvartrigo9, "Maíz": gasvarmaiz9, "Soja 1ra": gasvarsoja19, "Soja 2da": gasvarsoja29, "Girasol":gasvargirasol9, "Cebada": gasvarcebada9, "Sorgo": gasvarsorgo9},
        "Santa Fe Centro" : {"Trigo": gasvartrigo10, "Maíz": gasvarmaiz10, "Soja 1ra": gasvarsoja110, "Soja 2da": gasvarsoja210, "Girasol":gasvargirasol10, "Cebada": gasvarcebada10, "Sorgo": gasvarsorgo11},
        "Santa Fe Norte" : {"Trigo": gasvartrigo11, "Maíz": gasvarmaiz11, "Soja 1ra": gasvarsoja111, "Soja 2da": gasvarsoja211, "Girasol":gasvargirasol11, "Cebada": gasvarcebada11, "Sorgo": gasvarsorgo11},
        "Centro Este Entre Rios" : {"Trigo": gasvartrigo12, "Maíz": gasvarmaiz12, "Soja 1ra": gasvarsoja112, "Soja 2da": gasvarsoja212, "Girasol":gasvargirasol12, "Cebada": gasvarcebada12, "Sorgo": gasvarsorgo12},
        "NEA Oeste" : {"Trigo": gasvartrigo13, "Maíz": gasvarmaiz13, "Soja 1ra": gasvarsoja113, "Soja 2da": gasvarsoja213, "Girasol":gasvargirasol13, "Cebada": gasvarcebada13, "Sorgo": gasvarsorgo13},
        "NEA Este" : {"Trigo": gasvartrigo14, "Maíz": gasvarmaiz14, "Soja 1ra": gasvarsoja114, "Soja 2da": gasvarsoja214, "Girasol":gasvargirasol14, "Cebada": gasvarcebada14, "Sorgo": gasvarsorgo14},
        "NOA" : {"Trigo": gasvartrigo15, "Maíz": gasvarmaiz15, "Soja 1ra": gasvarsoja115, "Soja 2da": gasvarsoja215, "Girasol":gasvargirasol15, "Cebada": gasvarcebada15, "Sorgo": gasvarsorgo15},
        "San Luis" : {"Trigo": gasvartrigo16, "Maíz": gasvarmaiz16, "Soja 1ra": gasvarsoja116, "Soja 2da": gasvarsoja216, "Girasol":gasvargirasol16, "Cebada": gasvarcebada16, "Sorgo": gasvarsorgo16},
    } #No hay faltantes
    
    # Función para obtener el gasto variable de un cultivo en una región
    def obtener_gasvar(region, tipo):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in gasvar_por_region_cultivo and tipo in gasvar_por_region_cultivo[region]:
            return gasvar_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
        
###########
    #estimador gastos de estructura
    nro_hectareas = 0
    gestimado = 0
            
    gesp = {}
    for variable in list(variables_dict.keys())[467:578]:
        gesp[variable] = variables_dict[variable]
        
    gesp_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": gesptrigo1, "Maíz": gespmaiz1, "Soja 1ra": gespsoja11, "Soja 2da": gespsoja21, "Girasol":gespgirasol1 , "Cebada": gespcebada1, "Sorgo": gespsorgo1},
        "Zona Nucleo Sur" : {"Trigo": gesptrigo2, "Maíz": gespmaiz2, "Soja 1ra": gespsoja12, "Soja 2da": gespsoja22, "Girasol":gespgirasol2 , "Cebada": gespcebada2, "Sorgo": gespsorgo2},
        "Oeste Bs As - N La Pampa" : {"Trigo": gesptrigo3, "Maíz": gespmaiz3, "Soja 1ra": gespsoja13, "Soja 2da": gespsoja23, "Girasol":gespgirasol3, "Cebada": gespcebada3, "Sorgo": gespsorgo3},
        "SO Bs As - S La Pampa" : {"Trigo": gesptrigo4, "Maíz": gespmaiz4, "Soja 1ra": gespsoja14, "Soja 2da": gespsoja24, "Girasol":gespgirasol4, "Cebada": gespcebada4, "Sorgo": gespsorgo4},
        "SE Bs As" : {"Trigo": gesptrigo5, "Maíz": gespmaiz5, "Soja 1ra": gespsoja15, "Soja 2da": gespsoja25, "Girasol":gespgirasol5, "Cebada": gespcebada5, "Sorgo": gespsorgo5},
        "Centro Bs As" : {"Trigo": gesptrigo6, "Maíz": gespmaiz6, "Soja 1ra": gespsoja16, "Soja 2da": gespsoja26, "Girasol":gespgirasol6, "Cebada": gespcebada6, "Sorgo": gespsorgo6},
        "Cuenca Salado" : {"Trigo": gesptrigo7, "Maíz": gespmaiz7, "Soja 1ra": gespsoja17, "Soja 2da": gespsoja27, "Girasol":gespgirasol7, "Cebada": gespcebada7, "Sorgo": gespsorgo7},
        "Sur Cordoba" : {"Trigo": gesptrigo8, "Maíz": gespmaiz8, "Soja 1ra": gespsoja18, "Soja 2da": gespsoja28, "Girasol":gespgirasol8, "Cebada": gespcebada8, "Sorgo": gespsorgo8},
        "Centro Norte Cordoba" : {"Trigo": gesptrigo9, "Maíz": gespmaiz9, "Soja 1ra": gespsoja19, "Soja 2da": gespsoja29, "Girasol":gespgirasol9, "Cebada": gespcebada9, "Sorgo": gespsorgo9},
        "Santa Fe Centro" : {"Trigo": gesptrigo10, "Maíz": gespmaiz10, "Soja 1ra": gespsoja110, "Soja 2da": gespsoja210, "Girasol":gespgirasol10, "Cebada": gespcebada10, "Sorgo": gespsorgo11},
        "Santa Fe Norte" : {"Trigo": gesptrigo11, "Maíz": gespmaiz11, "Soja 1ra": gespsoja111, "Soja 2da": gespsoja211, "Girasol":gespgirasol11, "Cebada": gespcebada11, "Sorgo": gespsorgo11},
        "Centro Este Entre Rios" : {"Trigo": gesptrigo12, "Maíz": gespmaiz12, "Soja 1ra": gespsoja112, "Soja 2da": gespsoja212, "Girasol":gespgirasol12, "Cebada": gespcebada12, "Sorgo": gespsorgo12},
        "NEA Oeste" : {"Trigo": gesptrigo13, "Maíz": gespmaiz13, "Soja 1ra": gespsoja113, "Soja 2da": gespsoja213, "Girasol":gespgirasol13, "Cebada": gespcebada13, "Sorgo": gespsorgo13},
        "NEA Este" : {"Trigo": gesptrigo14, "Maíz": gespmaiz14, "Soja 1ra": gespsoja114, "Soja 2da": gespsoja214, "Girasol":gespgirasol14, "Cebada": gesptrigo14, "Sorgo": gespsorgo14},
        "NOA" : {"Trigo": gesptrigo15, "Maíz": gespmaiz15, "Soja 1ra": gespsoja115, "Soja 2da": gespsoja215, "Girasol":gespgirasol15, "Cebada": gespcebada15, "Sorgo": gespsorgo15},
        "San Luis" : {"Trigo": gesptrigo16, "Maíz": gespmaiz16, "Soja 1ra": gespsoja116, "Soja 2da": gespsoja216, "Girasol":gespgirasol16, "Cebada": gespcebada16, "Sorgo": gespsorgo16},
    }
    #No hay gesp de cebada en zona 14 se asignó trigo misma zona
    
    # Función para obtener el gasto variable de un cultivo en una región
    def obtener_gesp(region, tipo, cantidad):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in gesp_por_region_cultivo and tipo in gesp_por_region_cultivo[region]:
            return cantidad * gesp_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
    
    if 'gespr' not in st.session_state:
        st.session_state.gespr = []
        
    def gastos_estructura1():
        result = obtener_gesp(region, tipo, cantidad)
        result = round(result * dol, 2)
        st.session_state.gespr.append(result)


    gesa = {}
    for variable in list(variables_dict.keys())[578:585]:
        gesa[variable] = variables_dict[variable]
    
        
    gesa_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Zona Nucleo Sur" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Oeste Bs As - N La Pampa" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "SO Bs As - S La Pampa" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "SE Bs As" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Centro Bs As" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Cuenca Salado" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Sur Cordoba" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Centro Norte Cordoba" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Santa Fe Centro" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Santa Fe Norte" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Centro Este Entre Rios" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "NEA Oeste" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "NEA Este" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "NOA" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "San Luis" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
    }
    
    # Función para obtener el gasto estructura para campo arrendado de un cultivo en una región
    def obtener_gesa(region, tipo, cantidad):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in gesa_por_region_cultivo and tipo in gesa_por_region_cultivo[region]:
            return cantidad * gesa_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
    
    
    if 'gesar' not in st.session_state:
        st.session_state.gesar = []
        
    def gastos_estructura2():
        result = obtener_gesa(region, tipo, cantidad)
        result = round(result * dol, 2)
        st.session_state.gesar.append(result)

    arrend = {}
    for variable in list(variables_dict.keys())[585:]:
        arrend[variable] = variables_dict[variable]
        
    arrend_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": arrendtrigo1, "Maíz": arrendmaiz1, "Soja 1ra": arrendsoja11, "Soja 2da": arrendsoja21, "Girasol":arrendgirasol1 , "Cebada": arrendcebada1, "Sorgo": arrendsorgo1},
        "Zona Nucleo Sur" : {"Trigo": arrendtrigo2, "Maíz": arrendmaiz2, "Soja 1ra": arrendsoja12, "Soja 2da": arrendsoja22, "Girasol":arrendgirasol2 , "Cebada": arrendcebada2, "Sorgo": arrendsorgo2},
        "Oeste Bs As - N La Pampa" : {"Trigo": arrendtrigo3, "Maíz": arrendmaiz3, "Soja 1ra": arrendsoja13, "Soja 2da": arrendsoja23, "Girasol":arrendgirasol3, "Cebada": arrendcebada3, "Sorgo": arrendsorgo3},
        "SO Bs As - S La Pampa" : {"Trigo": arrendtrigo4, "Maíz": arrendmaiz4, "Soja 1ra": arrendsoja14, "Soja 2da": arrendsoja24, "Girasol":arrendgirasol4, "Cebada": arrendcebada4, "Sorgo": arrendsorgo4},
        "SE Bs As" : {"Trigo": arrendtrigo5, "Maíz": arrendmaiz5, "Soja 1ra": arrendsoja15, "Soja 2da": arrendsoja25, "Girasol":arrendgirasol5, "Cebada": arrendcebada5, "Sorgo": arrendsorgo5},
        "Centro Bs As" : {"Trigo": arrendtrigo6, "Maíz": arrendmaiz6, "Soja 1ra": arrendsoja16, "Soja 2da": arrendsoja26, "Girasol":arrendgirasol6, "Cebada": arrendcebada6, "Sorgo": arrendsorgo6},
        "Cuenca Salado" : {"Trigo": arrendtrigo7, "Maíz": arrendmaiz7, "Soja 1ra": arrendsoja17, "Soja 2da": arrendsoja27, "Girasol":arrendgirasol7, "Cebada": arrendcebada7, "Sorgo": arrendsorgo7},
        "Sur Cordoba" : {"Trigo": arrendtrigo8, "Maíz": arrendmaiz8, "Soja 1ra": arrendsoja18, "Soja 2da": arrendsoja28, "Girasol":arrendgirasol8, "Cebada": arrendcebada8, "Sorgo": arrendsorgo8},
        "Centro Norte Cordoba" : {"Trigo": arrendtrigo9, "Maíz": arrendmaiz9, "Soja 1ra": arrendsoja19, "Soja 2da": arrendsoja29, "Girasol":arrendgirasol9, "Cebada": arrendcebada9, "Sorgo": arrendsorgo9},
        "Santa Fe Centro" : {"Trigo": arrendtrigo10, "Maíz": arrendmaiz10, "Soja 1ra": arrendsoja110, "Soja 2da": arrendsoja210, "Girasol":arrendgirasol10, "Cebada": arrendcebada10, "Sorgo": arrendsorgo11},
        "Santa Fe Norte" : {"Trigo": arrendtrigo11, "Maíz": arrendmaiz11, "Soja 1ra": arrendsoja111, "Soja 2da": arrendsoja211, "Girasol":arrendgirasol11, "Cebada": arrendcebada11, "Sorgo": arrendsorgo11},
        "Centro Este Entre Rios" : {"Trigo": arrendtrigo12, "Maíz": arrendmaiz12, "Soja 1ra": arrendsoja112, "Soja 2da": arrendsoja212, "Girasol":arrendgirasol12, "Cebada": arrendcebada12, "Sorgo": arrendsorgo12},
        "NEA Oeste" : {"Trigo": arrendtrigo13, "Maíz": arrendmaiz13, "Soja 1ra": arrendsoja113, "Soja 2da": arrendsoja213, "Girasol":arrendgirasol13, "Cebada": arrendcebada13, "Sorgo": arrendsorgo13},
        "NEA Este" : {"Trigo": arrendtrigo14, "Maíz": arrendmaiz14, "Soja 1ra": arrendsoja114, "Soja 2da": arrendsoja214, "Girasol":arrendgirasol14, "Cebada": arrendtrigo14, "Sorgo": arrendsorgo14},
        "NOA" : {"Trigo": arrendtrigo15, "Maíz": arrendmaiz15, "Soja 1ra": arrendsoja115, "Soja 2da": arrendsoja215, "Girasol":arrendgirasol15, "Cebada": arrendcebada15, "Sorgo": arrendsorgo15},
        "San Luis" : {"Trigo": arrendtrigo16, "Maíz": arrendmaiz16, "Soja 1ra": arrendsoja116, "Soja 2da": arrendsoja216, "Girasol":arrendgirasol16, "Cebada": arrendcebada16, "Sorgo": arrendsorgo16},
    }
    
    # Función para obtener el gasto estructura para campo arrendado de un cultivo en una región
    def obtener_arrend(region, tipo, cantidad):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in arrend_por_region_cultivo and tipo in arrend_por_region_cultivo[region]:
            return cantidad * arrend_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
    
    if 'arrenda' not in st.session_state:
        st.session_state.arrenda = []
        
    def arrendamiento():
        resultado = obtener_arrend(region, tipo, cantidad)
        resultado = round(resultado * dol, 2)
        st.session_state.arrenda.append(resultado)

    def arrendamiento_inf():
        if propio == "Propios":
            return 0
        else:
            return obtener_arrend(region, tipo, 1)
    
    def ges_inf():
        if propio == "Propios":
            return obtener_gesp(region, tipo, 1)
        else:
            return obtener_gesa(region, tipo, 1)
    
    def gc_inf():
        return gasto*precio*rinde
    

###########

#FORMULARIO DE CARGA        
    center.write("Completar:")
    form = center.form("template_form") 
    tipo = form.selectbox('Tipo de cultivo: ', ["Soja 1ra", "Soja 2da", "Trigo","Maíz","Girasol", "Sorgo", "Cebada"])
    propio = form.selectbox('Campos: ', ["Propios","Arrendados","Aparcería"])
    cantidad = form.number_input("Superficie (has): ", step=1)   

    if not on:
        rinde = form.number_input("Rendimiento informado (en tn)")

    submit = form.form_submit_button("Ingresar")
    
    if on:
        rinde = float(rindeautomatico(tipo))
        
    right.write("Cuadro gastos (se completa solo una vez):")
    form2 = right.form("template_form2") 
    aparceria = form2.number_input("Porcentaje de aparcería (si falta el dato, sugerido 60%)", step=1)
    aparceria = aparceria/100
    
    rindeprom = round(float(obtener_rind(region, tipo)),2)
    precio = float(obtener_precio(tipo))
    costo = float(obtener_costo(region,tipo))
    gasto = float(obtener_gasvar(region,tipo))
    rindeinf = round(float((costo + arrendamiento_inf() + ges_inf() + gc_inf())/ precio),2)
    
    # Imprimir la lista de datos        
    def lista():
        def valor1():
            if propio == "Aparcería":
                return precio*dol*rinde*cantidad*aparceria
            else:
                return precio*dol*rinde*cantidad
        valors = round(valor1())
        
        def costo1():
            if propio == "Aparcería":
                return costo*dol*cantidad*aparceria
            else:
                return costo*dol*cantidad
        cost = round(costo1())
        
        def gc1():
            return gasto*valors
        gc = round(gc1())
        
        def neto():
            return valors-cost-gc
        net = round(neto()) 
        
        lista = [region, propio, tipo, cantidad, rinde, valors, cost, gc, net, rindeprom, rindeinf]
        return lista
    datos = []
    if "dfp" not in st.session_state:
        st.session_state.dfp = pd.DataFrame(columns=('Región                    ', 'Campos     ', 'Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos', 'Gastos comercialización','Margen bruto', 'RindeRegion', 'RindeIndif'))
    
    if submit:
        if propio == "Aparcería" and aparceria == 0:
            st.warning("Falta completar porcentaje de aparcería")
        else:
            datos.append(lista())
            dfo = pd.DataFrame(datos, columns=('Región                    ', 'Campos     ','Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos','Gastos comercialización', 'Margen bruto', 'RindeRegion', 'RindeIndif'))
            st.session_state.dfp = pd.concat([st.session_state.dfp, dfo])
    
    if "ingresos_totales" not in st.session_state:
        st.session_state["ingresos_totales"] = 0
        
    delete_last_row = st.button("Borrar última fila")
    if delete_last_row:
        if not st.session_state.dfp.empty:
            st.session_state["ingresos_totales"] -= st.session_state.dfp["Ingreso"].iloc[-1]
            st.session_state.dfp = st.session_state.dfp.iloc[:-1]

    st.dataframe(st.session_state.dfp.style.format({"Superficie (has)":"{:.0f}", "Rinde":"{:,}", "Ingreso":"${:,}", "Costos directos":"${:,}", "Gastos comercialización":"${:,}", "Margen bruto":"${:,}", "RindeRegion":"{:,}", "RindeIndif":"{:,}"}))
    css()
    
           
    if submit:
        if propio == "Propios":
            gastos_estructura1()
        else:
            gastos_estructura2()
    
    if st.session_state.dfp is not None:
        heca_arrendados = st.session_state.dfp.loc[st.session_state.dfp['Campos     '] == 'Arrendados', 'Superficie (has)'].sum()
        hecp_propios = st.session_state.dfp.loc[st.session_state.dfp['Campos     '] == 'Propios', 'Superficie (has)'].sum()
        hecp_aparceria = st.session_state.dfp.loc[st.session_state.dfp['Campos     '] == 'Aparcería', 'Superficie (has)'].sum()
        heca = heca_arrendados + hecp_aparceria
        hecp = hecp_propios
        nro_hectareas = heca + hecp

        if nro_hectareas > 0:
            gastos = sum(st.session_state.gespr) + sum(st.session_state.gesar)
            gestimado = gastos
                        
         
    if submit:
        if propio == "Arrendados":
            arrendamiento()
    
    arrenda_resultante = sum(st.session_state.arrenda)
    gestimado_str = "${:,.0f}".format(gestimado)
    arrend_str = "${:,.0f}".format(arrenda_resultante )
    arrendamiento = form2.number_input(f"Gastos de arrendamiento - Estimador: {arrend_str}", step=1)
    gast = form2.number_input(f"Gastos de estructura - Estimador: {gestimado_str}", step=1)
    submit2 = form2.form_submit_button("Ingresar")
    
    if submit2:
        st.session_state.df1 = [arrendamiento, gast, aparceria]
    

def app9():
    st.title("🌄 Sitios de utilidad")
    st.subheader("Valor de la tierra")

    # Lista de enlaces
    enlaces = {
        "Buenos Aires": "https://www.margenes.com/wp-content/uploads/2023/05/Buenos-Aires-Mayo-2023.pdf",
        "Chaco": "https://www.margenes.com/wp-content/uploads/2022/02/pag-38-B.pdf",
        "Córdoba": "https://www.margenes.com/wp-content/uploads/2023/06/Cordoba-Jun-23.pdf",
        "Corrientes": "https://www.margenes.com/wp-content/uploads/2022/09/Corrientes-Sep-22.pdf",
        "Entre Ríos": "https://www.margenes.com/wp-content/uploads/2023/07/Entre-Rios-Jul-23.pdf",
        "La Pampa": "https://www.margenes.com/wp-content/uploads/2022/12/La-Pampa-Dic-22.pdf",
        "Mendoza": "https://www.margenes.com/wp-content/uploads/2020/10/Mendoza-oct-20.pdf",
        "NOA": "https://www.margenes.com/wp-content/uploads/2023/01/NOA-2023.pdf",
        "San Luis": "https://www.margenes.com/wp-content/uploads/2022/11/San-Luis-Oct-22.pdf",
        "Santa Fe": "https://www.margenes.com/wp-content/uploads/2023/02/Santa-Fe-Feb-23.pdf",
        "Santiago de Estero": "https://www.margenes.com/wp-content/uploads/2022/11/Santiago-de-Estero-Nov-22.pdf"
    }
    
    # Dividir los enlaces en grupos de cinco
    enlaces_por_filas = [list(enlaces.items())[i:i+5] for i in range(0, len(enlaces), 5)]
    
    # Mostrar cada grupo de enlaces en una fila
    for fila in enlaces_por_filas:
        col1, col2, col3, col4, col5 = st.columns(5)
        for idx, (lugar, enlace) in enumerate(fila):
            if idx == 0:
                col1.markdown(f"**[{lugar}]({enlace})**")
            elif idx == 1:
                col2.markdown(f"**[{lugar}]({enlace})**")
            elif idx == 2:
                col3.markdown(f"**[{lugar}]({enlace})**")
            elif idx == 3:
                col4.markdown(f"**[{lugar}]({enlace})**")
            elif idx == 4:
                col5.markdown(f"**[{lugar}]({enlace})**")

    st.subheader("Reservas hídricas por zona - ORA")
    ora_semanal_link = "http://www.ora.gob.ar/camp_actual_reservas.php"
    st.markdown(f"**[Reservas hídricas (todas las regiones)]({ora_semanal_link})**")
    
    st.subheader("Mapa de Reservas hídricas - Todo el país")
    ora_semanal_link = "https://www.meteoblue.com/es/tiempo/mapas/federal_argentina_3433956#coords=4/-34.55/-61.8&map=soilMoisture~daily~auto~40-100%20cm%20down~none"
    st.markdown(f"**[Reservas hídricas (Meteoblue)]({ora_semanal_link})**")
     
    st.subheader("Informe semanal zona núcleo - GEA - Bolsa de Rosario")
    gea_semanal_link = "https://www.bcr.com.ar/es/mercados/gea/seguimiento-de-cultivos/informe-semanal-zona-nucleo"
    st.markdown(f"**[Informe semanal Zona Núcleo]({gea_semanal_link})**")

    st.subheader("Informe semanal Secretaria Agricultura")
    sec_semanal_link = "https://www.magyp.gob.ar/sitio/areas/estimaciones/estimaciones/informes/"
    st.markdown(f"**[Informe semanal Secretaria Agricultura (todas las regiones)]({sec_semanal_link})**")

    st.subheader("Mapa de datos e informes PAS - Bolsa de Buenos Aires")
    panorama_agricola_semanal_link = "https://www.bolsadecereales.com/estimaciones-informes"
    st.markdown(f"**[Panorama Agrícola Semanal]({panorama_agricola_semanal_link})**")
        
def app5():
    left, right = st.columns(2)
    css()
   
    # Obtener los dataframes existentes o None si no existen
    dfp = getattr(st.session_state, 'dfp', None)
    dfs = getattr(st.session_state, 'dfs', None)
    dfx = getattr(st.session_state, 'dfx', None)
    dfa = getattr(st.session_state, 'dfa', None)
    df1 = getattr(st.session_state, 'df1', None)
    
    df_fina = st.session_state.dfp[(st.session_state.dfp['Cultivo'] == "Trigo") | (st.session_state.dfp['Cultivo'] == "Cebada")]
    df_gruesa = st.session_state.dfp[(st.session_state.dfp['Cultivo'] != "Trigo") & (st.session_state.dfp['Cultivo'] != "Cebada")]
    
    if dfp is not None:
        st.subheader("Planteo productivo - Campaña 2023/2024")
        ingtotal = st.session_state.dfp['Ingreso'].sum()
        costtotal = st.session_state.dfp['Costos directos'].sum()
        gctotal = st.session_state.dfp['Gastos comercialización'].sum()
        mbtotal = st.session_state.dfp['Margen bruto'].sum()
        ingtotalfina = df_fina['Ingreso'].sum()
        costtotalfina = df_fina['Costos directos'].sum()
        gctotalfina = df_fina['Gastos comercialización'].sum()
        mbtotalfina = df_fina['Margen bruto'].sum()
        ingtotalgruesa = df_gruesa['Ingreso'].sum()
        costtotalgruesa = df_gruesa['Costos directos'].sum()
        gctotalgruesa = df_gruesa['Gastos comercialización'].sum()
        mbtotalgruesa = df_gruesa['Margen bruto'].sum()
    if df1 is not None:
        left, middle, right = st.columns(3)
        arrend = st.session_state.df1[0]
        gas = st.session_state.df1[1]
        result = int(mbtotal)-int(arrend)-int(gas)
        # Crear una lista de diccionarios con los datos
        
        data = [
            {'Concepto': 'Facturación campaña', 'Total': '${:,}'.format(round(ingtotal))},
            {'Concepto': 'Costos directos', 'Total': '${:,}'.format(round(costtotal))},
            {'Concepto': 'Gastos comercialización y cosecha', 'Total': '${:,}'.format(round(gctotal))},
            {'Concepto': 'Margen bruto total', 'Total': '${:,}'.format(round(mbtotal))},
            {'Concepto': 'Arrendamiento', 'Total': '${:,}'.format(arrend)},
            {'Concepto': 'Gastos estructura', 'Total': '${:,}'.format(gas)},
            {'Concepto': 'Generación operativa de fondos', 'Total': '${:,}'.format(result)}
        ]
        
        datafg = {
            'Concepto': ['Ingresos totales', 'Costos directos', 'Gastos comercialización', 'Margen bruto'],
            'Campaña Fina': [ingtotalfina, costtotalfina, gctotalfina, mbtotalfina],
            'Campaña Gruesa': [ingtotalgruesa, costtotalgruesa, gctotalgruesa, mbtotalgruesa]
        }
    
        df_totales = pd.DataFrame(datafg)
        
        # Crear un DataFrame
        left,right = st.columns(2)               
        df = pd.DataFrame(data)
        # Crear una tabla con Plotly con estilo personalizado
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='#f0f2f6',  # Cambiar el color a #f0f2f6
                        font=dict(family='sans-serif',  # Cambiar la fuente a sans-serif
                                  size=14),  # Cambiar el tamaño de la fuente a 14
                        align=['left', 'right']),
            cells=dict(values=[df.Concepto, df.Total],
                       fill_color='white',
                       font=dict(family='sans-serif',  # Cambiar la fuente a sans-serif
                                 size=14),
                       align=['left', 'right'],
                       height=30))
        ])
        
        # Ajustar el margen inferior y superior del gráfico
        fig.update_layout(height=len(df)*30+60)
        fig.update_layout(margin=dict(t=0, b=0))   
        with left:
            container = st.container()
            # Dividir el espacio en tres columnas dentro del contenedor
            col1, col2 = container.columns([3 , 1])
            
            # Mostrar el gráfico en las dos primeras columnas
            col1.plotly_chart(fig, use_container_width=True, padding=0)
            col2.empty()
            
        margenb = mbtotal/ingtotal
        margenb_porcentaje = "{:.0%}".format(margenb)
        margenn = result/ingtotal
        margenn_porcentaje = "{:.0%}".format(margenn)
        
        with right:
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Superficie has", value=st.session_state.dfp["Superficie (has)"].sum())
            col2.metric(label="Margen bruto", value=margenb_porcentaje)
            col3.metric(label="Margen neto", value=margenn_porcentaje)
        
        with right: 
            container = st.container() 
            col1, col2 = container.columns([3 , 1]) 
            df_totales['Campaña Fina'] = df_totales['Campaña Fina'].apply(lambda x: "${:,.0f}".format(x))
            df_totales['Campaña Gruesa'] = df_totales['Campaña Gruesa'].apply(lambda x: "${:,.0f}".format(x))
            df_totales_styled = df_totales.style \
                .set_table_styles([{'selector': 'th', 'props': [('text-align', 'right')]}]) \
                .set_properties(**{'font-size': '13px', 'text-align': 'right'}) \
                .hide_index()
            col1.table(df_totales_styled)
        
        left, center, right = st.columns(3)
        gastos_arrendamiento_estimados = left.checkbox("Los gastos de arrendamiento fueron estimados")
        gastos_estructura_estimados = center.checkbox("Los gastos de estructura fueron estimados")
        mejoresrindes = right.checkbox("Fueron contempladas campañas sin sequía")
        # Mensaje sobre los gastos de arrendamiento
        mensaje_arrendamiento = ("Los gastos de arrendamiento fueron estimados de acuerdo a valores de mercado por zona suministrados por organismos públicos."
                         if gastos_arrendamiento_estimados and arrend != 0
                         else "Los gastos de arrendamiento corresponden a los informados por el socio" if arrend != 0
                         else "")
        # Mensaje sobre los gastos de estructura
        mensaje_estructura = "fueron estimados de acuerdo a información suministrada por la Secretaria de Agricultura, Ganadería y Pesca" if gastos_estructura_estimados else "corresponden a los informados por el socio"

        st.write(f"**Aclaraciones del cálculo:** Los rindes utilizados para la proyección corresponden al promedio histórico de las últimas cinco campañas (desde 2018/2010 a 2022/2023) para el departamento de {st.session_state.departamento_seleccionado}, provincia de {st.session_state.provincia_seleccionada}. {mensaje_arrendamiento} Los gastos de estructura {mensaje_estructura}.")
        
        
        # Barras en tres columnas izquierda
        left, middle, right = st.columns(3)
        
        df_grouped = dfp.groupby('Cultivo')['Superficie (has)'].sum().reset_index()
        colors = px.colors.qualitative.Plotly
        fig = px.bar(df_grouped, x='Cultivo', y='Superficie (has)', color='Cultivo', color_discrete_sequence=colors)
        # Ajustar el margen inferior y superior del gráfico
        fig.update_layout(margin=dict(t=0, b=0))
        left.plotly_chart(fig, use_container_width=True)
        
        
        #GRAFICO TORTA
        # Agrupar por tipo de campo y sumar la superficie
        df_agrupado = dfp.groupby('Campos     ')['Superficie (has)'].sum()
        
        # Crear el gráfico de torta con Plotly
        fig1 = go.Figure(data=[go.Pie(labels=df_agrupado.index, values=df_agrupado.values)])
        
        # Actualizar las etiquetas con la suma de hectáreas
        labels = [f"{label}<br>({value} ha)" for label, value in zip(df_agrupado.index, df_agrupado.values)]
        fig1.update_traces(text=labels, textposition='inside', textinfo='text+percent')
        
        fig1.update_layout(legend=dict(x=0.6, y=1.2, orientation="v", title="Propiedad de los campos"))
        middle.plotly_chart(fig1, use_container_width=True)
        
        
        # Tabla dataframe entero
        st.dataframe(dfp.style.format({"Superficie (has)":"{:.0f}", "Rinde":"{:,}", "Ingreso":"${:,}", "Costos directos":"${:,}", "Gastos comercialización":"${:,}", "Margen bruto":"${:,}", "RindeRegion":"{:,}", "RindeIndif":"{:,}"}))

        #BULLET       
        
        # Función para generar gráficos de bullet
        def bulletgraph(data=None, limits=None, labels=None, axis_label=None, title="Rindes por cultivo",
                        size=(5, 3), palette=None, formatter=None, target_color="red",
                        bar_color="red", label_color="gray", show_title=True):
            
            # Determine the max value for adjusting the bar height
            # Dividing by 10 seems to work pretty well
            h = limits[-1] / 10
        
            # Use the green palette as a sensible default
            if palette is None:
                palette = sns.color_palette("RdYlGn", len(limits))
        
            # Must be able to handle one or many data sets via multiple subplots
            if len(data) == 1:
                fig, ax = plt.subplots(figsize=size, sharex=True)
            else:
                fig, axarr = plt.subplots(len(data), figsize=size, sharex=True)
        
            # Add each bullet graph bar to a subplot
            for idx, item in enumerate(data):
        
                # Get the axis from the array of axes returned when the plot is created
                if len(data) > 1:
                    ax = axarr[idx]
        
                # Formatting to get rid of extra marking clutter
                ax.set_aspect('equal')
                ax.set_yticklabels([item[0]])
                ax.set_yticks([1])
                ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]) # Agregado
                ax.set_xticklabels([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], fontsize=12) # Agregado
                ax.spines['bottom'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
        
                prev_limit = 0
                for idx2, lim in enumerate(limits):
                    # Draw the bar
                    ax.barh([1], lim - prev_limit, left=prev_limit, height=h,
                            color=palette[idx2], edgecolor=palette[idx2], linewidth=0)
                    prev_limit = lim
                rects = ax.patches
                # The last item in the list is the value we're measuring
                # Draw the value we're measuring
                ax.barh([1], item[1], height=(h / 6), color=bar_color)
        
                # Need the ymin and max in order to make sure the target marker
                # fits
                ymin, ymax = ax.get_ylim()
                if len(item) > 5 and item[5] == "red":
                    ax.vlines(item[4], ymin, ymax, linewidth=3, color=item[5])
                else:
                    ax.vlines(item[3], ymin, ymax, linewidth=3, color=target_color)
                    
                if len(item) > 7 and item[7] == "blue":
                    ax.vlines(item[6], ymin, ymax, linewidth=3, color=item[7])
                else:
                    ax.vlines(item[3], ymin, ymax, linewidth=3, color=target_color)

        
            # Now make some labels
            if labels is not None:
                for rect, label in zip(rects, labels):
                    height = rect.get_height()
                    ax.text(
                        rect.get_x() + rect.get_width() / 2,
                        -height * .4,
                        label,
                        ha='center',
                        va='bottom',
                        color=label_color,
                        fontsize=15)
            if formatter:
                ax.xaxis.set_major_formatter(formatter)
            if axis_label:
                ax.set_xlabel(axis_label)
            if show_title:
                if title:
                    fig.suptitle(title, fontsize=20)
                    fig.subplots_adjust(hspace=0)

        
        # Definir los límites para cada cultivo
        cultivo_limits = {
            "Maíz": [5, 7.25, 9.5, 11],
            "Trigo": [2, 3, 4,7],
            "Soja 1ra": [1.8 , 2.9 , 4, 6],
            "Soja 2da": [1.5,2.15,2.8,6],
            "Girasol":[1.5,2,2.6,5],
            "Sorgo":[5,2,6.5,8,10],
            "Cebada Forrajera":[3.5,4.2,5,7],
            "Cebada Cervecera":[3.5,4.2,5,7],
            # Agregar límites para otros cultivos aquí
        }
    
        # Obtener una lista de tuplas de cultivo y rinde
        data_to_plot = []
        for cultivo, rinde, rindeprom, rindeinf in zip(dfp["Cultivo"], dfp["Rinde"], dfp["RindeRegion"], dfp["RindeIndif"]): #,dfp["RindeMin"]
            if cultivo == "Soja 1ra":
                data_to_plot.append((cultivo, rinde, cultivo_limits[cultivo], 4, rindeprom, "red", rindeinf, "blue"))#,rindemin, "blue"
            elif cultivo == "Trigo":
                data_to_plot.append((cultivo, rinde, cultivo_limits[cultivo], 4, rindeprom, "red", rindeinf, "blue"))
            elif cultivo == "Soja 2da":
                data_to_plot.append((cultivo, rinde, cultivo_limits[cultivo], 4, rindeprom, "red", rindeinf, "blue"))
            elif cultivo == "Girasol":
                data_to_plot.append((cultivo, rinde, cultivo_limits[cultivo], 4, rindeprom, "red", rindeinf, "blue"))
            elif cultivo == "Sorgo":
                data_to_plot.append((cultivo, rinde, cultivo_limits[cultivo], 4, rindeprom, "red", rindeinf, "blue"))
            elif cultivo == "Maíz":
                data_to_plot.append((cultivo, rinde, cultivo_limits[cultivo], 4, rindeprom, "red", rindeinf, "blue"))
            elif cultivo == "Cebada":
                data_to_plot.append((cultivo, rinde, cultivo_limits[cultivo], 4, rindeprom, "red", rindeinf, "blue"))
        
        # Aumentar el tamaño de la fuente de los nombres de los cultivos
        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=15)
        
        
        if data_to_plot is not None:
            container = f'<div style="display: flex; justify-content: space-between; align-items: center;">'
            texto = "Rendimiento por cultivo"
            right.write(f"{container}<span style='font-size: 12px; color: #808080; font-family: Source Sans Pro, sans-serif;'>{texto}</span>", unsafe_allow_html=True)
            r = f'<div style="width: 10px; height: 10px; background-color: #f25911; display: inline-flex;"></div>'
            r1 = f'<div style="width: 10px; height: 10px; background-color: #fcce59; display: inline-flex;"></div>'
            r2 = f'<div style="width: 10px; height: 10px; background-color: #ABDDA4; display: inline-flex;"></div>'
            r3 = f'<div style="width: 10px; height: 10px; background-color: #1A9641; display: inline-flex;"></div>'
            r4 = f'<div style="width: 20px; height: 3px; background-color: #f25911; display: inline-flex;"></div>'
            r5 = f'<div style="width: 20px; height: 3px; background-color: #0000ff; display: inline-flex;"></div>'
            texto1 = f"<span style='font-size: 12px; font-family: Source Sans Pro, sans-serif;'>{r} Malo {r1} Regular {r2} Bueno {r3} Excelente {r4} RindeRegion {r5} RindeIndif</span><br><span style='font-size: 12px; font-family: Source Sans Pro, sans-serif;'>RindeRegion es el promedio de las ultimas 5 campañas en la región. Rindeindif es rinde necesario para cubrir los costos de producción (incluido arrendamientos)</span>"
            right.write(f"{container}<span style='font-size: 12px; color: #000000; font-family: Source Sans Pro, sans-serif;'>{texto1}</span>", unsafe_allow_html=True)
        
        # Agrupar los datos por cultivo
        
        grouped_data = pd.DataFrame(data_to_plot, columns=["Cultivo", "Rinde", "Limits", "O", "M", "X", "Z", "Y"]).groupby("Cultivo")
        
        # Iterar sobre los grupos para generar un gráfico de bullet por cada cultivo
        colors = ['#000000', '#f7f7f7', '#2ca02c', '#ff7f0e']
        for cultivo, group in grouped_data:
            bulletgraph(group.values.tolist(), limits=cultivo_limits[cultivo], labels=[], size=(8,5),
                        label_color="black", bar_color=colors[0], target_color=colors[1], show_title=False)
            plt.box(False)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            right.pyplot()
      

    if dfp is not None and df1 is None:
        st.write ("Sin planteo productivo o falta cargar gastos de estructura")
        
    if dfs is not None or dfx is not None or dfa is not None:
        if (dfs is not None and dfx is not None) or (dfs is not None and dfa is not None) or (dfx is not None and dfa is not None):
            right, left = st.columns(2)
        else:
            left = st
        if dfs is not None:
            valuacion_total = st.session_state.dfs['Valuación'].sum()
            left.subheader(f"Existencia de granos: ${valuacion_total:,}")
            left.table(dfs.style.format({"Cantidad (tn)":"{:.0f}", "Valuación":"${:,}"}))
        if dfx is not None:
            valuacion_total = st.session_state.dfx["Ingreso estimado"].sum()
            if right:
                right.subheader(f"Ingresos Serv. agrícolas: ${valuacion_total:,}")
                right.table(dfx.style.format({"Superficie(ha)":"{:.0f}", "Precio":"${:,}", "Ingreso estimado":"${:,}"}))
            else:
                left.subheader(f"Ingresos Serv. agrícolas: ${valuacion_total:,}")
                left.table(dfx.style.format({"Superficie(ha)":"{:.0f}", "Precio":"${:,}", "Ingreso estimado":"${:,}"}))
        if dfa is not None:
            valuacion_total = st.session_state.dfa['Valuación'].sum()
            if right:
                right.subheader(f"Existencia de hacienda: ${valuacion_total:,}")
                right.table(dfa.style.format({"Cantidad":"{:.0f}", "Peso":"{:.0f}", "Valuación":"${:,}"}))
            else:
                left.subheader(f"Existencia de hacienda: ${valuacion_total:,}")
                left.table(dfa.style.format({"Cantidad":"{:.0f}", "Peso":"{:.0f}", "Valuación":"${:,}"}))
  
        
    #topLeftMargin * 20 es donde manejas el ancho
    #allowTaint: true, scale: 3  es la definicion
    if st.button(BUTTON_TEXT):
        components.html(
                f"""
        <script>{HTML_2_CANVAS}</script>
        <script>{JSPDF}</script>
        <script>
        const html2canvas = window.html2canvas
        const {{ jsPDF }} = window.jspdf
        
        const streamlitDoc = window.parent.document;
        const stApp = streamlitDoc.querySelector('.main > .block-container');
        
        const buttons = Array.from(streamlitDoc.querySelectorAll('.stButton > button'));
        const pdfButton = buttons.find(el => el.innerText === '{BUTTON_TEXT}');
        const docHeight = stApp.scrollHeight;
        const docWidth = stApp.scrollWidth;
        
        let topLeftMargin = 30;
        let pdfWidth = docHeight + (topLeftMargin * 17);
        let pdfHeight = (pdfWidth * 1.5) + (topLeftMargin * 2);
        let canvasImageWidth = docWidth;
        let canvasImageHeight = docHeight;
        
        let totalPDFPages = Math.ceil(docHeight / pdfHeight)-1;
        
        pdfButton.innerText = 'Creating PDF...';
        
        html2canvas(stApp, {{ allowTaint: true, scale: 3 }}).then(function (canvas) {{
        
            canvas.getContext('2d');
            let imgData = canvas.toDataURL("image/jpeg", 1.0);
        
            let pdf = new jsPDF('p', 'px', [pdfWidth, pdfHeight]);
            pdf.addImage(imgData, 'JPG', topLeftMargin, topLeftMargin, canvasImageWidth, canvasImageHeight);
        
            for (var i = 1; i <= totalPDFPages; i++) {{
                pdf.addPage();
                pdf.addImage(imgData, 'JPG', topLeftMargin, -(pdfHeight * i) + (topLeftMargin*4), canvasImageWidth, canvasImageHeight);
            }}
        
            pdf.save('test.pdf');
            pdfButton.innerText = '{BUTTON_TEXT}';
        }})
        </script>
        """,
                    height=0,
                    width=0,
                )


#configuraciones de página   
#lottie_book = load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_d7OjnJ.json')
with st.sidebar:
    url = "https://raw.githubusercontent.com/Jthl1986/T1/master/logo.png"
    st.markdown(f'<div style="margin-top: -140px;"><img src="{url}" style="object-fit: cover; width: 100%; height: 100%;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 style="margin-top: -110px; text-align: center;">AgroApp</h1>', unsafe_allow_html=True)
my_button = st.sidebar.radio("Modulos",('Planteo productivo', 'Condiciones climáticas', 'Tenencia granos', 'Tenencia hacienda', 'Servicios agrícolas', 'Sitios de utilidad', 'Cuadro resumen'))
if my_button == 'Tenencia hacienda':
    app()
elif my_button == 'Tenencia granos':
    app1()
elif my_button == 'Servicios agrícolas':
    app2()
elif my_button == 'Condiciones climáticas':
    app3()
elif my_button == 'Sitios de utilidad':
    app9()
elif my_button == 'Cuadro resumen':
    app5()
else:    
    app4()
  
rss_url = "https://bichosdecampo.com/feed/"
rss_url1 = "https://www.infocampo.com.ar/feed/"
rss_url2 = "https://www.clarin.com/rss/rural/"
feed = feedparser.parse(rss_url)
feed1 = feedparser.parse(rss_url1)
feed2 = feedparser.parse(rss_url2)



with st.sidebar:
    st.markdown("---")
    st.markdown('<h4 style="margin-top: -25px; text-align: left;">Noticias</h4>', unsafe_allow_html=True)
    with st.spinner('Cargando noticias...'):
        news_html = ""
        for item in feed["items"][:10]:
            news_html += f'<a href="{item["link"]}" target="_blank">{item["title"]}</a> | '
        st.components.v1.html(f'<marquee behavior="scroll" direction="left" scrollamount="6">{news_html}</marquee>', height=30)
    with st.spinner('Cargando noticias...'):
        news_html = ""
        for item in feed1["items"][:10]:
            news_html += f'<a href="{item["link"]}" target="_blank">{item["title"]}</a> | '
        st.components.v1.html(f'<marquee behavior="scroll" direction="left" scrollamount="4">{news_html}</marquee>', height=30)
    with st.spinner('Cargando noticias...'):
        news_html = ""
        for item in feed2["items"][:10]:
            news_html += f'<a href="{item["link"]}" target="_blank">{item["title"]}</a> | '
        st.components.v1.html(f'<marquee behavior="scroll" direction="left" scrollamount="2">{news_html}</marquee>', height=30)
    st.markdown("---")
    st.caption("Desarrollado por JSantacecilia y JSaborido para Equipo Agro Banco Credicoop")
    st.caption("Datos del Informe Diciembre 2023 SAGYP")
    abrir_google_maps()
    #st_lottie(lottie_book, speed=0.5, height=50, key="initial")
