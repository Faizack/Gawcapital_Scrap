import os
import json
import pandas as pd
pd.options.mode.chained_assignment = None
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from utility import download_pdf,is_pdf_or_website

def scrape_links(df, pdf_dir='pdf/', json_dir='json/'):
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)
    
    for index, row in df.iterrows():
        link = row['link']
        file_name = str(index)  # Extract file name from the link
        print("File Name : ",file_name)
        
        if  is_pdf_or_website(link):
            options = Options()
            mobile_emulation = {
                "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36"
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            
            driver = webdriver.Chrome(options=options)
            driver.get(link)
            pdf_name=f'{file_name}.pdf'
            pdf_source = download_pdf(link, pdf_name)
            
            # Update DataFrame with source of PDF
            df.loc[index, 'source'] = 'pdf'
            df.loc[index, 'source_path'] = pdf_source
            
        else:
            options = Options()
            options.add_argument("window-size=1920,1080")
            driver = webdriver.Chrome(options=options)
            driver.set_window_size(1920, 1080)
            driver.get(link)
            try:
                # Initial load using Selenium

                # Wait for page to load completely
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                # Extract page source after loading with Selenium
                page_source = driver.page_source

                # Process page source with BeautifulSoup
                soup = BeautifulSoup(page_source, 'html.parser')

                # Extract name and keywords
                name = soup.title.string.strip()
                keywords = [word.strip() for word in name.split()]

                # Initialize content dictionary
                content = {
                    "name": name,
                    "keywords": keywords,
                    "url": link,
                    "content": {
                        "headings": [],
                        "span_tags": [],
                        "p_tags": []
                    }
                }

                # Extract headings, articles, and paragraphs
                headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                for heading in headings:
                    heading_content = heading.get_text().strip()
                    articles = []
                    article = {
                        "content": "",
                        "paragraphs": []
                    }
                    next_element = heading.find_next_sibling()
                    while next_element and next_element.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        if next_element.name == 'p':
                            article["paragraphs"].append({"content": next_element.get_text().strip()})
                        elif next_element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                            break
                        else:
                            article["content"] += next_element.get_text().strip() + " "
                        next_element = next_element.find_next_sibling()
                    if article["content"] or article["paragraphs"]:
                        articles.append(article)
                    content["content"]["headings"].append({
                        "tag": heading.name,
                        "content": heading_content,
                        "articles": articles
                    })

                # Extract span tags
                spans = soup.find_all('span')
                for span in spans:
                    content["content"]["span_tags"].append({"content": span.get_text().strip()})

                # Extract p tags
                paragraphs = soup.find_all('p')
                for paragraph in paragraphs:
                    content["content"]["p_tags"].append({"content": paragraph.get_text().strip()})

                # Save scraped data to JSON
                json_path = os.path.join(json_dir, f'{file_name}.json')
                with open(json_path, 'w') as json_file:
                    json.dump({"data": content}, json_file)

                # Update DataFrame with source of JSON data
                df.loc[index, 'source'] = 'json'
                df.loc[index, 'source_path'] = json_path

            except Exception as e:
                print(f"Error processing link {link}: {e}")
            
            finally:
                driver.quit()  # Close the WebDriver session
    
    return df

if __name__ == '__main__':

    df=pd.read_excel('data/Keywords.xlsx',sheet_name="Wilmar International")
    df1=df
    df3 = scrape_links(df1)
    df3.to_csv("dum.csv",index=False)