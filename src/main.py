from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_all_links(link):
    options = Options()
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.get(link)

    list_of_links = []

    # Initial load
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "link-for-btn-load-more")))

    for i in range(1, 10):  # Change range if needed
        # Execute JavaScript function to load more content
        driver.execute_script(f"loadmore({i});")

        # Wait for the new content to be loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='loop-container']")))

        # Find all loop-container elements
        loop_containers = driver.find_elements(By.CLASS_NAME, "loop-container")

        for loop_container in loop_containers:
            # Scrape links from each loop-container
            links = loop_container.find_elements(By.XPATH, ".//a[@href]")
            list_of_links.extend([link.get_attribute("href") for link in links])

    print("Scraping Completed")
    driver.quit()

    return list_of_links



def scrape_data(urls):
    data_list = []
    for url in urls:
        # Retrieve HTML content from the URL
        html_content = requests.get(url).content

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract relevant information
        title_element = soup.find('h1')
        status_element = soup.find('p', class_='exited')
        description_element = soup.find('div', class_='profo-main')
        image_element = soup.find('div', class_='featured-media-inner').find('img')

        # Check if the elements exist before accessing their attributes
        if title_element:
            title = title_element.text.strip()
        else:
            title = "Title not found"

        if status_element:
            status = status_element.text.strip()
        else:
            status = "Not exited"

        if description_element:
            description = description_element.text.strip()
        else:
            description = "Description not found"

        if image_element:
            image_url = image_element.get('src')
        else:
            image_url = "Image URL not found"

        # Find and extract area and asset management information
        area_element = soup.find('div', class_='metatitle', text='Area')
        if area_element:
            area = area_element.find_next_sibling('p', class_='metadata').text.strip()
        else:
            area = "Area not specified"

        asset_management_element = soup.find('div', class_='metatitle', text='Asset Management')
        if asset_management_element:
            asset_management = asset_management_element.find_next_sibling('p', class_='metadata').text.strip()
        else:
            asset_management = "Asset Management not specified"

        # Append extracted data to the list
        data_list.append({
            'Title': title,
            'Status': status,
            'Description': description,
            'Image URL': image_url,
            'Area': area,
            'Asset Management': asset_management
        })

    # Create DataFrame
    df_output = pd.DataFrame(data_list)

    # Write DataFrame to CSV
    df_output.to_excel('output.xlsx', index=False)

    print('Excel file has been created successfully.')




if __name__ == "__main__":
    link = "https://www.gawcapital.com/portfolio/"
    all_links = scrape_all_links(link)
  
    df = pd.DataFrame({'Links': all_links})
    
    # Save DataFrame as CSV
    df.to_csv('links.csv', index=False)

    # Scrape data from the links
    scrape_data(all_links)
