# PKLTrack (versi statis untuk GitHub Pages)

Versi ini adalah hasil konversi dari aplikasi Flask (Python + SQLite) menjadi
**satu file HTML mandiri** yang berjalan sepenuhnya di browser (tanpa server).
Semua data (kegiatan & kompetensi) disimpan di `localStorage` browser kamu.

Kenapa dikonversi? GitHub Pages hanya bisa menghosting file statis
(HTML/CSS/JS) — tidak bisa menjalankan Python/Flask. Supaya linknya bisa
langsung dibuka dan berjalan begitu diklik, aplikasinya dibuat ulang jadi
HTML + JavaScript murni, dengan tampilan dan fitur yang sama persis:

- Dashboard (statistik, grafik donat, progres kompetensi, kegiatan terbaru)
- Kegiatan harian (tambah, lihat, hapus, unggah foto dokumentasi)
- Kompetensi (tambah, update progres)
- Export laporan ke PDF (dibuat langsung di browser)

## Cara upload ke GitHub & mengaktifkan link-nya

1. Buat repository baru di GitHub (public), misalnya `pkltrack`.
2. Upload file `index.html` (dan `README.md` ini kalau mau) ke repo tersebut:
   - Klik **Add file → Upload files** di halaman repo, lalu seret file
     `index.html`, atau
   - Kalau pakai Git di komputer:
     ```
     git init
     git add index.html README.md
     git commit -m "PKLTrack static version"
     git branch -M main
     git remote add origin https://github.com/USERNAME/pkltrack.git
     git push -u origin main
     ```
3. Aktifkan GitHub Pages:
   - Masuk ke **Settings → Pages** pada repo.
   - Di bagian **Build and deployment**, pilih **Source: Deploy from a branch**.
   - Pilih **Branch: main**, folder **/(root)**, lalu **Save**.
4. Tunggu 1–2 menit, lalu buka link yang muncul, biasanya:
   ```
   https://USERNAME.github.io/pkltrack/
   ```
   Klik link itu — aplikasi langsung jalan di browser, tidak perlu instalasi
   apa pun.

## Catatan penting

- **Data tersimpan per-browser** (localStorage), bukan di server/database
  bersama. Kalau kamu buka linknya dari HP/laptop lain atau browser lain,
  datanya akan kosong lagi (mulai dari kompetensi bawaan). Ini cocok untuk
  penggunaan personal/dokumentasi PKL individu.
- Foto dokumentasi disimpan sebagai gambar langsung di dalam data browser,
  jadi jangan unggah foto yang terlalu besar/banyak (localStorage biasanya
  terbatas sekitar 5–10 MB).
- Kalau butuh data yang bisa diakses dari banyak perangkat/orang (misalnya
  untuk dipantau oleh pembimbing PKL), versi Flask aslinya (dengan
  database) perlu dijalankan di server yang mendukung Python, seperti
  Render, Railway, PythonAnywhere, dsb — bukan GitHub Pages.
