import flet as ft
import requests
import re



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
            
    class Anime_Results(ft.Container):
        def __init__(self, go_info):
            super().__init__()
            self.go_info = go_info
            self.expand = True
            self.alignment = ft.alignment.top_center
            

            self.charging = ft.Container(content=ft.ProgressRing(width=25, height=25), visible=False, alignment=ft.alignment.center)
            self.notif = ft.SnackBar(content=ft.Text("", color="white", size=15, weight=ft.FontWeight.W_400), bgcolor="#c20000")
            page.overlay.append(self.notif)
            self.search_entry = ft.Container(**self.search_entry_style())
            self.search_btn = ft.Container(content=ft.IconButton(**self.search_btn_style()))
            self.search_box = ft.Container(**self.search_box_style(), on_click= lambda _: self.search_entry.content.focus())
            
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
            page.update()
            results = False
            
            try:
                results = self.get_anime_results(nom_anime=self.search_entry.content.value)
            except:
                self.notif.content.value = "Erreur de connexion"
                self.notif.open = True
                self.charging.visible = False
                page.update()
        
            if results:
                self.result_box.controls.clear()
                for anime in results:
                    self.result_box.controls.append(Anime_Box(name=anime["title"], image=anime["image_url"], id=anime["id"], func=self.click))
                self.update()
                self.charging.visible = False
                page.update()
            else:
                self.notif.content.value = "Anime introuvable"
                self.notif.open = True
                self.charging.visible = False 
                page.update()
                
        def click(self, e):
            self.charging.visible = True
            self.charging.update()
            self.go_info(e)
            self.update()



    page.add(Anime_Results(go_info=None))
    
ft.app(target=main)
        
