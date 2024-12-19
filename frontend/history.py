import sqlite3
import flet as ft
from .backend.dbmanager import remove_table, load_tables_from_database, load_from_database

def history_screen(page: ft.Page):

    table_names = load_tables_from_database()


    table_list = ft.ListView(expand=True, spacing=10, padding=10)
    def load_data(name):
        filtered_items = load_from_database(name)
        first_item_title = filtered_items[0]
        page.session.set("items_check",first_item_title)
        page.go("/bibliography")
        
    def delete_data(name):
        remove_table(name)
        table_names = load_tables_from_database()
        table_list.update()
    for table_name in table_names:
        table_list.controls.append(
            ft.ListTile(
                leading=ft.Icon(ft.icons.TABLE_VIEW, color=ft.colors.BLUE),
                title=ft.Text(table_name),
                trailing=ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.RED,
                    on_click=lambda e: delete_data(table_name)
                ),on_click=lambda e: load_data(table_name)
            )
        )
    return ft.View(
        "/history",
        [
            ft.AppBar(title=ft.Text("Data"), bgcolor=ft.colors.SURFACE_VARIANT),
            table_list,
        ],
    )
