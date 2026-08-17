# Video Tips Otomotif — Jas Hujan Ponco

Video vertikal pendek (format Reels/Shorts/TikTok) yang merangkum tips otomotif
soal pemilihan jas hujan untuk pemotor.

| | |
|---|---|
| Berkas | `tips-jas-hujan-ponco.mp4` |
| Durasi | 22,1 detik (syarat minimal 10 detik terpenuhi) |
| Resolusi | 1080 × 1920 (9:16), 30 fps |
| Video | H.264 (yuv420p), CRF 20, `+faststart` |
| Audio | AAC 128 kbps stereo — ambience hujan sintetis + whoosh transisi |
| Ukuran | ± 10,4 MB |

Sumber materi: CNN Indonesia — *"Pemotor Tak Direkomendasi Pakai Jas Hujan
Ponco, Lalu yang Mana?"*
<https://www.cnnindonesia.com/otomotif/20260113075143-595-1316386/pemotor-tak-direkomendasi-pakai-jas-hujan-ponco-lalu-yang-mana>

## Alur konten

| Waktu | Scene | Isi |
|---|---|---|
| 0,0 – 3,4 s | Hook | "Jangan pakai jas hujan ponco" — ponco bukan didesain untuk berkendara |
| 3,4 – 6,4 s | Alasan 1 | Riskan tersangkut rantai, gir, atau jari-jari roda |
| 6,4 – 9,2 s | Alasan 2 | Banyak celah, angin masuk dan mengganggu keseimbangan |
| 9,2 – 12,0 s | Alasan 3 | Jubah panjang menutupi lampu rem dan sein |
| 12,0 – 14,7 s | Alasan 4 | Tidak menutup sampai kaki, celana tetap basah |
| 14,7 – 18,3 s | Rekomendasi | Jas hujan 2 potong: jaket + celana |
| 18,3 – 22,1 s | Checklist | Warna terang, material reflektif (scotchlite), bahan PVC |

## Cara render ulang

```bash
pip install pillow numpy imageio-ffmpeg
python3 make_video.py tips-jas-hujan-ponco.mp4
```

`make_video.py` menggambar tiap frame dengan Pillow, menyalurkannya sebagai
rawvideo ke ffmpeg (biner dari paket `imageio-ffmpeg`), dan menyintesis trek
audio dengan numpy. Tidak ada aset atau font eksternal yang perlu diunduh —
teks memakai DejaVu Sans, ikon dan animasi hujan digambar secara vektor.

Untuk menyunting isi, ubah teks di fungsi `build_scenes()`. Tata letak memakai
kelas `Block` yang mengukur tinggi tiap baris, jadi teks panjang tidak akan
saling menimpa; durasi per scene adalah argumen terakhir pada `reason_scene()`.
