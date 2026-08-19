# TIGGO V — Spec Reel (10s looping motion)

Motion loop 10 detik untuk peluncuran Chery TIGGO V di GIIAS 2026. Sepuluh fitur
unggulan dari siaran pers bergulir **ke bawah** seperti pemilih lagu, berhenti di
kursor, dan panel spesifikasi di kiri berganti sinkron dengan baris yang mendarat.

## Arah desain

Treatment press-kit: satu dunia visual (tanpa mode terang/gelap terpisah), semua
warna dinyatakan eksplisit.

- **Warna** — `--paper #F0F2EF` (netral dingin dengan bias hijau, bukan krem),
  `--paper-2 #E4E8E4` (plat baris aktif), `--ink #16211F` (nyaris hitam berbias
  teal), `--ink-60 #4E5A57`, `--accent #0E5F5F` (teal dalam, diturunkan dari warna
  cat TIGGO V), `--surround #0E1514` untuk area letterbox.
- **Tipografi** — **Archivo** (variable, lebar 110–122%) untuk masthead dan angka
  spesifikasi; **IBM Plex Sans** untuk daftar dan teks; **IBM Plex Mono** untuk
  label, satuan, dan data. Semua di-*inline* sebagai data URI, jadi artifact dan
  video memakai huruf yang sama persis.
- **Komposisi** — spread Full HD: garis rambut atas/bawah membingkai halaman,
  kolom kiri berisi foto + readout spesifikasi (nomor fitur, angka besar, satuan,
  satu kalimat fakta), kolom kanan berisi masthead + roller 10 fitur dengan header
  tabel, mask di kedua ujung, dan kursor tetap di tengah.

## Motion

- **10 detik, looping mulus** — verified: render pada `t=10s` menghasilkan hash
  piksel identik dengan `t=0`.
- Roller bergerak turun satu baris per detik dengan *detent* (45% awal tiap detik
  untuk bergerak, sisanya diam) — terasa seperti mekanis, bukan pegas.
- Angka spesifikasi berganti dengan *roll* ala odometer di dalam jendela clip;
  judul, satuan, dan deskripsi menyusul dengan fade + rise.
- Bar 10 segmen di kaki halaman: segmen aktif terisi sepanjang detiknya sendiri.
- Foto melakukan drift halus (skala + geser) memakai kurva sinus satu siklus penuh
  per loop, jadi tidak ada lompatan saat mengulang.

## 10 fitur unggulan (sumber: siaran pers GIIAS 2026)

| # | Fitur | Spesifikasi |
|---|---|---|
| 01 | Versatilitas 3-in-1 | 3 peran: SUV · MPV · Double Cab |
| 02 | Ground Clearance | 220 mm |
| 03 | Kemampuan Menanjak | 41° |
| 04 | Lintas Genangan | 700 mm |
| 05 | Easy Turn | radius putar −0,5 m |
| 06 | Sirkulasi Udara Kabin | AFCS, baris ke-3 + pilar C |
| 07 | Kabin Fleksibel | 2 · 4 · 5 · 7 kursi + bed mode |
| 08 | Chery Super Hybrid | 1.030 km (thermal eff. 42,5%) |
| 09 | Split Tailgate | 250 kg |
| 10 | Vehicle-to-Load | 2,2 kW |

## Berkas

| Berkas | Isi |
|---|---|
| `index.html` | Hasil build, self-contained (foto + huruf ter-embed) — buka langsung di browser |
| `src/template.html` | Sumber layout + motion, placeholder `__CAR_IMAGE__` dan `__FONTS__` |
| `src/fonts.py` → `src/fonts.css` | Unduh subset latin Google Fonts, simpan sebagai data URI |
| `src/crop.js` → `src/tiggo-v-card.jpg` | Crop + grading foto dari `src/tiggo-v-source.jpg` |
| `build.py` | Meng-inline foto dan huruf ke `index.html` |
| `export.js` | Render deterministik → `tiggo-v-motion.mp4`, `.gif`, `poster.jpg` |
| `tiggo-v-motion.mp4` | 1920×1080, 30 fps, 10 detik, siap di-loop |

## Cara pakai

```bash
python3 src/fonts.py              # sekali saja, atau saat daftar huruf berubah
node src/crop.js                  # saat foto sumber diganti
python3 build.py                  # rebuild index.html
node export.js                    # render ulang mp4 + gif + poster
node export.js --preview 0,4.6    # cek frame tertentu saja
```

Daftar fitur ada di array `FEATURES` (`src/template.html`). Jumlah entri
menentukan panjang loop — satu detik per fitur.

> Catatan teks: seluruh berkas sengaja dijaga ASCII (`&middot;`, `°`, dst.)
> supaya tidak ada mojibake ketika halaman dibuka tanpa header charset.
