from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import json
import colorama
from get_review import get_review_text


driver = webdriver.Chrome()
driver.get("https://www.goodreads.com/review/list/151962059")
pagination_elements = driver.find_elements(By.ID, "reviewPagination")[0].text
num_of_pages = int(pagination_elements.split()[2:-2][-1])
page_list = [str(i) for i in range(1, num_of_pages+1)]
page_list = [int(page) for page in page_list[:1]]


dict_store = []

rating_ref = {
    "it was amazing": 5,
    "really liked it": 4,
    "liked it": 3,
    "it was ok": 2,
    "did not like it": 1
}

print(colorama.Fore.BLUE + "Scraping Data...")
for page in tqdm(page_list):
    # print(colorama.Fore.GREEN + f"Page {page}"+ colorama.Style.RESET_ALL)
    driver.get(f"https://www.goodreads.com/review/list/151962059?page={page}&shelf=read")
    bookalike_reviews = driver.find_elements(By.CLASS_NAME, "bookalike")
    for review in bookalike_reviews:
        
        try:
            title = review.find_elements(By.CLASS_NAME, "title")[0].text
        except:
            title = "N/A"
            
        try:
            author = review.find_elements(By.CLASS_NAME, "author")[0].text
        except:
            author = "N/A"
        
        try:
            avg_rating = float(review.find_elements(By.CLASS_NAME, "avg_rating")[0].text)
        except:
            avg_rating = -1
        
        try:
            my_rating = rating_ref[review.find_elements(By.CLASS_NAME, "rating")[0].find_elements(By.CLASS_NAME, "value")[0].find_elements(By.TAG_NAME, "span")[0].get_attribute("title")]
        except:
            my_rating = -1
        
        try:
            read_date = review.find_elements(By.CLASS_NAME, "date_read_value")[0].text
        except:
            read_date = "N/A"
        
        #Get id of element
        review_id = review.get_attribute("id").replace("review_", "")
        review_link = f"https://www.goodreads.com/review/show/{review_id}"
        
        my_review, image_link = get_review_text(review_link)
        
        dict_store.append({
            "title": title,
            "author": author,
            "avg_rating": avg_rating,
            "my_rating": my_rating,
            "read_date": read_date,
            "review_link": review_link,
            "my_review": my_review,
            "image_link": image_link
        })

print(colorama.Fore.GREEN + "Data Scraped Successfully!"+ colorama.Style.RESET_ALL)
file_path = "exports/export.json"
json_data = json.dumps(dict_store, indent=4)
with open(file_path, "w") as file:
    file.write(json_data)
print(colorama.Fore.GREEN + f"Data Exported to {file_path}"+ colorama.Style.RESET_ALL)
