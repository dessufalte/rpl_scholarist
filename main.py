import flet as ft

# from frontend.home import HomeScreen
from frontend.settings import settings_screen
from frontend.history import history_screen
from frontend.home import HomeScreen
from frontend.biblio import bibliography_screen
from frontend.help import help_screen
from frontend.api_key import api_key_screen
from frontend.about import about_screen

def main(page: ft.Page):
    page.title = "Scholarist"
    home_screen = HomeScreen(page)
    home_screen.page.theme_mode = ft.ThemeMode.DARK

    def route_change(route):
        page.views.clear()
        page.views.append(home_screen.get_view())
        if page.route == "/settings":
            page.views.append(settings_screen(page))
        elif page.route == "/history":
            page.views.append(history_screen(page))
        elif page.route == "/help":
            page.views.append(help_screen(page))
        elif page.route == "/about":
            page.views.append(about_screen(page))
        elif page.route == "/api_key":
            page.views.append(api_key_screen(page))
        elif page.route == "/bibliography":
            items_check = page.session.get("items_check")
            if items_check is None:
                items_check = []
            page.views.append(bibliography_screen(page,items_check))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(main, view=ft.AppView.FLET_APP)
