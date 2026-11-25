#!/usr/bin/env python3
"""Render entry.png for news-image-20261124 v3 (Builder A).

Improved newspaper 'THE WORLD TODAY': 35 stories, giant date masthead,
three picture-led leads, a world map with 13 numbered pins + legend,
a labelled BY THE NUMBERS strip and a DATE CHECK strip.
Deterministic: no network, no randomness, fixed fonts.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/dejavu"

PAPER = (248, 244, 236)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (15, 42, 74)
NAVY2 = (23, 58, 96)
OCEAN = (214, 229, 238)
LAND = (147, 173, 127)
LANDLINE = (90, 110, 80)
GREY = (110, 110, 108)
LIGHT = (255, 255, 255)
PANEL = (255, 255, 255)
GREEN = (28, 120, 60)


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 54)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_SMALL = font("DejaVuSans-Bold.ttf", 10)
F_SMALL_R = font("DejaVuSans.ttf", 10)
F_KICK = font("DejaVuSans-Bold.ttf", 11)
F_HEAD = font("DejaVuSans-Bold.ttf", 18)
F_DECK = font("DejaVuSans.ttf", 12)
F_GRID_H = font("DejaVuSans-Bold.ttf", 12)
F_GRID_D = font("DejaVuSans.ttf", 10)
F_GRID_R = font("DejaVuSans-Bold.ttf", 9)
F_LEG = font("DejaVuSans.ttf", 10)
F_LEG_B = font("DejaVuSans-Bold.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 9)
F_PIN = font("DejaVuSans-Bold.ttf", 10)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one(draw, text, fnt, width):
    if draw.textlength(text, font=fnt) <= width:
        return text
    while len(text) > 3 and draw.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1]
    return text + "\u2026"


# --- world map data: simplified continent outlines (lon, lat) ---
NORTH_AMERICA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60),
                 (-135, 57), (-130, 54), (-125, 49), (-124, 42), (-120, 34),
                 (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
                 (-90, 14), (-86, 12), (-83, 9), (-79, 9), (-80, 13),
                 (-83, 15), (-86, 16), (-88, 18), (-90, 21), (-97, 26),
                 (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32),
                 (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44),
                 (-60, 47), (-55, 52), (-60, 55), (-65, 58), (-68, 58),
                 (-72, 62), (-78, 62), (-85, 66), (-92, 66), (-95, 69),
                 (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68),
             (-22, 70), (-20, 74), (-25, 78), (-35, 80), (-50, 80),
             (-58, 76), (-62, 72), (-60, 68)]
SOUTH_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
                 (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
                 (-74, -50), (-70, -54), (-66, -55), (-68, -50), (-65, -45),
                 (-62, -41), (-58, -35), (-52, -32), (-48, -28), (-41, -23),
                 (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
                 (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11),
                 (-72, 12), (-76, 10)]
AFRICA = [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-6, 34), (0, 36),
          (10, 37), (11, 34), (15, 32), (20, 32), (25, 32), (30, 31),
          (32, 31), (35, 28), (37, 22), (39, 18), (41, 12), (43, 11),
          (48, 11), (51, 12), (51, 10), (46, 6), (42, 2), (40, -4),
          (40, -10), (38, -16), (35, -22), (32, -28), (28, -33), (20, -35),
          (17, -32), (15, -27), (13, -20), (12, -14), (13, -10), (9, -1),
          (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8), (-17, 12)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (4, 52), (7, 54),
          (8, 57), (11, 58), (18, 56), (21, 55), (24, 59), (28, 60),
          (30, 62), (30, 65), (25, 66), (20, 68), (18, 70), (25, 71),
          (30, 70), (32, 68), (35, 66), (40, 64), (42, 60), (40, 56),
          (38, 52), (36, 48), (34, 46), (30, 46), (28, 44), (24, 42),
          (22, 40), (26, 40), (23, 37), (26, 36), (30, 36), (28, 38),
          (24, 38), (22, 39), (19, 42), (15, 44), (12, 44), (10, 44),
          (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36)]
ASIA = [(30, 36), (35, 36), (36, 33), (35, 31), (39, 31), (42, 33),
        (44, 36), (48, 38), (50, 40), (53, 38), (54, 37), (57, 38),
        (60, 40), (63, 42), (66, 44), (70, 44), (73, 45), (76, 46),
        (80, 48), (85, 50), (90, 52), (95, 53), (100, 55), (105, 58),
        (110, 60), (115, 62), (120, 64), (125, 66), (130, 68), (135, 68),
        (140, 66), (142, 62), (142, 58), (140, 52), (138, 48), (135, 44),
        (132, 43), (130, 42), (128, 40), (127, 38), (126, 36), (122, 38),
        (120, 36), (118, 34), (115, 32), (112, 30), (110, 28), (108, 24),
        (106, 20), (104, 16), (102, 12), (100, 10), (98, 8), (97, 10),
        (95, 14), (93, 18), (91, 22), (89, 22), (87, 21), (85, 19),
        (82, 17), (80, 14), (78, 10), (76, 8), (75, 12), (73, 16),
        (72, 20), (70, 22), (68, 24), (66, 25), (64, 25), (62, 25),
        (60, 25), (58, 26), (56, 27), (54, 26), (52, 26), (50, 28),
        (48, 30), (46, 30), (44, 29), (42, 29), (40, 28), (38, 28),
        (36, 29), (35, 31)]
AUSTRALIA = [(113, -22), (114, -30), (115, -34), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
             (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
             (118, -20)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
         (141, 38), (141, 41), (142, 44), (144, 44), (142, 42), (140, 39)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EUROPE,
              ASIA, AUSTRALIA, UK, JAPAN]

# pins: (number, name, lon, lat, legend text, badge offset dx, dy)
PINS = [
    (1, "New York", -74, 40.7, "New York \u2014 Dow 50,000", 0, 0),
    (2, "Washington", -77, 38.9, "Washington \u2014 blacklist", 0, 0),
    (3, "C\u00facuta", -72.5, 7.9, "C\u00facuta \u2014 drone attack", 0, 0),
    (4, "Paris", 2.35, 48.85, "Paris \u2014 Sanofi $41bn", 2, 12),
    (5, "Brussels", 4.35, 50.85, "Brussels \u2014 EU sanctions", -4, -13),
    (6, "Zaporizhzhia", 35.2, 47.85, "Zaporizhzhia \u2014 strike", 12, -9),
    (7, "Antalya", 30.7, 36.9, "Antalya \u2014 COP31 fails", 13, 5),
    (8, "Gaza", 34.45, 31.5, "Gaza \u2014 strikes kill 7", -11, 9),
    (9, "Riyadh", 46.7, 24.7, "Riyadh \u2014 tower hit", 0, 0),
    (10, "Hormuz", 56.5, 26.6, "Hormuz \u2014 tankers mined", 0, 0),
    (11, "Seoul", 127, 37.5, "Seoul \u2014 rate 3.25%", 0, 0),
    (12, "Tokyo", 139.7, 35.7, "Tokyo \u2014 Nikkei +3.9%", 0, 0),
    (13, "Dakar", -17.4, 14.7, "Dakar \u2014 migrants lost", 0, 0),
]

LEADS = [
    ("NEW YORK \u2014 MARKETS",
     "HUANG'S COMEBACK FADES IN A DAY",
     "Nvidia -5.9% on Tuesday after a record +31.5% rally on Monday; chips slide with it.",
     "bars"),
    ("PARIS \u2014 PHARMA",
     "SANOFI'S $41BN PILL",
     "French drugmaker to buy Insmed for $175 a share in cash \u2014 the year's biggest pharma deal.",
     "pill"),
    ("BENGHAZI \u2014 WAR AT SEA",
     "WARSHIP SUNK OFF LIBYA",
     "Ukraine says 7 sea drones sank the Russian corvette Merkury and hit the cargo ship Angara.",
     "ship"),
]

# (number, region, headline, deck) — stories 4..35
GRID = [
    (4, "NEW YORK", "Dow tops 50,000 at last",
     "First close above 50,000: 50,018.70, +0.85%"),
    (5, "WASHINGTON", "Confidence climbs to 103.3",
     "US consumer confidence up in November"),
    (6, "FLORIDA", "Trump to meet NATO's Rutte",
     "Talks set for Wednesday at the White House"),
    (7, "TRAVEL", "81.5m to travel for Thanksgiving",
     "AAA counts trips for 24\u201330 Nov; storm looms"),
    (8, "WASHINGTON", "US blacklists 7 more firms",
     "Alibaba unit and Megaspeed on chip list"),
    (9, "AUSTIN", "Dell: record sales, shares fall",
     "Revenue $54.9bn, +103%; stock down 11.8%"),
    (10, "ZAPORIZHZHIA", "Strike kills 2 in Zaporizhzhia",
     "Dozens hurt; Russia claims 699 drones downed"),
    (11, "BRUSSELS", "EU readies 22nd Russia package",
     "About 60 more banks and crypto networks"),
    (12, "BELGIUM", "National strike grounds flights",
     "Airports and transport halted for a day"),
    (13, "US COURT", "Huawei guilty of trade theft",
     "Jury convicts on secrets and fraud counts"),
    (14, "PARIS", "Sarkozy and Bruni to face trial",
     "Ex-president and wife face court together"),
    (15, "MOSCOW", "Russia counts ~500,000 war dead",
     "Kremlin's own figures show the toll"),
    (16, "NATO", "NATO vows to defend space",
     "Chief warns after nuclear-satellite reports"),
    (17, "HORMUZ", "3 tankers hit mines, Iran says",
     "Claim unverified; US sanctions exchanges"),
    (18, "GAZA", "Strikes kill 7 despite ceasefire",
     "Meningitis cases hit 272, eight times normal"),
    (19, "RIYADH", "Tower hit again in a week",
     "Second strike on PIF Tower in days"),
    (20, "ANTALYA", "COP31 ends with no pact",
     "UN chief \u2018deeply disappointed\u2019 in talks"),
    (21, "JERUSALEM", "Coalition talks, round three",
     "Netanyahu and Eisenkot meet again"),
    (22, "DAKAR", "~175 migrants missing at sea",
     "Boat lost off Senegal, feared sunk"),
    (23, "DAKAR", "Senegal's AFCON title restored",
     "CAS overturns stripping of 2025 crown"),
    (24, "KINSHASA", "Congo rebels pull back",
     "Retreat follows heavy clashes with army"),
    (25, "ABUJA", "92-year-old king suspended",
     "Nigerian monarch faces sex-assault claims"),
    (26, "TOKYO", "Nikkei jumps 3.9% in a day",
     "Kospi +6.3%, back above 5,000"),
    (27, "SEOUL", "Bank of Korea lifts rate",
     "Benchmark up to 3.25% on Tuesday"),
    (28, "HANOI", "Gas blast kills 6 in Hanoi",
     "Ten hurt as restaurant is renovated"),
    (29, "KUALA LUMPUR", "Malaysia to return 6,803",
     "Myanmar nationals, incl. 1,500 Rohingya"),
    (30, "JAKARTA", "Missile chemical seized at sea",
     "405 tonnes held from China-bound ship"),
    (31, "ISLAMABAD", "Pakistan's first astronaut",
     "To fly on China's Shenzhou-24 mission"),
    (32, "LAHORE", "World's smoggiest big city",
     "Lahore air index hits a hazardous 538"),
    (33, "HONIARA", "Solomons sign Australia pact",
     "Treaty bars foreign military bases"),
    (34, "C\u00daCUTA", "Drone hits Colombia police base",
     "3 hurt; gunmen hold dozens hostage"),
    (35, "WASHINGTON", "US measles cases hit 5,412",
     "CDC counts the 2026 total so far"),
]

NUMBERS_L1 = ("BY THE NUMBERS \u2014 DOW 50,018.70 (+0.85%) \u00b7 NASDAQ 23,733.54 "
              "(\u22121.48%) \u00b7 S&P 500 7,201.09 (\u22120.50%) \u00b7 NVIDIA \u22125.9% Tue (+31.5% Mon)")
NUMBERS_L2 = ("SANOFI $41bn \u00b7 NIKKEI +3.9% \u00b7 KOSPI +6.3% \u00b7 BANK OF KOREA 3.25% "
              "\u00b7 AAA 81.5m travellers \u00b7 MEASLES 5,412 cases \u00b7 198 UNFCCC Parties")
DATECHECK_L1 = ("DATE CHECK \u2014 Wires cut 23:59 UTC. Dated otherwise: Nvidia +31.5% was Monday 23 Nov \u00b7 "
                "COP31 closed Sun 22 Nov (UN reaction Tue) \u00b7 Hasina returns 16 Dec \u00b7 "
                "Congo cobalt halt starts 30 Nov.")
DATECHECK_L2 = ("Left out: CrowdStrike\u2013Zscaler deal (announced Mon 23 Nov), FIFA 2031 hosts (named Mon 23 Nov) "
                "and Venezuela pivot (18 Nov) \u2014 not Tuesday news.")
FOOTER = ("Sources: Reuters \u00b7 BBC \u00b7 AP \u00b7 Al Jazeera \u00b7 UN News \u00b7 Sanofi \u00b7 WSJ \u00b7 "
          "Morningstar \u2014 as reported Tuesday 24 November 2026 \u00b7 THE WORLD TODAY \u00b7 35 stories")


def draw_bars(draw, x, y, w, h):
    # Monday +31.5% green bar, Tuesday -5.9% red bar
    base = y + h - 14
    draw.line([(x, base), (x + w, base)], fill=INK, width=1)
    bw = 44
    gh = int((h - 22) * 0.85)
    draw.rectangle([x + 18, base - gh, x + 18 + bw, base], fill=GREEN)
    draw.rectangle([x + 18 + bw + 26, base - 8, x + 18 + 2 * bw + 26, base],
                   fill=RED)
    draw.text((x + 18, base - gh - 13), "+31.5%", font=F_SMALL, fill=GREEN)
    draw.text((x + 18 + bw + 26, base + 2), "-5.9%", font=F_SMALL, fill=RED)
    draw.text((x + 18, base + 2), "MON", font=F_SMALL_R, fill=GREY)
    draw.text((x + 18 + bw + 26, base - 22), "TUE", font=F_SMALL_R, fill=GREY)


def draw_pill(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 - 4
    draw.rounded_rectangle([cx - 78, cy - 16, cx + 78, cy + 16], radius=16,
                           fill=(255, 255, 255), outline=RED, width=3)
    draw.line([(cx, cy - 16), (cx, cy + 16)], fill=RED, width=3)
    draw.ellipse([cx - 92, cy - 16, cx - 60, cy + 16], fill=(200, 220, 240),
                 outline=NAVY, width=2)
    draw.ellipse([cx + 60, cy - 16, cx + 92, cy + 16], fill=(200, 220, 240),
                 outline=NAVY, width=2)
    draw.text((x + 8, y + h - 14), "$175 A SHARE \u00b7 CASH", font=F_SMALL,
              fill=NAVY)


def draw_ship(draw, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 + 6
    draw.polygon([(cx - 80, cy), (cx + 80, cy), (cx + 58, cy + 16),
                  (cx - 58, cy + 16)], fill=(70, 70, 78))
    draw.rectangle([cx - 34, cy - 20, cx + 10, cy], fill=(70, 70, 78))
    draw.line([(cx - 8, cy - 20), (cx - 8, cy - 34)], fill=INK, width=3)
    for sx, sy in [(cx - 58, cy - 26), (cx - 40, cy - 34), (cx - 72, cy - 32)]:
        draw.line([(sx - 7, sy - 7), (sx + 7, sy + 7)], fill=RED, width=2)
        draw.line([(sx - 7, sy + 7), (sx + 7, sy - 7)], fill=RED, width=2)
    draw.text((x + 8, y + h - 14), "7 SEA DRONES \u00b7 BENGHAZI", font=F_SMALL,
              fill=NAVY)


def draw_lead(draw, x, y, w, h, kicker, headline, deck, kind):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=(190, 185, 175))
    draw.text((x + 10, y + 8), kicker, font=F_KICK, fill=RED)
    hl = wrap(draw, headline, F_HEAD, w - 20)
    yy = y + 26
    for ln in hl[:2]:
        draw.text((x + 10, yy), ln, font=F_HEAD, fill=INK)
        yy += 21
    dc = wrap(draw, deck, F_DECK, w - 20)
    for ln in dc[:3]:
        draw.text((x + 10, yy), ln, font=F_DECK, fill=(40, 40, 40))
        yy += 15
    gy = y + h - 66
    if kind == "bars":
        draw_bars(draw, x + 10, gy, w - 20, 62)
    elif kind == "pill":
        draw_pill(draw, x + 10, gy, w - 20, 62)
    else:
        draw_ship(draw, x + 10, gy, w - 20, 62)


def draw_map(draw, mx, my, mw, mh):
    draw.rectangle([mx, my, mx + mw, my + mh], fill=OCEAN,
                   outline=(190, 185, 175))
    def proj(lon, lat):
        return (mx + (lon + 168) / 360.0 * mw,
                my + (78 - lat) / 136.0 * mh)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LANDLINE)
    for num, name, lon, lat, _leg, dx, dy in PINS:
        px, py = proj(lon, lat)
        bx, by = px + dx, py + dy
        if dx or dy:
            draw.line([(px, py), (bx, by)], fill=INK, width=1)
        draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED,
                     outline=(255, 255, 255), width=1)
        t = str(num)
        tw = draw.textlength(t, font=F_PIN)
        draw.text((bx - tw / 2, by - 7), t, font=F_PIN, fill=(255, 255, 255))


def draw_legend(draw, lx, ly, lw):
    draw.text((lx, ly), "THE DAY ON THE MAP", font=F_LEG_B, fill=NAVY)
    draw.text((lx + lw - 52, ly), "13 PINS", font=F_LEG_B, fill=RED)
    col_w = lw // 2
    for i, (_n, _nm, _lo, _la, leg, _dx, _dy) in enumerate(PINS):
        col = 0 if i < 7 else 1
        row = i if i < 7 else i - 7
        tx = lx + col * col_w
        ty = ly + 20 + row * 22
        n = str(i + 1)
        draw.ellipse([tx, ty + 1, tx + 13, ty + 14], fill=RED)
        tw = draw.textlength(n, font=F_PIN)
        draw.text((tx + 6.5 - tw / 2, ty + 2), n, font=F_PIN,
                  fill=(255, 255, 255))
        draw.text((tx + 18, ty + 2), fit_one(draw, leg, F_LEG, col_w - 20),
                  font=F_LEG, fill=INK)


def draw_grid(draw, gx, gy):
    draw.text((gx, gy), "THE DAY IN BRIEF", font=F_LEG_B, fill=NAVY)
    right = "32 MORE STORIES \u00b7 7 REGIONS + WORLD"
    tw = draw.textlength(right, font=F_LEG_B)
    draw.text((gx + 1000 - tw, gy), right, font=F_LEG_B, fill=GREY)
    col_w, row_h = 244, 46
    for idx, (num, region, headline, deck) in enumerate(GRID):
        col, row = idx % 4, idx // 4
        x = gx + col * (col_w + 8)
        y = gy + 18 + row * row_h
        draw.text((x, y), "%02d \u00b7 %s" % (num, region), font=F_GRID_R,
                  fill=RED)
        hl = wrap(draw, headline, F_GRID_H, col_w)
        yy = y + 12
        for ln in hl[:2]:
            draw.text((x, yy), ln, font=F_GRID_H, fill=INK)
            yy += 14
        draw.text((x, yy), fit_one(draw, deck, F_GRID_D, col_w),
                  font=F_GRID_D, fill=(60, 60, 60))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 116], fill=(255, 255, 255))
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 10), title, font=F_TITLE, fill=INK)
    date = "TUESDAY 24 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 72), date, font=F_DATE, fill=RED)
    d.text((14, 18), "No. 329", font=F_SMALL_R, fill=GREY)
    d.text((14, 34), "EST. 2026", font=F_SMALL_R, fill=GREY)
    d.text((W - 118, 18), "ONE DAY", font=F_SMALL_R, fill=GREY)
    d.text((W - 118, 34), "35 STORIES", font=F_SMALL_R, fill=GREY)
    d.line([(0, 116), (W, 116)], fill=INK, width=3)
    d.line([(0, 120), (W, 120)], fill=RED, width=1)
    # Leads
    ly, lh = 126, 206
    for i, (kick, head, deck, kind) in enumerate(LEADS):
        draw_lead(d, 12 + i * 338, ly, 324, lh, kick, head, deck, kind)
    # Map band
    my = 340
    d.line([(0, my - 4), (W, my - 4)], fill=INK, width=1)
    draw_map(d, 12, my, 628, 178)
    draw_legend(d, 656, my + 2, 356)
    # Grid
    d.line([(0, 524), (W, 524)], fill=INK, width=1)
    draw_grid(d, 12, 530)
    # BY THE NUMBERS
    ny = 918
    d.rectangle([0, ny, W, ny + 50], fill=NAVY)
    d.text((12, ny + 6), NUMBERS_L1, font=F_NUM, fill=(255, 255, 255))
    d.text((12, ny + 28), NUMBERS_L2, font=F_NUM, fill=(255, 255, 255))
    # DATE CHECK
    d.text((12, 974), DATECHECK_L1, font=F_SMALL_R, fill=(60, 60, 60))
    d.text((12, 988), DATECHECK_L2, font=F_SMALL_R, fill=(60, 60, 60))
    # Footer
    d.line([(0, 1004), (W, 1004)], fill=(190, 185, 175), width=1)
    d.text((12, 1008), FOOTER, font=F_FOOT, fill=GREY)
    out = os.path.join(BASE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
