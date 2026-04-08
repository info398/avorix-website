#!/usr/bin/env python3
"""Generate improved Avorix Leitfaden PDF with better layout and typography."""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import Color, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from io import BytesIO
import os

# ── Fonts ──────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('Inter',          '/tmp/inter_fonts/Inter-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Inter-Bold',     '/tmp/inter_fonts/Inter-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Inter-Medium',   '/tmp/inter_fonts/Inter-Medium.ttf'))
pdfmetrics.registerFont(TTFont('Inter-SemiBold', '/tmp/inter_fonts/Inter-SemiBold.ttf'))

# ── Dimensions ─────────────────────────────────────────────────────────────
W, H = A4  # 595.27 × 841.89 pt

# ── Colors ─────────────────────────────────────────────────────────────────
BLUE        = Color(61/255,  61/255,  222/255)
DARK        = Color(26/255,  26/255,  26/255)
GRAY        = Color(74/255,  74/255,  74/255)
SILVER      = Color(154/255, 154/255, 154/255)
LIGHT       = Color(232/255, 232/255, 232/255)
BLUE_LIGHT  = Color(235/255, 239/255, 255/255)
AMBER       = Color(240/255, 160/255, 40/255)
AMBER_LIGHT = Color(255/255, 248/255, 232/255)
WHITE       = white
BLUE_DARK   = Color(40/255,  40/255,  180/255)

# ── Layout constants ───────────────────────────────────────────────────────
ML           = 45          # left margin
MR           = 45          # right margin
CONTENT_W    = W - ML - MR # 505.27 pt
FOOTER_H     = 25
HEADER_H     = 28
PHOTO_COL_W  = 190         # right photo column
GAP          = 15
TEXT_COL_W   = CONTENT_W - PHOTO_COL_W - GAP  # 300.27 pt

IMG_DIR = 'public'
IMGS = {
    'kitchen_ai':      f'{IMG_DIR}/avorix_kitchen_ai.jpg',
    'kitchen_branded': f'{IMG_DIR}/avorix_kitchen_branded.jpg',
    'gastro_60':       f'{IMG_DIR}/avorix_gastro-hotel-60.jpg',
    'gastro_62':       f'{IMG_DIR}/avorix_gastro-hotel-62.jpg',
    'gastro_104':      f'{IMG_DIR}/avorix_gastro-hotel-104.jpg',
}

# ── Image cache (resize + compress once per path) ──────────────────────────
_img_cache = {}  # path -> (ImageReader, orig_width, orig_height)

def get_img_data(img_path, max_dim=1400):
    """Load, resize to max_dim if larger, compress and cache as ImageReader."""
    if img_path not in _img_cache:
        img = PILImage.open(img_path)
        iw, ih = img.size
        scale = min(max_dim / iw, max_dim / ih, 1.0)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        if scale < 1.0:
            img = img.resize((int(iw * scale), int(ih * scale)), PILImage.LANCZOS)
        buf = BytesIO()
        img.save(buf, format='JPEG', quality=80, optimize=True)
        buf.seek(0)
        _img_cache[img_path] = (ImageReader(buf), iw, ih)
    return _img_cache[img_path]


# ── Helpers ────────────────────────────────────────────────────────────────
def draw_image_fill(c, img_path, x, y, width, height):
    """Draw image centered and cropped to fill the given rectangle exactly."""
    reader, iw, ih = get_img_data(img_path)
    img_asp = iw / ih
    box_asp = width / height
    if img_asp > box_asp:
        dh = height
        dw = height * img_asp
        dx = x - (dw - width) / 2
        dy = y
    else:
        dw = width
        dh = width / img_asp
        dx = x
        dy = y - (dh - height) / 2
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, width, height)
    c.clipPath(p, stroke=0)
    c.drawImage(reader, dx, dy, dw, dh)
    c.restoreState()


def wrap_text(c, text, font, size, max_width):
    """Return list of wrapped lines."""
    words = text.split()
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        if c.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_block(c, text, x, y, width, font, size, color, line_h=None):
    """Draw wrapped text, return y after last line."""
    if line_h is None:
        line_h = size * 1.45
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(c, text, font, size, width):
        c.drawString(x, y, line)
        y -= line_h
    return y


