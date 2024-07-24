
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_image(url, folder_name, image_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, image_name), 'wb') as f:
            f.write(response.content)


# What you enter here will be searched for in
# Google Images
query = "dogs"
 
# Creating a webdriver instance
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
 
# Maximize the screen
driver.maximize_window()
 
# Open Google Images in the browser
driver.get('https://images.google.com/')
 
box = driver.find_element(By.NAME, 'q')
box.send_keys(query)
box.send_keys(Keys.ENTER)


 
# Function for scrolling to the bottom of Google
# Images results
def scroll_to_bottom():
 
    last_height = driver.execute_script('\
    return document.body.scrollHeight')
 
    while True:
        driver.execute_script('\
        window.scrollTo(0,document.body.scrollHeight)')
 
        # waiting for the results to load
        # Increase the sleep time if your internet is slow
        time.sleep(3)
 
        new_height = driver.execute_script('\
        return document.body.scrollHeight')
 
        # click on "Show more results" (if exists)
        try:
            driver.find_element_by_css_selector(".YstHxe input").click()
 
            # waiting for the results to load
            # Increase the sleep time if your internet is slow
            time.sleep(3)
 
        except:
            pass
 
        # checking if we have reached the bottom of the page
        if new_height == last_height:
            break
 
        last_height = new_height
 
 
# Calling the function
 
# NOTE: If you only want to capture a few images,
# there is no need to use the scroll_to_bottom() function.
scroll_to_bottom()

create_folder("dfz")

image_set = set()
downloaded_images = 0
 
 
# Loop to capture and save each image
for i in range(1, 50):
   
    # range(1, 50) will capture images 1 to 49 of the search results
    # You can change the range as per your need.
    try:
 
      # XPath of each image
        images = driver.find_elements(By.TAG_NAME, 'img') 
        print("imgs: ", images)

        for idx, image in enumerate(images):
            print("image: ", image)
            try:
                image.click()
                time.sleep(2)
                # Encuentra la imagen completa en el panel lateral
                full_images = driver.find_elements(By.TAG_NAME, 'img')
                for full_image in full_images:
                    src = full_image.get_attribute('src')
                    if src and 'http' in src and src not in image_set:
                        download_image(src, "dfz", f'image_{downloaded_images}.jpg')
                        image_set.add(src)
                        downloaded_images += 1
                        break
            except Exception as e:
                print(f"Error al descargar la imagen: {e}")
        # driver.find_element_by_xpath(
            #'//*[@id="islrg"]/div[1]/div[' +
          #str(i) + ']/a[1]/div[1]/img')
 
        # Enter the location of folder in which
        # the images will be saved
        images.screenshot('test' + 
                       query + ' (' + str(i) + ').png')
        # Each new screenshot will automatically
        # have its name updated
 
        # Just to avoid unwanted errors
        time.sleep(0.2)
 
    except:
         
        # if we can't find the XPath of an image,
        # we skip to the next image
        continue
 
# Finally, we close the driver
driver.close()