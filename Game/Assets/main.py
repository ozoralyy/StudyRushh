# -*- coding: utf-8 -*-
"""
==========================================================================
  STUDYRUSH  -  Game Kuis Informatika SMK Kelas 10
==========================================================================
Materi   : Gerbang Logika, Microsoft Office, Proposisi, Sejarah AI,
           Pengenalan Hardware & Software
Fitur    : 10 level x 10 soal, sistem nyawa, poin, Streak Rush (poin
           berlipat jika benar beruntun), Hint tersembunyi (harus dicari
           dulu), halaman start (input nama), beranda, papan skor,
           ulang game, animasi, karakter maskot "Rushy", dan efek suara.

CARA MENJALANKAN
  1. pip install pygame
  2. Letakkan file ini satu folder dengan file suara:
       Sound Start.mp3        -> musik halaman start & beranda
       Sound Keseluruhan.mp3  -> musik utama selama bermain
       Jawaban Benar.mp3      -> jawaban benar
       Sound Salah Jawab.mp3  -> jawaban salah
       Sound Nyawa.mp3        -> nyawa berkurang
       Sound Mati.mp3         -> nyawa habis (game over)
     (boleh juga di subfolder: sound / sounds / audio / assets)
  3. python StudyRush.py
==========================================================================
"""

import os
import sys
import json
import math
import random
import colorsys
import datetime

try:
    import pygame
except ImportError:
    print("Pygame belum terpasang. Jalankan perintah:  pip install pygame")
    sys.exit(1)


# =========================================================================
#  KONFIGURASI UMUM
# =========================================================================
W, H = 1100, 680
FPS = 60
MAX_LIVES = 5
QUESTIONS_PER_LEVEL = 10
TOTAL_LEVELS = 10

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "studyrush_data.json")

SOUND_FILES = {
    "start": "Sound Start.mp3",
    "main": "Sound Keseluruhan.mp3",
    "benar": "Jawaban Benar.mp3",
    "salah": "Sound Salah Jawab.mp3",
    "nyawa": "Sound Nyawa.mp3",
    "mati": "Sound Mati.mp3",
}

SEARCH_DIRS = [
    BASE_DIR,
    os.path.join(BASE_DIR, "sound"),
    os.path.join(BASE_DIR, "sounds"),
    os.path.join(BASE_DIR, "Sound"),
    os.path.join(BASE_DIR, "audio"),
    os.path.join(BASE_DIR, "assets"),
    os.getcwd(),
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 214, 70)
RED = (235, 60, 80)
GREEN = (60, 200, 120)
NAVY = (25, 35, 80)


