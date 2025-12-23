import requests
import tkinter as tk
from tkinter import ttk, messagebox

# 🔹 WEATHER FUNCTION
def get_weather():
    city = city_var.get()
    if city == "Select a city":
        messagebox.showwarning("Input Error", "Please select a city")
        return

    if city == "Custom City":
        city = custom_city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return

    api_key = "71427d502c0f8f09ffd24ec95593c60a"

    # ----- CURRENT WEATHER -----
    try:
        weather_response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"}
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
    except:
        messagebox.showerror("Error", "City not found or API error")
        return

    condition = weather_data["weather"][0]["main"]
    icon = weather_icon(condition)

    # Update current weather labels
    city_label_val.config(text=city)
    temp_label_val.config(text=f"{weather_data['main']['temp']} °C")
    humidity_label_val.config(text=f"{weather_data['main']['humidity']} %")
    condition_label_val.config(text=f"{icon} {condition}")

    update_ui(condition)

    # ----- 5-DAY FORECAST -----
    try:
        forecast_response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"q": city, "appid": api_key, "units": "metric"}
        )
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
    except:
        messagebox.showerror("Error", "Forecast not available")
        return

    forecast_list = forecast_data['list']

    # Clear previous forecast cards
    for widget in forecast_cards_frame.winfo_children():
        widget.destroy()

    # Create 5 forecast cards horizontally
    for i in range(0, 40, 8):
        day = forecast_list[i]
        dt = day['dt_txt'].split()[0]
        temp = day['main']['temp']
        cond = day['weather'][0]['main']
        icon = weather_icon(cond)

        card = tk.Frame(forecast_cards_frame, bg="#E3F2FD", bd=1, relief="raised", padx=10, pady=15)
        card.grid(row=0, column=i//8, padx=5, sticky="nsew")
        tk.Label(card, text=dt, font=("Arial", 10, "bold"), bg="#E3F2FD").pack(pady=2)
        tk.Label(card, text=icon, font=("Arial", 20), bg="#E3F2FD").pack(pady=2)
        tk.Label(card, text=f"{temp} °C", font=("Arial", 11), bg="#E3F2FD").pack(pady=2)
        tk.Label(card, text=cond, font=("Arial", 11), bg="#E3F2FD").pack(pady=2)

    # Make columns expand evenly
    for i in range(5):
        forecast_cards_frame.columnconfigure(i, weight=1)


# 🔹 MAP CONDITION TO EMOJI
def weather_icon(condition):
    mapping = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️"
    }
    return mapping.get(condition, "❓")


# 🔹 UPDATE BACKGROUND + SUN COLOR
def update_ui(condition):
    bg = "#F2F3F4"
    sun_color = "gray"

    if condition == "Clear":
        bg = "#87CEEB"
        sun_color = "gold"
    elif condition == "Clouds":
        bg = "#D3D3D3"
    elif condition in ["Rain", "Drizzle"]:
        bg = "#A9CCE3"
    elif condition == "Thunderstorm":
        bg = "#5D6D7E"
    elif condition == "Snow":
        bg = "#FFFFFF"
    elif condition in ["Mist", "Fog", "Haze"]:
        bg = "#E5E7E9"

    root.configure(bg=bg)
    top_frame.configure(bg=bg)
    forecast_frame.configure(bg=bg)
    sun_label.configure(bg=bg, fg=sun_color)


# 🔹 SHOW / HIDE CUSTOM CITY ENTRY
def toggle_custom(event):
    if city_var.get() == "Custom City":
        custom_city_entry.grid()  # show the entry
    else:
        custom_city_entry.grid_remove()  # hide it


# 🔹 MAIN WINDOW
root = tk.Tk()
root.title("Weatherman")
root.geometry("700x450")
root.resizable(True, True)

# Top frame: current weather and city input
top_frame = tk.Frame(root)
top_frame.pack(fill="x", pady=15, padx=10)

# Sun icon
sun_label = tk.Label(top_frame, text="☀️", font=("Arial", 40))
sun_label.grid(row=0, column=0, rowspan=2, padx=10)

# City dropdown + custom entry
cities = ["Select a city", "Chennai", "Delhi", "Mumbai", "Bengaluru",
          "Hyderabad", "Kolkata", "Pune", "Jaipur", "Custom City"]
city_var = tk.StringVar(value=cities[0])

tk.Label(top_frame, text="Select City:", font=("Arial", 12)).grid(row=0, column=1, sticky="w")
city_dropdown = ttk.Combobox(top_frame, textvariable=city_var, values=cities, state="readonly", font=("Arial", 11))
city_dropdown.grid(row=0, column=2, padx=5)
city_dropdown.bind("<<ComboboxSelected>>", toggle_custom)

# Custom city entry (column 3) hidden initially
custom_city_entry = tk.Entry(top_frame, font=("Arial", 11))
custom_city_entry.grid(row=0, column=3, padx=5)
custom_city_entry.grid_remove()  # hide initially

# Get Weather Button
tk.Button(top_frame, text="Get Weather", command=get_weather, font=("Arial", 11)).grid(row=0, column=4, padx=10)

# Current Weather Labels
weather_labels_frame = tk.Frame(top_frame)
weather_labels_frame.grid(row=1, column=1, columnspan=4, pady=15, sticky="ew")

tk.Label(weather_labels_frame, text="City:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", padx=5)
city_label_val = tk.Label(weather_labels_frame, text="-", font=("Arial", 11))
city_label_val.grid(row=0, column=1, sticky="w", padx=5)

tk.Label(weather_labels_frame, text="Temperature:", font=("Arial", 11, "bold")).grid(row=0, column=2, sticky="w", padx=5)
temp_label_val = tk.Label(weather_labels_frame, text="-", font=("Arial", 11))
temp_label_val.grid(row=0, column=3, sticky="w", padx=5)

tk.Label(weather_labels_frame, text="Humidity:", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w", padx=5)
humidity_label_val = tk.Label(weather_labels_frame, text="-", font=("Arial", 11))
humidity_label_val.grid(row=1, column=1, sticky="w", padx=5)

tk.Label(weather_labels_frame, text="Condition:", font=("Arial", 11, "bold")).grid(row=1, column=2, sticky="w", padx=5)
condition_label_val = tk.Label(weather_labels_frame, text="-", font=("Arial", 11))
condition_label_val.grid(row=1, column=3, sticky="w", padx=5)

# Forecast section
forecast_frame = tk.Frame(root)
forecast_frame.pack(fill="both", expand=True, padx=10, pady=15)

forecast_cards_frame = tk.Frame(forecast_frame)
forecast_cards_frame.pack(fill="x", pady=15)

root.mainloop()
