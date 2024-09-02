
import flet as ft
from scrapper import semanticc
from pybliometrics.scopus import ScopusSearch
import wikipediaapi as vikiped
import webbrowser
import scrapper.urls as urls
import requests

_dark: str = ft.colors.with_opacity(0.5, "white")
_light: str = ft.colors.with_opacity(1, "black")

toggle_style_sheet: dict = {"icon": ft.icons.DARK_MODE_ROUNDED, "icon_size": 18}
search_style_sheet: dict = {"icon": ft.icons.SEND, "icon_size": 18}

item_style_sheet: dict = {
    "height": 50,
    "expand": True,
    "border_color": _dark,
    "cursor_height": 24,
    "hint_text": "Search here...",
    "content_padding": 15,
}

item_style_sheet: dict = {"border_radius": 4}



class DaftarPustaka(ft.Container):
    #item
    def __init__(self, Body: object, title_text: str, author:str, abstract:str, year:int, theme: str):
        if theme == "dark":
            item_style_sheet["border"] = ft.border.all(1, _dark)
        else:
            item_style_sheet["border"] = ft.border.all(1, _light)

        super().__init__(**item_style_sheet)
        self.Body = Body
        self.authors_name = author
        self.abstract_text = abstract
        self.year_val = year
        self.title_text = title_text
        self.title_text_preprocessing = title_text[:70] + "..."  if len(title_text) > 70 else title_text
        self.title: ft.Text = ft.Text(self.title_text_preprocessing, size=16, weight="bold", no_wrap=False, max_lines=2)  # Judul lebih besar dan tebal
        self.title_tooltip = ft.Tooltip(
            message=self.title_text,
            content=self.title
        )
        self.tick = ft.Checkbox(on_change=lambda e: self.check(e))
        self.authors_text: ft.Text = ft.Text(self.authors_name, size=14, no_wrap=False, max_lines=1)
        self.year: ft.Text = ft.Text(self.year_val, size=14, no_wrap=False, max_lines=1)
        self.abstract: ft.Text = ft.Text(self.abstract_text, size=14, max_lines=3, text_align=ft.TextAlign.JUSTIFY)  # Menyediakan lebih banyak ruang untuk abstrak
       
        self.item_contents: ft.Container = ft.Container(
            content=self.title,
            
        )
        self.row: ft.Row = ft.Row(
            wrap=True,
            alignment="spaceBetween",
            controls=[
                ft.Row(controls=[self.tick,self.title_tooltip,]),
                ft.Row(controls=[self.abstract], wrap=True),
                ft.Row(controls=[self.authors_text,self.year]),
                
            ],
        )
        self.content = ft.Container(
            content=self.row,
            on_click=lambda e: self.handle_click(e),
            padding=10,
        )

    def handle_click(self, e):
        print("ok")


    def check(self, e):
        if e.control.value is True:
            print("ok")
        else:
            print("tdk")

        self.title.update()


