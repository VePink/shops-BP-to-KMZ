from POIs.functions import pack_attributes
import requests
from bs4 import BeautifulSoup

def scrape_BP():
    source_url = "https://balticpetroleum.lt/baltic-petroleum-degalines"
    html_content = requests.get(source_url, headers = {'User-Agent': 'Mozilla/5.0'}).text
    websiteContent = BeautifulSoup(html_content, "html.parser")
    addresses = websiteContent.find_all("td", {"class": "name small"})
    workHours = websiteContent.find_all("td", {"class": "laikas small"})

    all_BP_shops = [] #list for saving shops

    for i in range(len(addresses)):
        all_BP_shops.append(
            pack_attributes(
                "Baltic Petroleum", 
                addresses[i].text, 
                (websiteContent.find_all("td", {"class": "tel small"}))[i].text, 
                "not found", 
                workHours[i].text + workHours[i+1].text, 
                "", 
                "", 
                "BP.png")
        )
    
    return all_BP_shops 


result_path = (input("Paste path to folder. Result KML will be saved there: ") or "D:\\TMP")
print("Selected result folder: " + result_path)
result_path = (result_path + '\\').replace('\\\\','\\')

api_key = (input("Paste Google Maps Geocoding API key: ") or "AIzaSyABVFtB1GXC-ay7UQRFKTWr5o6bhhHxsEE")
print("key " + api_key + " will be used for geocoding")

all_shops = scrape_BP()

from POIs.functions import geolocate
geolocate(api_key, all_shops)

result_filename_prefix = "BP_"

import datetime
end_timestamp = str(datetime.datetime.now().strftime("%Y%m%d_%H%M"))

from POIs.functions import save_as_KMZ
save_as_KMZ(all_shops, result_path, result_filename_prefix, './Input/BP.png', end_timestamp)

from POIs.functions import save_as_ZIP
save_as_ZIP(result_path, result_filename_prefix, end_timestamp)

from CLTreport.summary import report_summary
report_summary()

