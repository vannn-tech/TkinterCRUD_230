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
# 2. FUNGSI PREDIKSI
# -----------------------------
def get_prediksi(bio, fis, ing):
    if bio > fis and bio > ing:
        return "Kedokteran"
    elif fis > bio and fis > ing:
        return "Teknik"
    else:
        return "Bahasa"

# -----------------------------
# 3. SUBMIT DATA
# -----------------------------
def submit_data():
    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fis.get())
    ing = int(entry_ing.get())

    prediksi = get_prediksi(bio, fis, ing)

    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, prediksi))

    conn.commit()
    messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi: {prediksi}")
    clear_entries()
    load_listbox()

# -----------------------------
# 4. UPDATE DATA
# -----------------------------
def update_data():
    try:
        selected = listbox.curselection()[0]
        data = listbox.get(selected)
        record_id = data.split(" | ")[0]

        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())

        prediksi = get_prediksi(bio, fis, ing)

        cursor.execute("""
            UPDATE nilai_siswa
            SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
            WHERE id=?
        """, (nama, bio, fis, ing, prediksi, record_id))

        conn.commit()
        messagebox.showinfo("Update", "Data berhasil diupdate!")
        clear_entries()
        load_listbox()

    except:
        messagebox.showwarning("Error", "Pilih data terlebih dahulu!")

# -----------------------------
# 5. DELETE DATA
# -----------------------------
def delete_data():
    try:
        selected = listbox.curselection()[0]
        data = listbox.get(selected)
        record_id = data.split(" | ")[0]

        cursor.execute("DELETE FROM nilai_siswa WHERE id=?", (record_id,))
        conn.commit()

        messagebox.showinfo("Delete", "Data berhasil dihapus!")
        clear_entries()
        load_listbox()

    except:
        messagebox.showwarning("Error", "Pilih data terlebih dahulu!")

# -----------------------------
# 6. LOAD DATA LISTBOX
# -----------------------------
def load_listbox():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM nilai_siswa")
    for row in cursor.fetchall():
        listbox.insert(tk.END, f"{row[0]} | {row[1]} | Bio:{row[2]} | Fis:{row[3]} | Ing:{row[4]} | {row[5]}")

# -----------------------------
# 7. CLEAR ENTRY
# -----------------------------
def clear_entries():
    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

# -----------------------------
# 8. GUI TKINTER
# -----------------------------
root = tk.Tk()
root.title("Prediksi Fakultas Siswa")

label_title = tk.Label(root, text="Input Nilai Siswa", font=("Arial", 14))
label_title.grid(row=0, column=0, columnspan=2, pady=10)

# Form Input
tk.Label(root, text="Nama Siswa").grid(row=1, column=0, sticky="w")
entry_nama = tk.Entry(root)
entry_nama.grid(row=1, column=1)

tk.Label(root, text="Nilai Biologi").grid(row=2, column=0, sticky="w")
entry_bio = tk.Entry(root)
entry_bio.grid(row=2, column=1)

tk.Label(root, text="Nilai Fisika").grid(row=3, column=0, sticky="w")
entry_fis = tk.Entry(root)
entry_fis.grid(row=3, column=1)

tk.Label(root, text="Nilai Inggris").grid(row=4, column=0, sticky="w")
entry_ing = tk.Entry(root)
entry_ing.grid(row=4, column=1)

# Tombol
btn_submit = tk.Button(root, text="Submit", command=submit_data)
btn_submit.grid(row=5, column=0, pady=10)

btn_update = tk.Button(root, text="Update", command=update_data)
btn_update.grid(row=5, column=1, pady=10)

btn_delete = tk.Button(root, text="Delete", command=delete_data)
btn_delete.grid(row=6, column=0, columnspan=2, pady=5)

# Listbox
listbox = tk.Listbox(root, width=65)
listbox.grid(row=7, column=0, columnspan=2, pady=10)

load_listbox()
root.mainloop()
