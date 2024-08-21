import flet as ft
from search import *
import time
from c import *


class Main_Page(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.visible = True
        self.margin = ft.margin.only(left=10, right=10, top=10)
        
       
        

class Search_Page(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = True
        self.visible = False
        self.padding = ft.padding.only(right=10, left=10, top=20)
        
        self.anime_results = Anime_Results(page=self.page, go_info=self.go_info)
        self.anime_info = Anime_Info(page=self.page, back=self.back)
        self.content = ft.Row([self.anime_results, self.anime_info])
        
    def back(self, e):
        self.anime_info.visible = False
        self.anime_results.visible = True
        self.anime_results.content.controls[1].visible = False
        self.update()
        
    def go_info(self, e):
        self.anime_info.visible = True
        self.anime_info.get_anime(id=self.page.client_storage.get("id"))
        self.anime_results.visible = False
        self.update()
        
        

class Whatchlist_Page(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.visible = False
        self.bgcolor = "green"


class Account_Page(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.visible = False
       



def main(page: ft.Page):
    page.bgcolor = "#050117"
    page.window.width = 375
    page.window.max_width = 375
    page.padding = 0
    page.title = "My anime"
    
    def change_page(e):
        index = x.selected_index
        
        match index:
            case 0:
                a.visible = True
                b.visible = False
                c.visible = False
                d.visible = False
                page.update()
            
            case 1:
                a.visible = False
                b.visible = True
                c.visible = False
                d.visible = False
                page.update()
            
            case 2:
                a.visible = False
                b.visible = False
                c.visible = True
                d.visible = False
                page.update()
            
            case 3:
                a.visible = False
                b.visible = False
                c.visible = False
                d.visible = True
                page.update()
    
    
    a = Main_Page()
    b = Search_Page(page=page)
    c = Whatchlist_Page()
    d = Account_Page()
    x = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.CALENDAR_MONTH_ROUNDED, label="Season"),
            ft.NavigationBarDestination(icon=ft.icons.SEARCH_ROUNDED, label="Search"),
            ft.NavigationBarDestination(icon=ft.icons.LIST, label="whatchlist"),
            ft.NavigationBarDestination(icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED, label="Compte"),
        ], on_change=change_page, bgcolor="#050117", indicator_color="#0a0329"
    )
    
    page.navigation_bar = x
    page.add(ft.SafeArea(content=ft.Row([a, b, c, d]), expand=True))

ft.app(target=main)
