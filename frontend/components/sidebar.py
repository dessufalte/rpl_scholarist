import flet as ft

# Sidebar sebagai objek
class Sidebar(ft.UserControl):
    def __init__(self, page: ft.Page, width: int = 250):
        super().__init__()
        self.page = page
        self.width = width
        self.is_open = False
        
        # Sidebar content
        self.sidebar_content = ft.Column([
            ft.Text("Sidebar Item 1"),
            ft.Text("Sidebar Item 2"),
            ft.Text("Sidebar Item 3"),
        ])
        
        # Sidebar container
        self.sidebar = ft.Container(
            content=self.sidebar_content,
            width=self.width,
            bgcolor=ft.colors.GREY_200,
            visible=self.is_open,
        )
        
        # Toggle button
        self.toggle_button = ft.IconButton(
            icon=ft.icons.MENU,
            on_click=self.toggle_sidebar,
        )

    def toggle_sidebar(self, e):
        # Toggle state open/close
        self.is_open = not self.is_open
        self.sidebar.visible = self.is_open
        self.update()

    def build(self):
        return ft.Row([self.toggle_button, self.sidebar])