# =========================================================================
#  BANK SOAL  (soal, jawaban_benar, salah1, salah2, salah3, hint)
#  Urutan pilihan diacak otomatis saat game berjalan.
# =========================================================================
LEVELS = [
    # ------------------------------------------------------------ LEVEL 1
    {
        "title": "Pengenalan Hardware",
        "topic": "Hardware",
        "desc": "Kenali perangkat keras komputer: CPU, RAM, input, output, dan penyimpanan.",
        "questions": [
            ("Komponen komputer yang bentuknya fisik dan dapat disentuh disebut ...",
             "Hardware", "Software", "Brainware", "Firmware",
             "Perangkat keras bisa dipegang, perangkat lunak tidak."),
            ("Bagian komputer yang berfungsi sebagai 'otak' pemroses instruksi adalah ...",
             "CPU (Processor)", "Monitor", "Keyboard", "Speaker",
             "Singkatan dari Central Processing Unit."),
            ("Memori utama yang bersifat sementara dan isinya hilang saat listrik padam adalah ...",
             "RAM", "Hard Disk", "Flashdisk", "DVD-ROM",
             "Random Access Memory."),
            ("Manakah yang termasuk perangkat INPUT?",
             "Scanner", "Printer", "Monitor", "Speaker",
             "Input = memasukkan data ke dalam komputer."),
            ("Manakah yang termasuk perangkat OUTPUT?",
             "Printer", "Mouse", "Keyboard", "Webcam",
             "Output = menghasilkan keluaran dari komputer."),
            ("Media penyimpanan permanen di dalam casing komputer adalah ...",
             "Hard Disk / SSD", "RAM", "Register", "Cache",
             "Data tetap ada walau komputer dimatikan."),
            ("Papan sirkuit utama yang menghubungkan semua komponen komputer disebut ...",
             "Motherboard", "Power Supply", "Heatsink", "Casing",
             "Papan induk tempat CPU dan RAM dipasang."),
            ("Kecepatan prosesor biasanya dinyatakan dalam satuan ...",
             "Hertz (GHz)", "Pixel", "Watt", "Decibel",
             "Berkaitan dengan jumlah siklus per detik."),
            ("Satu byte terdiri dari berapa bit?",
             "8 bit", "4 bit", "16 bit", "2 bit",
             "Dua pangkat tiga."),
            ("Port yang paling umum dipakai untuk menghubungkan flashdisk adalah ...",
             "USB", "VGA", "HDMI", "RJ-45",
             "Singkatan dari Universal Serial Bus."),
        ],
    },
    # ------------------------------------------------------------ LEVEL 2
    {
        "title": "Pengenalan Software",
        "topic": "Software",
        "desc": "Sistem operasi, aplikasi, bahasa pemrograman, dan jenis-jenis perangkat lunak.",
        "questions": [
            ("Windows, Linux, dan macOS termasuk jenis perangkat lunak ...",
             "Sistem Operasi", "Aplikasi Pengolah Kata", "Bahasa Pemrograman", "Antivirus",
             "Mengelola seluruh sumber daya komputer."),
            ("Microsoft Word dan Excel termasuk perangkat lunak ...",
             "Aplikasi", "Sistem Operasi", "Firmware", "Driver",
             "Dipakai pengguna untuk menyelesaikan tugas tertentu."),
            ("Orang yang mengoperasikan komputer disebut ...",
             "Brainware", "Hardware", "Software", "Malware",
             "Brain = otak, yaitu manusianya."),
            ("Software yang tertanam permanen pada perangkat keras, misalnya BIOS, disebut ...",
             "Firmware", "Freeware", "Shareware", "Spyware",
             "Firm artinya tetap / kokoh."),
            ("Sistem operasi yang kode sumbernya terbuka (open source) adalah ...",
             "Linux", "Windows", "macOS", "iOS",
             "Logonya penguin bernama Tux."),
            ("Program yang menerjemahkan kode program menjadi bahasa mesin disebut ...",
             "Compiler", "Browser", "Driver", "Defragmenter",
             "Menyusun / mengkompilasi seluruh kode."),
            ("Python, Java, dan C++ adalah contoh ...",
             "Bahasa Pemrograman", "Sistem Operasi", "Perangkat Input", "Jenis Memori",
             "Dipakai programmer untuk menulis kode."),
            ("Software untuk mendeteksi dan menghapus virus komputer adalah ...",
             "Antivirus", "Compiler", "Media Player", "Spreadsheet",
             "Anti = melawan."),
            ("Program kecil yang membuat OS mengenali perangkat keras seperti printer disebut ...",
             "Driver", "Plugin", "Browser", "Emulator",
             "Pengendali perangkat."),
            ("Software yang bebas digunakan secara gratis tanpa batas waktu disebut ...",
             "Freeware", "Trial", "Shareware", "Malware",
             "Free = gratis."),
        ],
    },
    # ------------------------------------------------------------ LEVEL 3
    {
        "title": "Gerbang Logika Dasar",
        "topic": "Gerbang Logika",
        "desc": "Kenali gerbang AND, OR, dan NOT beserta tabel kebenarannya.",
        "questions": [
            ("Gerbang AND menghasilkan output 1 hanya jika ...",
             "semua inputnya bernilai 1", "salah satu inputnya 1", "semua inputnya 0", "inputnya berbeda",
             "Bayangkan dua saklar seri: keduanya harus menyala."),
            ("Gerbang OR menghasilkan output 0 hanya jika ...",
             "semua inputnya bernilai 0", "semua inputnya 1", "salah satu input 1", "inputnya berbeda",
             "Cukup satu input 1, output sudah 1."),
            ("Gerbang NOT berfungsi untuk ...",
             "membalikkan nilai input", "menjumlahkan dua input", "mengalikan input", "menyimpan data",
             "Disebut juga inverter."),
            ("Jika A = 1 dan B = 0, output gerbang AND adalah ...",
             "0", "1", "10", "tidak terdefinisi",
             "Salah satu input 0, maka AND pasti 0."),
            ("Jika A = 1 dan B = 0, output gerbang OR adalah ...",
             "1", "0", "10", "tidak terdefinisi",
             "Ada satu input yang bernilai 1."),
            ("Output gerbang NOT jika inputnya 0 adalah ...",
             "1", "0", "0 dan 1", "tidak ada",
             "Kebalikan dari 0."),
            ("Dalam aljabar Boolean, gerbang AND dilambangkan dengan operasi ...",
             "perkalian (A . B)", "penjumlahan (A + B)", "pengurangan (A - B)", "pembagian (A / B)",
             "1 x 1 = 1, sisanya 0."),
            ("Dalam aljabar Boolean, gerbang OR dilambangkan dengan operasi ...",
             "penjumlahan (A + B)", "perkalian (A . B)", "negasi (A')", "pembagian (A / B)",
             "Tanda plus."),
            ("Gerbang logika yang hanya memiliki SATU input adalah ...",
             "NOT", "AND", "OR", "XOR",
             "Cuma membalik satu sinyal."),
            ("Hasil dari (1 AND 1) OR 0 adalah ...",
             "1", "0", "10", "tidak bisa dihitung",
             "Kerjakan dalam kurung dulu: 1 AND 1 = 1."),
        ],
    },
    # ------------------------------------------------------------ LEVEL 4
    {
        "title": "Microsoft Word",
        "topic": "Office",
        "desc": "Pintasan keyboard dan fitur penting pengolah kata Microsoft Word.",
        "questions": [
            ("Pintasan keyboard untuk menyimpan dokumen di Microsoft Word adalah ...",
             "Ctrl + S", "Ctrl + P", "Ctrl + O", "Ctrl + N",
             "S dari Save."),
            ("Pintasan keyboard untuk menebalkan teks (Bold) adalah ...",
             "Ctrl + B", "Ctrl + I", "Ctrl + U", "Ctrl + T",
             "B dari Bold."),
            ("Ekstensi file standar dokumen Microsoft Word versi modern adalah ...",
             ".docx", ".xlsx", ".pptx", ".pdf",
             "Doc + x."),
            ("Pintasan Ctrl + Z digunakan untuk ...",
             "Undo (membatalkan aksi terakhir)", "Redo (mengulang aksi)", "Menyalin teks", "Mencetak dokumen",
             "Salah ketik? Tekan ini."),
            ("Fitur Word untuk membuat surat massal dengan data penerima berbeda adalah ...",
             "Mail Merge", "Track Changes", "Word Count", "Spelling & Grammar",
             "Menggabungkan surat dengan daftar penerima."),
            ("Fitur untuk mengatur jarak antarbaris dalam paragraf disebut ...",
             "Line Spacing", "Indent", "Margin", "Orientation",
             "Spasi baris."),
            ("Tab yang dipakai untuk menyisipkan tabel, gambar, dan nomor halaman adalah ...",
             "Insert", "Home", "Review", "View",
             "Insert = menyisipkan."),
            ("Pintasan keyboard untuk mencetak dokumen adalah ...",
             "Ctrl + P", "Ctrl + S", "Ctrl + X", "Ctrl + K",
             "P dari Print."),
            ("Pintasan Ctrl + A pada Word berfungsi untuk ...",
             "Memilih seluruh isi dokumen", "Membuka dokumen baru", "Menambah halaman", "Menyimpan dokumen",
             "A dari All."),
            ("Fitur daftar isi otomatis (Table of Contents) terdapat pada tab ...",
             "References", "Layout", "Mailings", "Design",
             "Tab untuk daftar isi, catatan kaki, dan daftar pustaka."),
        ],
    },
    # ------------------------------------------------------------ LEVEL 5
    {
        "title": "Proposisi Dasar",
        "topic": "Proposisi",
        "desc": "Pahami pernyataan, nilai kebenaran, negasi, konjungsi, dan disjungsi.",
        "questions": [
            ("Kalimat yang dapat ditentukan nilai kebenarannya (benar atau salah, tidak keduanya) disebut ...",
             "Proposisi", "Perintah", "Pertanyaan", "Seruan",
             "Dasar dari logika matematika."),
            ("Manakah yang merupakan proposisi?",
             "5 + 3 = 8", "Tolong bukakan pintu!", "Jam berapa sekarang?", "Semoga kamu sukses.",
             "Cari kalimat pernyataan yang pasti benar atau salah."),
            ("Negasi dari 'Hari ini hujan' adalah ...",
             "Hari ini tidak hujan", "Hari ini hujan deras", "Kemarin hujan", "Besok hujan",
             "Tambahkan kata 'tidak'."),
            ("Konjungsi (p dan q) bernilai benar jika ...",
             "p benar dan q benar", "p benar atau q benar", "p salah dan q salah", "p salah dan q benar",
             "Keduanya harus benar, seperti gerbang AND."),
            ("Disjungsi (p atau q) bernilai salah jika ...",
             "p salah dan q salah", "p benar dan q salah", "p salah dan q benar", "p benar dan q benar",
             "Seperti OR: salah hanya bila semuanya salah."),
            ("Jika p bernilai salah, maka negasi p (~p) bernilai ...",
             "Benar", "Salah", "Benar dan salah", "Tidak tentu",
             "Negasi membalik nilai kebenaran."),
            ("Manakah kalimat yang BUKAN proposisi?",
             "Apakah kamu sudah makan?", "Jakarta ibu kota Indonesia", "2 x 4 = 9", "Bulan mengelilingi bumi",
             "Pertanyaan tidak bernilai benar atau salah."),
            ("Diketahui p: 5 > 3 (benar) dan q: 2 > 4 (salah). Nilai (p dan q) adalah ...",
             "Salah", "Benar", "Benar dan salah", "Tidak tentu",
             "Konjungsi dengan satu komponen salah."),
            ("Jika p benar dan q salah, nilai (p atau q) adalah ...",
             "Benar", "Salah", "Tidak tentu", "Kosong",
             "Cukup satu yang benar."),
            ("Kalimat 'x + 2 = 5' disebut kalimat terbuka karena ...",
             "nilai kebenarannya bergantung pada nilai x", "pasti bernilai benar", "pasti bernilai salah", "berupa pertanyaan",
             "Ada variabel yang belum diketahui."),
        ],
    },
    # ------------------------------------------------------------ LEVEL 6
    {
        "title": "Sejarah Kecerdasan Buatan",
        "topic": "Sejarah AI",
        "desc": "Tokoh, peristiwa, dan tonggak penting perjalanan Artificial Intelligence.",
        "questions": [
            ("Istilah 'Artificial Intelligence' pertama kali dicetuskan oleh ...",
             "John McCarthy", "Bill Gates", "Steve Jobs", "Mark Zuckerberg",
             "Ia juga menciptakan bahasa pemrograman LISP."),
            ("Konferensi Dartmouth yang menandai lahirnya bidang AI berlangsung pada tahun ...",
             "1956", "1936", "1986", "2006",
             "Pertengahan tahun 1950-an."),
            ("Alan Turing mengusulkan pengujian kecerdasan mesin yang dikenal sebagai ...",
             "Turing Test", "Binary Test", "Logic Test", "Dartmouth Test",
             "Menguji apakah mesin bisa meniru percakapan manusia."),
            ("Komputer catur Deep Blue milik IBM mengalahkan juara dunia ...",
             "Garry Kasparov", "Bobby Fischer", "Magnus Carlsen", "Lee Sedol",
             "Terjadi pada tahun 1997."),
            ("ELIZA, salah satu chatbot paling awal (1960-an), dibuat di ...",
             "MIT", "Google", "Apple", "Tesla",
             "Dibuat oleh Joseph Weizenbaum di institut teknologi Massachusetts."),
            ("AlphaGo milik DeepMind mengalahkan juara dunia permainan Go bernama ...",
             "Lee Sedol", "Garry Kasparov", "Ken Jennings", "Alan Turing",
             "Terjadi tahun 2016, pemainnya dari Korea Selatan."),
            ("'AI Winter' adalah istilah untuk periode ketika ...",
             "minat dan dana riset AI menurun drastis", "AI berkembang sangat pesat", "suhu server meningkat", "AI dilarang di semua negara",
             "Winter = musim dingin = masa sepi."),
            ("Sistem IBM Watson terkenal karena memenangkan kuis televisi ...",
             "Jeopardy!", "Who Wants to Be a Millionaire", "Cerdas Cermat", "Family Feud",
             "Terjadi pada tahun 2011."),
            ("Cabang AI yang membuat komputer belajar dari data tanpa diprogram eksplisit adalah ...",
             "Machine Learning", "Hardware Engineering", "Word Processing", "Data Entry",
             "Mesin belajar dari contoh."),
            ("Chatbot ChatGPT yang populer sejak 2022 dikembangkan oleh ...",
             "OpenAI", "Nintendo", "Intel", "Sony",
             "Nama perusahaannya mengandung singkatan AI."),
        ],
    },
    # ------------------------------------------------------------ LEVEL 7
    {
        "title": "Gerbang Logika Lanjutan",
        "topic": "Gerbang Logika",
        "desc": "NAND, NOR, XOR, XNOR, gerbang universal, dan half adder.",
        "questions": [
            ("Gerbang NAND adalah gabungan gerbang ...",
             "AND yang diikuti NOT", "OR yang diikuti NOT", "NOT yang diikuti OR", "XOR yang diikuti AND",
             "N = Not, lalu AND."),
            ("Output gerbang NOR bernilai 1 hanya jika ...",
             "semua inputnya 0", "semua inputnya 1", "inputnya berbeda", "salah satu inputnya 1",
             "NOR = kebalikan OR."),
            ("Gerbang XOR menghasilkan output 1 jika ...",
             "kedua input berbeda", "kedua input sama", "semua input 1", "semua input 0",
             "Exclusive OR: hanya salah satu yang 1."),
            ("Gerbang XNOR menghasilkan output 1 jika ...",
             "kedua input sama", "kedua input berbeda", "salah satu input 0", "kedua input 0 saja",
             "Kebalikan dari XOR."),
            ("Gerbang yang disebut 'gerbang universal' karena dapat membentuk semua gerbang lain adalah ...",
             "NAND dan NOR", "AND dan OR", "XOR dan XNOR", "NOT dan AND",
             "Dua gerbang yang diawali huruf N."),
            ("Jika A = 1 dan B = 1, output gerbang XOR adalah ...",
             "0", "1", "11", "tidak tentu",
             "Inputnya sama, bukan berbeda."),
            ("Jika A = 0 dan B = 0, output gerbang NAND adalah ...",
             "1", "0", "00", "tidak tentu",
             "0 AND 0 = 0, lalu dibalik."),
            ("Jika A = 1 dan B = 0, output gerbang NOR adalah ...",
             "0", "1", "10", "tidak tentu",
             "1 OR 0 = 1, lalu dibalik."),
            ("Tabel kebenaran untuk gerbang dengan 3 input memiliki berapa baris kombinasi?",
             "8", "6", "4", "9",
             "Dua pangkat tiga."),
            ("Pada rangkaian half adder, bit hasil penjumlahan (Sum) dibentuk oleh gerbang ...",
             "XOR", "NOT", "NOR", "XNOR",
             "Sum bernilai 1 jika kedua input berbeda."),
        ],
    },
    # ------------------------------------------------------------ LEVEL 8
    {
        "title": "Excel & PowerPoint",
        "topic": "Office",
        "desc": "Rumus Excel, alamat sel, fungsi logika, dan fitur presentasi PowerPoint.",
        "questions": [
            ("Rumus Excel untuk menjumlahkan sel A1 sampai A5 adalah ...",
             "=SUM(A1:A5)", "=ADD(A1:A5)", "=TOTAL(A1,A5)", "=PLUS(A1:A5)",
             "Fungsi jumlah dalam bahasa Inggris."),
            ("Fungsi Excel untuk mencari nilai rata-rata adalah ...",
             "AVERAGE", "MEAN", "MEDIAN", "COUNT",
             "Rata-rata dalam bahasa Inggris."),
            ("Alamat sel pada kolom B baris 3 adalah ...",
             "B3", "3B", "B-3", "C2",
             "Huruf kolom dulu, baru nomor baris."),
            ("Fungsi Excel untuk menemukan nilai tertinggi dalam sekumpulan data adalah ...",
             "MAX", "MIN", "TOP", "HIGH",
             "Maximum."),
            ("Setiap rumus di Excel harus diawali dengan tanda ...",
             "=", "#", "@", "&",
             "Tanda sama dengan."),
            ("Ekstensi file standar presentasi Microsoft PowerPoint adalah ...",
             ".pptx", ".docx", ".xlsx", ".txt",
             "P untuk PowerPoint."),
            ("Tombol keyboard untuk menjalankan slide show dari awal di PowerPoint adalah ...",
             "F5", "F1", "F7", "F12",
             "Tombol fungsi kelima."),
            ("Fitur PowerPoint untuk mengatur efek perpindahan antar slide adalah ...",
             "Transition", "Animation", "Design", "Review",
             "Transisi."),
            ("Fungsi Excel untuk mengambil keputusan berdasarkan kondisi (jika ... maka ...) adalah ...",
             "IF", "SUM", "LEN", "ROUND",
             "Dalam bahasa Inggris artinya 'jika'."),
            ("Penulisan referensi sel absolut di Excel yang benar adalah ...",
             "$A$1", "A1", "#A#1", "&A&1",
             "Tanda dolar mengunci kolom dan baris."),
        ],
    },
    # ------------------------------------------------------------ LEVEL 9
    {
        "title": "Proposisi Lanjutan",
        "topic": "Proposisi",
        "desc": "Implikasi, biimplikasi, tautologi, konvers, invers, kontraposisi, De Morgan.",
        "questions": [
            ("Implikasi 'jika p maka q' bernilai salah hanya jika ...",
             "p benar dan q salah", "p salah dan q benar", "p dan q keduanya salah", "p dan q keduanya benar",
             "Seperti janji yang dilanggar."),
            ("Biimplikasi (p jika dan hanya jika q) bernilai benar jika ...",
             "p dan q bernilai sama", "p dan q berbeda", "hanya p yang benar", "hanya q yang salah",
             "Mirip gerbang XNOR."),
            ("Pernyataan majemuk yang selalu benar apa pun nilai komponennya disebut ...",
             "Tautologi", "Kontradiksi", "Kontingensi", "Negasi",
             "Contoh: p atau ~p."),
            ("Pernyataan majemuk yang selalu salah disebut ...",
             "Kontradiksi", "Tautologi", "Implikasi", "Disjungsi",
             "Contoh: p dan ~p."),
            ("Konvers dari 'jika p maka q' adalah ...",
             "jika q maka p", "jika ~p maka ~q", "jika ~q maka ~p", "p dan q",
             "Tukar posisi p dan q."),
            ("Invers dari 'jika p maka q' adalah ...",
             "jika ~p maka ~q", "jika q maka p", "jika ~q maka ~p", "p atau q",
             "Negasikan kedua bagian, posisi tetap."),
            ("Kontraposisi dari 'jika p maka q' adalah ...",
             "jika ~q maka ~p", "jika q maka p", "jika ~p maka ~q", "p dan ~q",
             "Tukar posisi sekaligus negasikan; ekuivalen dengan aslinya."),
            ("Menurut hukum De Morgan, ~(p dan q) ekuivalen dengan ...",
             "~p atau ~q", "~p dan ~q", "p atau q", "p dan ~q",
             "Kata 'dan' berubah menjadi 'atau'."),
            ("Menurut hukum De Morgan, ~(p atau q) ekuivalen dengan ...",
             "~p dan ~q", "~p atau ~q", "p dan q", "~p atau q",
             "Kata 'atau' berubah menjadi 'dan'."),
            ("Jika p salah dan q benar, nilai kebenaran 'jika p maka q' adalah ...",
             "Benar", "Salah", "Tidak tentu", "Kosong",
             "Pangkal yang salah selalu membuat implikasi benar."),
        ],
    },
    # ----------------------------------------------------------- LEVEL 10
    {
        "title": "Boss Battle: Campuran",
        "topic": "Campuran",
        "desc": "Level terakhir! Gabungan semua materi. Buktikan kamu juara StudyRush!",
        "questions": [
            ("Komponen elektronik dasar penyusun gerbang logika di dalam prosesor adalah ...",
             "Transistor", "Kapasitor kertas", "Speaker", "Kabel LAN",
             "Bekerja seperti saklar mikroskopis."),
            ("Rumus Excel yang menerapkan logika AND dengan benar adalah ...",
             "=AND(A1>5, B1<10)", "=A1>5 AND B1<10", "=IF AND(A1,B1)", "=&(A1>5,B1<10)",
             "AND ditulis sebagai fungsi dengan tanda kurung."),
            ("Konjungsi pada proposisi paling mirip dengan gerbang ...",
             "AND", "OR", "NOT", "NOR",
             "Keduanya harus benar."),
            ("Turing Test bertujuan menguji ...",
             "apakah mesin mampu berperilaku seperti manusia", "kecepatan prosesor", "kapasitas hard disk", "kualitas layar monitor",
             "Dikenal juga sebagai imitation game."),
            ("Perangkat lunak yang mengatur dan membagi sumber daya hardware kepada program lain adalah ...",
             "Sistem Operasi", "Antivirus", "Aplikasi Presentasi", "Driver Printer",
             "Windows, Linux, dan Android adalah contohnya."),
            ("Hasil dari 1 XOR 1 XOR 1 adalah ...",
             "1", "0", "11", "tidak tentu",
             "Hitung bertahap: 1 XOR 1 = 0, lalu 0 XOR 1."),
            ("Bilangan biner 101 sama dengan bilangan desimal ...",
             "5", "3", "6", "7",
             "4 + 0 + 1."),
            ("Teknologi AI modern yang meniru otak dengan banyak lapisan disebut ...",
             "Deep Learning (Jaringan Saraf Tiruan)", "Spreadsheet", "Mail Merge", "Defragmentasi",
             "Neural network."),
            ("Kalimat 'Jika hujan turun maka jalanan basah' termasuk proposisi majemuk jenis ...",
             "Implikasi", "Konjungsi", "Disjungsi", "Negasi",
             "Pola kalimat: jika ... maka ..."),
            ("RAM, CPU, dan Motherboard adalah contoh ..., sedangkan Windows adalah contoh ...",
             "Hardware; Software", "Software; Hardware", "Brainware; Firmware", "Input; Output",
             "Bisa disentuh vs tidak bisa disentuh."),
        ],
    },
]

