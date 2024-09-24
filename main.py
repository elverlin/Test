import flet as ft
import requests
import time
import re
import os


def main(page: ft.Page):
    
    def get_seasonal_anime(e):
        try:
            response = requests.get("https://api.jikan.moe/v4/seasons/now")
            if response.status_code == 200:
                page.add(ft.Text("Good request"))
            
        except:
            page.add(ft.Text("Bad request"))
            
    def test(e):
        page.add(ft.Text("Je suis un texte"))   
        page.update()     
    
    bouton = ft.Row([ft.ElevatedButton("Bouton", on_click=get_seasonal_anime)], alignment=ft.MainAxisAlignment.CENTER)
    bouton2 = ft.Row([ft.ElevatedButton("Bouton", on_click=test)], alignment=ft.MainAxisAlignment.CENTER)
    
    
    page.add(bouton, bouton2)
    
ft.app(target=main)
