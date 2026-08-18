# TIGGO V — Feature Reel (10s looping motion)

Motion loop yang mengikuti layout referensi (panel kuning + kartu merah di kiri,
daftar teks melengkung di atas latar hijau tua di kanan). Area kuning–merah diisi
Chery TIGGO V, dan teks di kanan berisi 10 fitur unggulan dari siaran pers
"Chery Resmi Perkenalkan TIGGO V di GIIAS 2026".

## Motion

- Durasi **10 detik**, **looping mulus** (frame di detik ke-10 identik dengan detik ke-0).
- Daftar fitur bergerak **ke bawah**, satu baris per detik, dengan easing "snap"
  seperti pemilih lagu; baris terpilih berhenti tepat di titik hijau.
- Kartu di kiri ikut berganti (judul fitur, nomor `01/10`, spesifikasi, dan
  caption mono) sinkron dengan baris yang mendarat di titik hijau.
- Gerak ambient (panel, kartu, dan ken-burns pada foto) memakai kurva sinus satu
  siklus penuh per 10 detik sehingga tidak ada lompatan saat loop mengulang.

## 10 fitur unggulan (sumber: siaran pers GIIAS 2026)

| # | Baris di reel | Spesifikasi |
|---|---|---|
| 01 | 3-in-1 Versatility | SUV · MPV · Double Cab |
| 02 | Ground Clearance 220 mm | 220 mm |
| 03 | Tanjakan 41° | 41° |
| 04 | Wading 700 mm | 700 mm |
| 05 | Easy Turn | radius −0,5 m |
| 06 | Air Flow Calibration | baris ke-3 & pilar C |
| 07 | Kabin 2·4·5·7 Kursi | 2 / 4 / 5 / 7 + bed mode |
| 08 | Super Hybrid 1.030 km | 1.030 km (thermal eff. 42,5%) |
| 09 | Split Tailgate 250 kg | 250 kg |
| 10 | Vehicle-to-Load 2,2 kW | 2,2 kW |

## Berkas

| Berkas | Isi |
|---|---|
| `index.html` | Hasil build, self-contained (foto ter-embed base64) — buka langsung di browser |
| `src/template.html` | Sumber layout + motion, dengan placeholder `__CAR_IMAGE__` |
| `src/tiggo-v-source.jpg` | Foto asli TIGGO V di GIIAS 2026 |
| `src/tiggo-v-card.jpg` | Hasil crop 1075×614 untuk jendela foto di kartu |
| `src/crop.js` | Script crop + grading foto |
| `build.py` | Meng-inline foto ke `index.html` |
| `export.js` | Render deterministik → `tiggo-v-motion.mp4`, `.gif`, `poster.jpg` |
| `tiggo-v-motion.mp4` | Video 1600×900, 30 fps, 10 detik, siap di-loop |

## Cara pakai

```bash
python3 build.py                 # rebuild index.html setelah mengubah src/template.html
node export.js                   # render ulang mp4 + gif + poster
node export.js --preview 0,3.5   # cek frame tertentu saja
```

Mengubah daftar fitur cukup lewat array `FEATURES` di `src/template.html`
(10 entri = 10 detik; jumlah entri menentukan panjang loop, 1 detik per fitur).