# Setiap level punya 10 soal utama + 1 soal cadangan (11 soal). Saat level
# dimulai, soal diacak lalu 10 soal diambil, jadi tiap main soalnya bervariasi.
EXTRA_QUESTIONS = [
    ("Satuan terkecil data dalam komputer adalah ...",
     "Bit", "Byte", "Kilobyte", "Megabyte",
     "Hanya bernilai 0 atau 1."),
    ("Sistem operasi buatan Microsoft yang paling banyak dipakai di PC adalah ...",
     "Windows", "Android", "iOS", "Ubuntu",
     "Logonya berbentuk jendela."),
    ("Gerbang logika yang outputnya 1 jika SALAH SATU atau kedua input bernilai 1 adalah ...",
     "OR", "AND", "NOT", "NAND",
     "Cukup satu saja sudah menyala."),
    ("Pintasan keyboard untuk menyalin (copy) teks di Word adalah ...",
     "Ctrl + C", "Ctrl + V", "Ctrl + X", "Ctrl + Z",
     "C dari Copy."),
    ("'Hari ini cerah.' disimbolkan p. Maka 'Hari ini tidak cerah' disimbolkan ...",
     "~p", "p dan q", "p atau q", "q",
     "Tanda tilde berarti tidak."),
    ("Tokoh yang sering disebut sebagai bapak ilmu komputer dan mesin cerdas adalah ...",
     "Alan Turing", "Isaac Newton", "Thomas Edison", "Nikola Tesla",
     "Ia memecahkan kode mesin Enigma pada Perang Dunia II."),
    ("Output dari gerbang AND dengan input A = 1 dan B = 1 adalah ...",
     "1", "0", "2", "tidak tentu",
     "Keduanya bernilai 1."),
    ("Rumus Excel untuk menghitung banyaknya sel yang berisi angka adalah ...",
     "COUNT", "SUM", "ROUND", "IF",
     "Count = menghitung."),
    ("Invers dari 'jika hujan maka banjir' adalah ...",
     "jika tidak hujan maka tidak banjir", "jika banjir maka hujan", "jika tidak banjir maka tidak hujan", "hujan dan banjir",
     "Tambahkan kata 'tidak' pada kedua bagian."),
    ("Lambang aljabar Boolean untuk operasi NOT pada variabel A adalah ...",
     "A' (A aksen)", "A + A", "A . A", "A / A",
     "Tanda aksen di belakang huruf."),
]
# Satu soal tambahan dipasang per level (urutan sesuai level).
for _i, _lvl in enumerate(LEVELS):
    _lvl["questions"].append(EXTRA_QUESTIONS[_i])

THEMES = [
    ((18, 32, 84), (50, 130, 210), (110, 220, 255)),
    ((34, 24, 92), (120, 70, 200), (200, 160, 255)),
    ((12, 60, 70), (30, 160, 140), (120, 255, 210)),
    ((14, 40, 100), (40, 110, 230), (130, 190, 255)),
    ((70, 25, 90), (190, 70, 160), (255, 160, 220)),
    ((20, 20, 48), (70, 60, 150), (170, 170, 255)),
    ((10, 70, 50), (30, 150, 80), (150, 255, 150)),
    ((90, 40, 20), (220, 110, 40), (255, 200, 120)),
    ((60, 20, 70), (140, 50, 150), (240, 140, 255)),
    ((70, 15, 25), (190, 45, 50), (255, 190, 90)),
]
HOME_THEME = ((25, 20, 85), (95, 55, 175), (255, 205, 90))
OVER_THEME = ((25, 5, 12), (90, 15, 30), (255, 90, 110))
WIN_THEME = ((60, 40, 5), (200, 140, 20), (255, 240, 150))

CORRECT_LINES = [
    "Mantap! Jawabanmu tepat!", "Keren, terus semangat!", "Yes! Otakmu encer!",
    "Benar sekali!", "Wih, jago banget!", "Mantul! Lanjutkan!",
]
WRONG_LINES = [
    "Yah, belum tepat...", "Tenang, kamu pasti bisa!", "Aduh, hampir!",
    "Jangan menyerah ya!", "Ayo teliti lagi!",
]
STREAK_LINES = [
    "STREAK RUSH! Poinmu berlipat!", "Api semangat menyala!", "Jangan sampai putus, ya!",
]
ASK_LINES = [
    "Ayo semangat, {n}!", "Baca soal baik-baik ya.", "Cari bintang hint kalau bingung!",
    "Kamu pasti bisa, {n}!", "Fokus dan teliti!", "Waktunya beraksi!",
]

HOWTO_LINES = [
    ("Tujuan", "Taklukkan 10 level. Tiap level berisi 10 soal informatika SMK kelas 10."),
    ("Nyawa", "Kamu punya 5 nyawa. Salah atau waktu habis = nyawa berkurang. Jika nyawa habis, game diulang dari Level 1!"),
    ("Poin", "Jawab cepat untuk bonus waktu. Semakin tinggi level, semakin besar poin dasarnya."),
    ("Streak Rush", "Jawab benar beruntun! 3 benar = x2, 6 benar = x3, 9 benar = x4, 12+ = x5. Sekali salah, streak hilang."),
    ("Hint Rahasia", "Hint tidak diberikan gratis. Cari bintang kecil yang berkedip di layar lalu klik! Semakin dekat kursor, semakin terang. Poin soal itu jadi x0.7."),
    ("Kontrol", "Klik jawaban atau tekan 1-4 / A-D. P atau ESC = jeda. M = bisukan suara."),
]


# =========================================================================
#  FUNGSI BANTU
# =========================================================================
_FONTS = {}
_GRADIENTS = {}


def get_font(size, bold=False):
    key = (int(size), bool(bold))
    if key not in _FONTS:
        _FONTS[key] = pygame.font.SysFont(
            "segoeui,arial,helvetica,dejavusans,liberationsans", int(size), bold=bold)
    return _FONTS[key]


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    t = clamp(t, 0.0, 1.0)
    return (int(lerp(c1[0], c2[0], t)), int(lerp(c1[1], c2[1], t)), int(lerp(c1[2], c2[2], t)))


def R(x, y, w, h):
    return pygame.Rect(int(x), int(y), int(w), int(h))


def rainbow(h, s=0.55, v=1.0):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def find_asset(filename):
    for d in SEARCH_DIRS:
        p = os.path.join(d, filename)
        if os.path.isfile(p):
            return p
    low = filename.lower()
    for d in SEARCH_DIRS:
        try:
            for f in os.listdir(d):
                if f.lower() == low:
                    return os.path.join(d, f)
        except OSError:
            pass
    return None


def make_gradient(top, bottom):
    key = (top, bottom)
    if key in _GRADIENTS:
        return _GRADIENTS[key]
    surf = pygame.Surface((W, H))
    for y in range(H):
        pygame.draw.line(surf, lerp_color(top, bottom, y / float(H - 1)), (0, y), (W, y))
    _GRADIENTS[key] = surf
    return surf


def wrap_text(text, font, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text(surf, text, size, color, pos, anchor="topleft", bold=False, shadow=None, alpha=None):
    font = get_font(size, bold)
    img = font.render(text, True, color)
    if alpha is not None:
        img.set_alpha(alpha)
    rect = img.get_rect()
    setattr(rect, anchor, (int(pos[0]), int(pos[1])))
    if shadow:
        sh = font.render(text, True, shadow)
        if alpha is not None:
            sh.set_alpha(alpha)
        surf.blit(sh, rect.move(2, 2))
    surf.blit(img, rect)
    return rect


def draw_panel(surf, rect, color=(10, 15, 45, 190), radius=18, border=None, border_w=2):
    rect = pygame.Rect(rect)
    s = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(s, color, s.get_rect(), border_radius=radius)
    if border:
        pygame.draw.rect(s, border, s.get_rect(), width=border_w, border_radius=radius)
    surf.blit(s, rect.topleft)


def star_points(cx, cy, r, points=5, inner=0.45, rot=-math.pi / 2):
    pts = []
    for i in range(points * 2):
        ang = rot + i * math.pi / points
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    return pts


def heart_points(cx, cy, size, steps=44):
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * size / 34.0, cy - y * size / 34.0))
    return pts


def draw_heart(surf, cx, cy, size, fill, outline=None):
    pts = heart_points(cx, cy, size)
    pygame.draw.polygon(surf, fill, pts)
    if outline:
        pygame.draw.polygon(surf, outline, pts, 2)
    pygame.draw.circle(surf, lerp_color(fill, WHITE, 0.6),
                       (int(cx - size * 0.22), int(cy - size * 0.2)), max(1, int(size * 0.07)))


def draw_flame(surf, cx, cy, size, t):
    layers = ((1.0, (255, 80, 30)), (0.72, (255, 165, 40)), (0.45, (255, 238, 130)))
    for scale, color in layers:
        s = size * scale
        flick = math.sin(t * 12 + scale * 5) * 0.12
        pygame.draw.circle(surf, color, (int(cx), int(cy + s * 0.25)), int(s * 0.62))
        tip = [(cx - s * 0.55, cy + s * 0.05), (cx + s * 0.55, cy + s * 0.05),
               (cx + s * flick * 0.6, cy - s * (1.35 + flick))]
        pygame.draw.polygon(surf, color, tip)


def quad_bezier(p0, p1, p2, n=18):
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts


def make_gate_sprite(kind, color, h=44, alpha=80):
    w = int(h * 1.7)
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    c = (*color, 255)
    lw = 3
    if kind == "AND":
        pygame.draw.line(s, c, (4, 3), (w * 0.5, 3), lw)
        pygame.draw.line(s, c, (4, h - 3), (w * 0.5, h - 3), lw)
        pygame.draw.line(s, c, (4, 3), (4, h - 3), lw)
        pygame.draw.arc(s, c, R(w * 0.5 - h / 2 + h / 2 - 2, 3, h - 6 + 4, h - 6), -math.pi / 2, math.pi / 2, lw)
    elif kind in ("OR", "XOR"):
        top = quad_bezier((4, 3), (w * 0.55, 3), (w - 8, h / 2))
        bot = quad_bezier((4, h - 3), (w * 0.55, h - 3), (w - 8, h / 2))
        left = quad_bezier((4, 3), (w * 0.22, h / 2), (4, h - 3))
        pygame.draw.lines(s, c, False, top, lw)
        pygame.draw.lines(s, c, False, bot, lw)
        pygame.draw.lines(s, c, False, left, lw)
        if kind == "XOR":
            left2 = quad_bezier((-6, 3), (w * 0.12, h / 2), (-6, h - 3))
            pygame.draw.lines(s, c, False, left2, lw)
    else:  # NOT
        pygame.draw.polygon(s, c, [(4, 3), (4, h - 3), (w - 18, h / 2)], lw)
        pygame.draw.circle(s, c, (int(w - 12), int(h / 2)), 6, lw)
    s.set_alpha(alpha)
    return s


# =========================================================================
#  MANAJEMEN DATA (SKOR)
# =========================================================================
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                data.setdefault("last_name", "")
                data.setdefault("scores", [])
                return data
    except (OSError, ValueError):
        pass
    return {"last_name": "", "scores": []}


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as err:
        print("[StudyRush] Gagal menyimpan data:", err)


# =========================================================================
#  SOUND MANAGER
# =========================================================================
class SoundManager:
    def __init__(self):
        self.enabled = True
        self.muted = False
        self.music_volume = 0.45
        self.sfx_volume = 0.95
        self.sfx = {}
        self.current_music = None
        try:
            pygame.mixer.init()
        except pygame.error as err:
            print("[StudyRush] Audio tidak tersedia:", err)
            self.enabled = False
            return
        for key in ("benar", "salah", "nyawa", "mati"):
            self.sfx[key] = self._load_sfx(key)
        for key in ("start", "main"):
            if not find_asset(SOUND_FILES[key]):
                print("[StudyRush] File suara tidak ditemukan:", SOUND_FILES[key])

    def _load_sfx(self, key):
        path = find_asset(SOUND_FILES[key])
        if not path:
            print("[StudyRush] File suara tidak ditemukan:", SOUND_FILES[key])
            return None
        try:
            return pygame.mixer.Sound(path)
        except pygame.error as err:
            print("[StudyRush] Gagal memuat", SOUND_FILES[key], "->", err)
            return None

    def play_music(self, key):
        if not self.enabled or self.current_music == key:
            return
        self.current_music = None
        path = find_asset(SOUND_FILES[key])
        if not path:
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.0 if self.muted else self.music_volume)
            pygame.mixer.music.play(-1)
            self.current_music = key
        except pygame.error as err:
            print("[StudyRush] Gagal memutar musik:", err)

    def stop_music(self):
        if not self.enabled:
            return
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
        self.current_music = None

    def pause_music(self):
        if self.enabled:
            try:
                pygame.mixer.music.pause()
            except pygame.error:
                pass

    def resume_music(self):
        if self.enabled:
            try:
                pygame.mixer.music.unpause()
            except pygame.error:
                pass

    def play(self, key):
        if not self.enabled or self.muted:
            return
        snd = self.sfx.get(key)
        if snd:
            snd.set_volume(self.sfx_volume)
            snd.play()

    def toggle_mute(self):
        self.muted = not self.muted
        if self.enabled:
            try:
                pygame.mixer.music.set_volume(0.0 if self.muted else self.music_volume)
            except pygame.error:
                pass


