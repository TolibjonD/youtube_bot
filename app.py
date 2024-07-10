from pytube import YouTube, Playlist
import re
from io import BytesIO
import io
import json

def check_youtube_link(url):
    pattern = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.*"
    if re.match(pattern, url):
        return True
    else:
        return False

def number_formatter(num):
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return str(num // 1000) + "," + str(num % 1000)
    elif num < 1000000000:
        return str(num // 1000000) + "," + str((num % 1000000) // 1000) + "," + str(num % 1000)
    else:
        return str(num // 1000000000) + "," + str((num % 1000000000) // 1000000) + "," + str((num % 1000000) // 1000) + "," + str(num % 1000)

def download_youtube_video(url):
    try:
        
        yt = YouTube(url)
        if yt.age_restricted:
            return "Bu videoni yuklab olish imkonsiz, chunki unda yosh chegarasi mavjud !..."
        else:
            video = yt.streams.get_highest_resolution()
            thumbnail = yt.thumbnail_url
            views = yt.views
            audio = yt.streams.get_audio_only()
            title = yt.title
            video_size = video.filesize_mb
            audio_size = audio.filesize_mb

            caption = f"🎸<b>Nomi</b>: {title}\n\n"
            caption += f"📹<b>Video hajmi</b>: {video_size} MB\n\n"
            caption += f"📝<b>Musiqa hajmi</b>: {audio_size} MB\n\n"
            caption += f"👁<b>Ko'rganlar soni</b>: {number_formatter(int(views))}"

            buffer = io.BytesIO()
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            data = buffer.read()
            buff = io.BytesIO()
            audio.stream_to_buffer(buff)
            buff.seek(0)
            context = {
                "audio": buff.read(),
                "video": data,
                "title": title,
                "photo": thumbnail,
                "caption": caption
            }
            print("Ma'lumotlar yuklanmoqda !...")
            return context
    except Exception as e:
        return f"Xatolik yuz berdi: {e}"
    
def download_playlist(playlist_url="https://youtube.com/playlist?list=PLO9iTHH4zWX-fpFJ9j4cnFU5iyT_hAjjW&si=1Jv7HUoeq0lU6rO-"):
    try:
        playlist = Playlist(playlist_url).video_urls
        titles = []
        data = [

        ]
        for video in playlist:
            titles.append(YouTube(video).title)
        for video in playlist:
            data.append({YouTube(video).title: video})
        with open("video.json", "w+") as f:
            json.dump(data, f)
        return {
            "titles": titles,
            "count": len(titles)
        }
    except Exception as e:
        return f"Xatolik yuz berdi: {e}"