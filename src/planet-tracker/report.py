from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

def all_company(driver):
    company_dropdown = driver.find_element(By.NAME, "ptp_filter_tax_company")
    print(company_dropdown)
    # Extract options and their values
    options = company_dropdown.find_elements(By.TAG_NAME, "option")
    dropdown_values = [option.get_attribute("value") for option in options if option.get_attribute("value")]

    print(len(dropdown_values))

    import pandas as pd

    data={"company_name": dropdown_values}
    df = pd.DataFrame(data)
    df.to_excel('all_company_name.xlsx', index=False)

def clean_filename(name):
    """Clean the company name to make it suitable for a filename."""
    # Replace characters not allowed in filenames with underscores
    clean_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name)
    return clean_name.strip()

def scrape_report(link: str):
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
    time.sleep(10)
    company_dropdowns = driver.find_elements(By.XPATH, "//span[@class='select2-selection__rendered']")
    # time.sleep(3)
    # # Locate the text box within the dropdown and type text into it
    # text_box = driver.find_element(By.XPATH, "//span[@class='select2-search select2-search--dropdown']/input[@class='select2-search__field']")
    # text_box.send_keys("Report")
    # # Press Enter to confirm the selection
    # text_box.send_keys(Keys.ENTER)


    df=pd.read_excel('all_company_name_2.xlsx')
        # Initialize lists for each column
    Image = []
    Title = []
    Link_Title=[]
    Summary = []
    Date = []
    for data in df['company_name']:


        company_dropdowns[3].click()

        time.sleep(3)

        # Locate the text box within the dropdown and type text into it
        text_box = driver.find_element(By.XPATH, "//span[@class='select2-search select2-search--dropdown']/input[@class='select2-search__field']")
        text_box.send_keys(data)

        # Press Enter to confirm the selection
        text_box.send_keys(Keys.ENTER)

        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//tbody/tr")))

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
        clean_data = clean_filename(data)
        df.to_excel(f'data/{clean_data}_Report.xlsx', index=False)
        Image = []
        Title = []
        Link_Title=[]
        Summary = []
        Date = []




    print("Scraping Completed")
    driver.quit()



if __name__ == "__main__":
    link = "https://planet-tracker.org/reports/"
    scrape_report(link)