# =========================================================================
#  PARTIKEL & TEKS MELAYANG
# =========================================================================
class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color", "size", "grav", "shape")

    def __init__(self, x, y, vx, vy, life, color, size, grav, shape):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.life = self.max_life = life
        self.color, self.size, self.grav, self.shape = color, size, grav, shape


class ParticleSystem:
    def __init__(self):
        self.items = []

    def add(self, x, y, vx, vy, life, color, size, grav=0.0, shape="circle"):
        self.items.append(Particle(x, y, vx, vy, life, color, size, grav, shape))

    def burst(self, x, y, colors, n=24, speed=260, life=0.9, size=5, grav=400, shape="circle"):
        for _ in range(n):
            a = random.uniform(0, 2 * math.pi)
            sp = random.uniform(0.3, 1.0) * speed
            self.add(x, y, math.cos(a) * sp, math.sin(a) * sp, random.uniform(0.5, 1.0) * life,
                     random.choice(colors), random.uniform(0.6, 1.2) * size, grav, shape)

    def confetti(self, x, y, n=40):
        colors = [(255, 90, 120), (255, 214, 70), (90, 220, 255), (120, 255, 150), (200, 130, 255)]
        for _ in range(n):
            a = random.uniform(-math.pi * 0.95, -math.pi * 0.05)
            sp = random.uniform(200, 560)
            self.add(x, y, math.cos(a) * sp, math.sin(a) * sp, random.uniform(0.9, 1.7),
                     random.choice(colors), random.uniform(4, 8), 700, "square")

    def sparkle(self, x, y, n=18):
        self.burst(x, y, [(255, 240, 150), (255, 214, 70), WHITE], n, 220, 0.8, 5, 60, "star")

    def flame(self, x, y):
        self.add(x, y, random.uniform(-25, 25), random.uniform(-190, -100), random.uniform(0.5, 0.95),
                 random.choice([(255, 90, 30), (255, 160, 40), (255, 220, 90)]),
                 random.uniform(6, 12), -80, "circle")

    def update(self, dt):
        alive = []
        for p in self.items:
            p.life -= dt
            if p.life <= 0:
                continue
            p.vy += p.grav * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            alive.append(p)
        self.items = alive[-900:]

    def draw(self, surf):
        for p in self.items:
            k = p.life / p.max_life
            r = max(1, int(p.size * k))
            if p.shape == "square":
                pygame.draw.rect(surf, p.color, (int(p.x - r), int(p.y - r), r * 2, r * 2))
            elif p.shape == "star":
                pygame.draw.polygon(surf, p.color, star_points(p.x, p.y, r * 1.8, 4, 0.35))
            else:
                pygame.draw.circle(surf, p.color, (int(p.x), int(p.y)), r)


# =========================================================================
#  BACKGROUND ANIMASI
# =========================================================================
class Background:
    LABELS = ["0", "1", "AND", "OR", "NOT", "XOR", "NAND", "AI", "CPU", "RAM",
              "1", "0", "&", "+", "BIT", "USB", "IF", "SUM"]

    def __init__(self, theme):
        self.theme = theme
        self.t = 0.0
        self.set_theme(theme)

    def set_theme(self, theme):
        self.theme = theme
        top, bottom, accent = theme
        self.grad = make_gradient(top, bottom)
        self.glyphs = []
        self.gates = []
        self.stars = []
        self.circuits = []
        light = lerp_color(accent, WHITE, 0.4)
        for _ in range(34):
            layer = random.choice((0, 1, 2))
            size = (18, 26, 38)[layer]
            sprite = get_font(size, True).render(random.choice(self.LABELS), True, light)
            sprite.set_alpha((38, 62, 88)[layer])
            self.glyphs.append({
                "sprite": sprite, "x": random.uniform(0, W), "y": random.uniform(0, H),
                "vy": -random.uniform(8, 22) * (layer + 1) * 0.6,
                "phase": random.uniform(0, 6.28), "sway": random.uniform(6, 20)})
        for kind in ("AND", "OR", "NOT", "XOR", "AND", "OR", "NOT"):
            self.gates.append({
                "sprite": make_gate_sprite(kind, accent, random.choice((36, 48, 60)), random.choice((45, 65, 85))),
                "x": random.uniform(0, W), "y": random.uniform(0, H),
                "vy": -random.uniform(10, 26), "phase": random.uniform(0, 6.28)})
        for _ in range(70):
            self.stars.append((random.uniform(0, W), random.uniform(0, H),
                               random.choice((1, 1, 2, 2, 3)), random.uniform(0, 6.28),
                               random.uniform(1.0, 3.5)))
        for _ in range(6):
            x = random.randint(20, W - 200)
            y = random.randint(H - 105, H - 15)
            pts = [(x, y)]
            for _ in range(random.randint(4, 7)):
                if random.random() < 0.5:
                    x = clamp(x + random.choice((-1, 1)) * random.randint(60, 190), 10, W - 10)
                else:
                    y = clamp(y + random.choice((-1, 1)) * random.randint(25, 70), H - 110, H - 10)
                pts.append((x, y))
            cum = [0.0]
            for i in range(1, len(pts)):
                cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
            self.circuits.append({"pts": pts, "cum": cum, "pos": random.uniform(0, max(1, cum[-1])),
                                  "speed": random.uniform(70, 150)})

    def update(self, dt):
        self.t += dt
        for g in self.glyphs:
            g["y"] += g["vy"] * dt
            if g["y"] < -60:
                g["y"] = H + 40
                g["x"] = random.uniform(0, W)
        for g in self.gates:
            g["y"] += g["vy"] * dt
            if g["y"] < -80:
                g["y"] = H + 60
                g["x"] = random.uniform(0, W)
        for c in self.circuits:
            c["pos"] += c["speed"] * dt
            if c["pos"] > c["cum"][-1]:
                c["pos"] = 0.0

    @staticmethod
    def _point_on_path(c):
        d = c["pos"]
        for i in range(1, len(c["pts"])):
            if d <= c["cum"][i]:
                seg = c["cum"][i] - c["cum"][i - 1]
                k = 0 if seg == 0 else (d - c["cum"][i - 1]) / seg
                a, b = c["pts"][i - 1], c["pts"][i]
                return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))
        return c["pts"][-1]

    def draw(self, surf):
        surf.blit(self.grad, (0, 0))
        top, bottom, accent = self.theme
        for (x, y, r, ph, sp) in self.stars:
            b = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(self.t * sp + ph))
            pygame.draw.circle(surf, lerp_color(bottom, WHITE, b), (int(x), int(y)), r)
        line_col = lerp_color(bottom, accent, 0.35)
        for c in self.circuits:
            pygame.draw.lines(surf, line_col, False, c["pts"], 2)
            for p in c["pts"]:
                pygame.draw.circle(surf, line_col, (int(p[0]), int(p[1])), 4)
            dx, dy = self._point_on_path(c)
            pygame.draw.circle(surf, accent, (int(dx), int(dy)), 5)
        for g in self.glyphs:
            sx = g["x"] + math.sin(self.t + g["phase"]) * g["sway"]
            surf.blit(g["sprite"], (int(sx), int(g["y"])))
        for g in self.gates:
            sx = g["x"] + math.sin(self.t * 0.7 + g["phase"]) * 14
            surf.blit(g["sprite"], (int(sx), int(g["y"])))


# =========================================================================
#  MASKOT "RUSHY"
# =========================================================================
def draw_mascot(surf, cx, base_y, s, mood="normal", t=0.0):
    """Robot pelajar bertopi toga. mood: normal, happy, sad, think, fire, dead."""
    bob = math.sin(t * 3.0) * 4 * s
    cy = base_y + bob
    dead = mood == "dead"
    body_c = (135, 145, 158) if dead else (70, 185, 255)
    body_d = (92, 100, 112) if dead else (35, 120, 210)
    accent = (255, 205, 70)

    sh_w, sh_h = int(120 * s), max(4, int(20 * s))
    sh = pygame.Surface((sh_w, sh_h), pygame.SRCALPHA)
    pygame.draw.ellipse(sh, (0, 0, 0, 70), sh.get_rect())
    surf.blit(sh, (int(cx - sh_w / 2), int(base_y + 96 * s)))

    for dx in (-24, 6):
        pygame.draw.rect(surf, body_d, R(cx + dx * s, cy + 66 * s, 18 * s, 26 * s), border_radius=int(6 * s))
        pygame.draw.ellipse(surf, NAVY, R(cx + (dx - 3) * s, cy + 86 * s, 24 * s, 12 * s))

    wave = math.sin(t * 8) * 10
    sl, sr = (cx - 34 * s, cy + 22 * s), (cx + 34 * s, cy + 22 * s)
    if mood == "happy":
        hl, hr = (cx - 62 * s, cy + 34 * s), (cx + 62 * s, cy - 12 * s + wave * s)
    elif mood == "fire":
        hl, hr = (cx - 60 * s, cy - 8 * s + wave * s * 0.5), (cx + 60 * s, cy - 8 * s - wave * s * 0.5)
    elif mood in ("sad", "dead"):
        hl, hr = (cx - 46 * s, cy + 62 * s), (cx + 46 * s, cy + 62 * s)
    elif mood == "think":
        hl, hr = (cx - 56 * s, cy + 50 * s), (cx + 22 * s, cy + 2 * s)
    else:
        hl, hr = (cx - 58 * s, cy + 48 * s), (cx + 58 * s, cy + 48 * s)
    for shp, hnd in ((sl, hl), (sr, hr)):
        pygame.draw.line(surf, body_d, (int(shp[0]), int(shp[1])), (int(hnd[0]), int(hnd[1])), max(2, int(12 * s)))
        pygame.draw.circle(surf, (240, 245, 255), (int(hnd[0]), int(hnd[1])), max(2, int(9 * s)))

    pygame.draw.rect(surf, body_c, R(cx - 36 * s, cy + 8 * s, 72 * s, 64 * s), border_radius=int(18 * s))
    pygame.draw.rect(surf, body_d, R(cx - 36 * s, cy + 8 * s, 72 * s, 64 * s), width=max(1, int(3 * s)),
                     border_radius=int(18 * s))
    glow = 0.5 + 0.5 * math.sin(t * 4)
    chest = (255, int(120 + 100 * glow), 80) if mood == "fire" else (120, int(200 + 50 * glow), 160)
    if dead:
        chest = (80, 80, 90)
    pygame.draw.circle(surf, chest, (int(cx), int(cy + 40 * s)), max(2, int(10 * s)))
    pygame.draw.circle(surf, WHITE, (int(cx), int(cy + 40 * s)), max(2, int(10 * s)), 2)

    head = R(0, 0, 100 * s, 78 * s)
    head.center = (int(cx), int(cy - 30 * s))
    for sx in (-1, 1):
        pygame.draw.circle(surf, body_d, (int(cx + sx * 52 * s), int(cy - 30 * s)), max(2, int(8 * s)))
    pygame.draw.rect(surf, body_c, head, border_radius=int(24 * s))
    pygame.draw.rect(surf, body_d, head, width=max(1, int(3 * s)), border_radius=int(24 * s))
    face = R(0, 0, 78 * s, 54 * s)
    face.center = (int(cx), int(cy - 28 * s))
    pygame.draw.rect(surf, NAVY, face, border_radius=int(16 * s))

    eye_y = cy - 38 * s
    ex = (cx - 17 * s, cx + 17 * s)
    eye_c = (120, 255, 200)
    blink = (t % 3.4) < 0.12
    if dead:
        for x in ex:
            r = 6 * s
            pygame.draw.line(surf, (255, 110, 110), (x - r, eye_y - r), (x + r, eye_y + r), max(2, int(3 * s)))
            pygame.draw.line(surf, (255, 110, 110), (x - r, eye_y + r), (x + r, eye_y - r), max(2, int(3 * s)))
    elif blink:
        for x in ex:
            pygame.draw.line(surf, eye_c, (x - 7 * s, eye_y), (x + 7 * s, eye_y), max(2, int(3 * s)))
    elif mood == "fire":
        for x in ex:
            pygame.draw.polygon(surf, (255, 225, 90), star_points(x, eye_y, 9 * s, 5, 0.45))
    elif mood == "sad":
        for x in ex:
            pygame.draw.circle(surf, eye_c, (int(x), int(eye_y + 2 * s)), max(2, int(6 * s)))
        pygame.draw.line(surf, eye_c, (ex[0] - 9 * s, eye_y - 9 * s), (ex[0] + 6 * s, eye_y - 5 * s), max(2, int(3 * s)))
        pygame.draw.line(surf, eye_c, (ex[1] + 9 * s, eye_y - 9 * s), (ex[1] - 6 * s, eye_y - 5 * s), max(2, int(3 * s)))
        ty = eye_y + 10 * s + ((t * 25) % 14) * s
        pygame.draw.circle(surf, (130, 205, 255), (int(ex[0] - 4 * s), int(ty)), max(2, int(3 * s)))
    elif mood == "think":
        pygame.draw.circle(surf, eye_c, (int(ex[0]), int(eye_y)), max(2, int(6 * s)))
        pygame.draw.circle(surf, eye_c, (int(ex[1]), int(eye_y)), max(2, int(9 * s)))
        pygame.draw.circle(surf, NAVY, (int(ex[1] + 2 * s), int(eye_y - 2 * s)), max(1, int(3 * s)))
    else:
        for x in ex:
            pygame.draw.circle(surf, eye_c, (int(x), int(eye_y)), max(2, int(7 * s)))
            pygame.draw.circle(surf, WHITE, (int(x - 2 * s), int(eye_y - 2 * s)), max(1, int(2.5 * s)))

    my = cy - 19 * s
    lw = max(2, int(3 * s))
    if mood in ("normal", "happy"):
        pygame.draw.arc(surf, eye_c, R(cx - 13 * s, my - 10 * s, 26 * s, 18 * s), math.pi * 1.1, math.pi * 1.9, lw)
        if mood == "happy":
            for sx in (-1, 1):
                pygame.draw.circle(surf, (255, 140, 170), (int(cx + sx * 30 * s), int(my - 6 * s)), max(2, int(5 * s)))
    elif mood == "fire":
        pygame.draw.ellipse(surf, (255, 120, 100), R(cx - 12 * s, my - 8 * s, 24 * s, 15 * s))
    elif mood == "sad":
        pygame.draw.arc(surf, eye_c, R(cx - 10 * s, my - 2 * s, 20 * s, 14 * s), math.pi * 0.1, math.pi * 0.9, lw)
    elif mood == "think":
        pygame.draw.line(surf, eye_c, (cx - 8 * s, my), (cx + 8 * s, my - 2 * s), lw)
    else:
        pts = [(cx + (i - 3) * 5 * s, my + (3 * s if i % 2 else -3 * s)) for i in range(7)]
        pygame.draw.lines(surf, (255, 110, 110), False, pts, lw)

    top_y = cy - 30 * s - 39 * s
    pygame.draw.rect(surf, NAVY, R(cx - 28 * s, top_y + 4 * s, 56 * s, 14 * s), border_radius=int(4 * s))
    cap = [(cx - 58 * s, top_y + 2 * s), (cx, top_y - 16 * s), (cx + 58 * s, top_y + 2 * s), (cx, top_y + 14 * s)]
    pygame.draw.polygon(surf, (45, 60, 125), cap)
    pygame.draw.polygon(surf, NAVY, cap, max(1, int(2 * s)))
    tx = cx + 42 * s
    pygame.draw.line(surf, accent, (tx, top_y + 2 * s), (tx + 8 * s, top_y + 24 * s), max(1, int(2 * s)))
    pygame.draw.circle(surf, accent, (int(tx + 8 * s), int(top_y + 25 * s)), max(2, int(4 * s)))

    if mood == "fire":
        draw_flame(surf, cx, top_y - 26 * s, 16 * s, t)
    if mood == "think":
        draw_text(surf, "?", int(40 * s), accent, (cx + 62 * s, cy - 92 * s + math.sin(t * 4) * 4), "center", True)


