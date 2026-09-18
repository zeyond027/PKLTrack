# Template Portofolio / CV

Template website portofolio satu halaman, siap dipost ke GitHub Pages.

## Cara mengedit

1. Buka `index.html` pakai text editor apa saja (VS Code, Notepad, dll).
2. Cari kata **`GANTI:`** — setiap komentar itu menandai teks yang perlu kamu ganti dengan datamu sendiri (nama, peran, bio, pengalaman kerja, proyek, kontak, dll).
3. **Foto**: taruh file foto dengan nama persis `foto.jpg` di folder yang sama dengan `index.html`. Kalau file belum ada, otomatis muncul kotak placeholder bertuliskan "Taruh foto.jpg di folder ini" — jadi kamu tidak akan lupa.
4. **CV PDF**: kalau punya CV dalam bentuk PDF, taruh di folder yang sama dengan nama `cv.pdf`. Tombol "Unduh CV" otomatis mengarah ke file itu.
5. Buka `index.html` langsung di browser (klik dua kali) untuk melihat hasilnya sebelum diunggah.

## Cara mempost ke GitHub

1. Buat repository baru di GitHub, misalnya `portofolio-saya`.
2. Upload `index.html` (dan `foto.jpg`, `cv.pdf` kalau ada) ke repo tersebut.
3. Masuk ke **Settings → Pages**.
4. Di bagian **Branch**, pilih `main` dan folder `/root`, lalu klik **Save**.
5. Tunggu 1–2 menit, website akan aktif di:
   `https://username-kamu.github.io/portofolio-saya/`

## Struktur halaman

- **Tentang** — bio singkat & data cepat (lokasi, status, email)
- **Pengalaman** — linimasa kerja/pendidikan
- **Proyek** — grid kartu proyek dengan tag teknologi & link
- **Keahlian** — kelompok skill (bahasa, alat, soft skill)
- **Kontak** — email & sosial media

Semua styling ada langsung di dalam `index.html` (tidak perlu file CSS terpisah), jadi tinggal upload satu file saja kalau mau versi paling sederhana.