class Viki(ft.Container):
    def __init__(self, p: ft.Page):
        super().__init__()
        
        self.page = p
        self.title = ft.Text(
            value="xxxx",
            size=20,
            weight="bold",
            text_align="center"
        )
        self.hidden_link = ft.TextField(
            value="",
            visible=False
        )
        self.description = ft.Text(
            value="xxxx",
        )
        self.link_button = ft.ElevatedButton(
            text="Lihat selengkapnya",
            on_click=lambda e: self.open_link(self.hidden_link.value)
        )
        
        self.content = ft.Column(
            controls=[
                self.title,
                self.description,
                self.link_button,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10,
        )
         
        self.padding = 20

        self.controls = [self.content]

    def open_link(self, url):
         if url:
            webbrowser.open(url)
            print(f"Opening link: {url}")

class Details(ft.Container):
    def __init__(self, page: ft.Page, switch_page):
        super().__init__()
        self.page = page
        self.switch_page = switch_page

        self.title = ft.Text(value="Page 2", size=32)
        self.back_button = ft.ElevatedButton(
            text="Back to Page 1",
            on_click=lambda e: self.switch_page(1)
        )

        self.content = ft.Column(
            controls=[self.title, self.back_button],
            alignment="center",
            horizontal_alignment="center",
            spacing=10
        )
        
        self.controls = [self.content]

class Body(ft.SafeArea):
    def __init__(self, page: ft.Page):
        super().__init__(minimum=10, maintain_bottom_view_padding=True,content=Body)
        self.page = page
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.title: ft.Text = ft.Text("RPL Scholarist", size=20, weight="w800")
        self.toggle: ft.IconButton = ft.IconButton(
            **toggle_style_sheet, on_click=lambda e: self.switch(e)
        )
        self.suggestions_list = ft.ListTile(
            title="",
        )
        self.item = ft.SearchBar(
            bar_hint_text="Cari..",
            view_hint_text="Pilih dari saran pencarian...",
            on_change=self.on_search,
            on_submit=self.on_submit,
            on_tap=self.on_tap,
            controls=[
                ft.ListTile(title=ft.Text(f"Color {i}"), data=i)
                for i in range(10)
            ],
        )

        self.list_box: ft.Column = ft.Column(
            spacing=18,
            visible=False,
        )
        self.counter: ft.Text = ft.Text("0 item", italic=True)
        self.submit_button: ft.Container = ft.Container(
            content=ft.Text("Submit", color= ft.colors.BLUE_100),
            margin=10,
            alignment=ft.alignment.center,
            padding= 20,
            border_radius=10,
            ink=True,
            visible=False,
            on_click=lambda e: self.submit_item(e),
        )
        self.loading_indicator = ft.ProgressRing(
            color=ft.colors.BLUE_500,
            visible=False  # Initially hidden
        )
        self.viki_control = Viki(self.page)
        self.viki_control.visible = False
        self.main: ft.Column = ft.Column(
            controls=[
                
                ft.Row(
                    
                    alignment="spaceBetween",
                    controls=[self.title, self.toggle],
                ),
                ft.Divider(height=20),
                self.item,
                ft.Divider(height=10, color="transparent"),
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Text("Daftar Pustaka"),
                        self.counter,
                    ],
                ),
                self.loading_indicator,
                self.viki_control,
                self.list_box,
                self.submit_button,
                
            ]
        )
        self.content = self.main
    def on_submit(self, e):
        self.search(self.item.value.strip())

    def on_search(self, e):
        search_query = self.item.value.strip()
        if search_query:
            suggestions = self.get_wikipedia_suggestions(search_query)
            self.update_list_tiles(suggestions)
        else:
            self.item.controls = []
            self.item.update()

    def on_tap(self, e):
        # Handle the tap event, e.g., show suggestions
        self.item.open_view()
        # You could also trigger a search or show suggestions here if needed

    def on_close(self, e):
        # Handle the close event, e.g., clear the search or hide suggestions
        self.item.close_view()
    def get_wikipedia_suggestions(self, query):
        url = f"https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": query,
            "limit": 5,
            "namespace": 0,
            "format": "json"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data[1]  # List of titles
        return []
    def update_list_tiles(self, suggestions):
        self.item.controls = [
            ft.ListTile(
                title=ft.Text(suggestion),
                on_click=lambda e, s=suggestion: self.select_suggestion(s)
            )
            for suggestion in suggestions
        ]
        self.item.update()

    def select_suggestion(self, suggestion):
        self.item.value = suggestion
        self.item.controls = []
        self.update()
        self.search(suggestion)

    def on_focus_change(self, e):
        if not self.item.focused:
            self.update()

    def item_size(self):
        self.counter.value = f"{len(self.list_box.controls[:])} Item"
        self.counter.update()

    def search(self, query):
        self.loading_indicator.visible = True
        self.loading_indicator.update()
        self.viki_search(self, query)
        if self.viki_control.hidden_link.value:
            self.viki_control.visible = True
            self.viki_control.update()

        self.list_box.controls.clear()
        papers = semanticc.fetch_paper_details(urls.sscholar, query=query, limit=10)
        if papers:
            for paper in papers:
                if self.page.theme_mode == ft.ThemeMode.DARK:
                    self.list_box.controls.append(DaftarPustaka(self, paper["title"],paper["authors"],paper["summary"],paper["year"],"dark"))
                else:
                    self.list_box.controls.append(DaftarPustaka(self, paper["title"], "light"))

        self.loading_indicator.visible = False
        self.loading_indicator.update()
        self.list_box.visible = True
        self.submit_button.visible = True
        self.submit_button.update()
        self.list_box.update()
        self.item_size()
        self.item.value = ""
        self.item.update()

    def viki_search(self, e, query):
        wiki_wiki = vikiped.Wikipedia('scholarist (magnesiumsulfat04@gmail.com)', 'en')
        page = wiki_wiki.page(query)
        if page.exists():
            self.viki_control.hidden_link.value = page.fullurl
            self.viki_control.title.value = page.title
            self.viki_control.description.value = page.summary[:500]
        else:
            self.viki_control.hidden_link.value = ""
            self.viki_control.title.value = "Page not found"
            self.viki_control.description.value = "No results found for your query."

    def submit_item(self, e):
        if len(self.list_box.controls[:]) < 1:
            dlg = ft.AlertDialog(
                title=ft.Text("Peringatan"),
                content=ft.Text("Kamu belum memilih sumber referensi"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: self.page.close(dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            self.page.open(dlg)
    def switch(self, e):
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.toggle.icon = ft.icons.LIGHT_MODE_ROUNDED
            self.item.border_color = _light

            for item in self.list_box.controls[:]:
                item.border = ft.border.all(1, _light)

        else:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.toggle.icon = ft.icons.DARK_MODE_ROUNDED
            self.item.border_color = _dark

            for item in self.list_box.controls[:]:
                item.border = ft.border.all(1, _dark)

        self.page.update()








def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    theme = ft.Theme()
    page.theme = theme
    Mains: object = Body(page)
   
    page.add(Mains)
    page.update()
    Mains.list_box.controls.append(DaftarPustaka(Mains, title_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vel mollis nibh. Aenean vel mi fermentum purus imperdiet tincidunt sed consectetur mauris. Aliquam risus eros, vulputate eget pulvinar ac, faucibus et dolor. Duis tincidunt pellentesque neque sit amet dapibus. Curabitur tristique vehicula augue, at commodo urna varius porta. Quisque iaculis dapibus sem, non convallis sapien tempor eu. Morbi ac fringilla lorem. Praesent nec nisl rhoncus, tempus velit quis, accumsan quam. Cras fermentum pulvinar ante eu aliquet. Nulla quis augue sit amet velit sollicitudin condimentum. Nullam at sapien at eros molestie malesuada sit amet et est. Sed sed mauris ut ex cursus scelerisque eu ac eros.",abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vel mollis nibh. Aenean vel mi fermentum purus imperdiet tincidunt sed consectetur mauris. Aliquam risus eros, vulputate eget pulvinar ac, faucibus et dolor. Duis tincidunt pellentesque neque sit amet dapibus. Curabitur tristique vehicula augue, at commodo urna varius porta. Quisque iaculis dapibus sem, non convallis sapien tempor eu. Morbi ac fringilla lorem. Praesent nec nisl rhoncus, tempus velit quis, accumsan quam. Cras fermentum pulvinar ante eu aliquet. Nulla quis augue sit amet velit sollicitudin condimentum. Nullam at sapien at eros molestie malesuada sit amet et est. Sed sed mauris ut ex cursus scelerisque eu ac eros.", author="Agus",year="2003",theme="dark"))
    Mains.list_box.controls.append(DaftarPustaka(Mains, title_text="Lorem ipsum ",abstract="lorem lorem lorem", author="Agus",year="2003",theme="dark"))
    Mains.list_box.visible = True 
    Mains.list_box.update()
    


if __name__ == "__main__":
    ft.app(target=main)
