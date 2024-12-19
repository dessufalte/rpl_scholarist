import flet as ft
from .backend import autocomplete, searcher
import wikipediaapi as vikiped
import json
import time
import os

class HomeScreen:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK  # Set default theme mode
        self.page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)
        self.page.dark_theme = ft.Theme(color_scheme_seed=ft.colors.PRIMARY)
        self.gradient_value = 0.0
        self.increasing = True
        self.searching = False
        # AppBar
        self.app_bar = ft.AppBar(
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.DATA_OBJECT),
                                    ft.Text("Data"),
                                ],
                                width=200
                            ),
                            on_click=lambda _: self.page.go("/history"),
                        ),
                        ft.PopupMenuItem(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.icons.SETTINGS),
                                    ft.Text("Settings"),
                                ],
                                width=200
                            ),
                            on_click=lambda _: self.page.go("/settings"),
                        ),
                    ],
                ),
                # IconButton untuk toggle theme
                ft.IconButton(
                    icon=ft.icons.DARK_MODE,
                    on_click=self.toggle_theme,
                    tooltip="Toggle Theme",
                ),
            ],
            title=ft.Text("Scholarist", weight=ft.FontWeight.BOLD),
            
        )

        self.sort_button = ft.PopupMenuButton(
            icon=ft.icons.SORT,
            items=[
                ft.PopupMenuItem(text="Sort by Title (Asc)", on_click=lambda e: self.sort_items("title", ascending=True)),
                ft.PopupMenuItem(text="Sort by Title (Desc)", on_click=lambda e: self.sort_items("title", ascending=False)),
                ft.PopupMenuItem(text="Sort by Date (Asc)", on_click=lambda e: self.sort_items("date", ascending=True)),
                ft.PopupMenuItem(text="Sort by Date (Desc)", on_click=lambda e: self.sort_items("date", ascending=False)),
            ],visible=False
        )
        self.loadingbar = ft.Container(
    content=ft.ProgressBar(
        width=self.page.width, 
        height=4, 
        bgcolor=ft.colors.ON_SECONDARY
    ),visible=False,
    bgcolor=ft.colors.TRANSPARENT,  # Warna latar belakang container
    padding=0,
    margin=0,
    alignment=ft.alignment.top_center,
    expand=False,  # Agar ukurannya hanya sesuai dengan konten
        )
        self.description_container = ft.Container(
            content=ft.Column(
            [
                ft.Text("Deskription[D:]", weight=ft.FontWeight.W_100 ,size=20),
                ft.Text("lorem ipsum lroeamk adsaknsnk jjk hkah hagsjd gajsgd hksag dhsghj gjgajg jhaggsg sagd gd hd gshgd sjgd hg jkgshhsh jh dhj shjs kjgsgd hsghgsj asghj ghkj uwiu uiiu ihwygguh ks "),
                ft.ElevatedButton("Selengkapnya")
            ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH,    
            ),
            padding=20,
            alignment=ft.alignment.center,
            visible=False,
        )
        self.suggestionlist = ft.Column()

        self.input_field = ft.SearchBar(
            bar_hint_text="Cari..",
            on_tap= self.on_tap,
            expand=True,
            controls= [self.suggestionlist],
            on_change= self.on_autocomplete,
            on_submit= self.on_submit_searchbar,
        )
        
        # IconButton untuk kirim pesan
        self.send_button = ft.IconButton(
            icon=ft.icons.SEND,
            on_click=lambda e: self.go_search(self.input_field.value)
        )
        self.buah = ["apple", "banana", "orange", "grape", "strawberry", "watermelon", "kiwi", "pineapple", "mango", "pear"]
        
        self.input_row = ft.Row(
            [
                self.input_field,
                self.send_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # ListView
        self.list_view = ft.ListView(
            spacing=10,
            auto_scroll=False,
            expand=True,
            visible=False,
        )
        # MenuBar
        self.menu_bar = ft.MenuBar(
            [
                ft.MenuItemButton(ft.ElevatedButton("Test 1")),
                ft.MenuItemButton(ft.ElevatedButton("Test 2")),
                ft.MenuItemButton(ft.ElevatedButton("Test 3")),
            ]
        )
        self.deviders = ft.Divider(height=1)

        self.confirm_button = ft.FloatingActionButton(
            icon=ft.icons.CHECK,
            text="Confirm",
            visible=False,
            on_click= self.navigate_to_bibliography, 
        )
        self.item_count_text = ft.Text("Items: 0", italic=True, size=12, visible=False)
        self.status = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.sort_button,
                self.item_count_text, 
            ],
        )
        self.textcover = ft.Text("Mulailah Pencarian" , weight=ft.FontWeight.W_900, size=30)
        self.coverapp = ft.Column(
            [
                ft.Row([self.textcover,ft.Icon(ft.icons.EXPLORE)], alignment=ft.MainAxisAlignment.CENTER, height=150)   
            ]
        )
        self.manualplaceholder1 = ft.Container(ft.Column([ft.Icon(ft.icons.BOOK_ONLINE), ft.Text("Carilah kata kunci yang disesuaikan")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, expand=True, border_radius=20, height=100 , bgcolor=ft.colors.SECONDARY_CONTAINER)
        self.manualplaceholder2 = ft.Container(ft.Column([ft.Icon(ft.icons.LIST), ft.Text("Gunakan pembuatan daftar pustaka otomatis")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, expand=True, border_radius=20, height=100 , bgcolor=ft.colors.SECONDARY_CONTAINER)
        self.manualplaceholder3 = ft.Container(ft.Column([ft.Icon(ft.icons.COMPUTER), ft.Text("Koneksikan ke word, json, dan simpan")], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, expand=True, border_radius=20, height=100 ,  bgcolor=ft.colors.SECONDARY_CONTAINER)
        self.manual = ft.Row([
            self.manualplaceholder1,
            self.manualplaceholder2,
            self.manualplaceholder3,
            ], alignment=ft.MainAxisAlignment.CENTER)
        
        
        self.hiddendiv = ft.Divider(height=50, opacity=0)
        self.checked_items = []
        self.view = ft.View(
            "/",
            [   
                self.app_bar,
                
                self.deviders,
                self.loadingbar,
                self.coverapp,
                self.description_container,
              
                self.hiddendiv,
                
                self.status,
                self.list_view,
                self.input_row,
                self.manual,
                self.confirm_button,
                # self.manualcont
                
                # self.menu_bar,
            ]
        )
        
        self.theme_icon = self.app_bar.actions[-1]
    def on_submit_searchbar(self, e):
        self.go_search(self.input_field.value.strip())
    def start_search_process(self):
       
        self.loadingbar.value = 0
        self.page.update()

        total_steps = 10
        for i in range(total_steps + 1):
            time.sleep(0.02) 
            self.loadingbar.value = i / total_steps
            self.page.update()

        self.loadingbar.value = 1
        self.page.update()
    def update_item_count(self):
        item_count = len(self.list_view.controls)
        self.item_count_text.value = f"Items: {item_count}"
        self.item_count_text.update()
    def unfocus(self):
        self.input_field.close_view()
        self.input_field.will_unmount()
    async def toggle_loading(self):
        self.loadingbar.visible = not self.loadingbar.visible
        await self.page.update()
        
    def sort_items(self, key, ascending=True):
        """Sort item di list_view berdasarkan key tertentu."""
        self.list_view.controls.sort(
            key=lambda item: item.data[key], reverse=not ascending
        )
        self.page.update()
    def viki_search(self, query):
        wiki_wiki = vikiped.Wikipedia('scholarist (magnesiumsulfat04@gmail.com)', 'en')
        try:
            page = wiki_wiki.page(query)
            
            if page.exists():
                title_page = page.title
                description = page.summary
                page_url = f"https://en.wikipedia.org/wiki/{title_page.replace(' ', '_')}" 
                self.description_container.content = ft.Column([
                    ft.Text(title_page, weight=ft.FontWeight.W_100 ,size=20),
                    ft.Text(description, max_lines=8, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.ElevatedButton("Selengkapnya", on_click=lambda e: self.page.launch_url(page_url))
                ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
                
                self.description_container.visible = True 
            else:
                self.description_container.content = ft.Column([
                    ft.Text("Halaman tidak ditemukan di Wikipedia."),
                    ft.ElevatedButton("Coba Lagi")
                ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
                
                self.description_container.visible = True  
        except Exception as ex:
            self.description_container.content = ft.Column([
                ft.Text("Terjadi kesalahan saat mengambil data."),
                ft.ElevatedButton("Coba Lagi")
            ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
            
            self.description_container.visible = True 
            print(f"Error: {ex}") 

        self.description_container.update()  

    def create_item_container(self, title, authors, summary, date, source, link):
        
        if isinstance(authors, str):
            authors = [authors]
        max_display = 2
        displayed_authors = authors[:max_display]
        if len(authors) > max_display:
            displayed_authors.append("+") 
        authors_string = ", ".join(authors)
        author_chips = [
            ft.Chip(
                label=ft.Text(author),
                color=ft.colors.SECONDARY_CONTAINER,
                tooltip=authors_string if author == "+" else None,
            )
            for author in displayed_authors
        ]
        author_rows = ft.Row(author_chips,)
        
        checkmark = ft.Checkbox(value=False, on_change=self.confirm_action)
        self.checked_items.append({
            "checkmark": checkmark,
            "title": title,
            "authors": authors,
            "summary": summary,
            "date": date,
            "link": link,
            "source": source
        })
   
        
        title_text = ft.Text(
            title,
            weight=ft.FontWeight.W_200,
            size=20,
            overflow=ft.TextOverflow.ELLIPSIS,
            max_lines=1,
            width=350
        )
        
        is_expanded = False
        desc_text = ft.Text(summary, max_lines=3, overflow=ft.TextOverflow.FADE)
        def toggle_desc_text(e):
            nonlocal is_expanded
            is_expanded = not is_expanded
            desc_text.max_lines = None if is_expanded else 3
            desc_text.update()  
        metadata = {
            "title": title,
            "authors": authors,
            "summary": summary,
            "date": date,
            "source": source,
            "link": link,
        }
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            checkmark,
                            title_text
                        ]
                    ),
                    ft.Text(f"Date: {date}", size=12, italic=True, color=ft.colors.SECONDARY), 
                    author_rows,
                    desc_text,
                    ft.Row(
                        [
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.LIBRARY_BOOKS, size=17),
                                        ft.Text(source)
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    height=24
                                ),
                                border=ft.border.all(1),
                                padding=5,
                                border_radius=10
                            ),
                            ft.IconButton(ft.icons.TRAVEL_EXPLORE, icon_size=15, on_click=lambda e: self.page.launch_url(link)) 
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ]
            ),
            padding=10,
            bgcolor=ft.colors.ON_SECONDARY,
            border_radius=10,
            alignment=ft.alignment.center, 
            on_click=toggle_desc_text,
            data=metadata
        )
    # def show_bibliography(self, checked_items):
    #     bibliography_page = ft.Page()

    #     bibliography_page.appbar = ft.AppBar(
    #         title=ft.Text("Bibliography List"),
    #         bgcolor=ft.colors.PRIMARY
    #     )

    #     bibliography_column = ft.Column(
    #         controls=[
    #             ft.Column(
    #                 controls=[
    #                     ft.Text(f"Title: {item['title']}", size=16, weight=ft.FontWeight.W_600),
    #                     ft.Text(f"by {item['authors']}", size=12),
    #                     ft.Text(f"Summary: {item['summary']}", size=12),
    #                     ft.Text(f"Date: {item['date']}", size=12),
    #                     ft.Divider(),
    #                 ]
    #             ) for item in checked_items if item["checkmark"].value
    #         ]
    #     )

    #     bibliography_page.add(bibliography_column)

    #     # Navigasi ke halaman baru
    #     page.go("/bibliography")

    #     # Update halaman
    #     page.update()


    def navigate_to_bibliography(self, e):
        filtered_items = [item for item in self.checked_items if item['checkmark'].value is True]
        self.page.session.set("items_check",filtered_items)
        self.page.go("/bibliography")
        # Navigasi ke halaman baru dengan daftar pustaka
        # self.show_bibliography(self.checked_items)
        
    def on_tap(self, e):
            self.input_field.open_view()
    def get_view(self):
        return self.view
    def confirm_action(self, e):
        all_checked = any(cb["checkmark"].value for cb in self.checked_items)
        self.confirm_button.visible = all_checked
        self.page.update()
    async def on_autocomplete(self, e):
        search_query = self.input_field.value.strip()
        if search_query:
            suggestions = await autocomplete.get_autocomplete(search_query)
            self.update_list_tiles(suggestions)
    def update_list_tiles(self, suggestions):
        self.suggestionlist.controls.clear()
        for suggestion in suggestions[:5]:
            list_tile = ft.CupertinoListTile(
                title=ft.Text(suggestion),
                on_click=lambda e, s=suggestion: self.select_suggestion(s)
            )
            self.suggestionlist.controls.append(list_tile)
        self.suggestionlist.update()
    def select_suggestion(self, suggestion):
        self.go_search(suggestion)
    def on_animation_change(self, e):
        if self.increasing:
            self.gradient_value += 0.01
            if self.gradient_value >= 1.0:
                self.increasing = False
        else:
            self.gradient_value -= 0.01
            if self.gradient_value <= 0.0:
                self.increasing = True
        self.textcover.style.foreground = ft.Paint(
            gradient=ft.PaintLinearGradient(
                (self.gradient_value * 500, 20),
                ((1 - self.gradient_value) * 500, 20),
                [
                    ft.colors.PURPLE,
                    ft.colors.TEAL,
                ],
            )
        )
        self.textcover.update()
    def go_search(self, query):
        self.coverapp.visible = False
        self.manual.visible = False
        self.hiddendiv.visible = False
        self.loadingbar.visible=True
        self.loadingbar.update()
        # file_path = os.path.join(os.getcwd(), "frontend/test.json")
        # print(file_path)
        
        # with open(file_path, 'r') as file:
        #     papers = json.load(file)
        # self.toggle_loading()
        papers = searcher.run_smart_searching(query)
        if papers:
            items = [
                self.create_item_container(
                    paper.get('title'),
                    paper.get('authors'),
                    paper.get('summary'),
                    paper.get('date'),
                    paper.get('source'),
                    paper.get('link')
                )
                for paper in papers
            ]
            self.list_view.controls = items
        self.update_item_count()
        self.viki_search(query)
        self.sort_button.visible = True
        self.loadingbar.visible = False
        self.description_container.visible = True
        self.status.visible = True
        self.list_view.visible = True
        self.item_count_text.visible = True
        self.searching = True
        self.loadingbar.visible=False
        self.loadingbar.update()
        self.coverapp.update()
        self.sort_button.update()
        self.item_count_text.update()
        self.description_container.update()
        self.manual.update()
        self.hiddendiv.update()
        self.status.update()
        self.list_view.update()

    def toggle_theme(self, e):
        # Mengubah theme mode berdasarkan nilai IconButton
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_icon.icon = ft.icons.DARK_MODE
            self.textcover.style = ft.TextStyle(foreground=ft.Paint(gradient=ft.PaintLinearGradient((0,20),(500,20),[ft.colors.PURPLE,ft.colors.TEAL])))
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_icon.icon = ft.icons.LIGHT_MODE
            self.textcover.style = ft.TextStyle(foreground=ft.Paint(gradient=ft.PaintLinearGradient((0,20),(500,20),[ft.colors.PINK,ft.colors.ORANGE_300])))
        self.page.update()
