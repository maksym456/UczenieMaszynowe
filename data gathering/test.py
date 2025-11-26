import requests
url = "https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/SearchDetails.aspx?Id=cb64a077-1cd6-4c02-a250-1a791141a612"
response = requests.get(url)
print(response.status_code)
print(response.text[:500])  # Print the first 500 characters of the response content