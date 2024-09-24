import flet as ft
import yt_dlp



def main(page: ft.Page):
    
    def my_hook(d):
        if d['status'] == 'downloading':
            infos.value = f"Téléchargement : {d['_percent_str']} complété à une vitesse de {d['_speed_str']}, temps restant : {d['_eta_str']}"
            infos.update()
            
        elif d['status'] == 'finished':
            infos.value = 'Téléchargement terminé, démarrage du post-traitement...'
            infos.update()

    def telecharger_video(e):
        ydl_opts = {
            'format': 'best',
            'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',
            'progress_hooks': [my_hook],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://video.sibnet.ru/shell.php?videoid={video_id.value}.mp4"])
                
        except:
            infos.value = 'Erreur de téléchargement'
            infos.update()
            
    
    infos = ft.Text(value="")
    bouton = ft.ElevatedButton(text="Download", on_click=telecharger_video)
    video_id = ft.TextField()
    
    page.add(ft.Row([video_id, bouton], alignment=ft.MainAxisAlignment.CENTER), infos)

ft.app(target=main)
