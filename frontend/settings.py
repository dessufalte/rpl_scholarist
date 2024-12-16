import flet as ft

def settings_screen(page: ft.Page):
    # Fungsi untuk menangani klik pada item menu
    def on_menu_click(item):
        if item == "Change Theme":
            page.theme_mode = (
                ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
            )
            page.update()
        elif item == "Help":
            ft.dialog_alert(page, title="Help", content="This is the Help section.")
        elif item == "About":
            ft.dialog_alert(page, title="About", content="Settings screen for the application.")

    # Membuat daftar menu menggunakan ListTile
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
            on_click=lambda _: on_menu_click("About"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.icons.DATA_ARRAY),
            title=ft.Text("Data"),
            on_click=lambda _: on_menu_click("About"),
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