def draw_bubble(surf, rect, text, size=20, tail="left"):
    rect = pygame.Rect(rect)
    draw_panel(surf, rect.move(3, 5), (0, 0, 0, 60), 18)
    pygame.draw.rect(surf, WHITE, rect, border_radius=18)
    pygame.draw.rect(surf, (40, 50, 110), rect, width=3, border_radius=18)
    if tail == "left":
        pts = [(rect.x + 2, rect.centery - 12), (rect.x - 24, rect.centery + 10), (rect.x + 2, rect.centery + 14)]
        pygame.draw.polygon(surf, WHITE, pts)
        pygame.draw.lines(surf, (40, 50, 110), False, pts, 3)
        pygame.draw.line(surf, WHITE, (rect.x + 1, rect.centery - 11), (rect.x + 1, rect.centery + 13), 4)
    elif tail == "bottom":
        pts = [(rect.centerx - 14, rect.bottom - 2), (rect.centerx - 6, rect.bottom + 22), (rect.centerx + 10, rect.bottom - 2)]
        pygame.draw.polygon(surf, WHITE, pts)
        pygame.draw.lines(surf, (40, 50, 110), False, pts, 3)
        pygame.draw.line(surf, WHITE, (rect.centerx - 13, rect.bottom - 1), (rect.centerx + 9, rect.bottom - 1), 4)
    font = get_font(size)
    lines = wrap_text(text, font, rect.w - 30)
    total = len(lines) * (size + 4)
    y = rect.centery - total / 2
    for ln in lines:
        draw_text(surf, ln, size, (30, 35, 80), (rect.centerx, y), "midtop")
        y += size + 4


# =========================================================================
#  TOMBOL
# =========================================================================
class Button:
    def __init__(self, name, rect, text, color=(50, 120, 230), size=26):
        self.name = name
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.size = size
        self.hover = 0.0

    def update(self, mouse, dt):
        target = 1.0 if self.rect.collidepoint(mouse) else 0.0
        self.hover += (target - self.hover) * min(1.0, dt * 14)

    def hit(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surf):
        hv = self.hover
        col = lerp_color(self.color, WHITE, 0.2 * hv)
        dark = lerp_color(self.color, BLACK, 0.45)
        r = self.rect.copy()
        r.y -= int(4 * hv)
        if hv > 0.5 and pygame.mouse.get_pressed()[0]:
            r.y += 5
        pygame.draw.rect(surf, dark, r.move(0, 6), border_radius=16)
        pygame.draw.rect(surf, col, r, border_radius=16)
        pygame.draw.rect(surf, lerp_color(col, WHITE, 0.45), R(r.x + 6, r.y + 3, r.w - 12, 4), border_radius=3)
        pygame.draw.rect(surf, lerp_color(col, BLACK, 0.3), r, width=2, border_radius=16)
        draw_text(surf, self.text, self.size, WHITE, r.center, "center", True, shadow=(0, 0, 0))


# =========================================================================
#  HINT ORB (bintang rahasia)
# =========================================================================
class HintOrb:
    def __init__(self):
        self.x0 = random.randint(40, W - 40)
        self.y0 = random.randint(95, H - 30)
        self.t = random.uniform(0, 10)
        self.found = False

    @property
    def pos(self):
        return (self.x0 + math.sin(self.t * 0.9) * 9, self.y0 + math.cos(self.t * 0.7) * 7)

    def update(self, dt):
        self.t += dt

    def hit(self, p):
        x, y = self.pos
        return (p[0] - x) ** 2 + (p[1] - y) ** 2 <= 20 ** 2

    def draw(self, surf, mouse):
        if self.found:
            return
        x, y = self.pos
        dist = math.hypot(mouse[0] - x, mouse[1] - y)
        near = clamp(1.0 - dist / 140.0, 0.0, 1.0)
        twinkle = 0.5 + 0.5 * math.sin(self.t * 5)
        size = 5 + 2 * twinkle + 9 * near
        layer = pygame.Surface((90, 90), pygame.SRCALPHA)
        if near > 0:
            pygame.draw.circle(layer, (255, 230, 120, int(35 + 110 * near)), (45, 45), int(14 + 26 * near))
        a = int(90 + 70 * twinkle + 90 * near)
        pts = star_points(45, 45, size * 1.6, 4, 0.28)
        pygame.draw.polygon(layer, (255, 245, 170, min(255, a)), pts)
        pygame.draw.circle(layer, (255, 255, 255, min(255, a)), (45, 45), max(1, int(size * 0.35)))
        surf.blit(layer, (int(x - 45), int(y - 45)))