def draw_info_box(c, x, y, width, label, text, bg, accent, font_size=8.5):
    """Info box with left accent bar. Returns height consumed."""
    accent_w = 3
    pad_x, pad_y = 14, 12
    inner_w = width - accent_w - pad_x * 2
    label_h = 20
    line_h = font_size * 1.55
    lines = wrap_text(c, text, 'Inter', font_size, inner_w)
    total_h = pad_y + label_h + len(lines) * line_h + pad_y
    # Background
    c.setFillColor(bg)
    c.rect(x, y - total_h, width, total_h, fill=1, stroke=0)
    # Accent bar
    c.setFillColor(accent)
    c.rect(x, y - total_h, accent_w, total_h, fill=1, stroke=0)
    # Label
    c.setFont('Inter-Bold', 7.5)
    c.setFillColor(accent)
    c.drawString(x + accent_w + pad_x, y - pad_y - 9, label)
    # Body
    c.setFont('Inter', font_size)
    c.setFillColor(DARK)
    ty = y - pad_y - label_h - 2
    for line in lines:
        c.drawString(x + accent_w + pad_x, ty, line)
        ty -= line_h
    return total_h


def draw_bullet_section(c, items, x, y, width, font_size=8.5):
    """Draw bullet list, return y after last item."""
    c.setFont('Inter-Bold', 7.5)
    c.setFillColor(BLUE)
    c.drawString(x, y, 'WAS HILFT:')
    y -= 15
    line_h = font_size * 1.55
    for item in items:
        lines = wrap_text(c, item, 'Inter', font_size, width - 14)
        c.setFillColor(DARK)
        c.rect(x, y + 2.5, 5, 5, fill=1, stroke=0)
        c.setFont('Inter', font_size)
        for i, line in enumerate(lines):
            c.drawString(x + 14, y, line)
            y -= line_h
        y -= 3
    return y


def draw_badge(c, number, x, y, size=28):
    c.setFillColor(BLUE)
    c.rect(x, y - size, size, size, fill=1, stroke=0)
    c.setFont('Inter-Bold', size * 0.52)
    c.setFillColor(WHITE)
    c.drawCentredString(x + size / 2, y - size + size * 0.24, str(number))


def draw_page_header(c):
    c.setFillColor(BLUE)
    c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)


def draw_page_footer(c, page_num):
    c.setFillColor(LIGHT)
    c.rect(0, 0, W, FOOTER_H, fill=1, stroke=0)
    c.setFont('Inter', 7)
    c.setFillColor(GRAY)
    c.drawString(ML, 8, 'avorix.cloud  |  5 Strategien gegen den Fachkräftemangel in der Küche')
    c.setFillColor(SILVER)
    c.drawRightString(W - MR, 8, str(page_num))


