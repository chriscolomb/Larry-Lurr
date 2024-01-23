from bs4 import BeautifulSoup
import requests

# Define the URL of the webpage
url = "https://kumamate.net/vip/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with the class "RecentMatch"
    recent_match2_elements = soup.find_all(class_="RecentMatch2")
    recent_match1_elements = soup.find_all(class_="RecentMatch1")

    tiers = []
    for element in recent_match2_elements:
        tiers.append(element.text)
    for element in recent_match1_elements:
        tiers.append(element.text)
    
    sorted_tiers = sorted(tiers, key=lambda x: x.split()[-1][:-1])

    # Print the sorted lines
    for tier in sorted_tiers:
        print(tier)

    

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
