import flet as ft
from .backend.word_exporter import export_to_word
from .backend.dbmanager import save_to_database
from .backend.json_exporter import save_configuration

def bibliography_screen(page: ft.Page, filtered_items):
    # Membuat daftar pustaka menggunakan ListView
    bibliography_list = ft.ListView(spacing=10)
    format_bibl = "IEEE"
    # Elemen teks untuk menampilkan daftar pustaka yang diformat
    formatted_view = ft.Text(value="", expand=True )
    def show_save_popup():
        def confirm_save(e):
            table_name = save_name_field.value.strip()
            if table_name:
                save_to_database(table_name, filtered_items, selected_format.value)
                page.dialog.open = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Data berhasil disimpan ke tabel '{table_name}'!"),
                    open=True,
                )
                page.update()
            else:
                error_text.value = "Nama tabel tidak boleh kosong!"
                error_text.update()

        def cancel_save(e):
            page.dialog.open = False
            page.update()

        error_text = ft.Text(value="", color=ft.colors.RED)
        save_name_field = ft.TextField(label="Nama Tabel")

        page.dialog = ft.AlertDialog(
            title=ft.Text("Simpan ke Database"),
            content=ft.Column([save_name_field, error_text]),
            actions=[
                ft.TextButton("Batalkan", on_click=cancel_save),
                ft.TextButton("Simpan", on_click=confirm_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()
    # Fungsi ekspor ke berbagai format
    def export_to(format_type):
        if filtered_items:
            if format_type == "Word":
                export_to_word(formatted_view.value)
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Berhasil diekspor ke Word!"),
                    open=True,
                )
            elif format_type == "Save":
                show_save_popup()
            elif format_type == "JSON":
                save_configuration(formatted_view.value, format_bibl)
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Berhasil diekspor ke JSON!"),
                    open=True,
                )
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Tidak ada data untuk diekspor."),
                open=True,
            )
        page.update()

    # Menu bar untuk ekspor file
    menu_bar = ft.MenuBar(
        [
            ft.MenuItemButton(ft.Text("To Word"), on_click=lambda _: export_to("Word")),
            ft.MenuItemButton(ft.Text("To XML"), on_click=lambda _: export_to("XML"), disabled=False),
            ft.MenuItemButton(ft.Text("To JSON"), on_click=lambda _: export_to("JSON"), disabled=False),
            ft.MenuItemButton(ft.Text("Save"), on_click=lambda _: export_to("Save")),
        ],
        style=ft.MenuStyle(
            alignment=ft.alignment.center,
            bgcolor=ft.colors.ON_SECONDARY,
        ),
        expand=True,
    )

    # Fungsi untuk memperbarui tampilan daftar pustaka yang diformat
    def update_formatted_view(format_choice):
        if filtered_items:
            if format_choice == "IEEE":
                format_bibl = "IEEE"
                formatted_items = [
                    f"[{i+1}] {', '.join(item['authors'])}, \"{item['title']}\", Available: {item['link']}."
                    for i, item in enumerate(filtered_items)
                ]
            elif format_choice == "APA":
                format_bibl = "APA"
                formatted_items = [
                    f"{', '.join(item['authors'])} ({item['date'][:4]}). {item['title']}. Retrieved from {item['link']}"
                    for item in filtered_items
                ]
            elif format_choice == "MLA":
                format_bibl = "MLA"
                formatted_items = [
                    f"{', '.join(item['authors'])}. \"{item['title']}\". {item['source']}, {item['date'][:10]}. <{item['link']}>."
                    for item in filtered_items
                ]
            # Gabungkan daftar pustaka yang diformat menjadi satu string
            formatted_view.value = "\n".join(formatted_items)
        else:
            # Tampilkan pesan jika tidak ada data
            formatted_view.value = "Tidak ada data pustaka tersedia."
        if formatted_view.page:
            formatted_view.update()

    # Fungsi untuk menghapus item dari daftar pustaka
    def remove_bibliography(item):
        filtered_items.remove(item)
        if filtered_items:
            bibliography_list.controls = [
                ft.ListTile(
                    leading=ft.Icon(ft.icons.BOOKMARK, color=ft.colors.BLUE),
                    title=ft.Text(it["title"]),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_color=ft.colors.RED,
                        on_click=lambda e, it=it: remove_bibliography(it),
                    ),
                )
                for it in filtered_items
            ]
        else:
            # Tampilkan pesan jika daftar menjadi kosong
            bibliography_list.controls = [
                ft.Text("Tidak ada data pustaka tersedia.", color=ft.colors.ON_SECONDARY, size=16)
            ]
            page.go("/")
        bibliography_list.update()

        update_formatted_view(selected_format.value)

    # Inisialisasi daftar pustaka
    if filtered_items:
        for item in filtered_items:
            bibliography_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.BOOKMARK, color=ft.colors.BLUE),
                    title=ft.Text(item["title"]),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_color=ft.colors.RED,
                        on_click=lambda e, item=item: remove_bibliography(item),
                    ),
                    bgcolor=ft.colors.ON_SECONDARY,
                    expand=True,
                    width=1000,
                    on_long_press=lambda e, it=item: show_reorder_popup(it),
                )
            )
    else:
        # Tampilkan pesan jika data kosong sejak awal
        bibliography_list.controls.append(
            ft.Text("Tidak ada data pustaka tersedia.", color=ft.colors.GREY, size=16)
        )

    # Format referensi yang dipilih (default: IEEE)
    selected_format = ft.Text(value="IEEE")
    def update_bibliography_list():
        bibliography_list.controls = [
            ft.ListTile(
                leading=ft.Icon(ft.icons.BOOKMARK, color=ft.colors.BLUE),
                title=ft.Text(item["title"]),
                trailing=ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color=ft.colors.RED,
                    on_click=lambda e, it=item: remove_bibliography(it),
                ),
                on_click=lambda e, it=item: show_reorder_popup(it),
            )
            for item in filtered_items
        ]
        bibliography_list.update()
    def show_reorder_popup(item):
        def confirm_reorder(e):
            try:
                new_index = int(new_position_field.value) - 1
                if 0 <= new_index < len(filtered_items):
                    filtered_items.remove(item)
                    filtered_items.insert(new_index, item)
                    update_bibliography_list()
                    update_formatted_view(selected_format.value)
                    page.dialog.open = False
                    page.update()
                else:
                    error_text.value = "Posisi di luar batas!"
                    error_text.update()
            except ValueError:
                error_text.value = "Masukkan angka valid!"
                error_text.update()

        def cancel_reorder(e):
            # Menutup dialog saat "Batalkan" ditekan
            page.dialog.open = False
            page.update()

        # Dialog untuk reorder
        error_text = ft.Text(value="", color=ft.colors.RED)
        new_position_field = ft.TextField(label="Posisi Baru", keyboard_type=ft.KeyboardType.NUMBER)

        page.dialog = ft.AlertDialog(
            title=ft.Text(f"Pindahkan '{item['title']}'"),
            content=ft.Column([new_position_field, error_text]),
            actions=[
                ft.TextButton("Batalkan", on_click=cancel_reorder),
                ft.TextButton("Konfirmasi", on_click=confirm_reorder),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    # NavigationBar untuk memilih format referensi
    format_navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.TEXT_FORMAT, label="APA"),
            ft.NavigationBarDestination(icon=ft.icons.TEXT_FORMAT, label="IEEE"),
            ft.NavigationBarDestination(icon=ft.icons.TEXT_FORMAT, label="MLA"),
        ],
        selected_index=1,  # IEEE sebagai default
        on_change=lambda e: update_formatted_view(
            format_navigation_bar.destinations[e.control.selected_index].label
        ),
    )

    # Perbarui tampilan awal daftar pustaka yang diformat
    update_formatted_view(selected_format.value)

    return ft.View(
        "/bibliography",
        [
            ft.AppBar(title=ft.Text("References Manager"), bgcolor=ft.colors.SURFACE_VARIANT),

            # Daftar pustaka
            ft.Column(
                [
                    ft.Text("Daftar Pustaka", size=20, weight=ft.FontWeight.BOLD),
                    bibliography_list,
                ],
            ),

            # Viewer untuk daftar pustaka yang diformat
            ft.Column(
                [
                    ft.Text("Preview Daftar Pustaka", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(formatted_view, padding=10, bgcolor=ft.colors.ON_SECONDARY, expand=True),
                ],expand=True
            ),

            # Menu bar di bagian bawah
            ft.Container(
                ft.Row(
                    [menu_bar],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            
            format_navigation_bar
        ],scroll= ft.ScrollMode.AUTO
    )
