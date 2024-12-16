from docx import Document
from docx.shared import Pt

def export_to_word(filtered_items):
    # Buat dokumen Word baru
    doc = Document()
    doc.add_heading("Daftar Pustaka", level=1)

    # Tambahkan setiap item dalam daftar pustaka
    paragraph = doc.add_paragraph()
    paragraph.add_run(filtered_items).font.size = Pt(12)

    # Simpan dokumen
    file_path = "Daftar_Pustaka.docx"
    doc.save(file_path)
    print(f"File berhasil disimpan: {file_path}")
