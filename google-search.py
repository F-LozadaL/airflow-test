import re
import requests
import pandas as pd

def clean_filename(filename):
    """
    Function to clean up string to be used as filename
    
    :param filename: the original string to be cleaned aup
    
    :return: Cleaned up string safe for use as a filename
    """
    filename = re.sub(r'[\\/*?:"<>|]', "" , filename ) #remove special characters
    return filename

def build_payload(query, start=1, num=10, date_restrict='m1', **params):
    """
    
    :param query: search term
    :param start: the index of the first result to return
    :param link-site: Specifies that all search results should contain a link to a particular URL
    :param search_type: Type of search(default is undefined, 'IMAGE' is for image search)
    :param date_restrict: Restricts results based on  recency (default is one month 'm1')
    :param params: Additional parameters for the API requests    
    """
    payload={
        'key':API_KEY,
        'q':query,
        'cx':SEARCH_ENGINE_ID,
        'start':start,
        'num':num,
        'dateRestrict':date_restrict,
    }
    
    payload.update(params)
    return payload

def make_requests(payload):
    """
    Function to send a GET request to the Google Search API and handle potential errors
    
    :param payload: Dictionary contaning the API requests parameters
    :return: JSON response from the API
    """  
    
    response = requests.get('https://www.googleapis.com/customsearch/v1',params=payload)
    if response.status_code!=200:
        raise Exception('Request Failed')
    return response.json()  
    
def main (query, result_total=10):
    """
    main function  to execute the script
    """
    items = []
    reminder = result_total%10
    if reminder > 0 :
        pages =(result_total//10) +1
    else:
        pages = result_total//10
        
    for i in range(pages):
        if pages == i + 1 and reminder>0:
            payload= build_payload(query, start=(i+1)*10, num = reminder)
        else:
            payload = build_payload(query, start=(i+1)*10)
        response= make_requests(payload)
        items.extend(response['items'])
    
    query_string_clean=clean_filename(query)
    df= pd.json_normalize(items)
    df.to_csv('Google Search Result_{0}.csv'.format(query_string_clean),index=False)        
if __name__ == '__main__':
    API_KEY = 'AIzaSyDgP-fyXWYXwhJZFLh1veEjbGkUG4rW69o'
    SEARCH_ENGINE_ID = '11741ca14e8414fe2'
    search_query='Neuro sama'
    total_results=35
    main(search_query,total_results)
    
    
    
