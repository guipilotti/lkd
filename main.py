
import time
import os
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json

# Credenciais Google embutidas
credentials_dict = {
  "type": "service_account",
  "project_id": "your_project_id",
  "private_key_id": "your_private_key_id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your_client_id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
with open("credentials.json", "w") as f:
    json.dump(credentials_dict, f)

# Configurações
li_at = os.environ.get("LI_AT")
spreadsheet_name = "Linkedin_Assistant"
sheet_name = "PostsFeed"
linkedin_url = "https://www.linkedin.com/search/results/content/?keywords=intelig%C3%AAncia%20artificial%20OR%20produto%20OR%20tecnologia&network=%5B%22F%22%5D&sortBy=%22date_posted%22"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://www.linkedin.com")
driver.add_cookie({"name": "li_at", "value": li_at, "domain": ".linkedin.com"})
driver.get(linkedin_url)
time.sleep(5)

for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

posts_data = []
posts = driver.find_elements(By.CLASS_NAME, "update-components-text")

for post in posts:
    try:
        texto = post.text.strip()
        if texto and len(texto) > 30:
            parent = post.find_element(By.XPATH, "..")
            link = parent.get_attribute("href") or ""
            autor = parent.get_attribute("aria-label") or ""
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            posts_data.append((texto, link, autor, timestamp))
    except:
        continue

driver.quit()

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open(spreadsheet_name).worksheet(sheet_name)
dados_existentes = sheet.col_values(1)

for texto, link, autor, data in posts_data:
    if texto not in dados_existentes:
        sheet.append_row([texto, link, autor, data, "Novo"])
        print(f"[✔] Post adicionado: {texto[:50]}...")

print("✅ Crawler finalizado.")
