# Changan Nevo Q05 — Price Reel (10s loop, 9:16)

Reel kedua untuk pendekatan ke Changan Indonesia. Kalau reel pertama menjual
spesifikasi, yang ini menjual **harga**: dua varian bergantian tiap 2,5 detik
dalam satu loop 10 detik (PRO → MAX → PRO → MAX), jadi penonton melihat kedua
harga dua kali dalam sekali putar.

Format **1080 × 1920 (9:16)**, **10 detik**, **looping mulus** — verified: render
`t=10s` menghasilkan hash piksel identik dengan `t=0`.

## Ide utamanya

Angka harga dibuat sebagai **odometer tiga kolom**. Karena Rp309 dan Rp359 hanya
beda di digit tengah, cuma digit itu yang berputar — 0 menggulung ke 5 dan
kembali lagi, dengan sedikit overshoot supaya mendarat "klik". Detail kecil ini
yang bikin pergantian varian terasa hidup, bukan sekadar teks berganti.

Aksen warna dipakai sebagai penanda varian, bukan hiasan:

| Varian | Aksen | Harga | Pembeda (flyer resmi) |
|---|---|---|---|
| PRO | lime `#C9FF3D` | Rp309 juta | Roda 17 inci, kursi pengemudi elektrik 6 arah |
| MAX | lavender `#CBC9F4` | Rp359 juta | Panoramic roof, kursi berventilasi, roda 18 inci |

Yang ikut berganti warna saat varian berpindah: sunburst di belakang stiker
JUTA, stiker JUTA-nya sendiri, chip spesifikasi yang menyala, titik pada pil
"100% ELECTRIC", dan serpihan konfeti.

## Elemen pop lain

- **Chip varian** (kotak hitam PRO/MAX) mendarat dengan efek stempel: skala
  turun dari 1,22 dan rotasi lurus ke &minus;2&deg;.
- **Ticker miring** bergulir terus: "HARGA PELUNCURAN &#9733; NEVO Q05 &#9733;
  100% ELECTRIC &#9733; S&K BERLAKU". Bergeser tepat dua kali panjang ulangannya
  per loop, jadi tidak pernah melompat.
- **Sunburst** berputar 180&deg; sepanjang loop, plus sentakan kecil tiap beat.
- **Tiga chip spesifikasi** (462 km, 51,9 kWh, isi 15 menit) menyala bergantian.
- **Mobil** ikut "mendarat" bersama harga (skala pop) lalu bernapas pelan.

## Catatan harga

Harga Rp309 juta / Rp359 juta sesuai yang diberikan klien, ditampilkan dengan
label **HARGA PELUNCURAN** dan **S&K BERLAKU** di ticker. Kalau harga ini terikat
periode atau kuota tertentu, sebaiknya ketentuannya ditegaskan di caption.

Isi pembeda varian dan angka pada chip diambil dari flyer resmi Nevo Q05
(PT Dinamika Indomobil Transportasi, 26/07/26) — tersimpan di
`../nevo-q05-ig-post/src/flyer-nevo-q05-260726.pdf`.

## Berkas

| Berkas | Isi |
|---|---|
| `index.html` | Hasil build, self-contained (foto + huruf ter-embed) |
| `src/template.html` | Sumber layout + motion (`__CAR_IMAGE__`, `__FONTS__`) |
| `src/cutout.py` → `src/nevo-q05-solo.webp` | Potong latar foto studio (rembg `isnet-general-use`) |
| `src/fonts.py` → `src/fonts.css` | Subset latin Google Fonts sebagai data URI |
| `build.py` | Meng-inline foto dan huruf ke `index.html` |
| `export.js` | Render deterministik → `nevo-q05-price.mp4`, `.gif`, `poster.jpg` |
| `nevo-q05-price.mp4` | 1080×1920, 30 fps, 10 detik, H.264 + trek audio senyap |

```bash
python3 src/cutout.py    # saat foto sumber diganti
python3 build.py         # rebuild index.html
node export.js           # render ulang mp4 + gif + poster
```

Harga dan isi varian ada di array `TRIMS` (`src/template.html`); ritmenya diatur
lewat `BEAT` — empat beat 2,5 detik mengisi satu loop 10 detik.
