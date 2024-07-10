from aiogram import Bot, Dispatcher, types
import asyncio
import io
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from app import download_youtube_video, download_playlist
import logging
from sys import stdout
from aiogram.types.input_file import BufferedInputFile
from app import check_youtube_link
from aiogram.methods.send_media_group import SendMediaGroup
from aiogram.types.input_media_audio import InputMediaAudio
from aiogram.types.input_media_video import InputMediaVideo
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Filter
from time import sleep
from keyboards import startKey, military_keybrd, divide_chunks
from keyboards import titles, divide_chunks
import json

ADMIN = 5944280734

class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: types.Message) -> bool:
        return message.text == self.my_text

dp = Dispatcher()
bot = Bot(token="5987687553:AAHSaBhvaYMzhNEVsRXgMLWbGMQt4UlQICM", default=DefaultBotProperties(parse_mode=ParseMode.HTML))


index=0
for title in range(0,len(titles),20):
    index+=1
    @dp.message(MyFilter(f"{index}. Military Motivation 🎵"))
    async def get_playlist(message: types.Message):
        user = message.from_user
        with open("video.json", "r") as f:
            data = json.load(f)
        chunks = divide_chunks(data,20)
        text = message.text.split(".")[0]
        for n in chunks[int(text)-1]:
            for m,url in n.items():
                data = download_youtube_video(url)
                if data:
                    if type(data)==str:
                        await message.answer(data)
                        sleep(5)
                    else:
                        try:
                            await bot.send_chat_action(chat_id=user.id, action=ChatAction.UPLOAD_DOCUMENT)
                            audio = io.BytesIO(data["audio"]).read()
                            title = data['title']
                            photo = data['photo']
                            caption = data['caption']
                            video = io.BytesIO(data["video"]).read()
                            aud = BufferedInputFile(file=audio, filename=f"{title}.mp3")
                            vd = BufferedInputFile(file=video, filename=f"{title}.mp4")
                            media = [InputMediaPhoto(media=photo, caption=caption), InputMediaVideo(media=vd)]
                            await bot.send_chat_action(chat_id=user.id, action=ChatAction.UPLOAD_DOCUMENT)
                            await bot(SendMediaGroup(chat_id=message.from_user.id, media=media))
                            await message.answer_audio(audio=aud , reply_markup=startKey)
                        except:
                            await message.answer("Xatolik yuz berdi yoki siz yuborgan havola yaroqsiz !" , reply_markup=startKey)
                else:
                    try:
                        await message.send_copy(chat_id=message.from_user.id, disable_notification=True, reply_markup=startKey)
                        sleep(5)
                    except:
                        await message.answer("Nice try !", reply_markup=startKey)
                        sleep(5)

async def military_download(message: types.Message):
    # titles = download_playlist()['titles']
    await message.answer("Pastdan kerakli qismlarni tanlang: ", reply_markup=military_keybrd)

async def cancel(message: types.Message):
    await message.answer("Youtube Havola yuboring yoki pastdagi bo'limni tanlang", reply_markup=startKey)


async def start(message: types.Message):
    await bot.send_message(chat_id=ADMIN, text=f"Bot ishga tushdi\n\nUser: {message.from_user.mention_html(message.from_user.full_name)}")
    await message.answer(f"Salom {message.from_user.full_name}\nMenga yutube video havolasini yuboring !", reply_markup=startKey)


async def echo(message: types.Message):
    havola = message.text
    user = message.from_user
    text = "Bot ishlatilmoqda: \n\n"
    text += f"User: {user.mention_html(user.full_name)}\n"
    text += f"UserID: {user.id}\n"
    text += f"Xabar: {havola}"
    await bot.send_message(chat_id=ADMIN, text=text)
    if check_youtube_link(havola):
        data = download_youtube_video(havola)
        if data:
            if type(data)== str:
                await message.answer(data)
                sleep(5)
                await message.delete()
            else:
                try:
                    audio = io.BytesIO(data["audio"]).read()
                    title = data['title']
                    photo = data['photo']
                    caption = data['caption']
                    video = io.BytesIO(data["video"]).read()
                    aud = BufferedInputFile(file=audio, filename=f"{title}.mp3")
                    vd = BufferedInputFile(file=video, filename=f"{title}.mp4")
                    media = [InputMediaPhoto(media=photo, caption=caption), InputMediaVideo(media=vd)]
                    await bot.send_chat_action(chat_id=user.id, action=ChatAction.UPLOAD_DOCUMENT)
                    await bot(SendMediaGroup(chat_id=message.from_user.id, media=media))
                    await message.answer_audio(audio=aud , reply_markup=startKey)
                    await message.delete()
                except:
                    await message.answer("Xatolik yuz berdi yoki siz yuborgan haola yaroqsiz !" , reply_markup=startKey)
                    sleep(5)
                    await message.delete()
        else:
            try:
                await message.send_copy(chat_id=message.from_user.id, disable_notification=True, reply_markup=startKey)
                sleep(5)
                await message.delete()
            except:
                await message.answer("Nice try !", reply_markup=startKey)
                sleep(5)
                await message.delete()
    else:
        await message.answer("Iltimos, youtube video havolasini yuboring !", reply_markup=startKey)
        sleep(5)
        await message.delete()

async def main():
    dp.message.register(military_download, MyFilter("Special Forces Group Music & Videos 💣"))
    dp.message.register(cancel, MyFilter("Ortga 🔙"))
    dp.message.register(start, CommandStart())
    dp.message.register(echo)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=stdout)
    asyncio.run(main())