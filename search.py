import flet as ft
import requests
import time
import os
import re



class Anime_Box(ft.Container):
    def __init__(self, page, name, image, id, func):
        super().__init__()
        self.id = id
        self.page = page
        self.func = func
        self.height = 100
        self.border_radius = 8
        self.bgcolor = "#0a0329"
        self.alignment = ft.alignment.center_left
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
            "content" : ft.Container(content=ft.Text(value=name, size=15, weight=ft.FontWeight.BOLD, color="white"), padding=ft.padding.only(top=5))
        }
        
        
    def save_data(self, e):
        self.page.client_storage.remove("id")
        self.page.client_storage.set("id", self.id)
        self.func(e)


class Anime_Info(ft.Container):
    def __init__(self, page, back):
        super().__init__()
        self.page = page
        self.expand = True
        self.visible = True
        self.bgcolor = "#050117"
        
        
        self.back_btn = ft.IconButton(icon=ft.icons.ARROW_BACK_ROUNDED, on_click=back, icon_color="white")
        self.favorite = ft.TextButton(text="Whatchlist", icon=ft.icons.ADD_BOX_ROUNDED, icon_color="red", on_click=self.add_to_list, style=ft.ButtonStyle(color="white"))
        self.notif = ft.SnackBar(content=ft.Text("", color="white", size=15, weight=ft.FontWeight.W_400), bgcolor="#c20000")
        self.page.overlay.append(self.notif)
        
        self.image = ft.Image(**self.image_style())
        self.name = ft.Container(height=200, width=self.calcul(), content=ft.Column([
                                                    ft.Text(value="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", size=15, weight=ft.FontWeight.BOLD, color="white", max_lines=3, overflow=ft.TextOverflow.ELLIPSIS), 
                                                    ft.Divider(color="#6d0bb6"),
                                                    ft.Text("Studio:", weight=ft.FontWeight.BOLD, color="white"), 
                                                    ft.Text("Type:", weight=ft.FontWeight.BOLD, color="white"), 
                                                    ft.Text("Status:", weight=ft.FontWeight.BOLD, color="white"), 
                                                    ft.Text("Note:", weight=ft.FontWeight.BOLD, color="white")]))
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
            
            # Attendre avant de refaire une tentative
            time.sleep(retry_delay)
            retry_delay += 2  # Augmenter le délai entre les tentatives
    
    def add_to_list(self, e):
        name = self.name.content.controls[0].value
        nb_episodes = self.episodes_sub.content.value
        image_src = self.image.src
        dossier = "C:/Users/Abdoul Karim/3D Objects/My anime/source code/Dossier"
        
        os.makedirs(dossier, exist_ok=True)
        nom_complet = f"{nb_episodes};{name}.png"
        chemin_complet = os.path.join(dossier, nom_complet)
        
        try:
            response = requests.get(image_src)
            if response.status_code == 200:
                with open(chemin_complet, 'wb') as fichier:
                    fichier.write(response.content)
                    self.notif.content.value = "Anime ajouter à la watchlist"
                    self.notif.open = True
                    self.page.update()
            else:
                self.notif.content.value = "Veuillez patienter et réessayer"
                self.notif.open = True
                self.page.update()
        except:
            self.notif.content.value = "Erreur de connexion"
            self.notif.open = True
            self.page.update()
      
    def calcul(self):
        a = self.page.window.width * 185
        b = a/375-20
        c = int(b)
        
        return c
              
      
