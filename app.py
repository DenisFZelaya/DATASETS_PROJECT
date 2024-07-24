import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_image(url, folder_name, image_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, image_name), 'wb') as f:
            f.write(response.content)

def get_images(query, folder_name, max_images=100):
    # Configura el navegador (en este caso, Chrome)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Abre Google Images
    # https://www.google.com/search?q
    driver.get('https://images.google.com/')

    # Encuentra la barra de búsqueda y realiza la búsqueda
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)

    # Espera a que se carguen las imágenes
    time.sleep(2)

    # Crea la carpeta para almacenar las imágenes
    create_folder(folder_name)

    # Variables para el control de flujo
    downloaded_images = 0
    image_set = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while downloaded_images < max_images:
        # Encuentra todos los elementos de imagen en los resultados
        time.sleep(2)
        images = driver.find_elements(By.TAG_NAME, 'img')
        print("Images: ", images)
        for idx, image in enumerate(images):
            if downloaded_images >= max_images:
                break
            try:
                image.click()
                time.sleep(2)
                # Encuentra la imagen completa en el panel lateral
                full_images = driver.find_elements(By.TAG_NAME, 'img')
                for full_image in full_images:
                    src = full_image.get_attribute('src')
                    if src and 'http' in src and src not in image_set:
                        download_image(src, folder_name, f'image_{downloaded_images}.jpg')
                        image_set.add(src)
                        downloaded_images += 1
                        break
            except Exception as e:
                print(f"Error al descargar la imagen: {e}")

        # Desplázate hacia abajo y espera a que se carguen más imágenes
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Calcula la nueva altura del documento y verifica si se han cargado más imágenes
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No se han cargado más imágenes. Deteniendo.")
            break
        last_height = new_height

    # Cierra el navegador
    driver.quit()

# Parámetros
query = 'gatos'
folder_name = 'imagenes_gatos'
max_images = 100

# Obtener imágenes
get_images(query, folder_name, max_images)
