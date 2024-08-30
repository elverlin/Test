import flet as ft
import os


def main(page: ft.Page):
    page.appbar = ft.AppBar(title=ft.Text("PermissionHandler Tests"))
    ph = ft.PermissionHandler()
    page.overlay.append(ph)
    

    chemin_repertoire = "/storage/emulated/0/Android/data"
    nom_dossier = "My anime"
    chemin_complet = os.path.join(chemin_repertoire, nom_dossier)
    
    if not os.path.exists(chemin_complet):
        os.makedirs(chemin_complet)



    page.add(ft.OutlinedButton("Check Microphone Permission",data=ft.PermissionType.STORAGE))
    
ft.app(target=main)