class Anime_Results(ft.Container):
    def __init__(self, page, go_info):
        super().__init__()
        self.page = page
        self.go_info = go_info
        self.expand = True
        self.alignment = ft.alignment.top_center
        

        self.charging = ft.Container(content=ft.ProgressRing(width=25, height=25), visible=False, alignment=ft.alignment.center)
        self.notif = ft.SnackBar(content=ft.Text("", color="white", size=15, weight=ft.FontWeight.W_400), bgcolor="#c20000")
        self.page.overlay.append(self.notif)
        self.search_entry = ft.Container(**self.search_entry_style())
        self.search_btn = ft.Container(content=ft.IconButton(**self.search_btn_style()))
        self.search_box = ft.Container(**self.search_box_style())
        
        self.result_box = ft.Column([], scroll=ft.ScrollMode.ALWAYS)
        
        self.content = ft.Column([self.search_box, self.charging, self.result_box], scroll=ft.ScrollMode.ALWAYS)


    def search_entry_style(self):
        return{
            "expand" : True,
            "content" : ft.TextField(border_width=0, height=20, cursor_color="#c20000", content_padding=ft.padding.only(left=17), hint_text="Rechercher un anime")
        }

    def search_btn_style(self):
        return{
            "bgcolor" : "#c20000", 
            "icon_color" : "white", 
            "icon" : ft.icons.SEARCH_SHARP, 
            "on_click" : self.search_anime
        }

    def search_box_style(self):
        return{
            "border_radius" : 20,
            "bgcolor" : "#0a0329",
            "alignment" : ft.alignment.center_right,
            "content" : ft.Row([self.search_entry, self.search_btn], alignment=ft.MainAxisAlignment.CENTER)
        }



    def nettoyer_texte(self, texte):
        texte_nettoye = re.sub(r'[^\w\s]', '', texte)
        return texte_nettoye.lower()

    def correspond_titre(self, anime, mots_cles):
        titres = [
            anime.get('title', ''),
            anime.get('title_english', ''),
            anime.get('title_japanese', '')
        ] + anime.get('title_synonyms', [])
        
        # Nettoyer chaque titre et vérifier la correspondance
        for titre in titres:
            titre_nettoye = self.nettoyer_texte(titre)
            if any(mot in titre_nettoye for mot in mots_cles):
                return True
        return False

    def get_anime_results(self, nom_anime):
        # URL de l'API Jikan pour la recherche d'anime
        url = f"https://api.jikan.moe/v4/anime?q={nom_anime}&limit=10"
        
        # Effectuer la requête GET
        response = requests.get(url)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Convertir la réponse en JSON
            data = response.json()
            
            # Si des résultats ont été trouvés
            if data['data']:
                mots_cles = self.nettoyer_texte(nom_anime).split()
                animes_filtres = [anime for anime in data['data'] if self.correspond_titre(anime, mots_cles)]
                
                if animes_filtres:
                    # Trier les animes filtrés par ordre croissant de leur ID
                    animes_filtres.sort(key=lambda anime: anime['mal_id'])
                    
                    # Retourner les informations des animes triés
                    return [
                        {
                            "id": anime['mal_id'],
                            "title": anime['title'],
                            "image_url": anime['images']["jpg"]["large_image_url"]
                        }
                        for anime in animes_filtres
                    ]
                else:
                    return "Aucun anime correspondant trouvé."
            else:
                return "Aucun anime trouvé pour ce nom."
        else:
            return f"Erreur lors de la requête : {response.status_code}"

      
    def search_anime(self, e):
        self.charging.visible = True
        self.page.update()
        results = False
        
        try:
            results = self.get_anime_results(nom_anime=self.search_entry.content.value)
        except:
            self.notif.content.value = "Erreur de connexion"
            self.notif.open = True
            self.charging.visible = False
            self.page.update()
       
        if results:
            self.result_box.controls.clear()
            for anime in results:
                self.result_box.controls.append(Anime_Box(name=anime["title"], image=anime["image_url"], id=anime["id"], func=self.click, page=self.page))
            self.update()
            self.charging.visible = False
            self.page.update()
        else:
            self.notif.content.value = "Erreur de connexion"
            self.notif.open = True
            self.charging.visible = False 
            self.page.update()
            
        
        
                  
    def click(self, e):
        self.charging.visible = True
        self.charging.update()
        self.go_info(e)
        self.update()
    
    
