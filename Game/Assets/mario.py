import json
import math
import os
import random
import sys

import pygame

# =============================================================================
#  KONFIGURASI
# =============================================================================
WIDTH, HEIGHT = 1100, 650
FPS = 60
GROUND_Y = 540

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "studyrush_save.json")

START_LIVES = 5
MAX_LIVES = 7
QUESTIONS_PER_LEVEL = 10
TOTAL_LEVELS = 10
QUESTION_TIME = 30.0
BASE_POINTS = 100
HINT_PENALTY = 30
RUSH_STREAK = 3
HINTS_PER_LEVEL = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVY = (22, 32, 80)
GREEN = (60, 190, 100)
RED = (230, 70, 70)
YELLOW = (255, 210, 60)
ORANGE = (255, 150, 40)
BLUE = (60, 140, 235)
GRAY = (140, 145, 160)

# =============================================================================
#  TEMA LEVEL
# =============================================================================
THEMES = [
    dict(title="Padang Hardware", topic="Pengenalan Hardware",
         sky_top=(90, 175, 255), sky_bot=(200, 238, 255), far=(140, 190, 225),
         mid=(85, 170, 105), grass=(95, 205, 85), dirt=(150, 100, 60),
         deco="hills", night=False, accent=(255, 140, 40)),
    dict(title="Lembah Software", topic="Pengenalan Software",
         sky_top=(255, 130, 110), sky_bot=(255, 225, 150), far=(190, 130, 170),
         mid=(120, 160, 90), grass=(125, 190, 70), dirt=(145, 95, 55),
         deco="hills", night=False, accent=(255, 110, 90)),
    dict(title="Kota Digital", topic="Hardware & Software",
         sky_top=(60, 60, 140), sky_bot=(245, 150, 160), far=(110, 90, 160),
         mid=(60, 60, 110), grass=(90, 170, 110), dirt=(120, 85, 70),
         deco="city", night=False, accent=(160, 110, 255)),
    dict(title="Kantor Word", topic="Office: Word & PowerPoint",
         sky_top=(150, 205, 250), sky_bot=(240, 248, 255), far=(170, 200, 230),
         mid=(110, 150, 200), grass=(80, 190, 170), dirt=(130, 110, 90),
         deco="city", night=False, accent=(60, 130, 230)),
    dict(title="Lembah Excel", topic="Microsoft Excel",
         sky_top=(100, 200, 150), sky_bot=(225, 250, 215), far=(150, 210, 170),
         mid=(70, 160, 110), grass=(60, 185, 100), dirt=(130, 100, 65),
         deco="grid", night=False, accent=(40, 170, 90)),
    dict(title="Hutan Proposisi", topic="Proposisi & Simbol Logika",
         sky_top=(25, 25, 80), sky_bot=(90, 70, 150), far=(60, 50, 120),
         mid=(35, 60, 90), grass=(70, 150, 120), dirt=(80, 65, 90),
         deco="hills", night=True, accent=(190, 140, 255)),
    dict(title="Danau Tabel Kebenaran", topic="Proposisi: Tabel Kebenaran",
         sky_top=(10, 30, 70), sky_bot=(40, 110, 150), far=(40, 80, 130),
         mid=(25, 70, 100), grass=(60, 170, 160), dirt=(60, 85, 100),
         deco="hills", night=True, accent=(70, 210, 230)),
    dict(title="Sirkuit Gerbang Logika", topic="Gerbang Logika",
         sky_top=(8, 12, 30), sky_bot=(20, 40, 70), far=(25, 50, 90),
         mid=(20, 35, 65), grass=(0, 200, 160), dirt=(30, 50, 70),
         deco="circuit", night=False, accent=(0, 230, 190)),
    dict(title="Laboratorium AI", topic="Sejarah Kecerdasan Buatan",
         sky_top=(12, 8, 40), sky_bot=(50, 20, 90), far=(50, 30, 100),
         mid=(30, 20, 70), grass=(210, 90, 200), dirt=(60, 35, 80),
         deco="binary", night=True, accent=(255, 100, 220)),
    dict(title="Galaksi Final", topic="Tantangan Campuran (Boss)",
         sky_top=(5, 5, 25), sky_bot=(40, 15, 70), far=(70, 40, 120),
         mid=(40, 25, 80), grass=(255, 200, 60), dirt=(70, 45, 60),
         deco="space", night=True, accent=(255, 200, 50)),
]

# =============================================================================
#  BANK SOAL  (soal, jawaban benar, salah1, salah2, salah3)
# =============================================================================
QUESTION_BANK = [
    # ---- LEVEL 1 : Hardware ------------------------------------------------
    [
        ("Komponen komputer yang berfungsi sebagai 'otak' pengolah instruksi adalah ...",
         "CPU (Processor)", "RAM", "Mouse", "Speaker"),
        ("Berikut ini yang termasuk perangkat input adalah ...",
         "Keyboard", "Monitor", "Printer", "Speaker"),
        ("Berikut ini yang termasuk perangkat output adalah ...",
         "Printer", "Scanner", "Mouse", "Webcam"),
        ("Memori sementara yang isinya hilang saat komputer dimatikan disebut ...",
         "RAM", "Hard disk", "SSD", "ROM"),
        ("Media penyimpanan berbasis flash tanpa bagian yang bergerak adalah ...",
         "SSD", "HDD", "RAM", "Motherboard"),
        ("Papan sirkuit utama tempat semua komponen komputer terpasang adalah ...",
         "Motherboard", "Processor", "Casing", "Power Supply"),
        ("Komponen yang berfungsi menyuplai listrik ke seluruh komponen komputer adalah ...",
         "Power Supply", "Motherboard", "VGA Card", "Heatsink"),
        ("Kartu yang khusus memproses tampilan grafis disebut ...",
         "VGA Card (GPU)", "Sound Card", "LAN Card", "Chipset"),
        ("Satuan yang digunakan untuk mengukur kecepatan prosesor adalah ...",
         "GHz", "Mbps", "DPI", "Pixel"),
        ("Perangkat yang berfungsi sebagai input sekaligus output adalah ...",
         "Layar sentuh (touchscreen)", "Keyboard", "Speaker", "Scanner"),
    ],
    # ---- LEVEL 2 : Software ------------------------------------------------
    [
        ("Perangkat lunak yang mengelola seluruh sumber daya komputer disebut ...",
         "Sistem operasi", "Program game", "Web browser", "Program Office"),
        ("Berikut ini yang merupakan contoh sistem operasi adalah ...",
         "Linux", "Microsoft Word", "Google Chrome", "Photoshop"),
        ("Program yang menerjemahkan bahasa pemrograman ke bahasa mesin adalah ...",
         "Compiler", "Browser", "Spreadsheet", "Antivirus"),
        ("Perangkat lunak yang berfungsi melindungi komputer dari virus adalah ...",
         "Antivirus", "Compiler", "Browser", "Media player"),
        ("Perangkat lunak penghubung antara sistem operasi dan hardware adalah ...",
         "Driver", "Browser", "Aplikasi presentasi", "Game"),
        ("Perangkat lunak yang kode sumbernya terbuka dan boleh dimodifikasi disebut ...",
         "Open source", "Shareware", "Proprietary", "Trial"),
        ("Perangkat lunak yang gratis dipakai tetapi kode sumbernya tertutup disebut ...",
         "Freeware", "Open source", "Malware", "Firmware"),
        ("Berikut ini yang termasuk software aplikasi adalah ...",
         "Google Chrome", "Windows 11", "Linux", "Driver printer"),
        ("Firmware adalah ...",
         "Perangkat lunak yang tertanam pada hardware",
         "Aplikasi yang diunduh dari internet",
         "Program untuk mengedit foto",
         "Program pelindung dari virus"),
        ("Berikut ini yang merupakan sistem operasi untuk smartphone adalah ...",
         "Android", "Microsoft Excel", "Adobe Photoshop", "Notepad"),
    ],
    # ---- LEVEL 3 : Hardware & Software campuran ---------------------------
    [
        ("Komponen komputer yang dapat dilihat dan disentuh secara fisik disebut ...",
         "Hardware", "Software", "Brainware", "Firmware"),
        ("Brainware dalam sistem komputer adalah ...",
         "Pengguna komputer", "Monitor", "Windows", "BIOS"),
        ("BIOS pada motherboard termasuk jenis ...",
         "Firmware", "Aplikasi office", "Antivirus", "Browser"),
        ("Sistem operasi Windows dikembangkan oleh perusahaan ...",
         "Microsoft", "Apple", "Google", "Canonical"),
        ("Satu byte sama dengan ... bit.",
         "8", "4", "16", "10"),
        ("Port yang umum dipakai menyalurkan video dan audio digital ke monitor/TV adalah ...",
         "HDMI", "PS/2", "RJ-45", "Audio jack"),
        ("Konektor RJ-45 digunakan untuk ...",
         "Kabel jaringan LAN", "Kabel audio", "Kabel monitor lama", "Keyboard"),
        ("Perangkat yang mengubah dokumen fisik menjadi file digital adalah ...",
         "Scanner", "Printer", "Plotter", "Speaker"),
        ("Alur kerja dasar sistem komputer yang benar adalah ...",
         "Input - Proses - Output", "Output - Proses - Input",
         "Proses - Input - Output", "Input - Output - Proses"),
        ("Memori cache berukuran kecil dan sangat cepat, letaknya dekat dengan ...",
         "Processor", "Hard disk", "Monitor", "Printer"),
    ],
    # ---- LEVEL 4 : Office (Word & PowerPoint) ------------------------------
    [
        ("Ekstensi file default Microsoft Word modern adalah ...",
         ".docx", ".xlsx", ".pptx", ".mp4"),
        ("Pintasan keyboard untuk menyimpan dokumen adalah ...",
         "Ctrl + S", "Ctrl + P", "Ctrl + Z", "Ctrl + C"),
        ("Pintasan keyboard untuk menyalin (copy) teks adalah ...",
         "Ctrl + C", "Ctrl + V", "Ctrl + X", "Ctrl + B"),
        ("Pintasan keyboard untuk mencetak dokumen adalah ...",
         "Ctrl + P", "Ctrl + O", "Ctrl + N", "Ctrl + A"),
        ("Daftar isi otomatis pada Word dibuat dengan bantuan fitur ...",
         "Heading (Styles)", "Word Art", "Watermark", "Text Box"),
        ("Fitur Word untuk membuat surat massal dengan nama penerima berbeda adalah ...",
         "Mail Merge", "Track Changes", "Find and Replace", "Spelling"),
        ("Fitur yang menampilkan jumlah kata dalam dokumen adalah ...",
         "Word Count", "Page Break", "Thesaurus", "Footnote"),
        ("Bagian di margin atas halaman yang isinya berulang di setiap halaman disebut ...",
         "Header", "Footer", "Margin", "Footnote"),
        ("Ekstensi file default Microsoft PowerPoint modern adalah ...",
         ".pptx", ".docx", ".xlsx", ".txt"),
        ("Efek perpindahan antar slide pada PowerPoint disebut ...",
         "Transition", "Animation", "Slide Master", "Outline"),
    ],
    # ---- LEVEL 5 : Office (Excel) -----------------------------------------
    [
        ("Pertemuan antara satu kolom dan satu baris pada Excel disebut ...",
         "Cell (sel)", "Range", "Sheet", "Workbook"),
        ("Fungsi Excel untuk menjumlahkan sekumpulan angka adalah ...",
         "=SUM()", "=COUNT()", "=AVERAGE()", "=MAX()"),
        ("Fungsi Excel untuk mencari nilai rata-rata adalah ...",
         "=AVERAGE()", "=SUM()", "=MIN()", "=LEN()"),
        ("Fungsi Excel untuk mencari nilai tertinggi adalah ...",
         "=MAX()", "=MIN()", "=SUM()", "=ROUND()"),
        ("Fungsi Excel untuk pengambilan keputusan berdasarkan kondisi adalah ...",
         "=IF()", "=SUM()", "=LEN()", "=ROUND()"),
        ("Fungsi Excel untuk menghitung banyaknya sel yang berisi angka adalah ...",
         "=COUNT()", "=SUM()", "=MAX()", "=TODAY()"),
        ("Setiap rumus di Excel harus diawali dengan tanda ...",
         "=", "#", "@", "$"),
        ("Penulisan referensi sel absolut yang benar adalah ...",
         "$A$1", "A1", "#A#1", "@A1"),
        ("Fungsi Excel untuk mencari data secara vertikal pada tabel adalah ...",
         "VLOOKUP", "HLOOKUP", "COUNTIF", "CONCAT"),
        ("Alamat sel pada kolom C baris ke-5 ditulis ...",
         "C5", "5C", "C.5", "CC"),
    ],
    # ---- LEVEL 6 : Proposisi dasar ---------------------------------------
    [
        ("Kalimat yang hanya bernilai benar atau salah, tetapi tidak keduanya, disebut ...",
         "Proposisi", "Kalimat tanya", "Kalimat perintah", "Kalimat seru"),
        ("Berikut ini yang merupakan proposisi adalah ...",
         "Jakarta adalah ibu kota Indonesia", "Tolong tutup pintunya",
         "Siapa namamu?", "Semoga besok cerah"),
        ("Berikut ini yang BUKAN proposisi adalah ...",
         "Apakah kamu sudah makan?", "2 + 3 = 5", "Bumi itu bulat",
         "Matahari terbit dari barat"),
        ("Nilai kebenaran dari 'Matahari terbit dari barat' adalah ...",
         "Salah", "Benar", "Benar dan salah", "Tidak punya nilai"),
        ("Simbol operator negasi (ingkaran) adalah ...",
         "¬", "∧", "∨", "→"),
        ("Simbol operator konjungsi (dan) adalah ...",
         "∧", "∨", "¬", "→"),
        ("Simbol operator disjungsi (atau) adalah ...",
         "∨", "∧", "↔", "¬"),
        ("Simbol operator implikasi (jika ... maka ...) adalah ...",
         "→", "↔", "∧", "¬"),
        ("Simbol operator biimplikasi (jika dan hanya jika) adalah ...",
         "↔", "→", "∨", "∧"),
        ("Negasi dari pernyataan 'Hari ini hujan' adalah ...",
         "Hari ini tidak hujan", "Hari ini mendung", "Besok hujan", "Hari ini hujan deras"),
    ],
    # ---- LEVEL 7 : Proposisi (tabel kebenaran) ------------------------------
    [
        ("Konjungsi p ∧ q bernilai benar jika ...",
         "p dan q keduanya benar", "salah satu benar saja", "keduanya salah", "p salah"),
        ("Disjungsi p ∨ q bernilai salah jika ...",
         "p dan q keduanya salah", "p benar", "q benar", "p dan q keduanya benar"),
        ("Implikasi p → q bernilai salah jika ...",
         "p benar dan q salah", "p salah dan q benar", "p dan q keduanya benar",
         "p dan q keduanya salah"),
        ("Biimplikasi p ↔ q bernilai benar jika ...",
         "p dan q bernilai sama", "p benar saja", "q salah saja", "p dan q berbeda nilai"),
        ("Jika p benar dan q salah, maka nilai p ∧ q adalah ...",
         "Salah", "Benar", "Tidak tentu", "Netral"),
        ("Jika p benar dan q salah, maka nilai p ∨ q adalah ...",
         "Benar", "Salah", "Tidak tentu", "Netral"),
        ("Jika p salah dan q benar, maka nilai p → q adalah ...",
         "Benar", "Salah", "Tidak tentu", "Netral"),
        ("Pernyataan ¬(¬p) ekuivalen dengan ...",
         "p", "¬p", "q", "p ∧ q"),
        ("Menurut hukum De Morgan, ¬(p ∧ q) ekuivalen dengan ...",
         "¬p ∨ ¬q", "¬p ∧ ¬q", "p ∨ q", "¬p → ¬q"),
        ("Konvers dari implikasi p → q adalah ...",
         "q → p", "¬p → ¬q", "¬q → ¬p", "p → ¬q"),
    ],
    # ---- LEVEL 8 : Gerbang logika ----------------------------------------
    [
        ("Gerbang AND menghasilkan output 1 jika ...",
         "semua input bernilai 1", "salah satu input bernilai 1",
         "semua input bernilai 0", "input berbeda"),
        ("Gerbang OR menghasilkan output 0 jika ...",
         "semua input bernilai 0", "salah satu input 1", "semua input 1", "input berbeda"),
        ("Fungsi gerbang NOT adalah ...",
         "membalik nilai input", "menjumlahkan input", "mengalikan input", "menyamakan input"),
        ("Gerbang NAND dengan input 1 dan 1 menghasilkan output ...",
         "0", "1", "2", "tidak tentu"),
        ("Gerbang NOR dengan input 0 dan 0 menghasilkan output ...",
         "1", "0", "2", "tidak tentu"),
        ("Gerbang XOR menghasilkan output 1 jika ...",
         "kedua input berbeda", "kedua input sama", "kedua input 0", "selalu"),
        ("Gerbang XNOR dengan input 0 dan 1 menghasilkan output ...",
         "0", "1", "2", "tidak terdefinisi"),
        ("Gerbang yang disebut gerbang universal karena dapat membentuk semua gerbang lain adalah ...",
         "NAND dan NOR", "AND dan OR", "XOR dan XNOR", "NOT dan Buffer"),
        ("Jika A = 1 dan B = 0, output gerbang OR adalah ...",
         "1", "0", "2", "tidak tentu"),
        ("Dalam aljabar Boolean, gerbang AND setara dengan operasi ...",
         "perkalian (A · B)", "penjumlahan (A + B)", "pengurangan (A - B)", "pembagian (A / B)"),
    ],
    # ---- LEVEL 9 : Sejarah AI --------------------------------------------
    [
        ("Istilah 'Artificial Intelligence' dipopulerkan oleh ...",
         "John McCarthy", "Bill Gates", "Steve Jobs", "Tim Berners-Lee"),
        ("Konferensi Dartmouth yang menandai lahirnya bidang AI diadakan pada tahun ...",
         "1956", "1946", "1969", "1984"),
        ("Tes yang mengukur apakah mesin dapat berperilaku seperti manusia dicetuskan oleh ...",
         "Alan Turing", "Charles Babbage", "Linus Torvalds", "Mark Zuckerberg"),
        ("Tes Turing digunakan untuk menguji ...",
         "kemampuan mesin menyerupai kecerdasan manusia",
         "kecepatan prosesor", "kapasitas memori", "keamanan jaringan"),
        ("Komputer IBM yang mengalahkan juara catur dunia Garry Kasparov tahun 1997 adalah ...",
         "Deep Blue", "Watson", "AlphaGo", "ChatGPT"),
        ("Program AlphaGo terkenal karena berhasil mengalahkan juara dunia permainan ...",
         "Go", "Catur", "Domino", "Ular tangga"),
        ("ELIZA, salah satu chatbot paling awal, diciptakan oleh ...",
         "Joseph Weizenbaum", "Alan Turing", "Elon Musk", "Larry Page"),
        ("Masa ketika dana dan minat riset AI menurun drastis disebut ...",
         "AI Winter", "AI Summer", "AI Spring", "AI Boom"),
        ("Cabang AI yang belajar dari data tanpa diprogram secara eksplisit adalah ...",
         "Machine Learning", "Web Design", "Basis Data", "Jaringan Kabel"),
        ("Contoh penerapan AI dalam kehidupan sehari-hari adalah ...",
         "Asisten virtual seperti Siri", "Kalkulator biasa", "Lampu senter", "Mesin ketik"),
    ],
    # ---- LEVEL 10 : Campuran (boss) -------------------------------------
    [
        ("Gerbang NOT dengan input 0 menghasilkan output ...",
         "1", "0", "2", "tidak ada"),
        ("Kontraposisi dari p → q adalah ...",
         "¬q → ¬p", "q → p", "¬p → ¬q", "p → ¬q"),
        ("Rumus Excel untuk mengambil 3 karakter pertama dari sel A1 adalah ...",
         "=LEFT(A1,3)", "=RIGHT(A1,3)", "=LEN(A1)", "=UPPER(A1)"),
        ("Satuan resolusi cetak pada printer adalah ...",
         "DPI", "RPM", "Hz", "Watt"),
        ("Sistem operasi bawaan iPhone adalah ...",
         "iOS", "Android", "Windows XP", "Chrome OS"),
        ("Gerbang XOR dengan input 1 dan 1 menghasilkan output ...",
         "0", "1", "2", "tidak tentu"),
        ("Mesin mekanik rancangan Charles Babbage yang dianggap cikal bakal komputer adalah ...",
         "Analytical Engine", "ENIAC", "Deep Blue", "ELIZA"),
        ("Jika p benar dan q salah, maka nilai p ↔ q adalah ...",
         "Salah", "Benar", "Tidak tentu", "Netral"),
        ("Memori yang hanya bisa dibaca dan isinya tetap saat listrik mati (menyimpan BIOS) adalah ...",
         "ROM", "RAM", "Cache", "Register"),
        ("Pintasan keyboard untuk membatalkan tindakan terakhir (undo) adalah ...",
         "Ctrl + Z", "Ctrl + Y", "Ctrl + X", "Ctrl + V"),
    ],
]

