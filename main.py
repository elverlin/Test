import flet as ft
import requests




def main(page: ft.Page):

    class Anime_Box(ft.Container):
        def __init__(self, name, image, id, func):
            super().__init__()
            self.id = id
            self.func = func
            self.height = 100
            self.border_radius = 8
            self.bgcolor = "#0a0329"
            self.padding = ft.padding.only(right=5)
            self.margin = ft.margin.symmetric(horizontal=10, vertical=5)
            
            self.image = ft.Image(**self.image_style(image=image))
            self.name = ft.Container(**self.name_style(name=name))
            
            self.content = ft.Row([self.image, self.name], alignment=ft.CrossAxisAlignment.START)
            self.on_click = self.save_data


        def image_style(self, image):
            return{
                "width" : 75,
                "height" : 100,
                "src" : image
            }
            
        def name_style(self, name):
            return{
                "height" : 100,
                "expand" : True,
                "content" : ft.Container(content=ft.Text(value=name, size=15, weight=ft.FontWeight.BOLD, color="white", max_lines=3, overflow=ft.TextOverflow.ELLIPSIS), padding=ft.padding.only(top=5))
            }
            
            
        def save_data(self, e):
            page.client_storage.remove("id")
            page.client_storage.set("id", self.id)
            self.func(e)

    class Anime_Info(ft.Container):
        def __init__(self, back):
            super().__init__()
            self.expand = True
            self.visible = False
            self.bgcolor = "#050117"
            
            
            self.back_btn = ft.IconButton(icon=ft.icons.ARROW_BACK_ROUNDED, on_click=back, icon_color="white")
            self.favorite = ft.TextButton(text="Whatchlist", icon=ft.icons.ADD_BOX_ROUNDED, icon_color="red", on_click=self.add_to_list, style=ft.ButtonStyle(color="white"))
            self.notif = ft.SnackBar(content=ft.Text("", color="white", size=15, weight=ft.FontWeight.W_400), bgcolor="#c20000")
            page.overlay.append(self.notif)
            
            self.image = ft.Image(**self.image_style())
            self.name = ft.Container(height=200, content=ft.Column([
                                                        ft.Text(value="", size=15, weight=ft.FontWeight.BOLD, color="white", max_lines=3, overflow=ft.TextOverflow.ELLIPSIS), 
                                                        ft.Divider(color="#6d0bb6"),
                                                        ft.Text("Studio:", weight=ft.FontWeight.BOLD, color="white", no_wrap=True), 
                                                        ft.Text("Type:", weight=ft.FontWeight.BOLD, color="white", no_wrap=True), 
                                                        ft.Text("Status:", weight=ft.FontWeight.BOLD, color="white", no_wrap=True), 
                                                        ft.Text("Note:", weight=ft.FontWeight.BOLD, color="white", no_wrap=True)]), expand=True)
            self.box = ft.Container(content=ft.Row([self.image, self.name]), margin=ft.margin.only(left=10, right=10))
            self.top_box = ft.Row([self.back_btn, self.favorite], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            
            self.genres_text = ft.Container(**self.box_text_style(type="Genres"))
            self.genres_sub = ft.Container(**self.box_sub_style(size=14))
            self.genres = ft.Container(**self.box_style(), content=ft.Column([self.genres_text, self.genres_sub]))
            
            self.themes_text = ft.Container(**self.box_text_style(type="Thèmes"))
            self.themes_sub = ft.Container(**self.box_sub_style(size=14))
            self.themes = ft.Container(**self.box_style(), content=ft.Column([self.themes_text, self.themes_sub]))
            
            self.episodes_text = ft.Container(**self.box_text_style(type="Episodes"))
            self.episodes_sub = ft.Container(**self.box_sub_style(size=20))
            self.episodes = ft.Container(**self.box_style(), content=ft.Column([self.episodes_text, self.episodes_sub]))
            
            self.synopsis_banner = ft.Container(content=ft.Container(**self.synopsis_banner_style()), margin=ft.margin.only(top=10))
            self.synopsis_text = ft.Container(content=ft.Text(value=""), padding=ft.padding.only(left=10, right=15, bottom=15))
            
            
            self.box_2 = ft.Container(content=ft.Row([self.genres, self.themes, self.episodes], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), margin=ft.margin.only(top=25, left=10, right=10))
            self.content = ft.Column([self.top_box, self.box, self.box_2, self.synopsis_banner, self.synopsis_text], horizontal_alignment=ft.CrossAxisAlignment.START, scroll=ft.ScrollMode.ADAPTIVE)
            
                
        def image_style(self):
            return {
                "width": 150,
                "height": 200,
                "src": "image.png"
            }

        def box_text_style(self, type):
            return {
                "width": 100,
                "bgcolor": "#c20000",
                "alignment": ft.alignment.center,
                "padding": ft.padding.symmetric(vertical=5),
                "content": ft.Text(value=type, weight=ft.FontWeight.BOLD, font_family="Roboto", color="white")
            }
            
        def box_sub_style(self, size):
            return {
                "width": 100,
                "height": 100,
                "alignment": ft.alignment.center,
                "padding": ft.padding.only(bottom=7),
                "content": ft.Text(value="", text_align=ft.TextAlign.CENTER, font_family="Roboto", weight=ft.FontWeight.W_500, color="white", size=size)
            }
        
        def box_style(self):
            return {
                "width": 100, 
                "bgcolor": "#0a0329",
                "border_radius": 10
            }
        
        def synopsis_banner_style(self):
            return {
                "width": 150,
                "height": 30,
                "bgcolor": "#c20000",
                "alignment": ft.alignment.center,
                "border_radius": ft.border_radius.only(top_right=10, bottom_right=10),
                "content": ft.Text(value="Synopsis", size=17, weight=ft.FontWeight.BOLD, color="white")
            }
        
        
        def match_status(self, status):
            match status:
                case "Finished Airing":
                    return "Fin de diffusion"
                
                case "Not yet aired":
                    return "Annoncé"
                
                case "Currently Airing":
                    return "En cours"

        def translate_synopsis(self, synopsis):
            return synopsis

        def get_anime(self, id):
            url = f"https://api.jikan.moe/v4/anime/{id}/full"
            max_retries = 4
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    response = requests.get(url)
                    response.raise_for_status() 
                    
                    data = response.json()
                    
                    self.name.content.controls[0].value = data["data"]["title"]
                    
                    genres = [genre["name"] for genre in data["data"]["genres"]]
                    genres_str = "\n".join(genres)
                    self.genres_sub.content.value = genres_str
                    
                    themes = [theme["name"] for theme in data["data"]["themes"]]
                    themes_str = "\n".join(themes)
                    self.themes_sub.content.value = themes_str
                    
                    episodes = data["data"]["episodes"]
                    self.episodes_sub.content.value = str(episodes)
                    
                    self.image.src = data["data"]["images"]["jpg"]["large_image_url"]
                    self.synopsis_text.content.value = self.translate_synopsis(synopsis=data["data"]["synopsis"])
                    
                    studio = ", ".join([studio["name"] for studio in data["data"]["studios"]])
                    type_ = data["data"]["type"]
                    status = self.match_status(status=data["data"]["status"])
                    rating = data["data"]["score"]

                    self.name.content.controls[2].value = f"Studio:  {studio}"
                    self.name.content.controls[3].value = f"Types:  {type_}"
                    self.name.content.controls[4].value = f"Status:  {status}"
                    self.name.content.controls[5].value = f"Note:  {rating}"
                    page.update()
                    
                    break
                
                except requests.exceptions.HTTPError as http_err:
                    print(f"Erreur HTTP : {http_err}")
                    if response.status_code == 404:
                        # Si l'ID de l'anime est incorrect, arrêter les tentatives
                        break
                except requests.exceptions.ConnectionError:
                    print("Erreur de connexion. Nouvelle tentative...")
                except requests.exceptions.Timeout:
                    print("Délai d'attente dépassé. Nouvelle tentative...")
                except requests.exceptions.RequestException as err:
                    print(f"Erreur de requête : {err}")
                    # Pour toute autre erreur de requête, arrêter les tentatives
                    break
                
                
                retry_delay += 2  # Augmenter le délai entre les tentatives
        
        def add_to_list(self, e):
            pass





    page.bgcolor = "#050117"
    page.padding = 0
    
    def func(e):
        a.visible = False
        try:
            b.get_anime(id=20)
        except:
            pass
        b.visible = True
        page.update()
    
    def back(e):
        a.visible = True
        b.visible = False
        page.update()
        
    
    a = Anime_Box(name="Test", image="image.png", id=20, func=func)
    b = Anime_Info( back=back)
    c = ft.Container(content=ft.Column([a, b]), expand=True)
    
    page.add(c)
        
ft.app(target=main)
  
