import sqlite3
import tkinter as tk
from tkinter import messagebox

# -----------------------------
# 1. KONEKSI & MEMBUAT DATABASE
# -----------------------------
conn = sqlite3.connect("nilai_siswa.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
""")

conn.commit()

# -----------------------------
# 2. FUNGSI PREDIKSI & SIMPAN
# -----------------------------
def submit_data():
    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fis.get())
    ing = int(entry_ing.get())

    # Tentukan hasil prediksi berdasarkan nilai tertinggi
    if bio > fis and bio > ing:
        prediksi = "Kedokteran"
    elif fis > bio and fis > ing:
        prediksi = "Teknik"
    else:
        prediksi = "Bahasa"

    # Simpan ke database SQLite
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, prediksi))

    conn.commit()

    messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")

    # Reset input
    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

# -----------------------------
# 3. GUI TKINTER
# -----------------------------
root = tk.Tk()
root.title("Prediksi Fakultas Siswa")

label_title = tk.Label(root, text="Input Nilai Siswa", font=("Arial", 14))
label_title.grid(row=0, column=0, columnspan=2, pady=10)

# Entry Nama
tk.Label(root, text="Nama Siswa").grid(row=1, column=0, sticky="w")
entry_nama = tk.Entry(root)
entry_nama.grid(row=1, column=1)

# Entry Biologi
tk.Label(root, text="Nilai Biologi").grid(row=2, column=0, sticky="w")
entry_bio = tk.Entry(root)
entry_bio.grid(row=2, column=1)

# Entry Fisika
tk.Label(root, text="Nilai Fisika").grid(row=3, column=0, sticky="w")
entry_fis = tk.Entry(root)
entry_fis.grid(row=3, column=1)

# Entry Inggris
tk.Label(root, text="Nilai Inggris").grid(row=4, column=0, sticky="w")
entry_ing = tk.Entry(root)
entry_ing.grid(row=4, column=1)

# Tombol Submit
btn_submit = tk.Button(root, text="Submit", command=submit_data)
btn_submit.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