# =============================================================================
#  UTILITAS UMUM
# =============================================================================
_font_cache = {}
_font_state = {"path": None, "checked": False}


def _find_font_path():
    """Cari font sistem yang mendukung simbol logika (∧ ∨ → ↔ ¬)."""
    if _font_state["checked"]:
        return _font_state["path"]
    _font_state["checked"] = True
    probe = "∧∨→↔¬·"
    names = ["segoeuisymbol", "segoeui", "dejavusans", "cambriamath", "arialunicodems",
             "notosans", "freesans", "liberationsans", "arial", "helvetica"]
    for name in names:
        path = pygame.font.match_font(name)
        if not path:
            continue
        try:
            f = pygame.font.Font(path, 20)
            if all(m is not None for m in f.metrics(probe)):
                _font_state["path"] = path
                return path
        except Exception:
            continue
    for name in ("segoeui", "arial", "dejavusans", "freesans"):
        path = pygame.font.match_font(name)
        if path:
            _font_state["path"] = path
            break
    return _font_state["path"]


def get_font(size, bold=True):
    key = (size, bold)
    if key not in _font_cache:
        path = _find_font_path()
        try:
            f = pygame.font.Font(path, size) if path else pygame.font.Font(None, size + 6)
        except Exception:
            f = pygame.font.Font(None, size + 6)
        f.set_bold(bold)
        _font_cache[key] = f
    return _font_cache[key]


def draw_text(surf, text, size, color, pos, anchor="topleft", bold=True,
              shadow=None, alpha=255):
    font = get_font(size, bold)
    img = font.render(str(text), True, color)
    if alpha < 255:
        img.set_alpha(alpha)
    rect = img.get_rect()
    setattr(rect, anchor, pos)
    if shadow:
        sh = font.render(str(text), True, shadow)
        if alpha < 255:
            sh.set_alpha(alpha)
        surf.blit(sh, (rect.x + 2, rect.y + 3))
    surf.blit(img, rect)
    return rect


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = w if not cur else cur + " " + w
        if font.size(test)[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3])


def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def draw_rrect(surf, color, rect, radius=12, width=0, alpha=255):
    rect = pygame.Rect(rect)
    if alpha >= 255:
        pygame.draw.rect(surf, color, rect, width, border_radius=radius)
    else:
        tmp = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(tmp, (*color[:3], alpha), tmp.get_rect(), width, border_radius=radius)
        surf.blit(tmp, rect.topleft)


