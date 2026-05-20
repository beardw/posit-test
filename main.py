import requests

base_url = "http://206.12.92.143/data/dashboard/" #CAWA/Canada/CAWA_Canada_1990.tif"

def get_data(url, code, country, year):
    response = requests.get(f"{url}/{code}/{country}/{code}_{country}_{year}.tif", stream=True)

    if response.status_code == 200:
        # with open(f"{code}_{country}_{year}.tif", 'wb') as file:
        #     file.write(response.content)
            # for chunk in response.iter_content(1024):
            #     file.write(chunk)
        data = response.content
        print("Data retrieved!")
        return data
    else:
        print(f"Failed to retrieve data {response.status_code}")
    


results = get_data(base_url, "CAWA", "Canada", "1990")
print(results)