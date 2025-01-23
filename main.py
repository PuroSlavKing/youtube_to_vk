import yt_dlp
import requests
import re
import vk_api
from vk_api.utils import get_random_id
import time
import os
from youtubers import youtubers_list


def main():
    VK_TOKEN = os.getenv('TOKEN_VK')
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    upload = vk_api.VkUpload(vk_session)
    vk = vk_session.get_api()
    ydl_opts = {"ffmpeg_location": "D:/Soft/FFmpeg/bin"} # Manual location

    user_id = os.getenv('USER_ID')

    while True:
        try:
            for youtuber in youtubers_list:
                print("CONSOLE | Получение HTML")
                html = requests.get(f"https://www.youtube.com/@{youtuber}/videos").text
                print("CONSOLE | Проверка последнего видео")

                URL = f"https://www.youtube.com/watch?v={re.search(r'videoId":"(.*?)"', html).group(1)}"

                with open("downloaded.txt", "r+") as file:
                    content = file.read()

                    if URL not in content:
                        ydl_opts = {
                            "format": "bestvideo+bestaudio/best",
                            "concurrent-fragments": "4",
                            "outtmpl": "video.%(ext)s",
                            "ignoreerrors": True,
                            "no-overwrites": True,
                            "continue": True,
                            "writethumbnail": True,
                            "embedthumbnail": True,
                            "convert-thumbnails": "jpg",
                            "postprocessors": [
                                {
                                    "format": "jpg",
                                    "key": "FFmpegThumbnailsConvertor",
                                    "when": "before_dl",
                                }
                            ],
                        }

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            try:
                                info_dict = ydl.extract_info(URL, download=True)
                                video_channel = info_dict.get("channel", None)
                                video_title = info_dict.get("title", None)
                                video_format = info_dict.get("ext", None)
                                video_name = f"[{video_channel}] {video_title}"
                                file_name = f"video.{video_format}"
                            except Exception as e:
                                vk.messages.send(
                                    user_id=user_id,
                                    random_id=get_random_id(),
                                    message=f"CONSOLE | ОШИБКА! СКАЧИВАНИЕ ВИДЕО {video_name} НЕ УДАЛОСЬ: {str(e)}",
                                )
                                break

                        print("CONSOLE | Загрузка видео в VK")
                        response = upload.video(
                            video_file=file_name,
                            name=video_name,
                            group_id=youtuber.group_id,
                            album_id=youtuber.pl_id,
                            wallpost="1",
                        )
                        print("CONSOLE | Загрузка обложки видео")
                        video_id = response.get("video_id")
                        response = upload.thumb_video(
                            photo_path="/root/video.jpg",
                            owner_id=f"-{youtuber.group_id}",
                            video_id=video_id,
                        )
                        vk.messages.send(
                            user_id=user_id,
                            random_id=get_random_id(),
                            message=f"CONSOLE | Видео {video_name} успешно загружено в группу",
                        )
                        file.write(URL + "\n")
                        os.remove(file_name)
                        os.remove("video.jpg")

                print("CONSOLE | Перерыв 10 минут")
                time.sleep(10 * 60)

        except Exception as e:
            vk.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                message=f"CONSOLE | Программа завершена из-за ошибки. Перезапустите скрипт: {str(e)}",
            )
            break


if __name__ == "__main__":
    main()
