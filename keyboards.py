from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app import download_playlist
import json


military_keybrd = ReplyKeyboardMarkup(keyboard=[],
resize_keyboard=True
)


def divide_chunks(my_list, n):
    return [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]

with open("video.json", "r") as f:
    data = json.load(f)
titles = []

for v in data:
    for key in v.keys():
        titles.append(key)

startKey = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Special Forces Group Music & Videos 💣")]
    ]
    ,
    resize_keyboard=True
)



cancel=[]
cancel.append(KeyboardButton(text="Ortga 🔙"))
military_keybrd.keyboard.append(cancel)
index=0
for title in range(0,len(titles),20):
    index+=1
    row_btn = []
    row_btn.append(KeyboardButton(text=f"{index}. Military Motivation 🎵"))
    military_keybrd.keyboard.append(row_btn)