from bs4 import BeautifulSoup as bs
import requests
import re
import youtube_dl
import os

requests.packages.urllib3.disable_warnings()

# Insert Playlist ID --> Click the playlist and copy the part after list= in the browser:
# https://www.youtube.com/watch?v=uHeQBDQlPD8&list=<get_playlist_id_here> (Last string after list=)
# https://www.youtube.com/watch?v=i3avL_uAvLg&list=PLZ0LWy2i9_iPRk2UgeceeB8eZ3g_yucaE

#Change it to your download folder example:
# folder_path = "~/Downloads/youtube_music_downloads"

#Where the music downloads to
folder_path = "~/youtube_music_downloads"

playlist_id = 'PLZ0LWy2i9_iPRk2UgeceeB8eZ3g_yucaE'
r = requests.get(f'https://www.youtube.com/watch?v=uHeQBDQlPD8&list={playlist_id}')
page = r.text
soup=bs(page,'html.parser')
res=soup.find_all('a',{'class':'pl-video-title-link'})
pattern = r"/watch\?[\w=&%]+"
matches = re.findall(pattern, page)
og_array = []
song_count = 0

# Create the music directory if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

for match in matches:
    og_music = f"https://youtube.com{match}"
    if og_music in og_array:
        continue
    if og_music == "https://youtube.com/watch?v":
        continue
    else:
        song_count += 1
        og_array.append(og_music)
        print(f"Full Link: {og_music} | Song Count: {song_count}")

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': f"{folder_path}/%(title)s.%(ext)s",
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([og_music])
        except Exception as e:
            print(f"Error downloading {og_music}: {e}")
            continue

print('Total Songs: ', song_count)
