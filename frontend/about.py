import flet as ft

def about_screen(page: ft.Page):
    return ft.View(
        "/about",
        [
            ft.AppBar(title=ft.Text("Tentang"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Scholarist", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "v 1.0.1",
                            size=16,
                            color=ft.colors.GREY,
                        ),
                        ft.Text(
                            "Aplikasi ini membantu Anda mencari dan mengelola makalah akademik dari berbagai sumber seperti Arxiv, Scopus, dan Google Scholar. "
                            "Anda dapat menyimpan kunci API untuk platform-platform ini, mengatur preferensi pencarian, dan dengan mudah mengekspor hasil pencarian ke berbagai format.",
                            size=16,
                            color=ft.colors.GREY,
                        ),
                        ft.Text(
                            "Fitur-fitur yang tersedia meliputi:\n"
                            "- Mencari makalah akademik dari Arxiv, Scopus, dan Google Scholar\n"
                            "- Menyimpan dan mengelola kunci API\n"
                            "- Memfilter hasil pencarian berdasarkan jenis konten dan tahun\n"
                            "- Deteksi plagiarisme\n"
                            "- Mengekspor hasil pencarian ke format Word, JSON, dan lainnya\n",
                            size=16,
                            color=ft.colors.GREY,
                        ),
                        ft.Text(
                            "Dikembangkan oleh: Kelompok 4",
                            size=14,
                            color=ft.colors.GREY,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
                padding=20,
                expand=True,
            ),
        ],
    )
