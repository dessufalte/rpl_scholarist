import flet as ft

def api_key_screen(page: ft.Page):
    def save_api_keys(e):
        arxiv_key = arxiv_key_field.value
        scopus_key = scopus_key_field.value
        google_scholar_key = google_scholar_key_field.value
        filter_content = filter_content_dropdown.value
        filter_year = filter_year_dropdown.value
        plagiarism_detection = plagiarism_detection_checkbox.value
        
        print(f"Arxiv API Key: {arxiv_key}")
        print(f"Scopus API Key: {scopus_key}")
        print(f"Google Scholar API Key: {google_scholar_key}")
        print(f"Filter Content: {filter_content}")
        print(f"Filter Year: {filter_year}")
        print(f"Plagiarism Detection: {plagiarism_detection}")
        
        page.client_storage.set("arxiv_key", arxiv_key)
        page.client_storage.set("scopus_key", scopus_key)
        page.client_storage.set("google_scholar_key", google_scholar_key)
        page.client_storage.set("filter_content", filter_content)
        page.client_storage.set("filter_year", filter_year)
        page.client_storage.set("plagiarism_detection", plagiarism_detection)
        
        page.snack_bar = ft.SnackBar(
            ft.Text("API Key dan Pengaturan tersimpan!"),
            bgcolor=ft.colors.GREEN,
            open=True,
        )
        page.update()

    arxiv_key = page.client_storage.get("arxiv_key")
    scopus_key = page.client_storage.get("scopus_key")
    google_scholar_key = page.client_storage.get("google_scholar_key")
    filter_content = page.client_storage.get("filter_content")
    filter_year = page.client_storage.get("filter_year")
    plagiarism_detection = page.client_storage.get("plagiarism_detection")

    arxiv_key_field = ft.TextField(label="Arxiv API Key", value=arxiv_key, password=False)
    scopus_key_field = ft.TextField(label="Scopus API Key", value=scopus_key, password=False)
    google_scholar_key_field = ft.TextField(label="Google Scholar API Key", value=google_scholar_key, password=False)

    filter_content_dropdown = ft.Dropdown(
        label="Filter Content",
        options=[
            ft.dropdown.Option("All"),
            ft.dropdown.Option("Journal Articles"),
            ft.dropdown.Option("Books"),
            ft.dropdown.Option("Conference Papers"),
        ],
        value=filter_content
    )
    
    filter_year_dropdown = ft.Dropdown(
        label="Filter Year",
        options=[
            ft.dropdown.Option("Any"),
            ft.dropdown.Option("2023"),
            ft.dropdown.Option("2022"),
            ft.dropdown.Option("2021"),
            ft.dropdown.Option("2020"),
        ],
        value=filter_year
    )
    
    plagiarism_detection_checkbox = ft.Checkbox(
        label="Enable Plagiarism Detection",
        value=plagiarism_detection
    )

    save_button = ft.ElevatedButton("Save API Keys & Settings", on_click=save_api_keys)

    return ft.View(
        "/api_key",
        [
            ft.AppBar(title=ft.Text("API Settings"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Masukkan API Key dan Pengaturan", size=20, weight=ft.FontWeight.BOLD),
                        arxiv_key_field,
                        scopus_key_field,
                        google_scholar_key_field,
                        ft.Text("Pilih jenis konten yang ingin dicari.", size=12, color=ft.colors.GREY),
                        filter_content_dropdown,
                        ft.Text("Pilih tahun untuk memfilter pencarian.", size=12, color=ft.colors.GREY),
                        filter_year_dropdown,
                        ft.Text("Aktifkan untuk mendeteksi plagiat pada dokumen.", size=12, color=ft.colors.GREY),
                        plagiarism_detection_checkbox,
                        save_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
                padding=20,
                expand=True,
            ),
        ],
    scroll= ft.ScrollMode.AUTO)
