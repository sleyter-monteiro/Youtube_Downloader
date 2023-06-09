from pytube import YouTube
import ffmpeg
import os

BASE_YOUTUBE_URL = "https://www.youtube.com"

def url_youtube():
    while True:
        url = input("Entrez l'URL de la vidéo (Youtube uniquement) : ")
        if url [:len(BASE_YOUTUBE_URL)] == BASE_YOUTUBE_URL:
            break
        print("Veuillez entrer une URL valide. Ex : https://www.youtube.com/") 
    return url    


def itag_youtube(streams):
    print("Qualité Vidéo")
    index = 1
    for stream in streams:
        print(f"{index} - {stream.resolution}")
        index += 1

    while True:    
        res_num = input("Choisissez la résolution : ")
        if res_num == "":
            print("ERREUR : Veuillez séléctionné une qualité vidéo")
        else:
            try:
                res_num_int = int(res_num)
            except:
                print("Vous devez rentrer un TAG")  
            else:
                if not 1 <= res_num_int <= len(streams):
                    print("ERREUR : Vous devez rentrer un chiffre entre 1 et", len(streams))  
                else:
                    break
                        
    itag = streams[res_num_int-1].itag
    return itag


url = url_youtube()
    

def telechargement(stream, chunk, bytes_remaining):
    bytes_downloaded = stream.filesize - bytes_remaining
    pourcentage = bytes_downloaded * 100 / stream.filesize
    
    print(f"Téléchargement en cours... {int(pourcentage)}%")

video = YouTube(url)

video.register_on_progress_callback(telechargement)
print("TITRE : " + video.title)
print("NB VUES : ", video.views)

print("")

print("STREAMS")
streams = video.streams.filter(progressive=False, file_extension='mp4', type="video").order_by('resolution').desc()
flux_video = streams[0]

streams = video.streams.filter(progressive=False, file_extension='mp4', type="audio").order_by('abr').desc()
flux_audio = streams[0]

print("Flux Vidéo:", flux_video)
print("Flux Audio:", flux_audio)

# for stream in streams:
#     print(stream)
# itag = itag_youtube(streams)
# print("itag: ", itag)    
      
# stream = video.streams.get_by_itag(itag)
# stream = video.streams.get_highest_resolution()
# print("Stream Vidéo : ", stream)
flux_video.download("videos")
flux_audio.download("audios")

audio_filename = os.path.join("audios", flux_audio.default_filename)
video_filename = os.path.join("videos", flux_video.default_filename)
output_filename = flux_video.default_filename

print("combinaison des fichiers...")
ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename, vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)

print("Succès")    