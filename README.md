# RPL Scholarist

Scholarist adalah aplikasi berbasis Flet yang dirancang untuk membantu pencarian, pengelolaan, dan ekspor dokumen akademik dari berbagai sumber seperti Arxiv, Scopus, dan Google Scholar. Proyek ini dikembangkan untuk memenuhi kebutuhan riset akademik dengan fitur yang lengkap dan mudah digunakan.

## Fitur Utama
- Pencarian dokumen akademik melalui Arxiv, Scopus, dan Google Scholar.
- Manajemen API key untuk setiap sumber data.
- Filter hasil pencarian berdasarkan tipe konten, tahun publikasi, dan lainnya.
- Deteksi AI untuk plagiarisme.
- Ekspor hasil pencarian ke format Word, JSON, dan lainnya.
- Tampilan responsif dan mudah dipahami.

## Persyaratan Sistem
- Python 3.8 atau lebih baru.
- [Flet](https://flet.dev/) sebagai framework utama.

## Instalasi

1. **Clone repositori**:
   ```bash
   git clone https://github.com/username/rpl_scholarist.git
   cd rpl_scholarist
   ```

2. **Buat lingkungan virtual (opsional)**:
   ```bash
   python -m venv env
   source env/bin/activate  # Untuk Linux/Mac
   env\Scripts\activate   # Untuk Windows
   ```

3. **Instal dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

   Dependensi utama meliputi:
   - `flet`
   - `docx`
   - `wikimedia`

4. **Jalankan aplikasi**:
   ```bash
   flet run main.py
   ```

## Konfigurasi API Keys
Untuk menggunakan fitur pencarian, Anda perlu mengatur API key untuk setiap layanan.

1. Masukkan API key di laman "API Key Management".
2. Klik tombol "Save API Keys" untuk menyimpan pengaturan.

## Struktur Direktori
```
.
├── main.py              # Berkas utama untuk menjalankan aplikasi.
├── screens              # Folder untuk layar-layar aplikasi.
│   ├── api_key_screen.py
│   ├── about_screen.py
│   └── ...
├── utils                # Berisi utilitas seperti helper dan konversi dokumen.
├── assets               # Berkas gambar, ikon, atau sumber daya lainnya.
├── requirements.txt     # Dependensi Python.
└── README.md            # Dokumentasi proyek.
```

## Kontribusi
Kami menyambut kontribusi untuk meningkatkan aplikasi ini. Berikut langkah untuk berkontribusi:

1. Fork repositori ini.
2. Buat branch baru untuk fitur atau perbaikan Anda.
   ```bash
   git checkout -b fitur-baru
   ```
3. Commit perubahan Anda.
   ```bash
   git commit -m "Menambahkan fitur baru"
   ```
4. Push branch Anda.
   ```bash
   git push origin fitur-baru
   ```
5. Buat Pull Request.

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

**Kelompok 4**
