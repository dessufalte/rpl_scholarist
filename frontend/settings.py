import flet as ft

def settings_screen(page: ft.Page):

    def on_menu_click(item):
        if item == "Change Theme":
            page.theme_mode = (
                ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
            )
            page.update()
        elif item == "Help":
            page.go("/help")
        elif item == "About":
            page.go("/about")
        elif item == "API":
            page.go("/api_key")

    menu_items = [
        ft.ListTile(
            leading=ft.Icon(ft.icons.BRIGHTNESS_6),
            title=ft.Text("Change Theme"),
            on_click=lambda _: on_menu_click("Change Theme"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.icons.HELP_OUTLINE),
            title=ft.Text("Help"),
            on_click=lambda _: on_menu_click("Help"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.icons.KEY),
            title=ft.Text("API Key"),
            on_click=lambda _: on_menu_click("API"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.icons.INFO_OUTLINE),
            title=ft.Text("About"),
            on_click=lambda _: on_menu_click("About"),
        ),
    ]

    return ft.View(
        "/settings",
        [
            ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Column(
                [
                    *menu_items, 
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
        ],
    )
