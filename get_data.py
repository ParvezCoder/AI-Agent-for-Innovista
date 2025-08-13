import pandas as pd
import requests
from io import StringIO
from agents import function_tool

@function_tool
def get_all_complaints_data(admin_pin:int) -> list:
    """
    Retrieves all complaints from the Google Sheet and returns them as a list of dictionaries.
    Each dictionary contains: name, complaint_type, complaint_detail.

    The returned data should be displayed to the user in a clear, numbered list format
    for better readability. Example:

    1. Name: Ali Khan
       Type: wifi
       Detail: Book not available
       etc..
    """
    sheet_url = "https://docs.google.com/spreadsheets/d/14rbtF3mSw_GasniwueCwF8eUb-raAYwN2opsJQFOcbg/export?format=csv&gid=0"
    
    if admin_pin !=0000:
        return [{"error": "Access Denied. Valid admin PIN required."}]
    
    response = requests.get(sheet_url)
    
    if response.status_code != 200:
        return [{"error": "Failed to fetch data from Google Sheet"}]
    
    df = pd.read_csv(StringIO(response.text))
    
    return df.to_dict(orient="records")