# ══════════════════════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ══════════════════════════════════════════════════════════════════════════
def draw_cover(c):
    # Blue background
    c.setFillColor(BLUE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Logo
    c.setFont('Inter-Bold', 10)
    c.setFillColor(WHITE)
    c.drawString(ML, H - 24, 'AVORIX')
    c.setFont('Inter', 8)
    c.setFillColor(Color(1, 1, 1, 0.65))
    c.drawString(ML, H - 37, 'avorix.cloud')

    # Title
    title_y = H - 95
    c.setFont('Inter-Bold', 32)
    c.setFillColor(WHITE)
    title = '5 Strategien, mit denen Hotels den Fachkräftemangel in der Küche meistern'
    for line in wrap_text(c, title, 'Inter-Bold', 32, W - ML - MR):
        c.drawString(ML, title_y, line)
        title_y -= 40

    title_y -= 8

    # Subtitle
    subtitle = 'Ein praxisnaher Leitfaden für Hoteliers und Küchenchefs in Tirol & Salzburg'
    title_y = draw_text_block(c, subtitle, ML, title_y, W - ML - MR,
                               'Inter', 13, Color(1, 1, 1, 0.8), 18)
    title_y -= 28

    # Full-width photo filling remaining space above the footer bar
    photo_y = FOOTER_H
    photo_h = title_y - photo_y - 5
    if photo_h > 60:
        draw_image_fill(c, IMGS['gastro_104'], 0, photo_y, W, photo_h)
        # Subtle dark tint at bottom to protect footer text
        c.setFillColor(Color(0, 0, 0, 0.25))
        c.rect(0, photo_y, W, 35, fill=1, stroke=0)

    # Footer
    c.setFont('Inter', 7)
    c.setFillColor(Color(1, 1, 1, 0.55))
    c.drawString(ML, 8, '© 2026 Avorix – Alle Rechte vorbehalten')
    c.drawRightString(W - MR, 8, 'avorix.cloud')


# ══════════════════════════════════════════════════════════════════════════
# PAGE 2 — INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════
def draw_intro(c):
    draw_page_header(c)
    draw_page_footer(c, 1)

    # Full-width photo below header
    photo_h = 195
    draw_image_fill(c, IMGS['gastro_60'], 0, H - HEADER_H - photo_h, W, photo_h)

    y = H - HEADER_H - photo_h - 18

    # Section label
    c.setFont('Inter-Bold', 7.5)
    c.setFillColor(BLUE)
    c.drawString(ML, y, 'EINLEITUNG')
    y -= 16

    # Main heading
    c.setFont('Inter-Bold', 21)
    c.setFillColor(DARK)
    c.drawString(ML, y, 'Der stille Kostenfaktor in Ihrer Küche')
    y -= 8

    # Divider
    c.setStrokeColor(LIGHT)
    c.setLineWidth(1)
    c.line(ML, y, W - MR, y)
    y -= 15

    # Body paragraphs
    paras = [
        ('82 % der Gastronomiebetriebe in Österreich klagen über akuten Fachkräftemangel in der '
         'Küche. Was oft als Personalproblem abgetan wird, ist in Wirklichkeit ein strategisches '
         'Risiko: Wenn ausgebildete Köche fehlen, leidet nicht nur die Qualität — sondern auch die '
         'Auslastung, der Ruf und am Ende die Gästezufriedenheit.'),
        ('Ferienhotels mit Halbpension-Betrieb stehen vor einer besonderen Herausforderung: Täglich '
         'mehrere Hundert Couverts, hohe Qualitätsansprüche, saisonale Peaks — und ein Stamm-Team, '
         'das immer dünner wird.'),
        ('Dieser Leitfaden zeigt Ihnen 5 bewährte Strategien, mit denen Hotelbetriebe in der Region '
         'diesen Druck reduzieren — ohne Abstriche bei der Qualität.'),
    ]
    for para in paras:
        y = draw_text_block(c, para, ML, y, CONTENT_W, 'Inter', 9, GRAY, 14.5)
        y -= 11

    y -= 8

    # Table of contents box
    toc_items = [
        '» Strategie 1: Wissen dokumentieren, bevor es geht',
        '» Strategie 2: Einarbeitung beschleunigen',
        '» Strategie 3: Qualität standardisieren statt kontrollieren',
        '» Strategie 4: Ausländische Fachkräfte erfolgreich integrieren',
        '» Strategie 5: Digitalisierung gezielt einsetzen',
    ]
    line_h = 13
    box_h = 20 + len(toc_items) * line_h + 14
    c.setFillColor(BLUE_LIGHT)
    c.rect(ML, y - box_h, CONTENT_W, box_h, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(ML, y - box_h, 3, box_h, fill=1, stroke=0)
    c.setFont('Inter-Bold', 8)
    c.setFillColor(BLUE)
    c.drawString(ML + 12, y - 13, 'IN DIESEM LEITFADEN:')
    ty = y - 27
    c.setFont('Inter', 8.5)
    c.setFillColor(DARK)
    for item in toc_items:
        c.drawString(ML + 18, ty, item)
        ty -= line_h


# ══════════════════════════════════════════════════════════════════════════
# PAGES 3–7 — STRATEGIES
# ══════════════════════════════════════════════════════════════════════════
STRATEGIES = [
    {
        'num': 1, 'page_num': 2,
        'title': 'Wissen dokumentieren, bevor es geht',
        'lead': ('In vielen Hotelküchen steckt das gesamte Rezept-Know-how in den Köpfen weniger '
                 'Schlüsselpersonen. Wenn diese Mitarbeiter gehen — durch Kündigung, Krankheit '
                 'oder Saisonende — geht das Wissen mit.'),
        'sub': 'Das stille Risiko: Was passiert, wenn Ihr bester Koch kündigt?',
        'bullets': [
            'Standardrezepturen schriftlich festhalten (mit Mengenangaben für 20, 50, 100 Couverts)',
            'Zubereitungsschritte mit Fotos dokumentieren',
            'Allergen- und Nährstoffinformationen einpflegen',
            'Rezeptbibliothek zentral und digital verfügbar machen',
        ],
        'ergebnis': ('Neues Personal kann eigenständig nach Standard arbeiten — Qualität wird '
                     'reproduzierbar, nicht personenabhängig.'),
        'tipp': ('Starten Sie mit Ihren 20 meistgekochten Gerichten. Schon diese Kernbasis '
                 'reduziert die Abhängigkeit von Einzelpersonen drastisch.'),
        'img': 'kitchen_branded',
    },
    {
        'num': 2, 'page_num': 3,
        'title': 'Einarbeitung beschleunigen',
        'lead': ('Die durchschnittliche Einarbeitungszeit in einer Hotelküche beträgt 3–6 Wochen. '
                 'In einer Saison, die oft nur 12–16 Wochen dauert, ist das ein erheblicher '
                 'Produktivitätsverlust.'),
        'sub': 'Neue Mitarbeiter produktiv machen — ab Tag 1',
        'bullets': [
            'Digitale Schritt-für-Schritt-Anleitungen für jedes Gericht',
            'Visuelle Hilfen (Fotos, Videos) statt rein mündlicher Einweisung',
            'Klare Verantwortungsbereiche für Saisonkräfte',
            'Strukturierte Onboarding-Checklisten für die ersten 3 Tage',
        ],
        'ergebnis': ('Neue Mitarbeiter — auch ohne Berufserfahrung — können nach kurzer '
                     'Eingewöhnung eigenständig nach Rezept arbeiten. Der Küchenchef wird entlastet.'),
        'tipp': ('Saisonkräfte bringen Lernbereitschaft mit — aber keine Zeit für lange Schulungen. '
                 'Je strukturierter Ihr Onboarding, desto schneller und zuverlässiger ist der Einstieg.'),
        'img': 'gastro_62',
    },
    {
        'num': 3, 'page_num': 4,
        'title': 'Qualität standardisieren statt kontrollieren',
        'lead': ('In vielen Küchen verbringt der Küchenchef mehr Zeit mit Kontrolle als mit '
                 'Kreativität. Der Grund: Wenn Prozesse nicht standardisiert sind, muss eine '
                 'Führungskraft ständig eingreifen.'),
        'sub': 'Vom Kontrolleur zum Enabler: Die Rolle des Küchenchefs neu denken',
        'bullets': [
            'Qualitätsstandards (Portionsgrössen, Anrichtebilder, Konsistenz) schriftlich definieren',
            'Mitarbeiter befähigen, selbst nach Standard zu prüfen',
            'Abweichungen schnell erkennbar und korrigierbar machen',
            'Rezeptversionen versionieren (Sommer-/Winterkarte etc.)',
        ],
        'ergebnis': ('Der Küchenchef kann sich auf Kreativität, Wareneinkauf und Gästequalität '
                     'konzentrieren — während das Team eigenständig nach definierten Standards arbeitet.'),
        'tipp': ('Ein guter Standard ist nicht der, den nur der Küchenchef kennt — sondern der, '
                 'der auch in seiner Abwesenheit funktioniert.'),
        'img': 'gastro_60',
    },
    {
        'num': 4, 'page_num': 5,
        'title': 'Ausländische Fachkräfte erfolgreich integrieren',
        'lead': ('Viele Betriebe rekrutieren heute aktiv in Südosteuropa, Lateinamerika oder Asien. '
                 'Das Potenzial ist real — aber die Integration scheitert oft an Sprachbarrieren '
                 'in der Küche.'),
        'sub': 'Sprachbarrieren als gelöstes Problem',
        'bullets': [
            'Rezepte mehrsprachig oder mit starkem Bildanteil aufbereiten',
            'Mengen und Schritte so klar formulieren, dass sie ohne Kochausbildung verständlich sind',
            'Küchenabläufe visuell strukturieren (Stationsübersichten, Mise-en-place-Listen)',
            'Onboarding-Materialien in der Muttersprache der Mitarbeiter anbieten',
        ],
        'ergebnis': ('Internationale Mitarbeiter können ab dem ersten Tag produktiv mitwirken. '
                     'Frustration und Fehler durch Missverständnisse sinken deutlich.'),
        'tipp': ('Bilder sind universell. Ein Foto des fertig angerichteten Tellers sagt mehr '
                 'als ein Rezepttext in einer Fremdsprache.'),
        'img': 'gastro_104',
    },
    {
        'num': 5, 'page_num': 6,
        'title': 'Digitalisierung gezielt einsetzen',
        'lead': ('Viele Hoteliers scheuen digitale Küchenlösungen aus Angst vor Komplexität oder '
                 'Widerstand im Team. Dabei muss Digitalisierung in der Küche kein grosses '
                 'IT-Projekt sein.'),
        'sub': 'Technologie als Küchenhilfe — nicht als Bürde',
        'bullets': [
            'Einstieg mit dem, was bereits vorhanden ist (Tablets, Smartphones)',
            'Fokus auf konkrete Arbeitsprozesse: Rezeptabruf, Küchenzettel, Allergenmanagement',
            'Lösung, die das Team unterstützt — nicht eine, die das Team überwacht',
            'Schrittweise Einführung: erst Kernrezepte, dann Erweiterung',
        ],
        'ergebnis': ('Teams, die mit digitaler Unterstützung arbeiten, machen weniger Fehler, '
                     'arbeiten selbstständiger und sind schneller eingearbeitet.'),
        'tipp': ('Der beste Einstieg in die Küchen-Digitalisierung ist die digitale Rezeptbibliothek. '
                 'Sie ist sofort nutzbar, spart Zeit und schafft Akzeptanz für weitere Schritte.'),
        'img': 'kitchen_ai',
    },
]


def draw_strategy(c, s):
    # Photo: full height of content area, right column
    photo_x = ML + TEXT_COL_W + GAP
    photo_y = FOOTER_H
    photo_h = H - HEADER_H - FOOTER_H
    draw_image_fill(c, IMGS[s['img']], photo_x, photo_y, PHOTO_COL_W, photo_h)

    draw_page_header(c)
    draw_page_footer(c, s['page_num'])

    # Content column
    x = ML
    cw = TEXT_COL_W
    y = H - HEADER_H - 18

    # Strategy label
    c.setFont('Inter-SemiBold', 7.5)
    c.setFillColor(BLUE)
    c.drawString(x + 34, y, f'STRATEGIE {s["num"]}')
    y -= 5

    # Badge + title
    badge_sz = 28
    draw_badge(c, s['num'], x, y, badge_sz)

    c.setFont('Inter-Bold', 17)
    c.setFillColor(DARK)
    title_x = x + badge_sz + 7
    title_w = cw - badge_sz - 7
    ty = y - 4
    for line in wrap_text(c, s['title'], 'Inter-Bold', 17, title_w):
        c.drawString(title_x, ty, line)
        ty -= 22

    y = min(ty, y - badge_sz) - 6

    # Divider
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.75)
    c.line(x, y, x + cw, y)
    y -= 14

    # Lead text
    y = draw_text_block(c, s['lead'], x, y, cw, 'Inter', 9, GRAY, 14.5)
    y -= 18

    # Sub-heading
    c.setFont('Inter-Bold', 11)
    c.setFillColor(DARK)
    for line in wrap_text(c, s['sub'], 'Inter-Bold', 11, cw):
        c.drawString(x, y, line)
        y -= 17
    y -= 8

    # Bullets
    y = draw_bullet_section(c, s['bullets'], x, y, cw)
    y -= 18

    # Ergebnis box
    h = draw_info_box(c, x, y, cw, 'ERGEBNIS', s['ergebnis'], BLUE_LIGHT, BLUE)
    y -= h + 14

    # Praxis-Tipp box
    draw_info_box(c, x, y, cw, 'PRAXIS-TIPP', s['tipp'], AMBER_LIGHT, AMBER)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 8 — SUMMARY
# ══════════════════════════════════════════════════════════════════════════
def draw_summary(c):
    draw_page_header(c)
    draw_page_footer(c, 7)

    y = H - HEADER_H - 22

    c.setFont('Inter-Bold', 7.5)
    c.setFillColor(BLUE)
    c.drawString(ML, y, 'ZUSAMMENFASSUNG')
    y -= 17

    c.setFont('Inter-Bold', 22)
    c.setFillColor(DARK)
    c.drawString(ML, y, 'Die 5 Strategien auf einen Blick')
    y -= 26

    # Table header
    col_w = [30, 195, 0]
    col_w[2] = CONTENT_W - col_w[0] - col_w[1]
    row_h = 30

    c.setFillColor(BLUE)
    c.rect(ML, y - row_h + 8, CONTENT_W, row_h, fill=1, stroke=0)
    c.setFont('Inter-Bold', 8.5)
    c.setFillColor(WHITE)
    headers = ['#', 'Strategie', 'Sofortmassnahme']
    xpos = ML + 10
    for hdr, cw in zip(headers, col_w):
        c.drawString(xpos, y - row_h + 8 + 9, hdr)
        xpos += cw
    y -= row_h - 8

    rows = [
        ('1', 'Wissen dokumentieren',          'Top-20-Rezepte schriftlich festhalten'),
        ('2', 'Einarbeitung beschleunigen',     'Onboarding-Tag-1-Checkliste erstellen'),
        ('3', 'Qualität standardisieren',       'Anrichtefotos für alle Hauptgerichte'),
        ('4', 'Internationale Teams integrieren','Bildgestützte Küchenpläne einführen'),
        ('5', 'Digitalisierung nutzen',         'Digitale Rezeptbibliothek aufbauen'),
    ]
    for idx, (num, strat, action) in enumerate(rows):
        bg = BLUE_LIGHT if idx % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.rect(ML, y - row_h + 4, CONTENT_W, row_h, fill=1, stroke=0)
        c.setStrokeColor(LIGHT)
        c.setLineWidth(0.5)
        c.line(ML, y - row_h + 4, ML + CONTENT_W, y - row_h + 4)
        xpos = ML + 10
        c.setFont('Inter-Bold', 9)
        c.setFillColor(BLUE)
        c.drawString(xpos, y - row_h + 4 + 9, num)
        xpos += col_w[0]
        c.setFont('Inter', 9)
        c.setFillColor(DARK)
        c.drawString(xpos, y - row_h + 4 + 9, strat)
        xpos += col_w[1]
        c.setFont('Inter', 9)
        c.setFillColor(GRAY)
        c.drawString(xpos, y - row_h + 4 + 9, action)
        y -= row_h

    y -= 22

    # Quick-win box
    qw_text = ('Sie müssen nicht alle 5 Strategien gleichzeitig angehen. Beginnen Sie mit Strategie 1: '
               'Dokumentieren Sie Ihre 20 meistgenutzten Rezepte — mit Mengen, Fotos und Schritten. '
               'Das dauert 1–2 Wochen und ist die Grundlage für alles Weitere.')
    inner_w = CONTENT_W - 3 - 28
    lines = wrap_text(c, qw_text, 'Inter', 9, inner_w)
    qw_line_h = 14.5
    box_h = 22 + len(lines) * qw_line_h + 16
    c.setFillColor(BLUE_LIGHT)
    c.rect(ML, y - box_h, CONTENT_W, box_h, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(ML, y - box_h, 3, box_h, fill=1, stroke=0)
    c.setFont('Inter-Bold', 8.5)
    c.setFillColor(BLUE)
    c.drawString(ML + 15, y - 14, 'Ihr nächster Schritt: Der Quick-Win')
    ty = y - 29
    c.setFont('Inter', 9)
    c.setFillColor(DARK)
    for line in lines:
        c.drawString(ML + 15, ty, line)
        ty -= qw_line_h

    y -= box_h + 18

    # Fill remaining space with a photo
    avail = y - FOOTER_H - 8
    if avail > 80:
        draw_image_fill(c, IMGS['kitchen_ai'], ML, FOOTER_H + 4, CONTENT_W, avail)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 9 — CTA
# ══════════════════════════════════════════════════════════════════════════
def draw_cta(c):
    # Blue background
    c.setFillColor(BLUE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Logo
    c.setFont('Inter-Bold', 10)
    c.setFillColor(WHITE)
    c.drawString(ML, H - 24, 'AVORIX')
    c.setFont('Inter', 8)
    c.setFillColor(Color(1, 1, 1, 0.65))
    c.drawString(ML, H - 37, 'avorix.cloud')

    y = H - 72

    # Big heading
    c.setFont('Inter-Bold', 34)
    c.setFillColor(WHITE)
    c.drawString(ML, y, 'Die Avorix Koch App')
    y -= 24

    c.setFont('Inter', 14)
    c.setFillColor(Color(1, 1, 1, 0.8))
    c.drawString(ML, y, 'Digitale Rezeptverwaltung für Hotelküchen')
    y -= 10

    c.setStrokeColor(Color(1, 1, 1, 0.3))
    c.setLineWidth(1)
    c.line(ML, y, W - MR, y)
    y -= 18

    # Body
    body = ('Avorix unterstützt Hotelküchen dabei, genau das umzusetzen, was dieser Leitfaden '
            'beschreibt: Rezepte digital verwalten, Teams Schritt für Schritt durch die Zubereitung '
            'führen und Qualität reproduzierbar machen — unabhängig vom Erfahrungsstand.')
    y = draw_text_block(c, body, ML, y, CONTENT_W, 'Inter', 10, Color(1, 1, 1, 0.85), 15)
    y -= 20

    c.setFont('Inter-Bold', 10)
    c.setFillColor(WHITE)
    c.drawString(ML, y, 'Für 4-Sterne-Ferienhotels, die:')
    y -= 17

    bullets = [
        'Saisonkräfte schnell und strukturiert einarbeiten wollen',
        'Rezept-Know-how nicht mehr in einzelnen Köpfen verankern wollen',
        'Küchenprozesse verlässlicher und effizienter gestalten möchten',
    ]
    for item in bullets:
        c.setFillColor(WHITE)
        c.rect(ML, y + 2.5, 5, 5, fill=1, stroke=0)
        c.setFont('Inter', 10)
        c.setFillColor(Color(1, 1, 1, 0.85))
        c.drawString(ML + 14, y, item)
        y -= 16

    y -= 14

    # White CTA box
    cta_h = 95
    c.setFillColor(WHITE)
    c.rect(ML, y - cta_h, CONTENT_W, cta_h, fill=1, stroke=0)

    c.setFont('Inter-Bold', 11)
    c.setFillColor(BLUE)
    c.drawString(ML + 15, y - 19, 'Interesse? Sprechen Sie mit uns.')

    half = CONTENT_W / 2
    c.setFont('Inter', 8.5)
    c.setFillColor(GRAY)
    c.drawString(ML + 15, y - 36, 'Demo vereinbaren:')
    c.drawString(ML + 15 + half, y - 36, 'Mehr erfahren:')

    c.setFont('Inter-Bold', 9)
    c.setFillColor(BLUE)
    c.drawString(ML + 15, y - 50, 'avorix.cloud/kontakt')
    c.drawString(ML + 15 + half, y - 50, 'avorix.cloud')

    c.setFont('Inter', 8.5)
    c.setFillColor(GRAY)
    c.drawString(ML + 15, y - 64, 'info@avorix.de')

    y -= cta_h + 15

    # Photo filling bottom
    avail = y - FOOTER_H - 5
    if avail > 80:
        draw_image_fill(c, IMGS['kitchen_branded'], 0, FOOTER_H, W, avail)
        # Dark tint over photo for footer legibility
        c.setFillColor(Color(0, 0, 0, 0.2))
        c.rect(0, FOOTER_H, W, 30, fill=1, stroke=0)

    # Footer
    c.setFont('Inter', 7)
    c.setFillColor(Color(1, 1, 1, 0.55))
    c.drawString(ML, 8, ('© 2026 Avorix – Alle Rechte vorbehalten  |  Dieser Leitfaden wurde '
                          'sorgfältig erstellt, erhebt jedoch keinen Anspruch auf Vollständigkeit.'))


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════
output_path = 'public/downloads/leitfaden-fachkraeftemangel.pdf'

c = rl_canvas.Canvas(output_path, pagesize=A4)
c.setTitle('5 Strategien gegen den Fachkräftemangel in der Küche – Avorix')
c.setAuthor('Avorix')
c.setSubject('Leitfaden für Hoteliers und Küchenchefs in Tirol & Salzburg')

draw_cover(c)
c.showPage()

draw_intro(c)
c.showPage()

for s in STRATEGIES:
    draw_strategy(c, s)
    c.showPage()

draw_summary(c)
c.showPage()

draw_cta(c)
c.showPage()

c.save()
print(f'PDF saved: {output_path}')
print(f'File size: {os.path.getsize(output_path):,} bytes')
