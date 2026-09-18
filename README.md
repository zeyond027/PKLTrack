# PKLTrack — Logbook PKL

Aplikasi web satu-file untuk mencatat kegiatan harian dan progres kompetensi selama Praktik Kerja Lapangan (PKL). Tidak butuh server atau instalasi apa pun — cukup buka `index.html` di browser, atau host lewat GitHub Pages.

## Fitur

- **Dashboard** — ringkasan total kegiatan, status (selesai/diproses/belum), rata-rata progres kompetensi, dan grafik distribusi status.
- **Kegiatan** — catat kegiatan harian lengkap dengan tanggal, deskripsi, status, dan foto dokumentasi.
- **Kompetensi** — catat kompetensi yang dipelajari, update progres, serta edit atau hapus jika ada kesalahan input.
- **Export PDF** — buat laporan PDF berisi daftar kompetensi dan seluruh kegiatan, siap dicetak atau dikumpulkan.

## Cara menjalankan

### Lokal
Unduh `index.html`, lalu buka langsung di browser (double click atau drag ke tab browser).

### GitHub Pages
1. Buat repository baru (public) di GitHub.
2. Upload `index.html` ke root repository.
3. Buka **Settings → Pages**.
4. Pada **Build and deployment**, pilih:
   - Source: `Deploy from a branch`
   - Branch: `main`, folder `/(root)`
5. Simpan, tunggu 1–2 menit. Situs akan aktif di:
   `https://<username-kamu>.github.io/<nama-repo>/`

## Penyimpanan data

Semua data disimpan di `localStorage` browser — artinya data tersimpan lokal di perangkat/browser yang dipakai untuk membuka aplikasi, bukan di server pusat. Implikasinya:

- Data tidak otomatis sinkron antar perangkat atau antar browser.
- Menghapus cache/data situs di browser akan menghapus data yang tersimpan.
- Aplikasi ini cocok untuk pencatatan pribadi satu perangkat; untuk pemakaian bersama/multi-perangkat dibutuhkan backend terpisah.

## Teknologi

- HTML, CSS, dan JavaScript murni (tanpa framework, tanpa proses build).
- [Chart.js](https://www.chartjs.org/) untuk grafik distribusi status.
- [jsPDF](https://github.com/parallax/jsPDF) untuk export laporan PDF.
- Font: Orbitron, Rajdhani, Inter, JetBrains Mono (dimuat dari Google Fonts).

## Lisensi

Bebas digunakan dan dimodifikasi untuk keperluan pribadi/sekolah.
