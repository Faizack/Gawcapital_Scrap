from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

def scrape_report(link: str, num_pages: int):
    """Scrape certificate data from a website."""
    options = Options()
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(link)

    try:
        accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "mgbutton")))
        accept_button.click()
    except:
        print("Failed to click on")
        pass  # If accept button not found or clickable, continue without accepting


    import time
    time.sleep(15)


    # Initialize lists for each column
    Image = []
    Title = []
    Link_Title=[]
    Summary = []
    Date = []

    for i in range(1, num_pages + 1):
        page_number = str(i)
        print("Scraping page:", page_number)
        
        # Wait until the page number link is present and clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, page_number)))
        
        # Click on the page number link
        driver.find_element(By.LINK_TEXT, page_number).click()
        
        # Wait for the table to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody/tr")))
        
        # Get the HTML of the table
        table_html = driver.page_source
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(table_html, 'html.parser')
        
        # Find all rows in the table body
        rows = soup.find_all('tr')
        
        # Iterate over each row and extract data
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 4:
                # Extract image URL
                img_tag = cells[0].find('img')
                if img_tag:
                    Image.append(img_tag.get('data-src'))
                else:
                    Image.append(None)

                Title_text = cells[1].text.strip()
                # Extract title and link separately
                title_link = cells[1].find('a')
                if title_link:
                    Title.append(title_link.text.strip())  # Extract title
                    Link_Title.append(title_link.get('href'))  # Extract link from title
                else:
                    Title.append(Title_text)
                    Link_Title.append(None)

                Summary.append(cells[2].text.strip())  # Extract summary
                Date.append(cells[3].text.strip())     # Extract date



    # Create DataFrame from the collected columns
    df = pd.DataFrame({
        "Image_Url": Image,
        "Title": Title,
        "Link_Title": Link_Title,
        "Summary": Summary,
        "Date": Date,
    })

    # Save DataFrame to Excel file
    df.to_excel('Report_Only_DataBase.xlsx', index=False)

    print("Scraping Completed")
    driver.quit()

if __name__ == "__main__":
    link = "https://planet-tracker.org/reports/"
    num_pages = 5 
    scrape_report(link, num_pages)
