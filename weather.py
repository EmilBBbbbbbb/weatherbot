import requests
from pprint import pprint
from config import open_wether_token

def get_wether(city, open_wether_token):
    try:
        r= requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_wether_token}&units=metric"
        )
        data= r.json()

        pprint(data) #all wether

        city=data["name"]
        temp_now=data["main"]["temp"]
        wind = data["wind"]["speed"]
        pressure=data["main"]["pressure"]


        print(f"Погода в городе {city} на сегодня:\n"
              f"Температура: {temp_now}°С\n"
              f"Скорость ветра: {wind}м/с\n"
              f"Давление: {pressure}мм р.с\n")
    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city=input("Введите город: ")
    get_wether(city, open_wether_token)


if __name__ == "__main__":
    main()
