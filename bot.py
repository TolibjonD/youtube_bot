from aiogram import Bot, Dispatcher, types
import asyncio
import io
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from app import download_youtube_video
import logging
from sys import stdout
from aiogram.types.input_file import BufferedInputFile
from app import check_youtube_link
from aiogram.methods.send_media_group import SendMediaGroup
from aiogram.types.input_media_audio import InputMediaAudio
from aiogram.types.input_media_video import InputMediaVideo
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.enums.chat_action import ChatAction
from time import sleep

ADMIN = 5944280734

dp = Dispatcher()
bot = Bot(token="5987687553:AAHSaBhvaYMzhNEVsRXgMLWbGMQt4UlQICM", default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def start(message: types.Message):
    await bot.send_message(chat_id=ADMIN, text=f"Bot ishga tushdi\n\nUser: {message.from_user.mention_html(message.from_user.full_name)}")
    await message.answer(f"Salom {message.from_user.full_name}\nMenga yutube video havolasini yuboring !")


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
                    await message.answer_audio(audio=aud)
                    await message.delete()
                except:
                    await message.answer("Xatolik yuz berdi yoki siz yuborgan haola yaroqsiz !")
                    sleep(5)
                    await message.delete()
        else:
            try:
                await message.send_copy(chat_id=message.from_user.id, disable_notification=True)
                sleep(5)
                await message.delete()
            except:
                await message.answer("Nice try !")
                sleep(5)
                await message.delete()
    else:
        await message.answer("Iltimos, youtube video havolasini yuboring !")
        sleep(5)
        await message.delete()

async def main():
    dp.message.register(start, CommandStart())
    dp.message.register(echo)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=stdout)
    asyncio.run(main())