# =========================================================================
#  GAME UTAMA
# =========================================================================
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("StudyRush - Kuis Informatika SMK Kelas 10")
        self.screen = pygame.display.set_mode((W, H))
        self.canvas = pygame.Surface((W, H))
        self.clock = pygame.time.Clock()
        self.sound = SoundManager()
        self.data = load_data()
        self.bg = Background(HOME_THEME)
        self.particles = ParticleSystem()
        self.floaters = []
        self.sched = []
        self.buttons = []
        self.pause_buttons = []
        self.time = 0.0
        self.state_time = 0.0
        self.mouse = (0, 0)
        self.running = True
        self.state = "start"
        self.pending = None
        self.fade = 255.0
        self.fade_dir = -1
        self.shake = 0.0
        self.flash = 0.0
        self.paused = False
        self.input_error = 0.0
        self.player_name = ""
        self.name_input = self.data.get("last_name", "")
        self.vignette = self._make_vignette((255, 110, 20))
        self.sound_rect = R(W - 56, 12, 40, 40)
        self.pause_rect = R(W - 104, 12, 40, 40)
        self.option_rects = [R(40, 300, 500, 92), R(560, 300, 500, 92),
                             R(40, 404, 500, 92), R(560, 404, 500, 92)]
        self.reset_run()
        self.on_enter("start")

    # ------------------------------------------------------------------
    @staticmethod
    def _make_vignette(color):
        s = pygame.Surface((W, H), pygame.SRCALPHA)
        for i in range(55):
            a = int(120 * (1 - i / 55.0) ** 2)
            pygame.draw.rect(s, (color[0], color[1], color[2], a), (i, i, W - 2 * i, H - 2 * i), width=1)
        return s

    def reset_run(self):
        self.level_idx = 0
        self.lives = MAX_LIVES
        self.score = 0
        self.disp_score = 0.0
        self.streak = 0
        self.best_streak = 0
        self.total_correct = 0
        self.total_answered = 0
        self.hints_used = 0
        self.saved = False
        self.q_list = []
        self.q_idx = 0
        self.level_correct = 0
        self.level_score_start = 0
        self.level_bonus = 0
        self.life_bonus = False
        self.level_gain = 0
        self.cur = None
        self.phase = "ask"
        self.selected = -2
        self.timer = 0.0
        self.time_limit = 30.0
        self.orb = HintOrb()
        self.hint_found = False
        self.mood = "normal"
        self.speech = ""
        self.banner = None
        self.heart_anim = None
        self.dying = False
        self.dying_t = 0.0
        self.paused = False

    # ------------------------------------------------------------------
    #  Utilitas umum
    # ------------------------------------------------------------------
    def after(self, delay, func):
        self.sched.append([delay, func])

    def update_sched(self, dt):
        remaining, due = [], []
        for item in self.sched:
            item[0] -= dt
            (due if item[0] <= 0 else remaining).append(item)
        self.sched = remaining
        for item in due:
            item[1]()

    def add_floater(self, text, pos, color=GOLD, size=36, vy=-70, life=1.3):
        self.floaters.append({"text": text, "x": pos[0], "y": pos[1], "vy": vy,
                              "life": life, "max": life, "color": color, "size": size})

    def goto(self, state):
        self.sched = []
        self.pending = state
        self.fade_dir = 1

    def make_buttons(self, specs, x, y, w=340, h=56, gap=66, size=26):
        self.buttons = []
        for i, (name, text, color) in enumerate(specs):
            self.buttons.append(Button(name, (x, y + i * gap, w, h), text, color, size))

    def multiplier(self, streak=None):
        s = self.streak if streak is None else streak
        return min(5, 1 + s // 3)

    # ------------------------------------------------------------------
    #  Perpindahan state
    # ------------------------------------------------------------------
    def on_enter(self, state):
        self.state = state
        self.state_time = 0.0
        self.paused = False
        self.buttons = []
        self.particles.items = []
        self.floaters = []
        if state == "start":
            self.bg.set_theme(HOME_THEME)
            self.sound.play_music("start")
            self.make_buttons([("start_go", "MULAI PETUALANGAN", (40, 170, 100))], 110, 420, 500, 62, 66, 26)
        elif state == "home":
            self.bg.set_theme(HOME_THEME)
            self.sound.play_music("start")
            self.make_buttons([
                ("play", "MULAI GAME", (40, 170, 100)),
                ("howto", "CARA BERMAIN", (50, 120, 230)),
                ("scores", "PAPAN SKOR", (130, 80, 220)),
                ("rename", "GANTI NAMA", (240, 140, 40)),
                ("quit", "KELUAR", (210, 65, 80)),
            ], 110, 262, 340, 54, 64, 24)
        elif state in ("howto", "scores"):
            self.bg.set_theme(HOME_THEME)
            self.sound.play_music("start")
            self.make_buttons([("back", "KEMBALI", (50, 120, 230))], 400, 610, 300, 54, 66, 24)
        elif state == "intro":
            self.prepare_level()
            self.sound.play_music("main")
            self.make_buttons([("begin", "MULAI LEVEL %d" % (self.level_idx + 1), (40, 170, 100))],
                              385, 560, 330, 62, 66, 28)
        elif state == "quiz":
            self.sound.play_music("main")
            self.load_question()
        elif state == "complete":
            self.sound.play_music("main")
            self.make_buttons([("next", "LANJUT KE LEVEL %d" % (self.level_idx + 2), (40, 170, 100))],
                              355, 575, 390, 62, 66, 26)
            for i in range(6):
                self.after(i * 0.28, lambda: self.particles.confetti(random.randint(150, W - 150), 420, 36))
        elif state == "gameover":
            self.bg.set_theme(OVER_THEME)
            self.make_buttons([
                ("retry", "ULANGI DARI LEVEL 1", (40, 170, 100)),
                ("home", "KE BERANDA", (50, 120, 230)),
            ], 640, 450, 380, 60, 72, 26)
        elif state == "victory":
            self.bg.set_theme(WIN_THEME)
            self.sound.play_music("main")
            self.make_buttons([
                ("retry", "MAIN LAGI", (40, 170, 100)),
                ("home", "KE BERANDA", (50, 120, 230)),
            ], 640, 470, 380, 60, 72, 26)
            for i in range(10):
                self.after(i * 0.35, lambda: self.particles.confetti(random.randint(100, W - 100), 500, 40))

    # ------------------------------------------------------------------
    #  Logika permainan
    # ------------------------------------------------------------------
    def start_run(self):
        self.reset_run()
        self.goto("intro")

    def prepare_level(self):
        lvl = LEVELS[self.level_idx]
        qs = list(lvl["questions"])
        random.shuffle(qs)
        self.q_list = []
        for text, correct, w1, w2, w3, hint in qs:
            opts = [correct, w1, w2, w3]
            random.shuffle(opts)
            self.q_list.append({"text": text, "options": opts, "correct": opts.index(correct), "hint": hint})
        self.q_idx = 0
        self.level_correct = 0
        self.level_score_start = self.score
        self.time_limit = max(16.0, 30.0 - self.level_idx * 1.5)
        self.bg.set_theme(THEMES[self.level_idx])
        self.mood = "normal"
        self.speech = "Level %d: %s. Siap?" % (self.level_idx + 1, lvl["topic"])

    def load_question(self):
        self.cur = self.q_list[self.q_idx]
        self.phase = "ask"
        self.selected = -2
        self.timer = self.time_limit
        self.hint_found = False
        self.orb = HintOrb()
        self.mood = "fire" if self.streak >= 3 else "normal"
        self.speech = random.choice(ASK_LINES).format(n=self.player_name or "Kawan")

    def reveal_hint(self):
        self.hint_found = True
        self.orb.found = True
        self.hints_used += 1
        x, y = self.orb.pos
        self.particles.sparkle(x, y, 26)
        self.add_floater("HINT DITEMUKAN! (poin x0.7)", (W // 2, 260), GOLD, 26, -20, 1.8)
        self.mood = "think"
        self.speech = "Bintang hint ketemu! Baca petunjuknya."

    def answer(self, idx):
        if self.phase != "ask":
            return
        self.phase = "feedback"
        self.selected = idx
        self.total_answered += 1
        if idx == self.cur["correct"]:
            self.on_correct()
        else:
            self.on_wrong(timeout=(idx == -1))

    def on_correct(self):
        prev_mult = self.multiplier()
        self.streak += 1
        self.best_streak = max(self.best_streak, self.streak)
        mult = self.multiplier()
        base = 100 + self.level_idx * 10
        bonus = int(max(0.0, self.timer) * 4)
        gain = (base + bonus) * mult
        if self.hint_found:
            gain = int(gain * 0.7)
        self.score += gain
        self.level_correct += 1
        self.total_correct += 1
        self.sound.play("benar")
        cx, cy = self.option_rects[self.selected].center
        self.particles.confetti(cx, cy, 34)
        self.add_floater("+%d" % gain, (cx, cy - 10), GOLD, 44)
        if mult > 1:
            self.add_floater("x%d STREAK!" % mult, (cx, cy + 34), (255, 150, 60), 28, -50, 1.2)
        if mult > prev_mult:
            self.banner = {"text": "STREAK RUSH x%d!" % mult, "t": 0.0}
        self.mood = "fire" if self.streak >= 3 else "happy"
        self.speech = random.choice(STREAK_LINES if self.streak >= 3 else CORRECT_LINES)
        self.after(1.4, self.next_question)

    def on_wrong(self, timeout=False):
        broke = self.streak >= 3
        self.streak = 0
        self.sound.play("salah")
        self.shake = 14.0
        self.mood = "sad"
        self.speech = "Waktu habis!" if timeout else random.choice(WRONG_LINES)
        if broke:
            self.add_floater("Streak putus!", (W // 2, 520), (255, 130, 90), 30, -30, 1.5)
        self.after(0.75, self.lose_life)

    def lose_life(self):
        self.lives -= 1
        self.heart_anim = {"idx": self.lives, "t": 0.0}
        self.sound.play("nyawa")
        self.shake = max(self.shake, 9.0)
        self.flash = 0.7
        self.add_floater("-1 NYAWA", (W - 230, 90), RED, 30, 40, 1.4)
        if self.lives <= 0:
            self.mood = "dead"
            self.speech = "Nyawamu habis..."
            self.after(1.0, self.death_sound)
            self.after(3.6, lambda: self.goto("gameover"))
        else:
            self.after(1.8, self.next_question)

    def death_sound(self):
        self.dying = True
        self.dying_t = 0.0
        self.sound.stop_music()
        self.sound.play("mati")
        self.save_score()

    def next_question(self):
        self.q_idx += 1
        if self.q_idx >= QUESTIONS_PER_LEVEL:
            self.finish_level()
        else:
            self.load_question()

    def finish_level(self):
        self.level_bonus = 500 if self.level_correct == QUESTIONS_PER_LEVEL else 0
        self.score += self.level_bonus
        self.life_bonus = False
        if self.level_idx < TOTAL_LEVELS - 1 and self.lives < MAX_LIVES:
            self.lives += 1
            self.life_bonus = True
        self.level_gain = self.score - self.level_score_start
        if self.level_idx >= TOTAL_LEVELS - 1:
            self.save_score()
            self.goto("victory")
        else:
            self.goto("complete")

    def save_score(self):
        if self.saved:
            return
        self.saved = True
        entry = {
            "name": self.player_name or "Pemain",
            "score": int(self.score),
            "level": self.level_idx + 1,
            "correct": self.total_correct,
            "date": datetime.date.today().strftime("%d/%m/%Y"),
        }
        self.data["scores"].append(entry)
        self.data["scores"].sort(key=lambda e: e.get("score", 0), reverse=True)
        self.data["scores"] = self.data["scores"][:20]
        save_data(self.data)

    def best_score(self):
        return max([e.get("score", 0) for e in self.data["scores"]] + [0])

    def submit_name(self):
        name = self.name_input.strip()
        if not name:
            self.input_error = 1.6
            self.shake = 8.0
            return
        self.player_name = name
        self.data["last_name"] = name
        save_data(self.data)
        self.goto("home")

    # ------------------------------------------------------------------
    #  Input
    # ------------------------------------------------------------------
    def handle_event(self, e):
        if e.type == pygame.QUIT:
            self.running = False
            return
        if self.fade_dir != 0:
            return
        if e.type == pygame.KEYDOWN:
            if self.state == "start":
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    self.submit_name()
                elif e.key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                elif e.key == pygame.K_ESCAPE and self.player_name:
                    self.goto("home")
                elif e.unicode and e.unicode.isprintable() and len(self.name_input) < 14:
                    self.name_input += e.unicode
                return
            if e.key == pygame.K_m:
                self.sound.toggle_mute()
            if self.state == "quiz":
                if e.key in (pygame.K_p, pygame.K_ESCAPE):
                    self.toggle_pause()
                elif not self.paused and self.phase == "ask":
                    keys = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3,
                            pygame.K_a: 0, pygame.K_b: 1, pygame.K_c: 2, pygame.K_d: 3}
                    if e.key in keys:
                        self.answer(keys[e.key])
            elif e.key == pygame.K_RETURN:
                for b in self.buttons:
                    if b.name in ("begin", "next"):
                        self.on_button(b.name)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.handle_click(e.pos)

    def toggle_pause(self):
        if self.dying or self.cur is None:
            return
        self.paused = not self.paused
        if self.paused:
            self.sound.pause_music()
            self.pause_buttons = [
                Button("resume", (400, 290, 300, 58), "LANJUTKAN", (40, 170, 100), 26),
                Button("tohome", (400, 366, 300, 58), "KE BERANDA", (210, 65, 80), 26),
            ]
        else:
            self.sound.resume_music()

    def handle_click(self, pos):
        if self.sound_rect.collidepoint(pos):
            self.sound.toggle_mute()
            return
        if self.state == "quiz":
            if self.paused:
                for b in self.pause_buttons:
                    if b.hit(pos):
                        if b.name == "resume":
                            self.toggle_pause()
                        else:
                            self.paused = False
                            self.sound.resume_music()
                            self.sound.stop_music()
                            self.goto("home")
                        return
                return
            if self.pause_rect.collidepoint(pos):
                self.toggle_pause()
                return
            if self.phase == "ask":
                if not self.hint_found and self.orb.hit(pos):
                    self.reveal_hint()
                    return
                for i, r in enumerate(self.option_rects):
                    if r.collidepoint(pos):
                        self.answer(i)
                        return
            return
        for b in self.buttons:
            if b.hit(pos):
                self.on_button(b.name)
                return

    def on_button(self, name):
        if name == "start_go":
            self.submit_name()
        elif name == "play":
            self.start_run()
        elif name == "howto":
            self.goto("howto")
        elif name == "scores":
            self.goto("scores")
        elif name == "rename":
            self.name_input = self.player_name
            self.goto("start")
        elif name == "quit":
            self.running = False
        elif name == "back":
            self.goto("home")
        elif name == "begin":
            self.goto("quiz")
        elif name == "next":
            self.level_idx += 1
            self.goto("intro")
        elif name == "retry":
            self.start_run()
        elif name == "home":
            self.sound.stop_music()
            self.goto("home")

    # ------------------------------------------------------------------
    #  Update
    # ------------------------------------------------------------------
    def update(self, dt):
        self.state_time += dt
        self.bg.update(dt)
        self.particles.update(dt)
        for b in self.buttons:
            b.update(self.mouse, dt)
        for b in self.pause_buttons:
            b.update(self.mouse, dt)
        for f in self.floaters:
            f["y"] += f["vy"] * dt
            f["life"] -= dt
        self.floaters = [f for f in self.floaters if f["life"] > 0]
        self.input_error = max(0.0, self.input_error - dt)
        self.shake = max(0.0, self.shake - dt * 30)
        self.flash = max(0.0, self.flash - dt * 1.6)

        if self.fade_dir == 1:
            self.fade += 900 * dt
            if self.fade >= 255:
                self.fade = 255
                self.fade_dir = -1
                new_state, self.pending = self.pending, None
                self.on_enter(new_state)
        elif self.fade_dir == -1:
            self.fade -= 900 * dt
            if self.fade <= 0:
                self.fade = 0
                self.fade_dir = 0

        if not self.paused:
            self.update_sched(dt)
        if self.state == "quiz":
            self.update_quiz(dt)

    def update_quiz(self, dt):
        if self.paused or self.cur is None:
            return
        self.orb.update(dt)
        self.disp_score += (self.score - self.disp_score) * min(1.0, dt * 6)
        if abs(self.score - self.disp_score) < 1:
            self.disp_score = float(self.score)
        if self.heart_anim:
            self.heart_anim["t"] += dt / 1.1
            if self.heart_anim["t"] >= 1.0:
                self.heart_anim = None
        if self.phase == "ask":
            self.timer -= dt
            if self.timer <= 0:
                self.timer = 0
                self.answer(-1)
        if self.streak >= 3 and random.random() < 0.6:
            self.particles.flame(random.choice((random.randint(0, 90), random.randint(W - 90, W))), H - 4)
        if self.banner:
            self.banner["t"] += dt
            if self.banner["t"] > 1.6:
                self.banner = None
        if self.dying:
            self.dying_t += dt

    # ------------------------------------------------------------------
    #  Gambar: elemen umum
    # ------------------------------------------------------------------
    def draw_wavy_title(self, surf, text, cx, cy, size):
        font = get_font(size, True)
        widths = [font.size(ch)[0] for ch in text]
        x = cx - sum(widths) / 2.0
        for i, ch in enumerate(text):
            dy = math.sin(self.time * 3 + i * 0.6) * 8
            col = rainbow(self.time * 0.3 + i * 0.09)
            sh = font.render(ch, True, (10, 10, 45))
            img = font.render(ch, True, col)
            surf.blit(sh, (x + 4, cy - img.get_height() / 2 + dy + 5))
            surf.blit(img, (x, cy - img.get_height() / 2 + dy))
            x += widths[i]

    def draw_sound_icon(self, surf):
        r = self.sound_rect
        hv = r.collidepoint(self.mouse)
        pygame.draw.circle(surf, (255, 255, 255, 255) if hv else (225, 230, 245), r.center, 20)
        pygame.draw.circle(surf, NAVY, r.center, 20, 2)
        x, y = r.x, r.y
        pts = [(x + 10, y + 16), (x + 16, y + 16), (x + 23, y + 10), (x + 23, y + 30), (x + 16, y + 24), (x + 10, y + 24)]
        pygame.draw.polygon(surf, NAVY, pts)
        if self.sound.muted or not self.sound.enabled:
            pygame.draw.line(surf, RED, (x + 26, y + 14), (x + 34, y + 26), 3)
            pygame.draw.line(surf, RED, (x + 34, y + 14), (x + 26, y + 26), 3)
        else:
            pygame.draw.arc(surf, NAVY, R(x + 18, y + 12, 12, 16), -1.0, 1.0, 3)
            pygame.draw.arc(surf, NAVY, R(x + 21, y + 8, 14, 24), -1.0, 1.0, 3)

    def draw_pause_icon(self, surf):
        r = self.pause_rect
        hv = r.collidepoint(self.mouse)
        pygame.draw.circle(surf, (255, 255, 255) if hv else (225, 230, 245), r.center, 20)
        pygame.draw.circle(surf, NAVY, r.center, 20, 2)
        pygame.draw.rect(surf, NAVY, R(r.x + 12, r.y + 11, 6, 18), border_radius=2)
        pygame.draw.rect(surf, NAVY, R(r.x + 22, r.y + 11, 6, 18), border_radius=2)

    def draw_level_map(self, surf, cx, y, current, width=760):
        xs = [cx - width / 2 + i * width / (TOTAL_LEVELS - 1) for i in range(TOTAL_LEVELS)]
        for i in range(TOTAL_LEVELS - 1):
            col = GREEN if i < current else (90, 100, 150)
            pygame.draw.line(surf, col, (xs[i], y), (xs[i + 1], y), 6)
        for i, x in enumerate(xs):
            if i < current:
                pygame.draw.circle(surf, GREEN, (int(x), y), 20)
            elif i == current:
                pulse = 4 * math.sin(self.time * 6)
                pygame.draw.circle(surf, (255, 230, 120), (int(x), y), int(30 + pulse), 3)
                pygame.draw.circle(surf, GOLD, (int(x), y), 22)
            else:
                pygame.draw.circle(surf, (70, 80, 130), (int(x), y), 20)
            pygame.draw.circle(surf, WHITE, (int(x), y), 20, 2)
            draw_text(surf, str(i + 1), 20, NAVY if i == current else WHITE, (x, y), "center", True)

    def draw_stat(self, surf, label, value, x, y, color=WHITE, w=320):
        draw_text(surf, label, 22, (200, 210, 245), (x, y))
        draw_text(surf, str(value), 26, color, (x + w, y - 2), "topright", True)

    # ------------------------------------------------------------------
    #  Gambar: tiap state
    # ------------------------------------------------------------------
    def draw_start(self, s):
        self.draw_wavy_title(s, "StudyRush", 360, 120, 86)
        draw_text(s, "Kuis Informatika SMK Kelas 10", 28, WHITE, (360, 190), "center", True, shadow=(0, 0, 40))
        draw_panel(s, (80, 240, 560, 320), (10, 15, 50, 175), 24, (140, 180, 255, 200))
        draw_text(s, "Siapa namamu, Pejuang Informatika?", 26, WHITE, (110, 262), "topleft", True)
        box = R(110, 310, 500, 62)
        shake = math.sin(self.time * 60) * 6 if self.input_error > 0 else 0
        box.x += int(shake)
        pygame.draw.rect(s, (250, 250, 255), box, border_radius=14)
        pygame.draw.rect(s, RED if self.input_error > 0 else (80, 140, 255), box, width=4, border_radius=14)
        if self.name_input:
            rt = draw_text(s, self.name_input, 34, NAVY, (box.x + 18, box.centery), "midleft", True)
            caret_x = rt.right + 4
        else:
            draw_text(s, "Ketik namamu di sini...", 28, (150, 155, 180), (box.x + 18, box.centery), "midleft")
            caret_x = box.x + 18
        if int(self.time * 2) % 2 == 0:
            pygame.draw.line(s, NAVY, (caret_x, box.y + 14), (caret_x, box.bottom - 14), 3)
        if self.input_error > 0:
            draw_text(s, "Nama tidak boleh kosong ya!", 20, (255, 140, 150), (110, 380))
        draw_text(s, "Tekan ENTER atau klik tombol untuk mulai", 18, (210, 220, 255), (110, 500))
        draw_text(s, "Maksimal 14 karakter", 16, (170, 185, 235), (110, 526))
        draw_mascot(s, 850, 440, 1.7, "happy", self.time)
        draw_bubble(s, (730, 150, 300, 80), "Halo! Aku Rushy. Siapa namamu?", 20, "bottom")
        draw_text(s, "Gerbang Logika  |  Office  |  Proposisi  |  Sejarah AI  |  Hardware & Software",
                  18, (220, 230, 255), (W // 2, H - 26), "center")

    def draw_home(self, s):
        self.draw_wavy_title(s, "StudyRush", 370, 100, 80)
        draw_text(s, "Kuis Informatika SMK Kelas 10", 26, WHITE, (370, 158), "center", True, shadow=(0, 0, 40))
        draw_text(s, "Halo, %s!" % self.player_name, 30, GOLD, (110, 196), "topleft", True, shadow=(0, 0, 0))
        draw_text(s, "Skor tertinggi: %d" % self.best_score(), 20, (220, 230, 255), (110, 232))
        for b in self.buttons:
            b.draw(s)
        draw_mascot(s, 850, 450, 1.7, "happy", self.time)
        draw_bubble(s, (700, 160, 340, 80), "Siap menaklukkan 10 level StudyRush?", 21, "bottom")
        draw_text(s, "10 Level  -  100 Soal  -  5 Nyawa  -  Streak Rush  -  Hint Rahasia", 18,
                  (220, 230, 255), (W // 2, H - 24), "center")

    def draw_howto(self, s):
        draw_text(s, "CARA BERMAIN", 46, GOLD, (W // 2, 62), "center", True, shadow=(0, 0, 0))
        draw_panel(s, (70, 110, 960, 480), (10, 15, 50, 195), 24, (140, 180, 255, 200))
        y = 132
        font = get_font(20)
        for title, text in HOWTO_LINES:
            lines = wrap_text(text, font, 700)
            draw_text(s, title, 24, rainbow(0.08 * len(title)), (100, y), "topleft", True)
            ly = y + 2
            for ln in lines:
                draw_text(s, ln, 20, WHITE, (290, ly))
                ly += 26
            y += max(len(lines) * 26, 34) + 20
        for b in self.buttons:
            b.draw(s)

    def draw_scores(self, s):
        draw_text(s, "PAPAN SKOR", 46, GOLD, (W // 2, 62), "center", True, shadow=(0, 0, 0))
        draw_panel(s, (150, 110, 800, 480), (10, 15, 50, 195), 24, (140, 180, 255, 200))
        draw_text(s, "#", 22, (180, 200, 255), (190, 130), "topleft", True)
        draw_text(s, "Nama", 22, (180, 200, 255), (250, 130), "topleft", True)
        draw_text(s, "Skor", 22, (180, 200, 255), (560, 130), "topright", True)
        draw_text(s, "Level", 22, (180, 200, 255), (660, 130), "topright", True)
        draw_text(s, "Tanggal", 22, (180, 200, 255), (900, 130), "topright", True)
        scores = self.data.get("scores", [])[:10]
        if not scores:
            draw_text(s, "Belum ada skor. Ayo main dulu!", 26, WHITE, (W // 2, 330), "center")
        for i, e in enumerate(scores):
            y = 175 + i * 40
            col = (GOLD, (220, 225, 235), (230, 160, 100))[i] if i < 3 else WHITE
            if e.get("name") == self.player_name:
                pygame.draw.rect(s, (60, 80, 160), R(165, y - 4, 770, 36), border_radius=10)
            draw_text(s, str(i + 1), 22, col, (190, y), "topleft", True)
            draw_text(s, str(e.get("name", "?"))[:14], 22, col, (250, y))
            draw_text(s, str(e.get("score", 0)), 22, col, (560, y), "topright", True)
            draw_text(s, str(e.get("level", 1)), 22, col, (660, y), "topright")
            draw_text(s, str(e.get("date", "")), 20, col, (900, y + 2), "topright")
        for b in self.buttons:
            b.draw(s)

    def draw_intro(self, s):
        lvl = LEVELS[self.level_idx]
        draw_panel(s, (170, 90, 760, 430), (8, 12, 45, 190), 26, (170, 200, 255, 220))
        draw_text(s, "LEVEL %d" % (self.level_idx + 1), 64, GOLD, (W // 2, 150), "center", True, shadow=(0, 0, 0))
        draw_text(s, lvl["title"], 36, WHITE, (W // 2, 215), "center", True)
        pill = R(W // 2 - 110, 250, 220, 34)
        pygame.draw.rect(s, THEMES[self.level_idx][2], pill, border_radius=17)
        draw_text(s, "Topik: " + lvl["topic"], 20, NAVY, pill.center, "center", True)
        lines = wrap_text(lvl["desc"], get_font(22), 560)
        for i, ln in enumerate(lines):
            draw_text(s, ln, 22, (225, 232, 255), (W // 2 + 60, 310 + i * 30), "midtop")
        info = "10 soal   |   Waktu %d detik / soal   |   Nyawa: %d" % (int(self.time_limit), self.lives)
        draw_text(s, info, 20, (200, 215, 255), (W // 2, 440), "center")
        draw_mascot(s, 290, 385, 0.9, "happy" if self.state_time > 0.3 else "normal", self.time)
        self.draw_level_map(s, W // 2, 495, self.level_idx, 700)
        for b in self.buttons:
            b.draw(s)

    def draw_hud(self, s):
        draw_panel(s, (0, 0, W, 64), (6, 10, 40, 215), 0)
        draw_text(s, self.player_name, 22, WHITE, (20, 8), "topleft", True)
        lvl = LEVELS[self.level_idx]
        draw_text(s, "Level %d/10 - %s" % (self.level_idx + 1, lvl["title"]), 17, (190, 210, 255), (20, 36))
        draw_text(s, "SKOR", 15, (160, 180, 235), (500, 6), "midtop")
        draw_text(s, "%d" % int(self.disp_score), 30, GOLD, (500, 20), "midtop", True)
        self.draw_hearts(s, W - 340, 32)
        self.draw_pause_icon(s)
        self.draw_sound_icon(s)

    def draw_hearts(self, s, x, y):
        for i in range(MAX_LIVES):
            cx = x + i * 44
            if i < self.lives:
                size = 30
                if self.lives == 1:
                    size += 3 * math.sin(self.time * 10)
                draw_heart(s, cx, y, size, (235, 50, 75), (255, 255, 255))
            elif self.heart_anim and self.heart_anim["idx"] == i:
                self.draw_broken_heart(s, cx, y, 30, self.heart_anim["t"])
            else:
                draw_heart(s, cx, y, 28, (45, 50, 85), (90, 100, 150))

    def draw_broken_heart(self, s, cx, cy, size, t):
        if t < 0.15:
            jit = random.uniform(-2, 2)
            draw_heart(s, cx + jit, cy, size + 4, (255, 90, 110), WHITE)
            return
        t = (t - 0.15) / 0.85
        dim = size + 10
        tmp = pygame.Surface((dim, dim), pygame.SRCALPHA)
        draw_heart(tmp, dim / 2.0, dim / 2.0 - 1, size, (235, 50, 75), WHITE)
        half = dim // 2
        left = tmp.subsurface((0, 0, half, dim)).copy()
        right = tmp.subsurface((half, 0, dim - half, dim)).copy()
        off, drop, ang = t * 16, t * t * 60, t * 55
        alpha = int(255 * (1 - t))
        lt = pygame.transform.rotate(left, ang)
        rt = pygame.transform.rotate(right, -ang)
        lt.set_alpha(alpha)
        rt.set_alpha(alpha)
        s.blit(lt, lt.get_rect(center=(int(cx - dim / 4 - off), int(cy + drop))))
        s.blit(rt, rt.get_rect(center=(int(cx + dim / 4 + off), int(cy + drop))))

    def draw_timer_bar(self, s):
        frac = clamp(self.timer / self.time_limit, 0.0, 1.0)
        col = lerp_color((230, 60, 60), (60, 210, 120), frac) if frac < 0.5 else lerp_color((255, 210, 60), (60, 210, 120), (frac - 0.5) * 2)
        pygame.draw.rect(s, (20, 25, 60), (0, 64, W, 9))
        pygame.draw.rect(s, col, (0, 64, int(W * frac), 9))
        if self.phase == "ask" and self.timer < 6:
            draw_text(s, str(int(math.ceil(self.timer))), 26, (255, 120, 120), (W // 2, 94), "center", True)

    def draw_question(self, s):
        panel = R(40, 84, 1020, 158)
        draw_panel(s, panel, (8, 12, 48, 205), 22, (150, 185, 255, 220))
        lvl = LEVELS[self.level_idx]
        chip = R(60, 94, 190, 28)
        pygame.draw.rect(s, THEMES[self.level_idx][2], chip, border_radius=14)
        draw_text(s, lvl["topic"].upper(), 16, NAVY, chip.center, "center", True)
        draw_text(s, "Soal %d / %d" % (self.q_idx + 1, QUESTIONS_PER_LEVEL), 18, (200, 215, 255),
                  (1040, 98), "topright", True)
        text = self.cur["text"]
        for size in (29, 26, 23, 20):
            lines = wrap_text(text, get_font(size, True), 960)
            if len(lines) * (size + 8) <= 108:
                break
        total = len(lines) * (size + 8)
        y = 130 + (108 - total) / 2
        for ln in lines:
            draw_text(s, ln, size, WHITE, (W // 2, y), "midtop", True, shadow=(0, 0, 30))
            y += size + 8

    def draw_hint_banner(self, s):
        r = R(40, 248, 1020, 44)
        if self.hint_found:
            draw_panel(s, r, (110, 80, 10, 225), 14, (255, 215, 90, 255), 2)
            draw_text(s, "HINT:", 20, GOLD, (r.x + 16, r.centery), "midleft", True)
            draw_text(s, self.cur["hint"], 20, WHITE, (r.x + 84, r.centery), "midleft")
        else:
            draw_panel(s, r, (10, 15, 45, 120), 14)
            draw_text(s, "Hint tersembunyi! Cari bintang kecil yang berkedip di layar, lalu klik.",
                      18, (190, 205, 245), r.center, "center")

    def draw_option(self, s, i, rect):
        hover = self.phase == "ask" and rect.collidepoint(self.mouse) and not self.paused
        base, light = (36, 52, 118), (60, 88, 185)
        col = light if hover else base
        border = (170, 200, 255)
        if self.phase == "feedback":
            if i == self.cur["correct"]:
                col, border = (30, 165, 95), (180, 255, 210)
            elif i == self.selected:
                col, border = (205, 55, 75), (255, 190, 200)
            else:
                col, border = (30, 36, 70), (80, 90, 130)
        r = rect.inflate(8, 8) if hover else rect.copy()
        if self.phase == "feedback" and i == self.cur["correct"]:
            pulse = int(4 + 3 * math.sin(self.time * 10))
            r = rect.inflate(pulse, pulse)
        draw_panel(s, r.move(0, 6), (0, 0, 0, 90), 18)
        pygame.draw.rect(s, col, r, border_radius=18)
        pygame.draw.rect(s, lerp_color(col, WHITE, 0.25), R(r.x + 10, r.y + 4, r.w - 20, 5), border_radius=3)
        pygame.draw.rect(s, border, r, width=3, border_radius=18)
        badge = (r.x + 40, r.centery)
        pygame.draw.circle(s, lerp_color(col, WHITE, 0.3), badge, 24)
        pygame.draw.circle(s, WHITE, badge, 24, 2)
        draw_text(s, "ABCD"[i], 26, WHITE, badge, "center", True)
        text = self.cur["options"][i]
        for size in (23, 20, 17):
            lines = wrap_text(text, get_font(size, True), r.w - 100)
            if len(lines) <= 2:
                break
        total = len(lines) * (size + 4)
        y = r.centery - total / 2
        for ln in lines:
            draw_text(s, ln, size, WHITE, (r.x + 80, y), "topleft", True)
            y += size + 4

    def draw_streak_meter(self, s):
        r = R(690, 534, 370, 124)
        glowing = self.streak >= 3
        draw_panel(s, r, (40, 15, 10, 215) if glowing else (8, 12, 48, 205), 20,
                   (255, 150, 50, 255) if glowing else (130, 160, 230, 200), 3)
        if self.streak > 0:
            draw_flame(s, r.x + 52, r.y + 62, 30 if glowing else 22, self.time)
        else:
            pygame.draw.circle(s, (70, 75, 110), (r.x + 52, r.y + 66), 20)
        draw_text(s, "STREAK RUSH", 17, (255, 200, 130) if glowing else (180, 195, 240), (r.x + 100, r.y + 10), "topleft", True)
        draw_text(s, str(self.streak), 46, WHITE, (r.x + 102, r.y + 28), "topleft", True)
        mult = self.multiplier()
        draw_text(s, "x%d" % mult, 50, GOLD if mult > 1 else (150, 160, 200), (r.right - 24, r.y + 26), "topright", True)
        bar = R(r.x + 100, r.y + 86, 250, 14)
        pygame.draw.rect(s, (25, 30, 70), bar, border_radius=7)
        prog = 1.0 if mult >= 5 else (self.streak % 3) / 3.0
        if prog > 0:
            pygame.draw.rect(s, (255, 170, 50), R(bar.x, bar.y, bar.w * prog, bar.h), border_radius=7)
        pygame.draw.rect(s, (130, 150, 220), bar, 2, border_radius=7)
        draw_text(s, "Benar beruntun = poin berlipat!", 15, (200, 212, 250), (r.x + 100, r.y + 103), "topleft")

    def draw_quiz(self, s):
        if self.cur is None:
            return
        self.draw_hud(s)
        self.draw_timer_bar(s)
        self.draw_question(s)
        self.draw_hint_banner(s)
        for i, r in enumerate(self.option_rects):
            self.draw_option(s, i, r)
        mood = self.mood
        draw_mascot(s, 130, 598, 0.82, mood, self.time)
        draw_bubble(s, (240, 538, 420, 100), self.speech, 21, "left")
        self.draw_streak_meter(s)
        if self.streak >= 3:
            self.vignette.set_alpha(int(150 + 90 * math.sin(self.time * 6)))
            s.blit(self.vignette, (0, 0))
        if self.banner:
            t = self.banner["t"]
            k = min(1.0, t * 5)
            size = int(30 + 40 * (1 - abs(1 - k * 2)) if k < 1 else 50)
            alpha = 255 if t < 1.2 else int(255 * (1 - (t - 1.2) / 0.4))
            draw_text(s, self.banner["text"], max(20, size), (255, 170, 60), (W // 2, 340), "center", True,
                      shadow=(120, 20, 0), alpha=max(0, alpha))
        self.orb.draw(s, self.mouse)
        if self.dying:
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((10, 0, 5, int(min(190, self.dying_t * 160))))
            s.blit(ov, (0, 0))
            if self.dying_t > 0.3:
                draw_text(s, "NYAWA HABIS!", 70, RED, (W // 2, 360), "center", True, shadow=(0, 0, 0))

    def draw_pause(self, s):
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 20, 190))
        s.blit(ov, (0, 0))
        draw_panel(s, (360, 190, 380, 260), (15, 20, 70, 240), 24, (170, 200, 255, 255), 3)
        draw_text(s, "JEDA", 48, GOLD, (W // 2, 238), "center", True, shadow=(0, 0, 0))
        for b in self.pause_buttons:
            b.draw(s)

    def draw_complete(self, s):
        draw_panel(s, (230, 60, 640, 500), (8, 12, 45, 205), 28, (170, 200, 255, 230), 3)
        draw_text(s, "LEVEL %d SELESAI!" % (self.level_idx + 1), 48, GOLD, (W // 2, 110), "center", True, shadow=(0, 0, 0))
        draw_text(s, LEVELS[self.level_idx]["title"], 26, WHITE, (W // 2, 158), "center", True)
        stars = 3 if self.level_correct >= 9 else (2 if self.level_correct >= 7 else 1)
        for i in range(3):
            k = clamp((self.state_time - 0.2 - i * 0.35) * 3.0, 0.0, 1.0)
            if k <= 0:
                continue
            ease = 1.0 + 0.35 * math.sin(k * math.pi)
            cx = W // 2 + (i - 1) * 110
            col = GOLD if i < stars else (80, 90, 130)
            pygame.draw.polygon(s, col, star_points(cx, 250, 46 * k * ease))
            pygame.draw.polygon(s, WHITE, star_points(cx, 250, 46 * k * ease), 3)
        x = 290
        self.draw_stat(s, "Jawaban benar", "%d / %d" % (self.level_correct, QUESTIONS_PER_LEVEL), x, 330, GREEN, 520)
        self.draw_stat(s, "Skor level ini", "+%d" % self.level_gain, x, 372, GOLD, 520)
        self.draw_stat(s, "Bonus level sempurna", "+%d" % self.level_bonus if self.level_bonus else "-", x, 414,
                       (255, 170, 80), 520)
        self.draw_stat(s, "Total skor", self.score, x, 456, WHITE, 520)
        self.draw_stat(s, "Nyawa", "%d / %d%s" % (self.lives, MAX_LIVES, "  (+1 bonus!)" if self.life_bonus else ""),
                       x, 498, (255, 120, 140), 520)
        draw_mascot(s, 135, 470, 1.0, "happy", self.time)
        for b in self.buttons:
            b.draw(s)

    def draw_gameover(self, s):
        shake = math.sin(self.time * 40) * 3 if self.state_time < 0.6 else 0
        draw_text(s, "GAME OVER", 100, RED, (W // 2 + shake, 120), "center", True, shadow=(0, 0, 0))
        draw_text(s, "Nyawamu habis. Kamu harus mengulang dari awal, %s!" % self.player_name, 24,
                  (255, 200, 210), (W // 2, 190), "center", True)
        draw_mascot(s, 290, 430, 1.9, "dead", self.time)
        draw_panel(s, (570, 230, 460, 200), (10, 5, 20, 205), 22, (255, 110, 130, 230), 3)
        self.draw_stat(s, "Skor akhir", self.score, 600, 250, GOLD, 400)
        self.draw_stat(s, "Level dicapai", "%d / %d" % (self.level_idx + 1, TOTAL_LEVELS), 600, 292, WHITE, 400)
        self.draw_stat(s, "Streak terbaik", self.best_streak, 600, 334, (255, 160, 80), 400)
        self.draw_stat(s, "Hint dipakai", self.hints_used, 600, 376, (255, 230, 130), 400)
        for b in self.buttons:
            b.draw(s)

    def draw_victory(self, s):
        self.draw_wavy_title(s, "SELAMAT!", W // 2, 90, 90)
        draw_text(s, "%s menamatkan StudyRush!" % self.player_name, 32, WHITE, (W // 2, 160), "center", True,
                  shadow=(60, 30, 0))
        acc = int(100 * self.total_correct / max(1, self.total_answered))
        rank = "Master Informatika" if acc >= 90 else ("Jagoan Teknologi" if acc >= 75 else "Siswa Berprestasi")
        draw_mascot(s, 290, 440, 1.9, "happy", self.time)
        draw_panel(s, (570, 200, 460, 250), (50, 30, 5, 215), 22, (255, 225, 120, 240), 3)
        draw_text(s, rank.upper(), 28, GOLD, (800, 214), "midtop", True)
        self.draw_stat(s, "Skor akhir", self.score, 600, 262, WHITE, 400)
        self.draw_stat(s, "Akurasi", "%d%%" % acc, 600, 304, GREEN, 400)
        self.draw_stat(s, "Streak terbaik", self.best_streak, 600, 346, (255, 160, 80), 400)
        self.draw_stat(s, "Hint dipakai", self.hints_used, 600, 388, (255, 230, 130), 400)
        for b in self.buttons:
            b.draw(s)

    # ------------------------------------------------------------------
    #  Draw utama
    # ------------------------------------------------------------------
    def draw(self):
        s = self.canvas
        self.bg.draw(s)
        st = self.state
        if st == "start":
            self.draw_start(s)
            self.draw_sound_icon(s)
        elif st == "home":
            self.draw_home(s)
            self.draw_sound_icon(s)
        elif st == "howto":
            self.draw_howto(s)
            self.draw_sound_icon(s)
        elif st == "scores":
            self.draw_scores(s)
            self.draw_sound_icon(s)
        elif st == "intro":
            self.draw_intro(s)
            self.draw_sound_icon(s)
        elif st == "quiz":
            self.draw_quiz(s)
        elif st == "complete":
            self.draw_complete(s)
            self.draw_sound_icon(s)
        elif st == "gameover":
            self.draw_gameover(s)
            self.draw_sound_icon(s)
        elif st == "victory":
            self.draw_victory(s)
            self.draw_sound_icon(s)
        self.particles.draw(s)
        for f in self.floaters:
            k = f["life"] / f["max"]
            draw_text(s, f["text"], f["size"], f["color"], (f["x"], f["y"]), "center", True,
                      shadow=(0, 0, 0), alpha=int(255 * min(1.0, k * 2)))
        if self.paused and st == "quiz":
            self.draw_pause(s)
        if self.flash > 0:
            fl = pygame.Surface((W, H), pygame.SRCALPHA)
            fl.fill((255, 30, 50, int(110 * self.flash)))
            s.blit(fl, (0, 0))
        if self.fade > 0:
            fd = pygame.Surface((W, H))
            fd.set_alpha(int(self.fade))
            s.blit(fd, (0, 0))
        ox = random.uniform(-self.shake, self.shake) if self.shake > 0 else 0
        oy = random.uniform(-self.shake, self.shake) if self.shake > 0 else 0
        self.screen.fill(BLACK)
        self.screen.blit(s, (int(ox), int(oy)))
        pygame.display.flip()

    # ------------------------------------------------------------------
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.time += dt
            self.mouse = pygame.mouse.get_pos()
            for e in pygame.event.get():
                self.handle_event(e)
            self.update(dt)
            self.draw()
        save_data(self.data)
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()