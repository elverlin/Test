import flet as ft
import requests
import time



class Anime_Box_Vertical_None(ft.Container):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 200
        self.alignment = ft.alignment.top_center
        
        
        self.image = ft.Image(**self.image_style(image=r"C:\Users\Abdoul Karim\Pictures\0.jpg"))
        self.name = ft.Container(**self.name_style(name="No connection"))
        
        self.content = ft.Column([self.image, self.name], alignment=ft.MainAxisAlignment.START, spacing=0)
        

    def image_style(self, image):
        return{
            "width" : 100,
            "height" : 150,
            "border_radius" : 5,
            "src" : image
        }
        
    def name_style(self, name):
        return{
            "height" : 100,
            "alignment" : ft.alignment.top_left,
            "content" : ft.Text(value=name, size=13, weight=ft.FontWeight.W_400, color="white", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)
        }

class Seasonal_Animes(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.alignment = ft.alignment.center
        
        self.grid = ft.GridView(runs_count=3, run_spacing=20, spacing=90, padding=ft.padding.only(bottom=75))
        
        for i in range(20):
            self.grid.controls.append(Anime_Box_Vertical_None())
        
            
        self.content = self.grid
        
