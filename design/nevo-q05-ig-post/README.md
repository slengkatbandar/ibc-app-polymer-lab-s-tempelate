# Changan Nevo Q05 — Reels Concept (10s loop, 9:16)

Materi konsep untuk pendekatan ke Changan Indonesia: satu Reel Instagram yang
memamerkan Nevo Q05. Sepuluh spesifikasi bergulir turun seperti pemilih lagu,
berhenti di baris lime, dan angka besar di atas berganti sinkron.

Format **1080 × 1920 (9:16)**, **10 detik**, **looping mulus** — verified: render
`t=10s` menghasilkan hash piksel identik dengan `t=0`.

## Sumber spesifikasi

Semua angka diambil dari **flyer resmi Nevo Q05** (PT Dinamika Indomobil
Transportasi, 26/07/26) yang tersimpan di `src/flyer-nevo-q05-260726.pdf`.
Situs `changan.co.id` sendiri diblokir oleh proxy jaringan sesi ini, jadi flyer
inilah sumber primernya.

| # | Baris | Angka | Kutipan flyer |
|---|---|---|---|
| 01 | Jarak Tempuh | 462 km | All Electric Range (NEDC) |
| 02 | Fast Charging | 15 menit | 3C Fast Charging, 30-80% in 15 Minutes |
| 03 | Baterai LFP | 51,9 kWh | Lithium Iron Phosphate (LFP) |
| 04 | Tenaga Motor | 120 kW | Maximum Power 120 kW / Torque 190 Nm |
| 05 | Wheelbase | 2.735 mm | 2735 mm wheelbase, longest in its class |
| 06 | Head Unit | 14,6 inci | 14.6" Touchscreen + cluster 10,17" |
| 07 | Fitur ADAS | 12 fungsi | 3R1V + 12 ADAS functions, L2-level |
| 08 | Koefisien Drag | 0,265 Cd | Drag coefficient as low as 0.265 Cd |
| 09 | Ruang Simpan | 27 titik | 27 practical storage spaces |
| 10 | Garansi Baterai | 8 tahun | 8 TAHUN / 240.000 KM |

Angka yang **tidak** dipakai karena tidak ada di flyer resmi: kapasitas bagasi
540 L, kamera 540 derajat, panoramic roof 1,8 m², dan jumlah airbag (flyer hanya
menyebut "Front & Side" untuk Pro dan "+ Side Curtain" untuk Max). Harga juga
tidak dicantumkan.

## Foto

`src/cutout.py` memotong latar foto studio dua unit Nevo Q05 memakai
[rembg](https://github.com/danielgatis/rembg) model `isnet-general-use`. Dua hal
yang menjaga hasilnya tetap bersih, termasuk saat sumbernya foto lokasi:

1. tiap mobil disegmentasi dari separuh framenya sendiri — sekali jalan pada
   frame beresolusi besar, model sempat memotong bagian bawah ban;
2. hanya dua komponen terbesar yang dipertahankan, sehingga sisa latar yang
   ikut tersegmentasi (misalnya garis parkir) terbuang.

Hasilnya di-*trim* ke batas alpha dan disimpan sebagai WebP beralpha — 61 KB,
jauh di bawah PNG-nya. Bayangan kontak yang hilang bersama latar dikembalikan
lewat dua elips lembut di CSS.

## Arah desain

Tema mengikuti referensi yang diberikan: brutalis-editorial, blok warna datar,
garis tepi tebal, label mono berkotak.

- **Warna** — mint `#A5DBD5`, lavender `#CBC9F4`, lime `#C9FF3D` sebagai satu-satunya
  warna sinyal, ink `#23232E` (hitam yang sedikit diangkat supaya tidak pekat di
  layar HP), paper `#F4F2EC`.
- **Tipografi** — Archivo Black untuk angka, Archivo untuk judul dan nama fitur,
  IBM Plex Mono untuk label. Semua di-*inline* sebagai data URI.
- **Ukuran huruf** — dinaikkan untuk dibaca di HP pada jarak ~30 cm: nama fitur
  48 px, judul 62 px, angka 172 px, catatan 38 px (pada kanvas 1080 px).
- **Area aman Reels** — semua elemen penting berada di atas y≈1520; bagian bawah
  sengaja hanya berisi wordmark outline, karena tertutup caption dan tombol IG.

## Berkas

| Berkas | Isi |
|---|---|
| `index.html` | Hasil build, self-contained (foto + huruf ter-embed) |
| `src/template.html` | Sumber layout + motion (`__CAR_IMAGE__`, `__FONTS__`) |
| `src/cutout.py` → `src/nevo-q05-pair.webp` | Segmentasi + pembersihan foto |
| `src/fonts.py` → `src/fonts.css` | Subset latin Google Fonts sebagai data URI |
| `src/flyer-nevo-q05-260726.pdf` | Flyer resmi, sumber seluruh angka |
| `build.py` | Meng-inline foto dan huruf ke `index.html` |
| `export.js` | Render deterministik → `nevo-q05-reels.mp4`, `.gif`, `poster.jpg` |
| `nevo-q05-reels.mp4` | 1080×1920, 30 fps, 10 detik, H.264 + trek audio senyap |

```bash
pip install "rembg[cli]" onnxruntime scipy pillow   # sekali saja
python3 src/cutout.py     # saat foto sumber diganti
python3 src/fonts.py      # saat daftar huruf berubah
python3 build.py          # rebuild index.html
node export.js            # render ulang mp4 + gif + poster
```

Daftar spesifikasi ada di array `FEATURES` (`src/template.html`) — jumlah entri
menentukan panjang loop, satu detik per entri.
