import flet as ft

def help_screen(page: ft.Page):
    steps = [
        "1. Buka aplikasi dan masukkan query pencarian di kolom yang tersedia.",
        "2. Klik tombol 'Search' untuk memulai pencarian.",
        "3. Tunggu hingga hasil pencarian muncul di daftar.",
        "4. Gunakan tombol 'Sort' untuk mengurutkan hasil pencarian (ascending/descending).",
        "5. Klik ikon 'View' untuk melihat detail lebih lanjut dari setiap hasil.",
        "6. Gunakan filter kategori jika ingin menyaring hasil pencarian.",
        "7. Simpan atau tandai hasil pencarian yang penting menggunakan checkbox.",
        "8. Gunakan tombol 'Export' untuk menyimpan hasil pencarian ke file.",
    ]

    return ft.View(
        "/help",
        [
            ft.AppBar(title=ft.Text("Help"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Langkah-Langkah Penggunaan Aplikasi", size=20, weight=ft.FontWeight.BOLD),
                        ft.ListView(
                            controls=[ft.Text(step, size=16) for step in steps],
                            expand=True,
                            spacing=10,
                            padding=10,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=20,
                expand=True,
            ),
        ],
    )
