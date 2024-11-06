import requests
from src.imagemanipulator import ImageManipulator

url = "http://api.forismatic.com/api/1.0/"
params = {
    "lang": "en",
    "method": "getQuote",
    "format": "json"
}

# Make the GET request
count = 0
total = 1
done = False
while not done:
    response = requests.get(url, params=params)
    try:
        if response.status_code == requests.codes.ok:
            data = response.json()
            print(data)
            result = ImageManipulator(prompt=data['quoteText'], seed=4)
            result.process_image()
            result.add_author(author=data['quoteAuthor'])
            # result.show_image()
            result.save_image(str(result))
            count+=1
            done=count>=total
        else:
            print("Error:", response.status_code, response.text)
    except requests.exceptions.JSONDecodeError:
        pass

# result = ImageManipulator(prompt="Chill", seed=4)
# result.process_image()
# result.save_image("Thanks.png")
# result.show_image()