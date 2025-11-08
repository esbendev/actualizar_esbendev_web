from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
import os

def descargar_imagen(nombre_imagen, url, path):
    if not os.path.exists(path):
        os.makedirs(path)
    r = requests.get(url)
    with open (f"{path}{nombre_imagen}.{url.split('.')[-1]}", "wb") as archivo:
        archivo.write(r.content)

def armar_tarjeta(titulo, url, thumbnail):
    return f"""
            <div class="tarjeta-video">
                <a href="{url}" target="_blank">
                    <img src="./imagenes/thumbnails/{thumbnail}.webp" alt="thumbnail para video con título: {titulo}">
                    <h3>{titulo}</h3>
                </a>
            </div>"""

def actualizar_pagina(pagina, tarjetas):
    with open(pagina, 'r') as archivo:
        contenido = archivo.read()
        inicio_tarjetas = contenido.find("<!-- INICIO TARJETAS VIDEOS -->")
        fin_tarjetas = contenido.find("<!-- FIN TARJETAS VIDEOS -->")
        contenido = contenido[:inicio_tarjetas] + "<!-- INICIO TARJETAS VIDEOS -->" + tarjetas + "\n            " + contenido[fin_tarjetas:]
    with open(pagina, 'w') as archivo:
        archivo.write(contenido)


def buscar_info_para_tarjetas(url):
    with sync_playwright() as p:
        #browser = p.chromium.launch()
        browser = p.chromium.connect("ws://0.0.0.0:3000/")
        page = browser.new_page()
        page.goto(url)
        print("yendo") 
        try:
            page.wait_for_selector('#contents', timeout=60000)
            videos = page.query_selector_all('#video-title-link')[:5]
            tarjetas = ""
            for video in videos:
                titulo_video = video.inner_text()
                id_video = video.get_attribute('href').split('=')[-1]
                thumbnail = f"https://i.ytimg.com/vi_webp/{id_video}/maxresdefault.webp"
                url_video = f"https://www.youtube.com/watch?v={id_video}"
                print(f"Titulo: {titulo_video}\nURL: {url_video}\nThumbnail: {thumbnail}\n")
                descargar_imagen(id_video ,thumbnail, dir_imagenes)
                tarjetas += armar_tarjeta(titulo_video, url_video, id_video)
            return tarjetas
        except PlaywrightTimeoutError:
            print("Timeout while waiting for the video list to load.")
        
        browser.close()

if __name__ == "__main__":
    # channel_url = "https://www.youtube.com/@esbendev/videos"
    channel_url = "https://www.youtube.com/@esbendev/videos?hl=es&persist_hl=1"
    path_principal = "../esbendev.github.io/"
    dir_imagenes = f"{path_principal}imagenes/thumbnails/"
    archivo_pagina_es = f"{path_principal}index.html"
    archivo_pagina_en = f"{path_principal}index-en.html"
    print(".")
    tarjetas = buscar_info_para_tarjetas(channel_url)
    actualizar_pagina(archivo_pagina_en,tarjetas)
    actualizar_pagina(archivo_pagina_es,tarjetas)
