# Changan Nevo Q05 — IG Post Concept (10s loop, 4:5)

Materi konsep untuk pendekatan ke Changan Indonesia: satu post Instagram yang
memamerkan Nevo Q05. Sepuluh spesifikasi bergulir turun seperti pemilih lagu,
berhenti di baris lime, dan angka besar di atas berganti sinkron.

Format **1080 × 1350 (4:5)**, **10 detik**, **looping mulus** — verified: render
`t=10s` menghasilkan hash piksel identik dengan `t=0`.

## Arah desain

Tema warna dan perlakuan teks mengikuti referensi yang diberikan (mockup crypto
portfolio): brutalis-editorial, blok warna datar, garis tepi tebal, label mono
berkotak.

- **Warna** (disampel langsung dari gambar referensi) — mint `#A5DBD5` sebagai
  ground, lavender `#CBC9F4` untuk struktur (band miring + header kartu), lime
  `#C9FF3D` sebagai satu-satunya warna sinyal (kotak satuan + baris aktif), ink
  `#12121B`, dan paper `#F4F2EC` untuk kartu spesifikasi.
- **Tipografi** — **Archivo Black** untuk angka besar, **Archivo** untuk judul dan
  nama fitur, **IBM Plex Mono** untuk label/satuan/kredit. Semua di-*inline*
  sebagai data URI supaya artifact dan video memakai huruf yang sama persis.
- **Komposisi** — bertingkat sesuai rasio 4:5: masthead + bar 10 segmen, lalu
  *hook* (angka besar + kotak satuan lime + judul fitur), lalu foto Nevo Q05 besar
  di dalam bingkai (`object-fit: contain`, tidak terpotong di atap maupun roda),
  lalu kartu spesifikasi bergaris tebal, lalu footer.

## Sepuluh spesifikasi yang ditampilkan

| # | Baris | Angka |
|---|---|---|
| 01 | Jarak Tempuh | 462 km (NEDC) |
| 02 | Fast Charging | 15 menit (30–80%) |
| 03 | Baterai CATL LFP | 51,9 kWh |
| 04 | Tenaga Motor | 120 kW / 190 Nm |
| 05 | Kapasitas Bagasi | 540 L → 1.380 L |
| 06 | Head Unit | 14,6 inci (+ cluster 10,17") |
| 07 | Surround View | 540° + transparent chassis |
| 08 | Airbag & ADAS | 6 airbag + ADAS Level 2 |
| 09 | Panoramic Roof | 1,8 m² (varian Max) |
| 10 | Garansi Baterai | 8 tahun / 240.000 km |

### Catatan sumber data

`changan.co.id` diblokir oleh proxy jaringan sesi ini, jadi angka di atas diambil
dari pemberitaan nasional Agustus 2026 (Kompas, oto.com, Otodriver, detikOto,
Moladin, Motomobi) dan dicek silang antar sumber. Dua hal yang sengaja **tidak**
dipakai karena sumbernya berbeda-beda atau terikat konteks:

- jumlah fitur ADAS (ada yang menyebut 18 + 7, ada yang 12 fungsi) — di materi ini
  cukup ditulis "ADAS Level 2";
- harga peluncuran (Rp309 jt / Rp359 jt) karena itu harga khusus periode pameran.

Sebelum dipakai ke klien, sebaiknya semua angka dikonfirmasi ke rilis resmi
Changan Indonesia.

## Berkas

| Berkas | Isi |
|---|---|
| `index.html` | Hasil build, self-contained (foto + huruf ter-embed) |
| `src/template.html` | Sumber layout + motion (`__CAR_IMAGE__`, `__FONTS__`) |
| `src/trim.js` → `src/nevo-q05.png` | Memangkas area transparan di sekeliling cutout mobil |
| `src/fonts.py` → `src/fonts.css` | Unduh subset latin Google Fonts sebagai data URI |
| `build.py` | Meng-inline foto dan huruf ke `index.html` |
| `export.js` | Render deterministik → `nevo-q05-post.mp4`, `.gif`, `poster.jpg` |
| `nevo-q05-post.mp4` | 1080×1350, 30 fps, 10 detik, H.264 + trek audio senyap (IG) |

```bash
python3 src/fonts.py     # sekali saja
node src/trim.js         # saat foto sumber diganti
python3 build.py         # rebuild index.html
node export.js           # render ulang mp4 + gif + poster
```

Daftar spesifikasi ada di array `FEATURES` (`src/template.html`) — jumlah entri
menentukan panjang loop, satu detik per entri.
