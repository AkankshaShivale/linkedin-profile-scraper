import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Edge browser configuration
options = Options()
options.add_argument("--start-maximized") 

# Path to msedgedriver.exe
service = Service("C:\\LinkedIn_Profile_Scrapping\\edgedriver_win64\\msedgedriver.exe")

# Initialize WebDriver for Edge
driver = webdriver.Edge(service=service, options=options)


driver.get('https://www.linkedin.com/login')

email = 'Your linkedin login email' # Please change this before you run the code.
password = 'Your linkedin login password' # Please change this before you run the code.

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(email)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)

# Login button click 
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@class="btn__primary--large from__button--floating"]'))
)
login_button.click()
 
first_name = "firstname"
last_name = "lastname"


search_query = f"{first_name} {last_name}"

# To locate search bar and input above query. 
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]'))
)
search_box.clear()
search_box.send_keys(search_query)

# Search button click 
search_box.send_keys(Keys.RETURN)

see_all_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "See all people results"))
)
see_all_link.click()

# wait until search results load  
results_container = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/in/")]'))
)

profile_links = []
try:
    for result in results_container[:5]:  
        profile_link = result.get_attribute("href")
        if profile_link: 
            profile_links.append(profile_link)
except TypeError as e:
    print(f"TypeError occurred: {e}")

# check profile links found or not
if not profile_links:
    print("No valid profile links found.")
    driver.quit()
    exit()


for index, link in enumerate(profile_links, start=1):
    print(f"Profile {index}: {link}")


output_file = "linkedin_profiles.csv"
fieldnames = ["Name", "Headline", "Location"]

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for profile_link in profile_links:
        driver.get(profile_link)  # Navigate to each profile
        time.sleep(2) 

        try:
            name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/overlay/about-this-profile/")]//h1'))
            ).text
        except:
            name = 'Not Found'

        try:
            headline = driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium.break-words').text
        except:
            headline = 'Not Found'

        try:
            location = driver.find_element(By.CSS_SELECTOR, 'span.text-body-small.inline.t-black--light.break-words').text
        except:
            location = 'Not Found'

        writer.writerow({
            "Name": name,
            "Headline": headline,
            "Location": location
        })

print(f"Data saved to {output_file}")
