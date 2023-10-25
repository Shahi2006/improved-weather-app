import requests
import json
from customtkinter import *
from PIL import Image, ImageTk 
API_KEY = "100f3bed62fec6af2f7c072e5eb87ecb"

root = CTk()
root.geometry("500x500")
root.title("WeatherSphere")
root.configure(fg_color="grey")

set_appearance_mode("system")
set_default_color_theme("green")
Standard = CTkFont(family="Arial", size=16, weight="bold")
Bfont = CTkFont(family="Arial", size=16, weight="bold")

main_frame = CTkFrame(master=root, fg_color="transparent")

top_frame = CTkFrame(master=main_frame, fg_color="transparent")
unit_frame=CTkFrame(master=main_frame,fg_color="transparent")
search_frame = CTkFrame(master=main_frame, fg_color="transparent")
bottom_frame = CTkFrame(master=main_frame, fg_color="transparent", corner_radius=20)
h1 = CTkLabel(
    master=top_frame, text="Weather App", font=("Arial Black", 30, "bold")
).pack(pady=20)
city_label = CTkLabel(master=top_frame, text="Enter city name:    ", font=Standard)
city_label.pack(pady=5, side="left")

city = CTkEntry(master=top_frame, font=Bfont)
city.pack(side="left")

com=CTkComboBox(master=unit_frame,font=("Arial Black", 15, "bold"),width=310,values=["imperial","metric","standard"],corner_radius=20)
com.set("select your preferred unit system")
com["state"]="readonly"
com.pack(side="left")

weather_icon_label = CTkLabel(master=bottom_frame, text="")
weather_icon_label.pack(side="right", padx=5)

output = CTkLabel(master=bottom_frame, text="", font=Standard)
output.pack(side="left", padx=10)


def get_weather_icon(icon_code):
    icon_mapping = {
        "01d": "https://openweathermap.org/img/wn/01d@2x.png",
        "02d": "https://openweathermap.org/img/wn/02d@2x.png",
        "03d": "https://openweathermap.org/img/wn/03d@2x.png",
        "04d": "https://openweathermap.org/img/wn/04d@2x.png",
        "09d": "https://openweathermap.org/img/wn/09d@2x.png",
        "10d": "https://openweathermap.org/img/wn/10d@2x.png",
        "11d": "https://openweathermap.org/img/wn/11d@2x.png",
        "13d": "https://openweathermap.org/img/wn/13d@2x.png",
        "50d": "https://openweathermap.org/img/wn/50d@2x.png",
        "01n": "https://openweathermap.org/img/wn/01n@2x.png",
        "02n": "https://openweathermap.org/img/wn/02n@2x.png",
        "03n": "https://openweathermap.org/img/wn/03n@2x.png",
        "04n": "https://openweathermap.org/img/wn/04n@2x.png",
        "09n": "https://openweathermap.org/img/wn/09n@2x.png",
        "10n": "https://openweathermap.org/img/wn/10n@2x.png",
        "11n": "https://openweathermap.org/img/wn/11n@2x.png",
        "13n": "https://openweathermap.org/img/wn/13n@2x.png",
        "50n": "https://openweathermap.org/img/wn/50n@2x.png",
    }

    icon_url = icon_mapping.get(
        icon_code, "https://openweathermap.org/img/wn/10d@2x.png"
    )

    icon_image = Image.open(requests.get(icon_url, stream=True).raw)

    return CTkImage(icon_image, size=(100, 100))


def weather():
    city_name = city.get()
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    unit=com.get()
    URL = BASE_URL + f"q={city_name}&appid={API_KEY}&units={unit}"
    

    response = requests.get(URL)
    data = response.json()
    print(data)
    if data["cod"] != "404":
        if unit=="imperial":
            uni="F"
        elif unit=="metric":
            uni="C"
        else:
            uni="K"
        main_data = data["main"]
        feel=main_data["feels_like"]
        temperature = main_data["temp"]
        humidity = main_data["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_data = data.get("weather", [])
        if weather_data:
            weather_description = weather_data[0].get("description", "N/A")
            weather_icon = weather_data[0].get("icon")
            icon = get_weather_icon(weather_icon)
        else:
            weather_description = "N/A"
            icon = get_weather_icon("default")

        weather_icon_label.configure(image=icon)
        weather_icon_label.image = icon

        output.configure(
            text=f"Temperature: {temperature} {uni} \nHumidity: {humidity}%\nWeather Description: {weather_description}\n Wind Speed: {round(wind_speed*3.6, 2)} Km/hr \n feels like: {feel} {uni} ")
        bottom_frame.configure(
            border_width=3, fg_color="#8eb69b", border_color="#306844"
        )
    else:
        output.configure(text="Enter valid city.")


search_icon_url = "https://thenounproject.com/api/private/icons/6210206/edit/?backgroundShape=SQUARE&backgroundShapeColor=%23000000&backgroundShapeOpacity=0&exportSize=752&flipX=false&flipY=false&foregroundColor=%23000000&foregroundOpacity=1&imageFormat=png&rotation=0"

icon_image = CTkImage(
    Image.open(requests.get(search_icon_url, stream=True).raw), size=(30, 30)
)

search_btn = CTkButton(
    master=search_frame,
    font=Bfont,
    text="",
    command=weather,
    fg_color="#f1e9d2",
    corner_radius=80,
    image=icon_image,
    width=80,
    hover_color="#cdb891"
)
search_btn.pack(pady=5, ipadx=0)


# Pack the frames one after another, horizontally centered
main_frame.pack(expand=True, fill="both", padx=20, pady=20)
main_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
top_frame.pack(pady=10, padx=20)
unit_frame.pack(pady=5,padx=20)
search_frame.pack(pady=5)
bottom_frame.pack(pady=20, padx=20, ipadx=20, ipady=20)
root.mainloop()
