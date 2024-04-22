from urllib import request
import requests
import os


def is_pdf(url):
    # Send a HEAD request to get the response headers
    response = requests.head(url)
    
    # Get the content type from the response headers
    content_type = response.headers.get('Content-Type', '')
    
    # Check if 'pdf' is present in the content type
    return 'pdf' in content_type.lower()

def is_pdf_or_website(url):
    # Check if the URL ends with '.pdf'
    if url.lower().endswith('.pdf'):
        return True
    return is_pdf(url)

def download_pdf(url: str, pdf_file_name: str) -> str:
    """Download PDF from given URL to local directory using proxy."""
    try:


        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = request.Request(url, headers=headers)
        with request.urlopen(req) as response:
            if response.status == 200:
                current_path=f'{os.getcwd()}/pdf/'
                filepath = os.path.join(current_path, pdf_file_name)
                with open(filepath, 'wb') as pdf_object:
                    pdf_object.write(response.read())
                print(f'{pdf_file_name} was successfully saved!')
                return filepath  # Return the path to the downloaded PDF file
            else:
                print(f'Uh oh! Could not download {pdf_file_name}, HTTP response status code: {response.status}')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

 