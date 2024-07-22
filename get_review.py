from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

def get_review_text(link):
    review = ""
    image_link = ""
    
    driver.get(link)
    try:
        review = driver.find_elements(By.CLASS_NAME, "reviewText")[0].text
    except AttributeError:
        review = driver.find_elements(By.CLASS_NAME, "reviewText")[0]
    except:
        review = ""
    
    
    left_container = driver.find_elements(By.CLASS_NAME, "leftAlignedImage")[0]
    anchor_tag = left_container.find_elements(By.TAG_NAME, "a")[0]
    image_tag = anchor_tag.find_elements(By.TAG_NAME, "img")[0]
    image_link = image_tag.get_attribute("src")
    
    return review, image_link