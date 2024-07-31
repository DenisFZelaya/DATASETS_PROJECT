import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import wget

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_image(url, folder_name, image_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, image_name), 'wb') as f:
            f.write(response.content)


def get_images_bing(query, folder_name, max_images=100):
    # Configura el navegador (en este caso, Chrome)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Abre Bing Images
    driver.get('https://www.bing.com/images')

    # Encuentra la barra de búsqueda y realiza la búsqueda
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Espera a que se carguen las imágenes
    time.sleep(2)

    # Crea la carpeta para almacenar las imágenes
    create_folder(folder_name)

    # Variables para el control de flujo
    downloaded_images = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    image_set = set()
    urls_imagenes = []

    while downloaded_images < max_images:
        # Encuentra todos los elementos de imagen en los resultados dentro del div con la clase "dg_b isvctrl"
        div_containers = driver.find_elements(By.CLASS_NAME, 'dg_b.isvctrl')
        for div in div_containers:
            if downloaded_images >= max_images:
                break
            images = div.find_elements(By.TAG_NAME, 'img')
            for idx, image in enumerate(images):
                src = image.get_attribute('src')

                urls_imagenes.append(src)
                downloaded_images += 1

                #
                if downloaded_images >= max_images:
                    break
        # Desplázate hacia abajo y espera a que se carguen más imágenes
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Calcula la nueva altura del documento y verifica si se han cargado más imágenes
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No se han cargado más imágenes. Deteniendo.")
            
            break
        last_height = new_height

    
    for idx, url in enumerate(urls_imagenes):
        try:
            image_name = os.path.join(folder_name, f'image_{idx+1}.jpg')
            wget.download(url, image_name)
            print(f"\nImagen guardada como {image_name}")
            
        except Exception as e:
            print("Error al descargar la imagen: ", url)


    # Cierra el navegador
    driver.quit()

# Parámetros
query = 'Catarata ocular'
folder_name = '/datasets/Catarata'
max_images = 200

# Obtener imágenes
get_images_bing(query, folder_name, max_images)