def draw_heart(surf, cx, cy, size, color, outline=None):
    if outline:
        draw_heart(surf, cx, cy, size * 1.14, outline)
    r = size * 0.27
    cx, cy = float(cx), float(cy)
    pygame.draw.circle(surf, color, (int(cx - r), int(cy - r * 0.55)), int(r) + 1)
    pygame.draw.circle(surf, color, (int(cx + r), int(cy - r * 0.55)), int(r) + 1)
    pts = [(cx - 2 * r + 1, cy - r * 0.2), (cx + 2 * r - 1, cy - r * 0.2),
           (cx, cy + size * 0.52)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.circle(surf, mix(color, WHITE, 0.6),
                       (int(cx - r * 1.15), int(cy - r * 0.95)), max(2, int(r * 0.3)))


def draw_flame(surf, cx, by, s, t):
    for scale, col in ((1.0, (255, 110, 20)), (0.72, (255, 190, 40)), (0.42, (255, 245, 170))):
        w = s * 0.5 * scale
        h = s * scale
        wob = math.sin(t * 12 + scale * 3) * s * 0.07
        pts = [(cx - w, by - w * 0.3), (cx - w * 0.85, by - h * 0.45),
               (cx - w * 0.2 + wob, by - h * 0.8), (cx + wob * 1.6, by - h),
               (cx + w * 0.3 + wob, by - h * 0.7), (cx + w * 0.9, by - h * 0.4),
               (cx + w, by - w * 0.3)]
        pygame.draw.polygon(surf, col, pts)
        pygame.draw.ellipse(surf, col, (cx - w, by - w * 1.3, w * 2, w * 1.5))


def draw_bulb_icon(surf, cx, cy, size, t=0.0, glow=True):
    if glow:
        g = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
        pulse = 0.6 + 0.4 * math.sin(t * 4)
        for rr, aa in ((1.4, 40), (1.0, 70)):
            pygame.draw.circle(g, (255, 235, 120, int(aa * pulse)),
                               (g.get_width() // 2, g.get_height() // 2), int(size * rr))
        surf.blit(g, (cx - g.get_width() // 2, cy - g.get_height() // 2))
    pygame.draw.circle(surf, (255, 225, 80), (cx, cy - size // 6), int(size * 0.5))
    pygame.draw.circle(surf, (255, 250, 200), (cx - size // 6, cy - size // 3), max(2, size // 6))
    pygame.draw.rect(surf, (150, 150, 165), (cx - size // 4, cy + size // 4, size // 2, size // 4),
                     border_radius=3)
    pygame.draw.rect(surf, (110, 110, 125), (cx - size // 6, cy + size // 2, size // 3, size // 8),
                     border_radius=2)
    pygame.draw.circle(surf, (190, 140, 20), (cx, cy - size // 6), int(size * 0.5), 2)


def load_save():
    data = {"name": "", "unlocked": 1, "level_best": {}, "top": []}
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        if isinstance(loaded, dict):
            data.update(loaded)
    except (OSError, ValueError):
        pass
    return data


def write_save(data):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def streak_multiplier(streak):
    return min(5.0, 1.0 + 0.5 * max(0, streak - 1))


def build_questions(level_idx):
    """Acak soal & urutan pilihan jawaban untuk satu level."""
    items = list(QUESTION_BANK[level_idx])
    random.shuffle(items)
    result = []
    for text, correct, w1, w2, w3 in items[:QUESTIONS_PER_LEVEL]:
        options = [correct, w1, w2, w3]
        random.shuffle(options)
        result.append({"text": text, "options": options, "ans": options.index(correct)})
    return result


# =============================================================================
#  AUDIO
# =============================================================================
def _norm(name):
    return "".join(ch for ch in name.lower() if ch.isalnum())


class Audio:
    FILES = {
        "salah": "Sound Salah Jawab.mp3",
        "main": "Sound Keseluruhan.mp3",
        "start": "Sound Start.mp3",
        "mati": "Sound Mati.mp3",
        "benar": "Jawaban Benar.mp3",
        "nyawa": "Sound Nyawa.mp3",
    }

    def __init__(self):
        self.ok = False
        self.muted = False
        self.music_vol = 0.45
        self.sfx_vol = 0.95
        self.current = None
        self.cache = {}
        self.warned = set()
        self.index = self._scan()
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.set_num_channels(12)
            self.ok = True
        except pygame.error as err:
            print("[Audio] Mixer tidak bisa dijalankan:", err)

    def _scan(self):
        index = {}
        for root in (BASE_DIR, os.getcwd()):
            for dirpath, dirnames, filenames in os.walk(root):
                depth = dirpath[len(root):].count(os.sep)
                if depth > 3:
                    dirnames[:] = []
                    continue
                for fn in filenames:
                    if fn.lower().endswith((".mp3", ".wav", ".ogg")):
                        index.setdefault(_norm(fn), os.path.join(dirpath, fn))
        return index

    def find(self, key):
        fname = self.FILES[key]
        path = self.index.get(_norm(fname))
        if path:
            return path
        stem = _norm(os.path.splitext(fname)[0])
        for k, v in self.index.items():
            if k.startswith(stem):
                return v
        if key not in self.warned:
            self.warned.add(key)
            print("[Audio] File tidak ditemukan: %s (letakkan di folder game)" % fname)
        return None

    def play_sfx(self, key):
        if not self.ok:
            return
        if key not in self.cache:
            snd = None
            path = self.find(key)
            if path:
                try:
                    snd = pygame.mixer.Sound(path)
                except pygame.error as err:
                    print("[Audio] Gagal memuat", path, err)
            self.cache[key] = snd
        snd = self.cache[key]
        if snd:
            snd.set_volume(0.0 if self.muted else self.sfx_vol)
            snd.play()

    def play_music(self, key):
        if not self.ok:
            return
        if self.current == key and pygame.mixer.music.get_busy():
            return
        path = self.find(key)
        if not path:
            self.current = None
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.0 if self.muted else self.music_vol)
            pygame.mixer.music.play(-1)
            self.current = key
        except pygame.error as err:
            print("[Audio] Gagal memutar musik", path, err)
            self.current = None

    def stop_music(self):
        if self.ok:
            pygame.mixer.music.stop()
        self.current = None

    def toggle_mute(self):
        self.muted = not self.muted
        if self.ok:
            pygame.mixer.music.set_volume(0.0 if self.muted else self.music_vol)


# =============================================================================
#  PARTIKEL & TEKS MELAYANG
# =============================================================================
class Particle:
    def __init__(self, x, y, vx, vy, life, color, size, grav=0.25, world=True):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.life = self.max_life = life
        self.color, self.size, self.grav, self.world = color, size, grav, world

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.grav
        self.life -= 1
        return self.life > 0

    def draw(self, surf, cam):
        k = self.life / self.max_life
        r = max(1, int(self.size * k))
        x = int(self.x - (cam if self.world else 0))
        pygame.draw.circle(surf, self.color, (x, int(self.y)), r)


class FloatText:
    def __init__(self, x, y, text, color, size=26, life=55, world=True):
        self.x, self.y, self.text, self.color = x, y, text, color
        self.size, self.life, self.max_life, self.world = size, life, life, world

    def update(self):
        self.y -= 0.9
        self.life -= 1
        return self.life > 0

    def draw(self, surf, cam):
        a = int(255 * min(1.0, self.life / (self.max_life * 0.5)))
        x = int(self.x - (cam if self.world else 0))
        draw_text(surf, self.text, self.size, self.color, (x, int(self.y)),
                  "center", shadow=(0, 0, 0), alpha=max(0, min(255, a)))


# =============================================================================
#  LATAR BELAKANG BERLAPIS (PARALLAX)
# =============================================================================
class Background:
    PERIOD = 2400

    def __init__(self, theme, seed=1):
        self.th = theme
        rng = random.Random(seed * 31 + 7)
        self.sky = pygame.Surface((WIDTH, HEIGHT))
        top, bot = theme["sky_top"], theme["sky_bot"]
        for y in range(HEIGHT):
            col = mix(top, bot, y / HEIGHT)
            pygame.draw.line(self.sky, col, (0, y), (WIDTH, y))
        self.stars = [(rng.randint(0, WIDTH), rng.randint(0, GROUND_Y - 160),
                       rng.random() * 1.8 + 0.8, rng.random() * 6.28) for _ in range(110)]
        self.orb = self._make_orb(theme["night"])
        self.cloud = self._make_cloud()
        self.clouds = [[rng.randint(0, 2400), rng.randint(30, 220), rng.uniform(0.7, 1.5),
                        rng.uniform(4, 14)] for _ in range(9)]
        self.buildings = []
        wx = 0
        while wx < self.PERIOD:
            w, h = rng.randint(60, 120), rng.randint(110, 300)
            self.buildings.append((wx, w, h, rng.randint(0, 99)))
            wx += w + rng.randint(0, 12)
        self.traces = [dict(y=rng.randint(60, GROUND_Y - 60), x0=rng.randint(0, self.PERIOD),
                            ln=rng.randint(300, 900), ph=rng.random() * 400,
                            stub=rng.choice((-1, 1)) * rng.randint(25, 70)) for _ in range(16)]
        gate_names = ["AND", "OR", "NOT", "XOR", "NAND", "NOR", "XNOR"]
        self.gates = [(rng.randint(0, self.PERIOD), rng.randint(70, 300), rng.choice(gate_names))
                      for _ in range(9)]
        formulas = ["=SUM()", "=IF()", "=MAX()", "=AVERAGE()", "=VLOOKUP()", "=COUNT()", "A1", "B2"]
        self.formulas = [(rng.randint(0, self.PERIOD), rng.randint(60, 300), rng.choice(formulas))
                         for _ in range(10)]
        self.rain = [(rng.randint(0, WIDTH), rng.uniform(40, 130), rng.randint(0, 1000))
                     for _ in range(32)]
        acc = theme["accent"]
        self.glyphs = {}
        for ch in "01":
            for lv in range(4):
                col = mix((0, 0, 0), acc, 0.25 + 0.25 * lv)
                self.glyphs[(ch, lv)] = get_font(22, True).render(ch, True, col)
        self.planets = [(rng.randint(0, self.PERIOD), rng.randint(60, 300), rng.randint(30, 80),
                         rng.choice([(200, 120, 90), (110, 160, 230), (230, 200, 120), (150, 110, 210)]),
                         rng.random() < 0.4) for _ in range(6)]
        self.grid = self._make_grid()

    def _make_orb(self, night):
        s = pygame.Surface((260, 260), pygame.SRCALPHA)
        col = (235, 235, 255) if night else (255, 240, 150)
        for r, a in ((125, 25), (95, 45), (70, 80)):
            pygame.draw.circle(s, (*col, a), (130, 130), r)
        pygame.draw.circle(s, col, (130, 130), 48)
        if night:
            pygame.draw.circle(s, (205, 205, 230), (115, 120), 9)
            pygame.draw.circle(s, (205, 205, 230), (145, 140), 7)
            pygame.draw.circle(s, (205, 205, 230), (132, 108), 5)
        return s

    def _make_cloud(self):
        s = pygame.Surface((180, 80), pygame.SRCALPHA)
        for cx, cy, r in ((50, 50, 28), (85, 38, 34), (120, 50, 28), (95, 56, 26), (65, 58, 22)):
            pygame.draw.circle(s, (255, 255, 255, 225), (cx, cy), r)
        pygame.draw.rect(s, (255, 255, 255, 225), (50, 50, 80, 28), border_radius=12)
        return s

    def _make_grid(self):
        s = pygame.Surface((WIDTH + 200, GROUND_Y), pygame.SRCALPHA)
        for x in range(0, WIDTH + 200, 100):
            pygame.draw.line(s, (255, 255, 255, 70), (x, 0), (x, GROUND_Y), 2)
        for y in range(0, GROUND_Y, 50):
            pygame.draw.line(s, (255, 255, 255, 70), (0, y), (WIDTH + 200, y), 2)
        return s

    # ---- lapisan dasar -----------------------------------------------------
    def _hills(self, surf, cam, par, base, amp, color, freq, phase):
        step = 6
        for sx in range(0, WIDTH + step, step):
            wx = sx + cam * par
            h = base + amp * math.sin(wx * freq + phase) + amp * 0.5 * math.sin(wx * freq * 2.3 + phase * 1.7)
            pygame.draw.rect(surf, color, (sx, GROUND_Y - h, step + 1, h + 4))

    def _labels(self, surf, cam, par, items, color, boxed):
        font = get_font(24, True)
        for (x, y, text) in items:
            for off in (0, -self.PERIOD):
                sx = (x - cam * par) % self.PERIOD + off - 200
                if -200 < sx < WIDTH + 50:
                    img = font.render(text, True, color)
                    if boxed:
                        r = pygame.Rect(sx, y, img.get_width() + 34, 60)
                        draw_rrect(surf, color, r, 14, 3, 150)
                        surf.blit(img, (r.x + 17, r.y + 14))
                    else:
                        pygame.draw.rect(surf, (255, 255, 255), (sx - 6, y - 4, img.get_width() + 16, 38), 2)
                        surf.blit(img, (sx + 2, y))

    def draw(self, surf, cam, t):
        th = self.th
        deco = th["deco"]
        surf.blit(self.sky, (0, 0))
        if th["night"] or deco == "circuit":
            for (x, y, r, ph) in self.stars:
                c = int(110 + 140 * (0.5 + 0.5 * math.sin(t * 2 + ph)))
                pygame.draw.circle(surf, (c, c, c), (int((x - cam * 0.04) % WIDTH), y), max(1, int(r)))
        if deco in ("hills", "city", "grid"):
            surf.blit(self.orb, (780 - int(cam * 0.02), 20))
            if not th["night"]:
                for c in self.clouds:
                    x = (c[0] - cam * 0.12 - t * c[3]) % (WIDTH + 400) - 200
                    cl = self.cloud if c[2] == 1 else pygame.transform.smoothscale(
                        self.cloud, (int(180 * c[2]), int(80 * c[2])))
                    surf.blit(cl, (x, c[1]))
        if deco == "hills":
            self._hills(surf, cam, 0.2, 170, 60, th["far"], 0.004, 1.0)
            self._hills(surf, cam, 0.45, 95, 36, th["mid"], 0.007, 3.0)
        elif deco == "city":
            self._hills(surf, cam, 0.2, 150, 50, th["far"], 0.004, 2.0)
            for (bx, w, h, seed) in self.buildings:
                sx = (bx - cam * 0.4) % self.PERIOD
                if sx > WIDTH + 50:
                    sx -= self.PERIOD
                if sx + w < -10:
                    continue
                pygame.draw.rect(surf, th["mid"], (sx, GROUND_Y - h, w, h + 5))
                pygame.draw.rect(surf, shade(th["mid"], 0.8), (sx, GROUND_Y - h, w, 6))
                for j, wy in enumerate(range(GROUND_Y - h + 16, GROUND_Y - 24, 26)):
                    for i, wx in enumerate(range(int(sx) + 10, int(sx) + w - 14, 22)):
                        lit = (i * 7 + j * 13 + seed) % 4 > 0
                        col = (255, 230, 140) if lit else shade(th["mid"], 0.7)
                        pygame.draw.rect(surf, col, (wx, wy, 12, 14))
        elif deco == "grid":
            off = (cam * 0.3) % 100
            surf.blit(self.grid, (-off, 0))
            self._labels(surf, cam, 0.4, self.formulas, (255, 255, 255), False)
            self._hills(surf, cam, 0.45, 70, 26, th["mid"], 0.007, 1.5)
        elif deco == "circuit":
            acc = th["accent"]
            for tr in self.traces:
                for off in (0, -self.PERIOD):
                    sx = (tr["x0"] - cam * 0.5) % self.PERIOD + off - 300
                    if sx > WIDTH or sx + tr["ln"] < 0:
                        continue
                    y = tr["y"]
                    pygame.draw.line(surf, shade(acc, 0.35), (sx, y), (sx + tr["ln"], y), 3)
                    pygame.draw.line(surf, shade(acc, 0.35), (sx + tr["ln"], y),
                                     (sx + tr["ln"], y + tr["stub"]), 3)
                    pygame.draw.circle(surf, shade(acc, 0.6), (int(sx), y), 6)
                    pygame.draw.circle(surf, shade(acc, 0.6), (int(sx + tr["ln"]), y + tr["stub"]), 6)
                    p = (t * 160 + tr["ph"]) % tr["ln"]
                    pygame.draw.circle(surf, acc, (int(sx + p), y), 5)
            self._labels(surf, cam, 0.3, self.gates, shade(acc, 0.8), True)
            self._hills(surf, cam, 0.5, 60, 24, th["mid"], 0.008, 0.5)
        elif deco == "binary":
            for (x, speed, off) in self.rain:
                col_x = int((x - cam * 0.1) % WIDTH)
                for j in range(9):
                    y = (t * speed + off + j * 26) % (GROUND_Y + 60) - 30
                    ch = "01"[(off + j + int(t * 2)) % 2]
                    surf.blit(self.glyphs[(ch, min(3, j // 2 if j < 6 else 3))], (col_x, y))
            self._hills(surf, cam, 0.35, 90, 30, th["far"], 0.005, 2.2)
            self._hills(surf, cam, 0.55, 55, 22, th["mid"], 0.008, 0.7)
        elif deco == "space":
            for (x, y, r, col, ring) in self.planets:
                for off in (0, -self.PERIOD):
                    sx = (x - cam * 0.15) % self.PERIOD + off - 100
                    if -100 < sx < WIDTH + 100:
                        if ring:
                            pygame.draw.ellipse(surf, shade(col, 1.2), (sx - r * 1.7, y - r * 0.35, r * 3.4, r * 0.7), 4)
                        pygame.draw.circle(surf, col, (int(sx), y), r)
                        pygame.draw.circle(surf, shade(col, 0.7), (int(sx + r * 0.3), int(y + r * 0.2)), int(r * 0.7))
                        pygame.draw.circle(surf, shade(col, 1.25), (int(sx - r * 0.35), int(y - r * 0.35)), int(r * 0.3))
            self._hills(surf, cam, 0.3, 80, 28, th["far"], 0.006, 4.0)
            self._hills(surf, cam, 0.5, 50, 20, th["mid"], 0.009, 1.0)


# =============================================================================
#  SPRITE & GAMBAR OBJEK (semua digambar lewat kode, tanpa aset gambar)
# =============================================================================
def draw_ground_piece(surf, sx, w, cam, theme):
    x0, x1 = max(int(sx), 0), min(int(sx + w), WIDTH)
    if x1 <= x0:
        return
    grass, dirt = theme["grass"], theme["dirt"]
    pygame.draw.rect(surf, dirt, (x0, GROUND_Y, x1 - x0, HEIGHT - GROUND_Y))
    pygame.draw.rect(surf, shade(dirt, 0.85), (x0, GROUND_Y + 70, x1 - x0, HEIGHT))
    pygame.draw.rect(surf, grass, (x0, GROUND_Y, x1 - x0, 18))
    pygame.draw.rect(surf, mix(grass, WHITE, 0.35), (x0, GROUND_Y, x1 - x0, 5))
    start = (x0 + int(cam)) // 18 * 18 - int(cam)
    for gx in range(start, x1 + 18, 18):
        wx = gx + int(cam)
        if gx < x0 - 18:
            continue
        hgt = 6 + (wx * 7 % 5)
        pygame.draw.polygon(surf, shade(grass, 0.88),
                            [(gx, GROUND_Y + 14), (gx + 9, GROUND_Y + 14), (gx + 4, GROUND_Y + 18 + hgt)])
    start = (x0 + int(cam)) // 60 * 60 - int(cam)
    for gx in range(start, x1 + 60, 60):
        wx = gx + int(cam)
        dy = GROUND_Y + 36 + (wx * 13 % 40)
        pygame.draw.ellipse(surf, shade(dirt, 0.75), (gx + 8, dy, 18, 11))
        pygame.draw.ellipse(surf, shade(dirt, 1.15), (gx + 30, dy + 28, 12, 8))


def draw_pipe(surf, x, y, w, h):
    green, dark = (60, 190, 80), (30, 120, 50)
    pygame.draw.rect(surf, green, (x + 6, y + 22, w - 12, h - 22))
    pygame.draw.rect(surf, dark, (x + 6, y + 22, w - 12, h - 22), 3)
    pygame.draw.rect(surf, (140, 235, 150), (x + 14, y + 26, 8, h - 30))
    pygame.draw.rect(surf, green, (x, y, w, 26), border_radius=5)
    pygame.draw.rect(surf, dark, (x, y, w, 26), 3, border_radius=5)
    pygame.draw.rect(surf, (140, 235, 150), (x + 8, y + 4, 8, 18), border_radius=3)


def draw_step(surf, rect):
    pygame.draw.rect(surf, (190, 140, 90), rect)
    pygame.draw.rect(surf, (110, 70, 40), rect, 3)
    for yy in range(rect.y, rect.bottom, 40):
        pygame.draw.rect(surf, (220, 175, 120), (rect.x + 4, yy + 4, rect.w - 8, 6))
        pygame.draw.circle(surf, (110, 70, 40), (rect.x + 8, yy + 20), 3)
        pygame.draw.circle(surf, (110, 70, 40), (rect.right - 8, yy + 20), 3)


def draw_platform(surf, rect, theme):
    pygame.draw.rect(surf, shade(theme["dirt"], 1.1), rect, border_radius=6)
    pygame.draw.rect(surf, theme["grass"], (rect.x, rect.y, rect.w, 10), border_radius=5)
    pygame.draw.rect(surf, mix(theme["grass"], WHITE, 0.4), (rect.x + 3, rect.y + 1, rect.w - 6, 3), border_radius=2)
    pygame.draw.rect(surf, shade(theme["dirt"], 0.6), rect, 3, border_radius=6)
    for xx in range(rect.x + 14, rect.right - 8, 36):
        pygame.draw.circle(surf, shade(theme["dirt"], 0.75), (xx, rect.y + 17), 3)


def draw_brick(surf, rect, used, t):
    base = (150, 150, 160) if used else (205, 95, 60)
    pygame.draw.rect(surf, base, rect)
    pygame.draw.rect(surf, shade(base, 0.55), rect, 3)
    if not used:
        for i in range(3):
            yy = rect.y + 4 + i * 15
            pygame.draw.line(surf, shade(base, 0.6), (rect.x, yy + 12), (rect.right, yy + 12), 2)
        pygame.draw.line(surf, shade(base, 0.6), (rect.centerx, rect.y), (rect.centerx, rect.y + 16), 2)
        pygame.draw.line(surf, shade(base, 0.6), (rect.x + 12, rect.y + 16), (rect.x + 12, rect.y + 32), 2)
        pygame.draw.line(surf, shade(base, 0.6), (rect.right - 12, rect.y + 16), (rect.right - 12, rect.y + 32), 2)
        pygame.draw.line(surf, mix(base, WHITE, 0.45), (rect.x + 3, rect.y + 3), (rect.right - 4, rect.y + 3), 2)


def draw_qblock(surf, rect, used, t):
    if used:
        pygame.draw.rect(surf, (150, 120, 90), rect, border_radius=6)
        pygame.draw.rect(surf, (95, 70, 50), rect, 3, border_radius=6)
        for cx, cy in ((rect.x + 7, rect.y + 7), (rect.right - 7, rect.y + 7),
                       (rect.x + 7, rect.bottom - 7), (rect.right - 7, rect.bottom - 7)):
            pygame.draw.circle(surf, (95, 70, 50), (cx, cy), 3)
        return
    glow = pygame.Surface((rect.w + 40, rect.h + 40), pygame.SRCALPHA)
    pygame.draw.rect(glow, (255, 230, 90, int(40 + 30 * math.sin(t * 5))), glow.get_rect(), border_radius=18)
    surf.blit(glow, (rect.x - 20, rect.y - 20))
    pygame.draw.rect(surf, (255, 195, 40), rect, border_radius=6)
    pygame.draw.rect(surf, (200, 120, 10), rect, 3, border_radius=6)
    pygame.draw.rect(surf, (255, 235, 130), (rect.x + 4, rect.y + 4, rect.w - 8, 8), border_radius=4)
    for cx, cy in ((rect.x + 7, rect.y + 7), (rect.right - 7, rect.y + 7),
                   (rect.x + 7, rect.bottom - 7), (rect.right - 7, rect.bottom - 7)):
        pygame.draw.circle(surf, (200, 120, 10), (cx, cy), 3)
    draw_text(surf, "?", 38, WHITE, (rect.centerx, rect.centery + 2), "center", shadow=(150, 80, 0))


def draw_gate(surf, rect, answered, t):
    pygame.draw.rect(surf, (60, 60, 80), (rect.x - 8, rect.y, 12, rect.h))
    pygame.draw.rect(surf, (60, 60, 80), (rect.right - 4, rect.y, 12, rect.h))
    for yy in range(rect.y + 10, rect.bottom, 28):
        pygame.draw.rect(surf, (170, 175, 195), (rect.x, yy, rect.w, 10), border_radius=4)
        pygame.draw.rect(surf, (90, 95, 115), (rect.x, yy, rect.w, 10), 2, border_radius=4)
    lock = pygame.Rect(rect.centerx - 22, rect.centery - 18, 44, 36)
    pygame.draw.rect(surf, (255, 195, 40), lock, border_radius=6)
    pygame.draw.rect(surf, (170, 110, 10), lock, 3, border_radius=6)
    pygame.draw.arc(surf, (170, 110, 10), (lock.x + 6, lock.y - 22, 32, 36), 0, math.pi, 5)
    draw_text(surf, "%d/%d" % (answered, QUESTIONS_PER_LEVEL), 20, NAVY, lock.center, "center")
    draw_text(surf, "GERBANG KUIS", 18, WHITE, (rect.centerx, rect.y - 16), "center", shadow=BLACK)


def draw_coin(surf, cx, cy, t, phase):
    w = max(4, int(abs(math.cos(t * 3.2 + phase)) * 22))
    pygame.draw.ellipse(surf, (255, 200, 30), (cx - w // 2, cy - 12, w, 24))
    pygame.draw.ellipse(surf, (200, 140, 10), (cx - w // 2, cy - 12, w, 24), 2)
    if w > 10:
        pygame.draw.ellipse(surf, (255, 240, 140), (cx - w // 4, cy - 7, max(2, w // 2), 14), 2)


def draw_flag(surf, x, t):
    pygame.draw.rect(surf, (225, 225, 235), (x - 4, GROUND_Y - 300, 8, 300))
    pygame.draw.circle(surf, (255, 215, 60), (x, GROUND_Y - 304), 9)
    wave = math.sin(t * 5) * 4
    pts = [(x + 4, GROUND_Y - 290), (x + 70, GROUND_Y - 270 + wave), (x + 4, GROUND_Y - 240)]
    pygame.draw.polygon(surf, (60, 200, 100), pts)
    pygame.draw.polygon(surf, (30, 130, 60), pts, 3)
    draw_text(surf, "GO!", 16, WHITE, (x + 26, GROUND_Y - 266 + wave / 2), "center")
    pygame.draw.rect(surf, (120, 120, 135), (x - 16, GROUND_Y - 14, 32, 14), border_radius=4)


def draw_castle(surf, x):
    body = (170, 170, 185)
    pygame.draw.rect(surf, body, (x, GROUND_Y - 150, 170, 150))
    pygame.draw.rect(surf, shade(body, 0.6), (x, GROUND_Y - 150, 170, 150), 4)
    for i in range(5):
        pygame.draw.rect(surf, body, (x + i * 36, GROUND_Y - 175, 24, 26))
        pygame.draw.rect(surf, shade(body, 0.6), (x + i * 36, GROUND_Y - 175, 24, 26), 3)
    pygame.draw.rect(surf, (90, 60, 40), (x + 62, GROUND_Y - 80, 46, 80), border_top_left_radius=23,
                     border_top_right_radius=23)
    for wx in (x + 20, x + 128):
        pygame.draw.rect(surf, (255, 225, 120), (wx, GROUND_Y - 120, 22, 30), border_radius=6)
    pygame.draw.rect(surf, (220, 60, 60), (x + 83, GROUND_Y - 220, 5, 48))
    pygame.draw.polygon(surf, (255, 215, 60), [(x + 88, GROUND_Y - 220), (x + 120, GROUND_Y - 208), (x + 88, GROUND_Y - 196)])


def draw_character(surf, x, y, facing, t, moving, air, blink=False):
    """Karakter 'Rush' (pelajar petualang). (x, y) = pojok kiri-atas kotak 34x52."""
    if blink:
        return
    s = pygame.Surface((46, 64), pygame.SRCALPHA)
    swing = math.sin(t * 0.55) * 7 if moving and not air else 0
    # tas punggung
    pygame.draw.ellipse(s, (255, 150, 40), (3, 28, 14, 20))
    pygame.draw.ellipse(s, (200, 100, 20), (3, 28, 14, 20), 2)
    # kaki
    if air:
        l1, l2 = (15, 44, 9, 12), (26, 42, 9, 10)
    else:
        l1, l2 = (15 + swing, 44, 9, 14), (26 - swing, 44, 9, 14)
    for r in (l1, l2):
        pygame.draw.rect(s, (40, 70, 175), r, border_radius=3)
        pygame.draw.rect(s, (110, 60, 30), (r[0] - 1, r[1] + r[3] - 1, r[2] + 4, 7), border_radius=3)
    # badan
    pygame.draw.rect(s, (230, 60, 60), (11, 28, 26, 16), border_radius=5)
    pygame.draw.rect(s, (45, 80, 190), (14, 34, 20, 13), border_radius=4)
    pygame.draw.rect(s, (45, 80, 190), (15, 28, 5, 8))
    pygame.draw.rect(s, (45, 80, 190), (28, 28, 5, 8))
    pygame.draw.circle(s, YELLOW, (17, 38), 2)
    pygame.draw.circle(s, YELLOW, (31, 38), 2)
    # lengan
    arm = 0 if air else swing * 0.8
    if air:
        pygame.draw.rect(s, (230, 60, 60), (33, 24, 7, 10), border_radius=3)
        pygame.draw.circle(s, (255, 205, 160), (38, 22), 5)
        pygame.draw.rect(s, (230, 60, 60), (7, 26, 7, 10), border_radius=3)
        pygame.draw.circle(s, (255, 205, 160), (8, 24), 5)
    else:
        pygame.draw.rect(s, (230, 60, 60), (33 + arm * 0.3, 30, 7, 10), border_radius=3)
        pygame.draw.circle(s, (255, 205, 160), (int(37 + arm * 0.5), 42), 5)
        pygame.draw.rect(s, (230, 60, 60), (7 - arm * 0.3, 30, 7, 10), border_radius=3)
        pygame.draw.circle(s, (255, 205, 160), (int(10 - arm * 0.5), 42), 5)
    # kepala
    pygame.draw.circle(s, (255, 205, 160), (24, 20), 13)
    pygame.draw.circle(s, (90, 55, 30), (14, 22), 6)
    pygame.draw.circle(s, WHITE, (30, 18), 5)
    pygame.draw.circle(s, BLACK, (32, 18), 2)
    pygame.draw.circle(s, (235, 170, 130), (36, 23), 4)
    pygame.draw.rect(s, (90, 55, 30), (27, 25, 10, 3), border_radius=1)
    # topi
    pygame.draw.ellipse(s, (230, 60, 60), (10, 4, 28, 18))
    pygame.draw.rect(s, (230, 60, 60), (10, 12, 28, 6))
    pygame.draw.ellipse(s, (170, 30, 30), (26, 12, 17, 7))
    pygame.draw.circle(s, WHITE, (23, 11), 6)
    draw_text(s, "S", 11, (200, 40, 40), (23, 11), "center")
    if facing < 0:
        s = pygame.transform.flip(s, True, False)
    surf.blit(s, (x - 6, y - 6 + (0 if not moving or air else int(abs(math.sin(t * 0.55)) * -1))))


def draw_bug(surf, rect, t, dead_t=0):
    """Musuh 'Bug' (kutu program)."""
    if dead_t:
        pygame.draw.ellipse(surf, (80, 170, 80), (rect.x - 4, rect.bottom - 10, rect.w + 8, 10))
        pygame.draw.ellipse(surf, (40, 100, 40), (rect.x - 4, rect.bottom - 10, rect.w + 8, 10), 2)
        return
    cx = rect.centerx
    wig = math.sin(t * 0.5) * 4
    for i, off in enumerate((-14, 0, 14)):
        d = wig if i % 2 == 0 else -wig
        pygame.draw.line(surf, (30, 80, 40), (cx + off, rect.bottom - 8), (cx + off + 6 + d, rect.bottom), 3)
        pygame.draw.line(surf, (30, 80, 40), (cx + off, rect.bottom - 8), (cx + off - 6 - d, rect.bottom), 3)
    pygame.draw.ellipse(surf, (90, 200, 90), (rect.x, rect.y + 2, rect.w, rect.h - 4))
    pygame.draw.ellipse(surf, (35, 110, 45), (rect.x, rect.y + 2, rect.w, rect.h - 4), 3)
    for sx, sy in ((cx - 10, rect.y + 8), (cx + 8, rect.y + 6), (cx, rect.y + 17)):
        pygame.draw.circle(surf, (220, 70, 70), (sx, sy), 4)
    pygame.draw.line(surf, (30, 80, 40), (cx - 8, rect.y + 3), (cx - 14, rect.y - 8), 3)
    pygame.draw.line(surf, (30, 80, 40), (cx + 8, rect.y + 3), (cx + 14, rect.y - 8), 3)
    pygame.draw.circle(surf, (220, 70, 70), (cx - 14, rect.y - 8), 3)
    pygame.draw.circle(surf, (220, 70, 70), (cx + 14, rect.y - 8), 3)
    for ex in (cx - 8, cx + 8):
        pygame.draw.circle(surf, WHITE, (ex, rect.y + 14), 6)
        pygame.draw.circle(surf, BLACK, (ex, rect.y + 15), 3)
    pygame.draw.line(surf, BLACK, (cx - 14, rect.y + 6), (cx - 4, rect.y + 10), 3)
    pygame.draw.line(surf, BLACK, (cx + 14, rect.y + 6), (cx + 4, rect.y + 10), 3)


# =============================================================================
#  OBJEK DUNIA GAME
# =============================================================================
class Solid:
    def __init__(self, rect, kind):
        self.rect = pygame.Rect(rect)
        self.kind = kind
        self.bump = 0
        self.has_hint = False
        self.used = False
        self.qidx = -1


class Coin:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(x - 12, y - 12, 24, 24)
        self.taken = False
        self.phase = random.random() * 6


class Bulb:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(x - 18, y - 22, 36, 44)
        self.taken = False


class Enemy:
    W, H = 40, 32

    def __init__(self, left, right, x, speed):
        self.left, self.right, self.x = left, right, float(x)
        self.speed = speed
        self.dir = random.choice((-1, 1))
        self.alive = True
        self.dead_t = 0
        self.t = random.random() * 10
        self.rect = pygame.Rect(0, 0, self.W, self.H)
        self.rect.midbottom = (int(x), GROUND_Y)

    def update(self):
        self.t += 1
        if not self.alive:
            self.dead_t += 1
            return
        self.x += self.dir * self.speed
        if self.x < self.left:
            self.x, self.dir = self.left, 1
        elif self.x > self.right:
            self.x, self.dir = self.right, -1
        self.rect.midbottom = (int(self.x), GROUND_Y)


class Level:
    """Level dibangun otomatis (prosedural) agar selalu bisa diselesaikan."""

    def __init__(self, n):
        self.n = n
        self.theme = THEMES[n]
        self.solids, self.coins, self.bulbs, self.enemies, self.qblocks = [], [], [], [], []
        self.gate = None
        self.flag_x = 0
        self.width = 0
        self._build()

    def add_ground(self, x0, x1):
        self.solids.append(Solid((x0, GROUND_Y, x1 - x0, HEIGHT - GROUND_Y + 300), "ground"))

    def add_pipe(self, x, h):
        self.solids.append(Solid((x, GROUND_Y - h, 70, h), "pipe"))

    def add_step(self, x, h):
        self.solids.append(Solid((x, GROUND_Y - h, 50, h), "step"))

    def add_platform(self, x, y, w):
        self.solids.append(Solid((x, y, w, 24), "platform"))

    def add_bricks(self, x, y, count, hint_idx):
        for k in range(count):
            s = Solid((x + k * 48, y, 48, 48), "brick")
            s.has_hint = (k == hint_idx)
            self.solids.append(s)

    def add_coins(self, x, y, count, gap, arc=0):
        for k in range(count):
            cy = y - (arc * math.sin(k / max(1, count - 1) * math.pi) if count > 1 else 0)
            self.coins.append(Coin(x + k * gap, int(cy)))

    def _build(self):
        n = self.n
        rng = random.Random(4242 + n * 97)
        self.add_ground(0, 520)
        x = 520
        slots = rng.sample(range(QUESTIONS_PER_LEVEL), HINTS_PER_LEVEL)
        brick_slots, hill_slots = set(slots[:2]), set(slots[2:])
        simple = ["plain", "pipe", "stairs", "platform"]
        for i in range(QUESTIONS_PER_LEVEL):
            if i > 0 and rng.random() < min(0.85, 0.4 + 0.05 * n):
                x += rng.randint(90, 115 + min(n * 5, 40))
            gx, seglen = x, 780
            self.add_ground(gx, gx + seglen)
            if i in brick_slots:
                pat = "bricks"
            elif i in hill_slots:
                pat = "hill"
            else:
                pat = rng.choice(simple)
            if pat == "plain":
                self.add_coins(gx + 120, GROUND_Y - 40, 6, 40, arc=50)
            elif pat == "pipe":
                h = rng.choice((60, 90))
                self.add_pipe(gx + 210, h)
                self.add_coins(gx + 200, GROUND_Y - h - 60, 3, 32)
            elif pat == "stairs":
                for k in range(3):
                    self.add_step(gx + 120 + k * 50, 40 * (k + 1))
                self.add_coins(gx + 120, GROUND_Y - 190, 3, 50)
            elif pat == "platform":
                self.add_platform(gx + 150, GROUND_Y - 110, 220)
                self.add_coins(gx + 170, GROUND_Y - 150, 5, 38)
            elif pat == "hill":
                self.add_platform(gx + 60, GROUND_Y - 100, 150)
                self.add_platform(gx + 250, GROUND_Y - 200, 130)
                self.bulbs.append(Bulb(gx + 315, GROUND_Y - 245))
                self.add_coins(gx + 80, GROUND_Y - 140, 4, 35)
            elif pat == "bricks":
                self.add_bricks(gx + 150, GROUND_Y - 150, 5, rng.randrange(5))
            qb = Solid((gx + 500, GROUND_Y - 150, 48, 48), "qblock")
            qb.qidx = i
            self.solids.append(qb)
            self.qblocks.append(qb)
            if n == 0 and i < 2:
                ecount = 0
            elif n > 3:
                ecount = rng.choice((0, 1, 1, 2))
            else:
                ecount = rng.choice((0, 0, 1, 1))
            for e in range(ecount):
                sp = 1.0 + 0.12 * n + rng.random() * 0.4
                self.enemies.append(Enemy(gx + 580, gx + 740, gx + 600 + e * 70, sp))
            x = gx + seglen
        self.add_ground(x, x + 700)
        gate = Solid((x + 230, GROUND_Y - 270, 24, 270), "gate")
        self.solids.append(gate)
        self.gate = gate
        self.flag_x = x + 430
        self.width = x + 700


# =============================================================================
#  PEMAIN
# =============================================================================
class Player:
    W, H = 34, 52
    ACC, MAXV, GRAV, JUMP = 0.7, 5.6, 0.62, -14.2

    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.vx = self.vy = 0.0
        self.rect = pygame.Rect(x, y, self.W, self.H)
        self.on_ground = False
        self.facing = 1
        self.coyote = 0
        self.jump_buf = 0
        self.invul = 0
        self.anim = 0.0
        self.safe = (x, y)
        self.land = None
        self.moving = False

    def press_jump(self):
        self.jump_buf = 8

    def update(self, keys, solids, on_bump, level_w):
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        held = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        d = (1 if right else 0) - (1 if left else 0)
        self.moving = d != 0
        if d:
            self.vx += d * self.ACC
            if self.vx * d < 0:
                self.vx += d * self.ACC
            self.facing = d
        else:
            self.vx *= 0.78
            if abs(self.vx) < 0.2:
                self.vx = 0.0
        self.vx = max(-self.MAXV, min(self.MAXV, self.vx))
        if self.invul:
            self.invul -= 1

        # ---- gerak horizontal
        self.x += self.vx
        self.rect.x = int(round(self.x))
        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.vx > 0:
                    self.rect.right = s.rect.left
                elif self.vx < 0:
                    self.rect.left = s.rect.right
                self.x = float(self.rect.x)
                self.vx = 0.0
        if self.rect.left < 0:
            self.rect.left = 0
            self.x, self.vx = 0.0, 0.0
        if self.rect.right > level_w:
            self.rect.right = level_w
            self.x = float(self.rect.x)

        # ---- lompat
        self.coyote -= 1
        self.jump_buf -= 1
        if self.on_ground:
            self.coyote = 6
        if self.jump_buf > 0 and self.coyote > 0:
            self.vy = self.JUMP
            self.coyote = 0
            self.jump_buf = 0
            self.on_ground = False
        if not held and self.vy < -5:
            self.vy = -5

        # ---- gerak vertikal
        self.vy = min(self.vy + self.GRAV, 17)
        self.y += self.vy
        self.rect.y = int(round(self.y))
        self.on_ground = False
        for s in solids:
            if self.rect.colliderect(s.rect):
                if self.vy >= 0:
                    self.rect.bottom = s.rect.top
                    self.on_ground = True
                    self.land = s
                elif self.vy < 0:
                    self.rect.top = s.rect.bottom
                    on_bump(s)
                self.y = float(self.rect.y)
                self.vy = 0.0
        if self.on_ground and self.land is not None and self.land.kind == "ground":
            lr = self.land.rect
            if lr.left + 50 < self.rect.left and self.rect.right < lr.right - 60:
                self.safe = (self.rect.x, self.rect.y)
        self.x = float(self.rect.x)
        self.anim += 1 + abs(self.vx) * 0.25

    def respawn(self):
        self.x, self.y = float(self.safe[0]), float(self.safe[1])
        self.rect.topleft = self.safe
        self.vx = self.vy = 0.0
        self.invul = 130


# =============================================================================
#  TOMBOL
# =============================================================================
class Button:
    def __init__(self, rect, text, action, color=ORANGE, size=28):
        self.rect = pygame.Rect(rect)
        self.text, self.action, self.color, self.size = text, action, color, size
        self.hover = 0.0
        self.enabled = True

    def update(self, mouse, focused):
        target = 1.0 if (focused or self.rect.collidepoint(mouse)) and self.enabled else 0.0
        self.hover += (target - self.hover) * 0.28

    def draw(self, surf):
        r = self.rect.inflate(int(self.hover * 16), int(self.hover * 6))
        col = self.color if self.enabled else (110, 115, 130)
        draw_rrect(surf, (0, 0, 0), r.move(0, 6), 16, alpha=90)
        draw_rrect(surf, shade(col, 0.7), r.move(0, 4), 16)
        draw_rrect(surf, mix(col, WHITE, 0.15 * self.hover), r, 16)
        draw_rrect(surf, mix(col, WHITE, 0.45), (r.x + 6, r.y + 5, r.w - 12, r.h // 3), 10, alpha=110)
        draw_rrect(surf, WHITE, r, 16, 3, alpha=200 if self.hover > 0.5 else 120)
        draw_text(surf, self.text, self.size, WHITE, r.center, "center", shadow=shade(col, 0.45))


# =============================================================================
#  GAME UTAMA
# =============================================================================
QP = pygame.Rect(60, 30, 980, 590)
OPT_X, OPT_W, OPT_H, OPT_Y0, OPT_GAP = QP.x + 40, QP.w - 80, 62, QP.y + 200, 14
HINT_RECT = pygame.Rect(QP.x + 40, QP.bottom - 70, 240, 50)


def opt_rect(i):
    return pygame.Rect(OPT_X, OPT_Y0 + i * (OPT_H + OPT_GAP), OPT_W, OPT_H)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("StudyRush - Petualangan Kuis Informatika")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.audio = Audio()
        self.save = load_save()
        self.name = self.save.get("name", "")
        self.input_text = self.name
        self.t = 0.0
        self.menu_bg = Background(THEMES[0], 1)
        self.menu_scroll = 0.0
        self.buttons, self.focus, self.card_focus = [], 0, 0
        self.particles, self.floats = [], []
        self.shake = 0.0
        self.toast = ("", 0.0)
        self.banner = None
        self.err_t = 0.0
        self.disp_score = 0.0
        self.hud_jit = 0.0
        self.heart_big = None
        self.reset_run()
        self.state = ""
        self.enter_state("start")

    # ------------------------------------------------------------------ data
    def reset_run(self):
        self.score = 0
        self.lives = START_LIVES
        self.streak = 0
        self.best_streak = 0
        self.hints = 0
        self.total_correct = 0
        self.total_wrong = 0
        self.level_idx = 0
        self.level = None
        self.player = None
        self.bg = None
        self.cam = 0.0
        self.level_questions = []
        self.lvl_correct = self.lvl_wrong = self.lvl_answered = 0
        self.level_start = (0, START_LIVES, 0)
        self.quiz = None
        self.disp_score = 0.0
        self.last_stats = {}

    def enter_state(self, st):
        self.state = st
        self.focus = 0
        builder = getattr(self, "bt_" + st, None)
        self.buttons = builder() if builder else []
        music = {"start": "start", "home": "start", "levels": "start", "howto": "start",
                 "scores": "start", "victory": "start", "play": "main", "quiz": "main",
                 "pause": "main", "levelclear": "main"}
        if st in music:
            self.audio.play_music(music[st])

    def col_menu(self, items, top, w=380, h=52, gap=12, colors=None):
        out = []
        for i, (text, action) in enumerate(items):
            col = colors[i] if colors else ORANGE
            out.append(Button((WIDTH // 2 - w // 2, top + i * (h + gap), w, h), text, action, col))
        return out

    # ------------------------------------------------------ pembuat tombol
    def bt_start(self):
        return [Button((WIDTH // 2 - 150, 478, 300, 62), "MULAI", self.submit_name, GREEN, 32)]

    def bt_home(self):
        return self.col_menu([
            ("MULAI PETUALANGAN", lambda: self.new_game(0)),
            ("PILIH LEVEL", lambda: self.enter_state("levels")),
            ("CARA BERMAIN", lambda: self.enter_state("howto")),
            ("SKOR TERTINGGI", lambda: self.enter_state("scores")),
            ("GANTI NAMA", self.change_name),
            ("KELUAR", self.quit),
        ], 205, colors=[GREEN, BLUE, ORANGE, (170, 100, 230), (60, 170, 190), RED])

    def bt_levels(self):
        return [Button((WIDTH // 2 - 130, 575, 260, 52), "KEMBALI", lambda: self.enter_state("home"), BLUE)]

    bt_howto = bt_scores = bt_levels

    def bt_pause(self):
        return self.col_menu([
            ("LANJUTKAN", lambda: self.enter_state("play")),
            ("ULANGI LEVEL", self.replay_level),
            ("BERANDA", lambda: self.enter_state("home")),
        ], 290, colors=[GREEN, ORANGE, RED])

    def bt_levelclear(self):
        last = self.level_idx >= TOTAL_LEVELS - 1
        nxt = ("LIHAT HASIL AKHIR", self.go_victory) if last else \
            ("LEVEL BERIKUTNYA", lambda: self.start_level(self.level_idx + 1))
        items = [nxt, ("ULANGI LEVEL", self.replay_level), ("BERANDA", lambda: self.enter_state("home"))]
        cols = [GREEN, ORANGE, RED]
        return [Button((60 + i * 345, 545, 320, 56), t, a, cols[i]) for i, (t, a) in enumerate(items)]

    def bt_gameover(self):
        return self.col_menu([("MAIN LAGI DARI AWAL", lambda: self.new_game(0)),
                              ("BERANDA", lambda: self.enter_state("home"))],
                             470, w=420, colors=[GREEN, BLUE])

    def bt_victory(self):
        return self.col_menu([("MAIN LAGI", lambda: self.new_game(0)),
                              ("BERANDA", lambda: self.enter_state("home"))],
                             510, w=360, colors=[GREEN, BLUE])

    # --------------------------------------------------------- aksi umum
    def submit_name(self):
        nm = self.input_text.strip()
        if not nm:
            self.err_t = 1.3
            return
        self.name = nm
        self.save["name"] = nm
        write_save(self.save)
        self.enter_state("home")

    def change_name(self):
        self.input_text = self.name
        self.enter_state("start")

    def quit(self):
        write_save(self.save)
        pygame.quit()
        sys.exit()

    def new_game(self, start_idx):
        self.reset_run()
        self.start_level(start_idx)

    def start_level(self, idx):
        self.level_idx = idx
        self.level = Level(idx)
        self.bg = Background(self.level.theme, idx + 1)
        self.player = Player(80, GROUND_Y - Player.H)
        self.cam = 0.0
        self.level_questions = build_questions(idx)
        self.lvl_correct = self.lvl_wrong = self.lvl_answered = 0
        self.level_start = (self.score, self.lives, self.hints)
        self.particles, self.floats = [], []
        self.quiz = None
        th = self.level.theme
        self.banner = {"title": "LEVEL %d" % (idx + 1), "sub": th["title"], "topic": th["topic"], "t": 3.2}
        self.toast = ("", 0.0)
        self.enter_state("play")

    def replay_level(self):
        sc, lv, hn = self.level_start
        self.score, self.lives, self.hints, self.streak = sc, lv, hn, 0
        self.start_level(self.level_idx)

    def go_gameover(self):
        self.audio.stop_music()
        self.audio.play_sfx("mati")
        self.record_score()
        self.enter_state("gameover")

    def go_victory(self):
        self.record_score()
        self.audio.play_sfx("benar")
        self.enter_state("victory")

    def record_score(self):
        top = self.save.setdefault("top", [])
        top.append({"name": self.name or "Pemain", "score": int(self.score),
                    "level": self.level_idx + 1 if self.lvl_answered else max(1, self.level_idx)})
        top.sort(key=lambda e: e["score"], reverse=True)
        self.save["top"] = top[:8]
        write_save(self.save)

    # ------------------------------------------------------ efek visual
    def burst(self, x, y, color, n=18, world=True, speed=4.5):
        for _ in range(n):
            a = random.random() * math.tau
            sp = random.random() * speed + 1
            self.particles.append(Particle(x, y, math.cos(a) * sp, math.sin(a) * sp - 2,
                                           random.randint(25, 45), color, random.randint(3, 6),
                                           0.22, world))

    def say(self, text, seconds=2.4):
        self.toast = (text, seconds)

    # ================================================================ LOOP
    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.t += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_m
                        and self.state != "start"):
                    self.audio.toggle_mute()
                    continue
                handler = getattr(self, "ev_" + self.state, None)
                if handler:
                    handler(event)
            updater = getattr(self, "up_" + self.state, None)
            if updater:
                updater(dt)
            self.err_t = max(0.0, self.err_t - dt)
            tt, tl = self.toast
            self.toast = (tt, max(0.0, tl - dt))
            self.canvas.fill((20, 20, 40))
            drawer = getattr(self, "dr_" + self.state, None)
            if drawer:
                drawer(self.canvas)
            ox = oy = 0
            if self.shake > 0:
                self.shake = max(0.0, self.shake - dt * 30)
                ox = random.randint(-int(self.shake), int(self.shake))
                oy = random.randint(-int(self.shake), int(self.shake))
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.canvas, (ox, oy))
            pygame.display.flip()

    # ============================================================ MENU UMUM
    def update_buttons(self):
        mouse = pygame.mouse.get_pos()
        for i, b in enumerate(self.buttons):
            b.update(mouse, i == self.focus)

    def ev_menu(self, event):
        if event.type == pygame.MOUSEMOTION:
            for i, b in enumerate(self.buttons):
                if b.enabled and b.rect.collidepoint(event.pos):
                    self.focus = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for b in list(self.buttons):
                if b.enabled and b.rect.collidepoint(event.pos):
                    b.action()
                    break
        elif event.type == pygame.KEYDOWN and self.buttons:
            if event.key in (pygame.K_DOWN, pygame.K_RIGHT, pygame.K_s):
                self.focus = (self.focus + 1) % len(self.buttons)
            elif event.key in (pygame.K_UP, pygame.K_LEFT, pygame.K_w):
                self.focus = (self.focus - 1) % len(self.buttons)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                self.buttons[self.focus].action()

    ev_home = ev_howto = ev_scores = ev_gameover = ev_victory = ev_levelclear = ev_menu

    def up_menu(self, dt):
        self.menu_scroll += 85 * dt
        self.update_buttons()
        self.particles = [p for p in self.particles if p.update()]
        self.floats = [f for f in self.floats if f.update()]

    up_start = up_home = up_levels = up_howto = up_scores = up_menu
    up_gameover = up_victory = up_menu

    # ---------------------------------------------------- adegan menu/latar
    def draw_menu_scene(self, surf):
        cam = self.menu_scroll
        self.menu_bg.draw(surf, cam, self.t)
        draw_ground_piece(surf, 0, WIDTH, cam, THEMES[0])
        base = int(cam // 700)
        for k in range(base - 1, base + 3):
            wx = k * 700
            draw_pipe(surf, wx + 420 - cam, GROUND_Y - 90, 70, 90)
            draw_qblock(surf, pygame.Rect(wx + 120 - cam, GROUND_Y - 170, 48, 48), False, self.t)
            draw_qblock(surf, pygame.Rect(wx + 168 - cam, GROUND_Y - 170, 48, 48), (k % 2 == 0), self.t)
            draw_bulb_icon(surf, int(wx + 560 - cam), int(GROUND_Y - 120 + math.sin(self.t * 3 + k) * 8),
                           22, self.t)
        bx = WIDTH - ((self.t * 70) % (WIDTH + 200))
        draw_bug(surf, pygame.Rect(int(bx), GROUND_Y - 32, 40, 32), self.t * 20)
        ph = self.t % 2.8
        jump = math.sin(ph / 1.0 * math.pi) * 130 if ph < 1.0 else 0
        draw_character(surf, 170, int(GROUND_Y - Player.H - jump), 1, self.t * 12, True, jump > 0)

    def draw_buttons(self, surf):
        for b in self.buttons:
            b.draw(surf)

    def draw_title(self, surf, cy, size=96):
        word = "StudyRush"
        font = get_font(size, True)
        colors = [(255, 90, 90), (255, 160, 50), (255, 220, 60), (110, 220, 90), (70, 190, 255),
                  (120, 120, 255), (200, 100, 240), (255, 100, 170), (255, 255, 255)]
        total = sum(font.size(c)[0] for c in word)
        x = WIDTH // 2 - total // 2
        for i, ch in enumerate(word):
            w = font.size(ch)[0]
            y = cy + math.sin(self.t * 3 + i * 0.55) * 9
            for dx, dy in ((4, 6), (-2, 3)):
                surf.blit(font.render(ch, True, (30, 20, 60)), (x + dx, y + dy))
            surf.blit(font.render(ch, True, colors[i % len(colors)]), (x, y))
            x += w

    def draw_panel(self, surf, rect, alpha=215, color=(18, 24, 60)):
        draw_rrect(surf, (0, 0, 0), pygame.Rect(rect).move(0, 8), 26, alpha=80)
        draw_rrect(surf, color, rect, 26, alpha=alpha)
        draw_rrect(surf, WHITE, rect, 26, 3, alpha=140)

    # ---------------------------------------------------------- START PAGE
    def ev_start(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_name()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                if self.name:
                    self.enter_state("home")
            elif event.unicode and event.unicode.isprintable() and len(self.input_text) < 14:
                self.input_text += event.unicode
        else:
            self.ev_menu(event)

    def dr_start(self, surf):
        self.draw_menu_scene(surf)
        self.draw_title(surf, 120)
        draw_text(surf, "Petualangan Kuis Informatika  -  SMK Kelas 10", 28, WHITE,
                  (WIDTH // 2, 255), "center", shadow=NAVY)
        self.draw_panel(surf, (WIDTH // 2 - 270, 290, 540, 270), 190)
        draw_text(surf, "Masukkan namamu, Petualang!", 28, WHITE, (WIDTH // 2, 328), "center")
        shake = int(math.sin(self.t * 60) * 8) if self.err_t > 0 else 0
        box = pygame.Rect(WIDTH // 2 - 200 + shake, 365, 400, 60)
        draw_rrect(surf, WHITE, box, 16)
        draw_rrect(surf, RED if self.err_t > 0 else ORANGE, box, 16, 4)
        cursor = "|" if int(self.t * 2) % 2 == 0 else ""
        draw_text(surf, self.input_text + cursor, 34, NAVY, box.center, "center")
        if self.err_t > 0:
            draw_text(surf, "Nama tidak boleh kosong ya!", 22, (255, 140, 140),
                      (WIDTH // 2, 445), "center")
        else:
            draw_text(surf, "Tekan ENTER atau klik MULAI", 20, (200, 210, 255),
                      (WIDTH // 2, 445), "center", bold=False)
        self.draw_buttons(surf)
        draw_text(surf, "M = suara on/off", 18, WHITE, (WIDTH - 14, HEIGHT - 12), "bottomright",
                  bold=False, shadow=BLACK)

    # ----------------------------------------------------------- HOME PAGE
    def dr_home(self, surf):
        self.draw_menu_scene(surf)
        self.draw_title(surf, 28, 78)
        draw_text(surf, "Halo, %s!  Siap berpetualang?" % self.name, 30, WHITE,
                  (WIDTH // 2, 158), "center", shadow=NAVY)
        self.draw_buttons(surf)
        best = self.save.get("top", [])
        if best:
            draw_text(surf, "Skor terbaik: %d" % best[0]["score"], 22, YELLOW,
                      (WIDTH - 20, 20), "topright", shadow=BLACK)
        draw_text(surf, "Level terbuka: %d/%d" % (self.save.get("unlocked", 1), TOTAL_LEVELS), 22,
                  WHITE, (20, 20), "topleft", shadow=BLACK)

    # --------------------------------------------------------- PILIH LEVEL
    def card_rect(self, i):
        col, row = i % 5, i // 5
        return pygame.Rect(39 + col * 208, 150 + row * 200, 190, 180)

    def ev_levels(self, event):
        unlocked = self.save.get("unlocked", 1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(TOTAL_LEVELS):
                if self.card_rect(i).collidepoint(event.pos) and i < unlocked:
                    self.new_game(i)
                    return
            self.ev_menu(event)
        elif event.type == pygame.MOUSEMOTION:
            for i in range(TOTAL_LEVELS):
                if self.card_rect(i).collidepoint(event.pos):
                    self.card_focus = i
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.card_focus = (self.card_focus + 1) % TOTAL_LEVELS
            elif event.key == pygame.K_LEFT:
                self.card_focus = (self.card_focus - 1) % TOTAL_LEVELS
            elif event.key == pygame.K_DOWN:
                self.card_focus = (self.card_focus + 5) % TOTAL_LEVELS
            elif event.key == pygame.K_UP:
                self.card_focus = (self.card_focus - 5) % TOTAL_LEVELS
            elif event.key == pygame.K_RETURN and self.card_focus < unlocked:
                self.new_game(self.card_focus)
            elif event.key == pygame.K_ESCAPE:
                self.enter_state("home")

    def dr_levels(self, surf):
        self.draw_menu_scene(surf)
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((10, 15, 40, 150))
        surf.blit(dim, (0, 0))
        draw_text(surf, "PILIH LEVEL", 56, WHITE, (WIDTH // 2, 70), "center", shadow=NAVY)
        draw_text(surf, "Selesaikan level untuk membuka level berikutnya", 22, (200, 215, 255),
                  (WIDTH // 2, 115), "center", bold=False)
        unlocked = self.save.get("unlocked", 1)
        best = self.save.get("level_best", {})
        for i in range(TOTAL_LEVELS):
            r = self.card_rect(i)
            th = THEMES[i]
            open_ = i < unlocked
            sel = (i == self.card_focus)
            rr = r.inflate(10, 10) if sel else r
            col = th["accent"] if open_ else (70, 75, 95)
            draw_rrect(surf, (0, 0, 0), rr.move(0, 6), 18, alpha=90)
            draw_rrect(surf, shade(col, 0.55), rr, 18)
            draw_rrect(surf, col, (rr.x + 4, rr.y + 4, rr.w - 8, 62), 14)
            draw_rrect(surf, WHITE, rr, 18, 3 if sel else 2, alpha=230 if sel else 120)
            draw_text(surf, str(i + 1), 44, WHITE, (rr.centerx, rr.y + 36), "center", shadow=BLACK)
            if open_:
                for k, line in enumerate(wrap_text(th["title"], get_font(19, True), rr.w - 18)[:2]):
                    draw_text(surf, line, 19, WHITE, (rr.centerx, rr.y + 90 + k * 22), "center")
                for k, line in enumerate(wrap_text(th["topic"], get_font(16, False), rr.w - 18)[:2]):
                    draw_text(surf, line, 16, (225, 230, 250), (rr.centerx, rr.y + 138 + k * 18),
                              "center", bold=False)
                bs = best.get(str(i))
                if bs:
                    draw_text(surf, "Best %d" % bs, 16, YELLOW, (rr.centerx, rr.bottom - 14), "center")
            else:
                pygame.draw.rect(surf, (200, 200, 215), (rr.centerx - 18, rr.y + 100, 36, 30), border_radius=6)
                pygame.draw.arc(surf, (200, 200, 215), (rr.centerx - 13, rr.y + 78, 26, 40), 0, math.pi, 5)
                draw_text(surf, "Terkunci", 18, (190, 195, 215), (rr.centerx, rr.y + 150), "center")
        self.draw_buttons(surf)

    # --------------------------------------------------------- CARA BERMAIN
    def dr_howto(self, surf):
        self.draw_menu_scene(surf)
        self.draw_panel(surf, (70, 40, WIDTH - 140, 515), 225)
        draw_text(surf, "CARA BERMAIN", 46, YELLOW, (WIDTH // 2, 82), "center", shadow=BLACK)
        lines = [
            ("Gerak", "Panah kiri/kanan atau A / D. Lompat: Spasi, Panah atas, atau W."),
            ("Blok ?", "Sundul atau sentuh blok '?' untuk membuka soal. Ada 10 soal tiap level."),
            ("Gerbang", "Jawab semua 10 soal agar gerbang terkunci terbuka, lalu capai bendera!"),
            ("Hint", "Lampu bohlam dan BLOK BATA TERSEMBUNYI menyimpan hint. Cari dulu hintnya!"),
            ("Pakai hint", "Saat soal muncul, tekan H atau klik tombol HINT: 2 jawaban salah dihapus."),
            ("Nyawa", "Salah jawab, waktu habis, tersentuh Bug, atau jatuh = nyawa berkurang."),
            ("Bug", "Injak Bug dari atas untuk mengalahkannya (+50 poin). Jangan disentuh dari samping!"),
            ("Streak Rush", "Jawab benar beruntun! Mulai streak 3 poin berlipat (hingga x5) dan RUSH aktif."),
            ("Bonus", "Setiap kelipatan 5 streak: +1 nyawa. Selesai level: +2 nyawa. 10/10 benar: +500."),
            ("Tombol lain", "ESC = jeda,  M = suara on/off,  1-4 atau A-D = pilih jawaban."),
        ]
        y = 120
        for head, body in lines:
            draw_text(surf, head, 22, (255, 190, 90), (100, y), "topleft")
            draw_text(surf, body, 20, WHITE, (255, y + 1), "topleft", bold=False)
            y += 42
        self.draw_buttons(surf)

    # ---------------------------------------------------------- SKOR TINGGI
    def dr_scores(self, surf):
        self.draw_menu_scene(surf)
        self.draw_panel(surf, (230, 60, WIDTH - 460, 495), 225)
        draw_text(surf, "SKOR TERTINGGI", 46, YELLOW, (WIDTH // 2, 105), "center", shadow=BLACK)
        top = self.save.get("top", [])
        if not top:
            draw_text(surf, "Belum ada skor. Ayo main dulu!", 26, WHITE, (WIDTH // 2, 300), "center")
        medals = [(255, 215, 60), (205, 210, 225), (205, 130, 70)]
        for i, e in enumerate(top[:8]):
            y = 160 + i * 48
            row = pygame.Rect(260, y, WIDTH - 520, 42)
            draw_rrect(surf, (255, 255, 255), row, 12, alpha=30)
            pygame.draw.circle(surf, medals[i] if i < 3 else (90, 100, 150), (row.x + 24, row.centery), 16)
            draw_text(surf, str(i + 1), 20, BLACK if i < 3 else WHITE, (row.x + 24, row.centery), "center")
            draw_text(surf, e["name"], 24, WHITE, (row.x + 56, row.centery), "midleft")
            draw_text(surf, "Lv %d" % e.get("level", 1), 20, (180, 200, 255), (row.right - 170, row.centery), "midright")
            draw_text(surf, str(e["score"]), 26, YELLOW, (row.right - 14, row.centery), "midright")
        self.draw_buttons(surf)

    # ================================================================ PLAY
    def ev_play(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                self.player.press_jump()
            elif event.key == pygame.K_ESCAPE:
                self.enter_state("pause")

    def on_bump(self, s):
        if s.kind not in ("brick", "qblock"):
            return
        s.bump = 10
        if s.kind == "brick" and s.has_hint:
            s.has_hint = False
            s.used = True
            self.hints += 1
            self.burst(s.rect.centerx, s.rect.top, (255, 235, 90), 26)
            self.floats.append(FloatText(s.rect.centerx, s.rect.top - 20, "HINT DITEMUKAN! +1", YELLOW, 28, 80))
            self.say("Kamu menemukan HINT tersembunyi!  (tekan H saat menjawab soal)")

    def lose_life(self, source):
        """Kurangi nyawa karena musuh/jatuh (nyawa karena kuis ditangani terpisah)."""
        self.lives -= 1
        self.audio.play_sfx("nyawa")
        self.shake = 12
        self.hud_jit = 1.0
        p = self.player
        self.burst(p.rect.centerx, p.rect.centery, (255, 90, 90), 24)
        self.floats.append(FloatText(p.rect.centerx, p.rect.top - 10, "-1 NYAWA", (255, 110, 110), 30, 60))
        self.streak = 0
        if self.lives <= 0:
            self.go_gameover()
            return True
        return False

    def up_play(self, dt):
        lv, p = self.level, self.player
        keys = pygame.key.get_pressed()
        for s in lv.solids:
            if s.bump > 0:
                s.bump -= 1
        p.update(keys, lv.solids, self.on_bump, lv.width)

        # ---- blok soal
        for qb in lv.qblocks:
            if not qb.used and p.rect.inflate(8, 8).colliderect(qb.rect):
                self.open_quiz(qb)
                return
        # ---- gerbang
        if lv.gate in lv.solids and self.lvl_answered >= QUESTIONS_PER_LEVEL:
            lv.solids.remove(lv.gate)
            self.burst(lv.gate.rect.centerx, lv.gate.rect.centery, (255, 220, 90), 40)
            self.say("GERBANG TERBUKA! Menujulah ke bendera!", 3.0)
        # ---- koin & bohlam
        for c in lv.coins:
            if not c.taken and p.rect.colliderect(c.rect):
                c.taken = True
                self.score += 10
                self.burst(c.x, c.y, (255, 220, 60), 8, speed=3)
                self.floats.append(FloatText(c.x, c.y - 14, "+10", YELLOW, 20, 35))
        for b in lv.bulbs:
            if not b.taken and p.rect.colliderect(b.rect):
                b.taken = True
                self.hints += 1
                self.burst(b.x, b.y, (255, 240, 120), 28)
                self.floats.append(FloatText(b.x, b.y - 30, "HINT +1", YELLOW, 28, 70))
                self.say("HINT didapat!  Tekan H saat menjawab soal untuk memakainya.")
        # ---- musuh
        for e in lv.enemies:
            e.update()
            if e.alive and p.rect.colliderect(e.rect):
                if p.vy > 0 and p.rect.bottom - e.rect.top < 26:
                    e.alive = False
                    p.vy = -9.5
                    p.y = float(p.rect.y)
                    self.score += 50
                    self.burst(e.rect.centerx, e.rect.centery, (120, 230, 120), 16)
                    self.floats.append(FloatText(e.rect.centerx, e.rect.top - 10, "+50", (160, 255, 160), 24, 45))
                elif p.invul == 0:
                    p.invul = 120
                    p.vy = -8
                    p.vx = -p.facing * 7
                    if self.lose_life("bug"):
                        return
        lv.enemies = [e for e in lv.enemies if e.alive or e.dead_t < 25]
        # ---- jatuh ke jurang
        if p.rect.top > HEIGHT + 60:
            if self.lose_life("jatuh"):
                return
            p.respawn()
        # ---- bendera
        if p.rect.right >= lv.flag_x and self.lvl_answered >= QUESTIONS_PER_LEVEL:
            self.finish_level()
            return
        # ---- kamera
        target = p.rect.centerx - WIDTH * 0.4
        self.cam += (target - self.cam) * 0.12
        self.cam = max(0, min(self.cam, lv.width - WIDTH))
        # ---- efek & HUD
        self.particles = [q for q in self.particles if q.update()]
        self.floats = [f for f in self.floats if f.update()]
        self.disp_score += (self.score - self.disp_score) * 0.15
        if abs(self.score - self.disp_score) < 1:
            self.disp_score = self.score
        self.hud_jit = max(0.0, self.hud_jit - dt * 1.6)
        if self.banner:
            self.banner["t"] -= dt
            if self.banner["t"] <= 0:
                self.banner = None

    def finish_level(self):
        correct = self.lvl_correct
        bonus = 500 if correct == QUESTIONS_PER_LEVEL else 0
        self.score += bonus
        old = self.lives
        self.lives = min(MAX_LIVES, self.lives + 2)
        stars = 3 if correct >= 9 else 2 if correct >= 7 else 1 if correct >= 5 else 0
        gained = self.score - self.level_start[0]
        self.last_stats = {"correct": correct, "wrong": self.lvl_wrong, "bonus": bonus,
                           "stars": stars, "gained": gained, "heal": self.lives - old}
        self.save["unlocked"] = max(self.save.get("unlocked", 1), min(TOTAL_LEVELS, self.level_idx + 2))
        lb = self.save.setdefault("level_best", {})
        key = str(self.level_idx)
        lb[key] = max(lb.get(key, 0), int(gained))
        write_save(self.save)
        self.audio.play_sfx("benar")
        self.burst(WIDTH // 2, 200, (255, 220, 90), 60, world=False, speed=7)
        self.enter_state("levelclear")

    # ----------------------------------------------------- gambar dunia
    def draw_world(self, surf):
        lv, p, cam = self.level, self.player, int(self.cam)
        self.bg.draw(surf, cam, self.t)
        th = lv.theme
        draw_castle(surf, lv.flag_x + 110 - cam)
        draw_flag(surf, lv.flag_x - cam, self.t)
        for s in lv.solids:
            if s.rect.right < cam - 20 or s.rect.left > cam + WIDTH + 20:
                continue
            r = s.rect.move(-cam, 0)
            off = -int(math.sin(s.bump / 10 * math.pi) * 9) if s.bump > 0 else 0
            if s.kind == "ground":
                draw_ground_piece(surf, r.x, r.w, cam, th)
            elif s.kind == "pipe":
                draw_pipe(surf, r.x, r.y, r.w, r.h)
            elif s.kind == "step":
                draw_step(surf, r)
            elif s.kind == "platform":
                draw_platform(surf, r, th)
            elif s.kind == "brick":
                draw_brick(surf, r.move(0, off), s.used, self.t)
            elif s.kind == "qblock":
                draw_qblock(surf, r.move(0, off), s.used, self.t)
            elif s.kind == "gate":
                draw_gate(surf, r, self.lvl_answered, self.t)
        for c in lv.coins:
            if not c.taken and cam - 30 < c.x < cam + WIDTH + 30:
                draw_coin(surf, c.x - cam, c.y, self.t, c.phase)
        for b in lv.bulbs:
            if not b.taken and cam - 40 < b.x < cam + WIDTH + 40:
                draw_bulb_icon(surf, b.x - cam, int(b.y + math.sin(self.t * 3 + b.x) * 6), 26, self.t)
        for e in lv.enemies:
            if cam - 60 < e.rect.x < cam + WIDTH + 60:
                draw_bug(surf, e.rect.move(-cam, 0), e.t, e.dead_t if not e.alive else 0)
        blink = p.invul > 0 and (p.invul // 5) % 2 == 0
        draw_character(surf, p.rect.x - cam, p.rect.y, p.facing, p.anim, p.moving, not p.on_ground, blink)
        for q in self.particles:
            if q.world:
                q.draw(surf, cam)
        for f in self.floats:
            if f.world:
                f.draw(surf, cam)
        self.draw_rush_glow(surf)
        self.draw_hud(surf)
        self.draw_overlay_text(surf)

    def draw_rush_glow(self, surf):
        if self.streak < RUSH_STREAK:
            return
        a = int(55 + 35 * math.sin(self.t * 8))
        edge = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(10):
            pygame.draw.rect(edge, (255, 120, 20, max(0, a - i * 6)), (i * 5, i * 5, WIDTH - i * 10, HEIGHT - i * 10), 5)
        surf.blit(edge, (0, 0))

    def draw_hud(self, surf):
        jit = lambda: int(random.uniform(-4, 4) * self.hud_jit)
        bar = pygame.Rect(10, 8, WIDTH - 20, 62)
        draw_rrect(surf, (10, 15, 40), bar, 18, alpha=185)
        draw_rrect(surf, WHITE, bar, 18, 2, alpha=110)
        # nyawa
        shown = max(START_LIVES, self.lives)
        for i in range(shown):
            cx, cy = 34 + i * 31 + jit(), 38 + jit()
            if i < self.lives:
                draw_heart(surf, cx, cy, 26, (240, 60, 80), (90, 10, 30))
            else:
                draw_heart(surf, cx, cy, 24, (60, 60, 80), (30, 30, 45))
        # skor
        draw_text(surf, "SKOR", 15, (160, 180, 230), (262, 14))
        draw_text(surf, "%d" % self.disp_score, 30, WHITE, (262, 28), shadow=BLACK)
        # streak
        sx = 430
        hot = self.streak >= RUSH_STREAK
        box = pygame.Rect(sx, 14, 215, 50)
        draw_rrect(surf, (255, 120, 20) if hot else (40, 50, 95), box, 14, alpha=235 if hot else 200)
        draw_rrect(surf, YELLOW if hot else (120, 135, 200), box, 14, 2)
        if hot:
            draw_flame(surf, box.x + 26, box.bottom - 8, 40, self.t)
        draw_text(surf, "STREAK %d" % self.streak, 20, WHITE, (box.x + 52, box.y + 6))
        mult = streak_multiplier(self.streak)
        draw_text(surf, ("RUSH x%.1f" % mult) if hot else "x%.1f" % mult, 18,
                  YELLOW if hot else (190, 200, 235), (box.x + 52, box.y + 27), bold=True)
        # hint
        draw_bulb_icon(surf, 676, 40, 22, self.t, glow=self.hints > 0)
        draw_text(surf, "x%d" % self.hints, 26, YELLOW if self.hints else GRAY, (698, 40), "midleft", shadow=BLACK)
        # level & soal
        draw_text(surf, "LEVEL %d" % (self.level_idx + 1), 20, (255, 200, 120), (775, 14))
        draw_text(surf, "Soal %d/%d" % (self.lvl_answered, QUESTIONS_PER_LEVEL), 22, WHITE, (775, 38))
        draw_text(surf, self.name, 20, (200, 215, 255), (WIDTH - 24, 14), "topright")
        draw_text(surf, "SUARA %s" % ("OFF" if self.audio.muted else "ON"), 14, GRAY, (WIDTH - 24, 44), "topright", bold=False)
        # progres
        prog = max(0.0, min(1.0, self.player.rect.centerx / self.level.flag_x))
        pb = pygame.Rect(30, 76, WIDTH - 60, 8)
        draw_rrect(surf, (0, 0, 0), pb, 4, alpha=110)
        draw_rrect(surf, (110, 230, 140), (pb.x, pb.y, int(pb.w * prog), pb.h), 4)
        pygame.draw.circle(surf, WHITE, (pb.x + int(pb.w * prog), pb.centery), 8)

    def draw_overlay_text(self, surf):
        if self.banner:
            b = self.banner
            a = int(255 * min(1.0, b["t"] / 0.8)) if b["t"] < 0.8 else 255
            slide = int((1 - ease_out((3.2 - b["t"]) / 0.5)) * 60)
            draw_text(surf, b["title"], 70, WHITE, (WIDTH // 2, 190 - slide), "center", shadow=NAVY, alpha=a)
            draw_text(surf, b["sub"], 38, YELLOW, (WIDTH // 2, 252 - slide), "center", shadow=BLACK, alpha=a)
            draw_text(surf, "Materi: " + b["topic"], 24, WHITE, (WIDTH // 2, 295 - slide), "center",
                      shadow=BLACK, alpha=a, bold=False)
        text, left = self.toast
        if left > 0:
            a = int(255 * min(1.0, left / 0.5))
            r = draw_text(surf, text, 24, WHITE, (WIDTH // 2, HEIGHT - 40), "center", alpha=0)
            box = r.inflate(40, 18)
            draw_rrect(surf, (10, 15, 40), box, 16, alpha=min(210, a))
            draw_text(surf, text, 24, WHITE, (WIDTH // 2, HEIGHT - 40), "center", alpha=a)
        if self.level_idx == 0 and self.lvl_answered == 0 and self.t % 100 < 100 and not self.banner:
            if self.player.rect.x < 700:
                draw_text(surf, "Panah / A D = gerak     Spasi = lompat     ESC = jeda", 20, WHITE,
                          (WIDTH // 2, 108), "center", shadow=BLACK)

    def dr_play(self, surf):
        self.draw_world(surf)
        for q in self.particles:
            if not q.world:
                q.draw(surf, 0)

    # ---------------------------------------------------------------- PAUSE
    def ev_pause(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.enter_state("play")
        else:
            self.ev_menu(event)

    def up_pause(self, dt):
        self.update_buttons()

    def dr_pause(self, surf):
        self.draw_world(surf)
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((5, 8, 25, 170))
        surf.blit(dim, (0, 0))
        draw_text(surf, "JEDA", 80, WHITE, (WIDTH // 2, 170), "center", shadow=NAVY)
        self.draw_buttons(surf)

    # ================================================================= QUIZ
    def open_quiz(self, block):
        block.used = True
        block.bump = 10
        self.lvl_answered += 1
        q = self.level_questions[block.qidx]
        self.quiz = {"q": q, "block": block, "left": QUESTION_TIME, "elim": set(), "chosen": None,
                     "phase": "ask", "pt": 0.0, "age": 0.0, "correct": False, "hint_used": False,
                     "gain": 0, "msg": "", "msg_t": 0.0, "timeout": False, "split_done": False}
        self.player.vx = 0
        self.audio.play_music("main")
        self.state = "quiz"
        self.focus = 0
        self.buttons = []

    def use_hint(self):
        qz = self.quiz
        if qz["phase"] != "ask" or qz["hint_used"]:
            return
        if self.hints <= 0:
            qz["msg"] = "Belum punya hint! Cari bohlam & blok bata tersembunyi di dunia game."
            qz["msg_t"] = 2.6
            return
        wrong = [i for i in range(4) if i != qz["q"]["ans"] and i not in qz["elim"]]
        random.shuffle(wrong)
        qz["elim"].update(wrong[:2])
        qz["hint_used"] = True
        self.hints -= 1
        qz["msg"] = "Hint dipakai: 2 jawaban salah dihapus! (poin dasar -%d)" % HINT_PENALTY
        qz["msg_t"] = 3.0

    def answer(self, idx):
        qz = self.quiz
        if qz["phase"] != "ask":
            return
        q = qz["q"]
        qz["chosen"] = idx
        qz["phase"], qz["pt"] = "result", 0.0
        qz["timeout"] = idx is None
        qz["correct"] = (idx == q["ans"])
        b = qz["block"]
        if qz["correct"]:
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            self.lvl_correct += 1
            self.total_correct += 1
            mult = streak_multiplier(self.streak)
            base = BASE_POINTS - (HINT_PENALTY if qz["hint_used"] else 0)
            bonus = int(50 * max(0.0, qz["left"]) / QUESTION_TIME)
            qz["gain"] = int((base + bonus) * mult)
            self.score += qz["gain"]
            self.audio.play_sfx("benar")
            self.burst(b.rect.centerx, b.rect.centery, (255, 230, 90), 28)
            extra = ""
            if self.streak % 5 == 0 and self.lives < MAX_LIVES:
                self.lives += 1
                extra = "  +1 NYAWA!"
            qz["msg"] = "BENAR!  +%d poin  (x%.1f)%s" % (qz["gain"], mult, extra)
            if self.streak == RUSH_STREAK:
                qz["msg"] += "   RUSH AKTIF!"
            self.floats.append(FloatText(b.rect.centerx, b.rect.top - 10, "+%d" % qz["gain"], YELLOW, 32, 70))
        else:
            self.streak = 0
            self.lvl_wrong += 1
            self.total_wrong += 1
            self.audio.play_sfx("salah")
            self.burst(b.rect.centerx, b.rect.centery, (255, 100, 100), 22)
            qz["msg"] = "WAKTU HABIS!" if qz["timeout"] else "SALAH!  Streak kembali ke 0"

    def ev_quiz(self, event):
        qz = self.quiz
        if event.type == pygame.KEYDOWN:
            keymap = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3,
                      pygame.K_a: 0, pygame.K_b: 1, pygame.K_c: 2, pygame.K_d: 3,
                      pygame.K_KP1: 0, pygame.K_KP2: 1, pygame.K_KP3: 2, pygame.K_KP4: 3}
            if event.key in keymap and keymap[event.key] not in qz["elim"]:
                self.answer(keymap[event.key])
            elif event.key == pygame.K_h:
                self.use_hint()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(4):
                if opt_rect(i).collidepoint(event.pos) and i not in qz["elim"]:
                    self.answer(i)
                    return
            if HINT_RECT.collidepoint(event.pos):
                self.use_hint()

    def up_quiz(self, dt):
        qz = self.quiz
        qz["pt"] += dt
        qz["age"] += dt
        qz["msg_t"] = max(0.0, qz["msg_t"] - dt)
        self.particles = [q for q in self.particles if q.update()]
        self.floats = [f for f in self.floats if f.update()]
        self.disp_score += (self.score - self.disp_score) * 0.15
        self.hud_jit = max(0.0, self.hud_jit - dt * 1.6)
        if qz["phase"] == "ask":
            qz["left"] -= dt
            if qz["left"] <= 0:
                qz["left"] = 0
                self.answer(None)
        elif qz["phase"] == "result":
            if qz["pt"] > (1.4 if qz["correct"] else 1.2):
                if qz["correct"]:
                    self.close_quiz()
                else:
                    qz["phase"], qz["pt"] = "life", 0.0
                    self.lives -= 1
                    self.audio.play_sfx("nyawa")
                    self.hud_jit = 1.0
                    self.shake = 10
        elif qz["phase"] == "life":
            if qz["pt"] > 0.45 and not qz["split_done"]:
                qz["split_done"] = True
                self.burst(WIDTH // 2, 330, (255, 90, 110), 34, world=False, speed=6)
            if qz["pt"] > 1.7:
                if self.lives <= 0:
                    self.go_gameover()
                else:
                    self.close_quiz()

    def close_quiz(self):
        self.quiz = None
        self.player.invul = max(self.player.invul, 40)
        self.enter_state("play")

    # --------------------------------------------------------- gambar kuis
    def get_big_heart(self):
        if self.heart_big is None:
            s = pygame.Surface((160, 160), pygame.SRCALPHA)
            draw_heart(s, 80, 70, 120, (240, 50, 80), (100, 10, 35))
            self.heart_big = s
        return self.heart_big

    def dr_quiz(self, surf):
        qz = self.quiz
        self.draw_world(surf)
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((8, 10, 30, 175))
        surf.blit(dim, (0, 0))
        th = self.level.theme
        acc = th["accent"]
        hot = self.streak >= RUSH_STREAK
        pop = ease_out(qz["age"] / 0.28)
        oy = int((1 - pop) * -50)
        panel = QP.move(0, oy)
        draw_rrect(surf, (0, 0, 0), panel.move(0, 8), 28, alpha=90)
        draw_rrect(surf, (252, 249, 238), panel, 28)
        glow_col = (255, 140, 30) if hot else acc
        draw_rrect(surf, glow_col, panel, 28, 5)
        head = pygame.Rect(panel.x, panel.y, panel.w, 56)
        pygame.draw.rect(surf, acc, head, border_top_left_radius=28, border_top_right_radius=28)
        idx = self.lvl_answered
        draw_text(surf, "SOAL %d / %d" % (idx, QUESTIONS_PER_LEVEL), 28, WHITE, (panel.x + 30, panel.y + 28),
                  "midleft", shadow=shade(acc, 0.5))
        draw_text(surf, th["topic"], 20, WHITE, (panel.centerx, panel.y + 28), "center", bold=False)
        chip = pygame.Rect(panel.right - 250, panel.y + 8, 232, 40)
        draw_rrect(surf, (255, 120, 20) if hot else shade(acc, 0.6), chip, 14)
        if hot:
            draw_flame(surf, chip.x + 22, chip.bottom - 4, 34, self.t)
        draw_text(surf, "STREAK %d  x%.1f" % (self.streak, streak_multiplier(self.streak)), 20, WHITE,
                  (chip.x + 48, chip.centery), "midleft")
        # timer
        tb = pygame.Rect(panel.x + 40, panel.y + 70, panel.w - 140, 16)
        frac = max(0.0, qz["left"] / QUESTION_TIME)
        col = (60, 200, 100) if frac > 0.5 else (255, 190, 40) if frac > 0.25 else (235, 70, 70)
        draw_rrect(surf, (210, 215, 230), tb, 8)
        if frac > 0:
            draw_rrect(surf, col, (tb.x, tb.y, int(tb.w * frac), tb.h), 8)
        draw_text(surf, "%ds" % math.ceil(qz["left"]), 22, NAVY, (tb.right + 14, tb.centery), "midleft")
        # teks soal
        q = qz["q"]
        size = 29
        lines = wrap_text(q["text"], get_font(size, True), panel.w - 90)
        if len(lines) > 3:
            size = 24
            lines = wrap_text(q["text"], get_font(size, True), panel.w - 90)
        for i, ln in enumerate(lines[:4]):
            draw_text(surf, ln, size, NAVY, (panel.x + 45, panel.y + 102 + i * (size + 8)))
        # pilihan jawaban
        mouse = pygame.mouse.get_pos()
        for i in range(4):
            r = opt_rect(i).move(0, oy)
            elim = i in qz["elim"]
            base, border, txt = WHITE, (150, 160, 200), NAVY
            if qz["phase"] == "ask":
                if r.collidepoint(mouse) and not elim:
                    base, border = (225, 238, 255), acc
                    r = r.inflate(10, 4)
            else:
                if i == q["ans"]:
                    base, border, txt = (170, 240, 185), (40, 170, 80), (10, 70, 30)
                elif i == qz["chosen"]:
                    base, border, txt = (255, 185, 185), (220, 60, 60), (110, 10, 10)
            if elim:
                base, border, txt = (225, 227, 235), (190, 195, 210), (165, 170, 185)
            draw_rrect(surf, base, r, 18)
            draw_rrect(surf, border, r, 18, 3)
            circ = (r.x + 36, r.centery)
            pygame.draw.circle(surf, border if not elim else (190, 195, 210), circ, 20)
            draw_text(surf, "ABCD"[i], 26, WHITE, circ, "center")
            fs = 25 if get_font(25, True).size(q["options"][i])[0] < r.w - 120 else 20
            draw_text(surf, q["options"][i], fs, txt, (r.x + 72, r.centery), "midleft")
            if elim:
                pygame.draw.line(surf, (200, 90, 90), (r.x + 66, r.centery), (r.right - 24, r.centery), 3)
        # tombol hint
        hr = HINT_RECT.move(0, oy)
        can = self.hints > 0 and qz["phase"] == "ask" and not qz["hint_used"]
        hcol = (255, 190, 40) if can else (185, 190, 205)
        if can and hr.collidepoint(mouse):
            hr = hr.inflate(8, 4)
        draw_rrect(surf, shade(hcol, 0.7), hr.move(0, 4), 16)
        draw_rrect(surf, hcol, hr, 16)
        draw_bulb_icon(surf, hr.x + 30, hr.centery, 22, self.t, glow=can)
        draw_text(surf, "HINT [H]  x%d" % self.hints, 24, WHITE if can else (120, 125, 140),
                  (hr.x + 58, hr.centery), "midleft")
        # pesan
        msg_col = NAVY
        if qz["phase"] != "ask":
            msg_col = (30, 150, 70) if qz["correct"] else (210, 50, 50)
        if qz["msg"] and (qz["phase"] != "ask" or qz["msg_t"] > 0):
            draw_text(surf, qz["msg"], 24 if qz["phase"] == "ask" else 28, msg_col,
                      (panel.x + 310, panel.bottom - 45 + 0), "midleft")
        elif qz["phase"] == "ask":
            draw_text(surf, "Klik jawaban atau tekan 1-4 / A-D", 20, (110, 120, 160),
                      (panel.x + 310, panel.bottom - 45), "midleft", bold=False)
        # animasi nyawa berkurang
        if qz["phase"] == "life":
            self.draw_life_loss(surf, qz)
        for p in self.particles:
            if not p.world:
                p.draw(surf, 0)
        for f in self.floats:
            if not f.world:
                f.draw(surf, 0)

    def draw_life_loss(self, surf, qz):
        t = qz["pt"]
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((30, 0, 10, int(170 * min(1.0, t / 0.2))))
        surf.blit(veil, (0, 0))
        heart = self.get_big_heart()
        cx, cy = WIDTH // 2, 300
        if t < 0.45:
            sc = 1.0 + 0.18 * math.sin(t / 0.45 * math.pi * 3)
            img = pygame.transform.rotozoom(heart, 0, sc)
            surf.blit(img, img.get_rect(center=(cx, cy)))
        else:
            k = (t - 0.45) / 1.0
            fade = max(0, 255 - int(k * 255))
            halves = ((heart.subsurface((0, 0, 80, 160)).copy(), -1),
                      (heart.subsurface((80, 0, 80, 160)).copy(), 1))
            for img, d in halves:
                img = pygame.transform.rotate(img, d * -k * 55)
                img.set_alpha(fade)
                surf.blit(img, img.get_rect(center=(cx + d * (40 + k * 90), cy + k * k * 150)))
        draw_text(surf, "NYAWA BERKURANG!", 54, (255, 120, 130), (WIDTH // 2, 150), "center", shadow=BLACK)
        for i in range(max(START_LIVES, self.lives + 1)):
            hx = WIDTH // 2 - (max(START_LIVES, self.lives + 1) - 1) * 24 + i * 48
            if i < self.lives:
                draw_heart(surf, hx, 470, 38, (240, 60, 80), (90, 10, 30))
            elif i == self.lives:
                shrink = max(0.0, 1.0 - t / 0.9)
                if shrink > 0:
                    draw_heart(surf, hx, 470, 38 * shrink, (240, 60, 80), (90, 10, 30))
                else:
                    draw_heart(surf, hx, 470, 34, (70, 70, 90), (35, 35, 50))
            else:
                draw_heart(surf, hx, 470, 34, (70, 70, 90), (35, 35, 50))
        if self.lives <= 0:
            draw_text(surf, "Nyawa habis...", 30, WHITE, (WIDTH // 2, 540), "center", shadow=BLACK)

    # ============================================================ LEVEL CLEAR
    def up_levelclear(self, dt):
        self.update_buttons()
        self.t += 0
        self.particles = [q for q in self.particles if q.update()]
        if random.random() < 0.25:
            self.burst(random.randint(100, WIDTH - 100), random.randint(80, 220),
                       random.choice([(255, 220, 90), (120, 230, 140), (120, 190, 255), (255, 130, 200)]),
                       10, world=False, speed=4)

    def draw_star(self, surf, cx, cy, r, color):
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = r if i % 2 == 0 else r * 0.45
            pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
        pygame.draw.polygon(surf, color, pts)
        pygame.draw.polygon(surf, shade(color, 0.6), pts, 3)

    def dr_levelclear(self, surf):
        self.draw_world(surf)
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((8, 10, 30, 190))
        surf.blit(dim, (0, 0))
        st = self.last_stats
        self.draw_panel(surf, (160, 60, WIDTH - 320, 450), 235)
        draw_text(surf, "LEVEL %d SELESAI!" % (self.level_idx + 1), 56, YELLOW, (WIDTH // 2, 112),
                  "center", shadow=BLACK)
        draw_text(surf, self.level.theme["title"], 26, WHITE, (WIDTH // 2, 158), "center", bold=False)
        for i in range(3):
            lit = i < st.get("stars", 0)
            bob = math.sin(self.t * 4 + i) * 4
            self.draw_star(surf, WIDTH // 2 - 90 + i * 90, int(220 + bob - (14 if i == 1 else 0)), 38,
                           (255, 215, 60) if lit else (80, 85, 110))
        rows = [("Jawaban benar", "%d / %d" % (st.get("correct", 0), QUESTIONS_PER_LEVEL)),
                ("Jawaban salah", str(st.get("wrong", 0))),
                ("Poin level ini", str(st.get("gained", 0))),
                ("Bonus sempurna", "+%d" % st.get("bonus", 0)),
                ("Total skor", str(self.score)),
                ("Nyawa bonus", "+%d  (sisa %d)" % (st.get("heal", 0), self.lives))]
        for i, (a, b) in enumerate(rows):
            y = 285 + i * 36
            draw_text(surf, a, 24, (200, 215, 255), (WIDTH // 2 - 200, y), "midleft", bold=False)
            draw_text(surf, b, 26, WHITE, (WIDTH // 2 + 200, y), "midright")
        self.draw_buttons(surf)
        for q in self.particles:
            if not q.world:
                q.draw(surf, 0)

    # ================================================================ GAME OVER
    def dr_gameover(self, surf):
        self.menu_bg.draw(surf, self.menu_scroll * 0.2, self.t)
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((40, 0, 15, 170))
        surf.blit(dim, (0, 0))
        draw_text(surf, "GAME OVER", 100, (255, 90, 100), (WIDTH // 2, 100 + math.sin(self.t * 3) * 6),
                  "center", shadow=BLACK)
        draw_text(surf, "Nyawa habis, %s! Yuk ulangi dari awal." % self.name, 30, WHITE,
                  (WIDTH // 2, 190), "center", shadow=BLACK)
        self.draw_panel(surf, (WIDTH // 2 - 280, 230, 560, 215), 215, (30, 12, 35))
        rows = [("Skor akhir", str(self.score)),
                ("Mencapai level", str(self.level_idx + 1)),
                ("Jawaban benar / salah", "%d / %d" % (self.total_correct, self.total_wrong)),
                ("Streak terbaik", str(self.best_streak))]
        for i, (a, b) in enumerate(rows):
            y = 265 + i * 45
            draw_text(surf, a, 26, (210, 215, 245), (WIDTH // 2 - 240, y), "midleft", bold=False)
            draw_text(surf, b, 30, YELLOW, (WIDTH // 2 + 240, y), "midright")
        self.draw_buttons(surf)

    # ================================================================== VICTORY
    def dr_victory(self, surf):
        self.draw_menu_scene(surf)
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((10, 10, 50, 150))
        surf.blit(dim, (0, 0))
        if random.random() < 0.3:
            self.burst(random.randint(80, WIDTH - 80), random.randint(60, 300),
                       random.choice([(255, 220, 90), (120, 230, 140), (120, 190, 255), (255, 130, 200)]),
                       12, world=False, speed=5)
        if self.score >= 40000:
            rank = "Legenda Informatika"
        elif self.score >= 25000:
            rank = "Master Digital"
        elif self.score >= 12000:
            rank = "Programmer Handal"
        else:
            rank = "Petualang Pemula"
        draw_text(surf, "SELAMAT, %s!" % self.name.upper(), 60, YELLOW, (WIDTH // 2, 70), "center", shadow=BLACK)
        draw_text(surf, "Kamu menamatkan seluruh 10 level StudyRush!", 28, WHITE, (WIDTH // 2, 125), "center",
                  shadow=BLACK)
        self.draw_panel(surf, (WIDTH // 2 - 290, 170, 580, 310), 225)
        draw_text(surf, "Gelar: " + rank, 38, (255, 190, 90), (WIDTH // 2, 215), "center", shadow=BLACK)
        rows = [("Skor total", str(self.score)),
                ("Jawaban benar", "%d / %d" % (self.total_correct, self.total_correct + self.total_wrong)),
                ("Streak terbaik", str(self.best_streak)),
                ("Nyawa tersisa", str(self.lives))]
        for i, (a, b) in enumerate(rows):
            y = 275 + i * 46
            draw_text(surf, a, 26, (205, 215, 250), (WIDTH // 2 - 250, y), "midleft", bold=False)
            draw_text(surf, b, 30, WHITE, (WIDTH // 2 + 250, y), "midright")
        self.draw_buttons(surf)
        for q in self.particles:
            if not q.world:
                q.draw(surf, 0)


# =============================================================================
#  PROGRAM UTAMA
# =============================================================================
def main():
    Game().run()


if __name__ == "__main__":
    main()