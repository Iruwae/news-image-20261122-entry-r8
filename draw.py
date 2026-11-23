"""Draw the Sunday 22 November 2026 news broadsheet (1024x1024 PNG).

Fresh code for the r8 top-5 push. Stories verified Monday 23 Nov 2026 ~00:00 UTC:
COP31 collapsed with no deal; Ukraine overnight barrage 186 drones / 161 downed;
Bahrain radar claims; Liverpool 4-0 Man Utd; Alcaraz wins ATP Finals; Hong Kong
record 98.79% turnout. Layout: broadsheet skeleton (kicker, giant date, sub-headline,
number strip, region bar, UTC strip, 3 heroes, 10 panels, map + list, DATE CHECK).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (26, 26, 26)
NAVY = (30, 58, 95)
RED = (169, 28, 28)
DARKRED = (127, 20, 20)
GREY = (90, 88, 82)
LIGHTGREY = (120, 118, 110)
TEAL = (15, 118, 110)
GOLD = (180, 130, 29)
CREAM2 = (238, 232, 214)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANSB = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", width=None):
    """Draw lines; returns y just below the last line."""
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        if align == "center":
            draw.text((x + (width - draw.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=fill)
        elif align == "right":
            draw.text((x + width - draw.textlength(ln, font=fnt), y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_size(draw, text, fnt_fn, start, max_w, minimum=10):
    """Largest font size (from start down) whose text fits max_w."""
    s = start
    while s > minimum:
        f = fnt_fn(s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return fnt_fn(minimum)


def badge(draw, x, y, label, fill):
    """Small certainty badge; returns width used."""
    f = F_SANSB(10)
    tw = draw.textlength(label, font=f)
    w = int(tw + 12)
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=2, fill=fill)
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def scene_box(draw, box, bg, outline=(60, 60, 60)):
    draw.rectangle(box, fill=bg, outline=outline, width=1)


# ---------------------------------------------------------------- stories
# Every story happened, or was first reported, on Sunday 22 November 2026.
HEROES = [
    {
        "n": 1, "tag": "ANTALYA, TURKIYE · CLIMATE", "badge": ("CONFIRMED", NAVY),
        "head": "COP31 collapses: no deal at all",
        "body": ("After a record 44 hours of overtime, the EU rejects the final "
                 "text — it never names fossil fuels. Kurum: \u201cThere is "
                 "nothing to do.\u201d No deal since Copenhagen 2009."),
        "src": "Reuters, AP",
    },
    {
        "n": 2, "tag": "KYIV REGION, UKRAINE · WAR", "badge": ("REPORTED", TEAL),
        "head": "Russia fires 186 drones: a Kyiv-region block is destroyed",
        "body": ("186 drones and three ballistic missiles overnight; 161 downed; "
                 "strikes at 18 sites. A five-storey block in Dymer is destroyed: "
                 "14 may be trapped."),
        "src": "Ukrainian Air Force via Kyiv Independent",
    },
    {
        "n": 3, "tag": "MANAMA, BAHRAIN · IRAN WAR", "badge": ("CLAIM", RED),
        "head": "Iran claims two US radars hit; Bahrain denies it",
        "body": ("The IRGC says it destroyed two Patriot radars at al-Riffa and "
                 "Awali Sakir. Bahrain says the attacks were intercepted: a fire "
                 "at a civilian site, no injuries."),
        "src": "IRGC statement, Al Jazeera",
    },
]

PANELS = [
    {"n": 4, "tag": "STRAIT OF HORMUZ · IRAN WAR", "head": "Two tankers hit leaving Hormuz",
     "body": "Torkel still burning at anchor Sunday; no casualties.", "src": "UKMTO"},
    {"n": 5, "tag": "GULF OF FINLAND · SEA", "head": "Russian cargo ship Sparta II still burning",
     "body": "Hit Saturday, drifts in Finnish waters; 16 crew safe.", "src": "Reuters"},
    {"n": 6, "tag": "HONG KONG · ELECTION", "head": "Hong Kong votes: record 98.79% turnout",
     "body": "856 candidates, 723 seats; count done 22:15.", "src": "SCMP"},
    {"n": 7, "tag": "WELLINGTON · CRICKET", "head": "India declare on a record 720/9 in New Zealand",
     "body": "Pant 128, Rahul 136; a record Test total in NZ.", "src": "Reuters"},
    {"n": 8, "tag": "LAS VEGAS · FORMULA 1", "head": "Verstappen takes the Las Vegas GP",
     "body": "Beats Norris and Piastri; Russell hits the wall.", "src": "FIA"},
    {"n": 9, "tag": "LIVERPOOL · FOOTBALL", "head": "Liverpool thrash Man Utd 4–0",
     "body": "Szoboszlai, Wirtz, Ngumoha, Muñoz; Yoro off at 8'.", "src": "Reuters"},
    {"n": 10, "tag": "TURIN · TENNIS", "head": "Alcaraz beats Zverev to win the ATP Finals",
     "body": "6-2 7-6(7); a maiden title; a 14th straight win.", "src": "ATP"},
    {"n": 11, "tag": "GAZA CITY · CEASEFIRE", "head": "Hamas seeks urgent talks after aid strike",
     "body": "The strike was Saturday; Hamas calls the meeting Sunday.", "src": "Anadolu"},
    {"n": 12, "tag": "TEHRAN · ENERGY", "head": "Iran begins rationing electricity",
     "body": "Two-hour daily cuts begin as gas output falls.", "src": "Tavnir, RFE/RL"},
    {"n": 13, "tag": "NEW DELHI · DIPLOMACY", "head": "Nepal PM lands in Delhi on first state visit",
     "body": "Balendra Shah; talks with Modi on Monday.", "src": "IANS"},
]

# (number, region, text, source) — 23 items, 14–36
LISTED = [
    (14, "ASIA-PACIFIC", "Manila: Chinese bomber turns back 170 km", "AP"),
    (15, "EUROPE", "Tallinn: Estonia to shut its Russia border from 1 Dec", "Reuters"),
    (16, "AMERICAS", "Washington: Trump shares a senator\u2019s \u201cTrumpCare\u201d plan", "AP"),
    (17, "AFRICA", "DR Congo: Cantine attack, 40 killed", "Local officials"),
    (18, "EUROPE", "Geneva: UN sets path on killer-robot rules", "AP"),
    (19, "ASIA-PACIFIC", "Palawan: Philippines M3.9 quake, 688 km deep", "EMSC"),
    (20, "ASIA-PACIFIC", "Tokyo: 92% feel friendly to South Korea", "JKN"),
    (21, "EUROPE", "London: UK and Ukraine sign drone-production deals", "UK MoD"),
    (22, "EUROPE", "Poland: Sweden IDs downed Russian drone", "Reuters"),
    (23, "EUROPE", "Brussels: EU approves \u20ac1bn military aid for Ukraine", "EU"),
    (24, "EUROPE", "Paris: France seeks UN talks on Kyiv strikes", "France"),
    (25, "MIDDLE EAST", "Gaza: 1,671 killed since truce", "Gaza ministry"),
    (26, "MIDDLE EAST", "Doha: Iran talks to Qatari mediators", "Al Jazeera"),
    (27, "AFRICA", "Nairobi: Kenya nears Ebola-free status", "WHO"),
    (28, "AFRICA", "Khartoum: Drones strike homes near Khartoum", "AFP"),
    (29, "EUROPE", "Vatican: Pope Leo XIV hosts 1,300 poor guests", "Vatican News"),
    (30, "ASIA-PACIFIC", "Serang: Candy-factory fire, 3 dead, 36 missing", "Detiknews"),
    (31, "AMERICAS", "Brasilia: Bolsonaro in intensive care", "Reuters"),
    (32, "OCEANIA", "Canberra: Marles rejects US report on AUKUS subs", "ABC"),
    (33, "ASIA-PACIFIC", "Seoul: AI cheating in college exam", "Reuters"),
    (34, "MIDDLE EAST", "Jerusalem: Eisenkot invites Likud to coalition talks", "Straits Times"),
    (35, "MIDDLE EAST", "Riyadh: Saudi downs Houthi missile aimed at Riyadh", "Anadolu"),
    (36, "EUROPE", "Copenhagen: Denmark expels Russian attaché", "Guardian"),
]

REGIONS = [
    ("EUROPE", (15, 118, 110)),
    ("MIDDLE EAST", (169, 28, 28)),
    ("AMERICAS", (30, 58, 150)),
    ("ASIA-PACIFIC", (180, 120, 30)),
    ("AFRICA", (34, 120, 60)),
    ("OCEANIA", (110, 70, 150)),
    ("WORLD", (100, 100, 100)),
]

NUMBERS = [
    ("186", "drones fired overnight", "Ukrainian Air Force"),
    ("161", "downed or jammed", "Ukrainian Air Force"),
    ("0", "deals agreed at COP31", "UN"),
    ("98.79%", "record HK turnout", "Electoral Affairs Commission"),
    ("720/9", "India's record Test total", "ESPNcricinfo"),
    ("4–0", "Liverpool beat Man Utd", "Reuters"),
]

UTC_STRIP = [
    ("01:00", "HK polls"),
    ("03:00", "Objections"),
    ("04:00", "Lights out"),
    ("06:00", "161 downed"),
    ("08:00", "Plenary"),
    ("14:15", "Count done"),
    ("14:48", "No deal"),
]

DATE_CHECK = (
    "Wires read up to 23:45 UTC, Sunday 22 November 2026. Left out on purpose, first reported "
    "Friday or Saturday: Peru quake (Fri 20 Nov) · Russia's 400-drone barrage (19–20 Nov) · "
    "Shenzhen summit (19 Nov) · \u2018El Chapo Isidro\u2019 capture (Fri night) · Kryvyi Rih "
    "double-tap (Fri 20–Sat 21) · BepiColombo's Mercury burn (Sat) · Basra fire (Sat 21 Nov) · "
    "Bayelsa boat disaster (Fri 20 Nov). Tonight's real count: 186 drones, not 400."
)


# ---------------------------------------------------------------- sections
def header(draw, y):
    # Kicker bar
    draw.rectangle([0, y, W, y + 24], fill=NAVY)
    draw.text((24, y + 4), "THE WORLD IN ONE DAY", font=F_SANSB(15), fill=(255, 255, 255))
    right = "36 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    draw.text((W - 24 - draw.textlength(right, font=F_SANSB(13)), y + 5), right,
              font=F_SANSB(13), fill=(220, 220, 210))
    y += 24
    # Giant date
    f = fit_size(draw, "Sunday 22 November 2026", F_SERIF, 68, W - 48)
    draw.text(((W - draw.textlength("Sunday 22 November 2026", font=f)) / 2, y + 4),
              "Sunday 22 November 2026", font=f, fill=INK)
    y += 4 + f.size + 6
    # Sub-headline: COP31 outcome first, never a sports result
    sub = ("COP31 collapses with no deal  ·  186 drones over Ukraine in the night  ·  "
           "Iran\u2019s radar claim meets Bahrain\u2019s denial")
    fs = fit_size(draw, sub, F_SANSB, 19, W - 48)
    draw.text(((W - draw.textlength(sub, font=fs)) / 2, y), sub, font=fs, fill=RED)
    y += fs.size + 8
    draw.line([24, y, W - 24, y], fill=INK, width=2)
    return y + 4


def number_strip(draw, y):
    h = 52
    cell_w = (W - 48) / len(NUMBERS)
    for i, (fig, label, src) in enumerate(NUMBERS):
        x = 24 + i * cell_w
        ff = fit_size(draw, fig, F_SANSB, 32, cell_w - 12)
        draw.text((x + 4, y), fig, font=ff, fill=RED)
        ly = y + ff.size + 2
        draw.text((x + 4, ly), label, font=F_SANS(11), fill=INK)
        draw.text((x + 4, ly + 13), src, font=F_SANS(9), fill=GREY)
        if i:
            draw.line([x, y + 4, x, y + h - 4], fill=(200, 195, 180), width=1)
    return y + h


def region_bar(draw, y):
    counts = {name: 0 for name, _ in REGIONS}
    for h in HEROES:
        counts["WORLD" if h["n"] == 1 else
               ("EUROPE" if h["n"] == 2 else "MIDDLE EAST")] += 1
    # pictured 4-13 regions: Hormuz ME, Sparta EU, HK AP, Wellington OC, Vegas AM,
    # Liverpool EU, Turin EU, Gaza ME, Tehran ME, Delhi AP
    for r in ["MIDDLE EAST", "EUROPE", "ASIA-PACIFIC", "OCEANIA", "AMERICAS",
              "EUROPE", "EUROPE", "MIDDLE EAST", "MIDDLE EAST", "ASIA-PACIFIC"]:
        counts[r] += 1
    for _, r, _, _ in LISTED:
        counts[r] += 1
    total = sum(counts.values())
    assert total == 36, f"region bar sums to {total}, want 36"
    x = 24
    f = F_SANSB(11)
    for name, color in REGIONS:
        w = (W - 48) * counts[name] / total
        draw.rectangle([x, y, x + w, y + 20], fill=color)
        label = f"{name} {counts[name]}"
        if draw.textlength(label, font=f) <= w - 8:
            draw.text((x + 4, y + 4), label, font=f, fill=(255, 255, 255))
        x += w
    return y + 20


def utc_strip(draw, y):
    draw.rectangle([24, y, W - 24, y + 22], fill=(40, 40, 40))
    draw.text((32, y + 5), "THE DAY IN UTC", font=F_SANSB(11), fill=(255, 210, 90))
    x = 32 + draw.textlength("THE DAY IN UTC", font=F_SANSB(11)) + 14
    slot_w = (W - 24 - x) / len(UTC_STRIP)
    for t, label in UTC_STRIP:
        draw.text((x, y + 5), t, font=F_SANSB(11), fill=(255, 255, 255))
        lx = x + draw.textlength(t, font=F_SANSB(11)) + 5
        lf = F_SANS(10)
        short = label
        while draw.textlength(short, font=lf) > slot_w - (lx - x) - 8 and len(short) > 8:
            short = short[:-2]
        draw.text((lx, y + 6), short, font=lf, fill=(210, 210, 200))
        x += slot_w
    return y + 22


# ---------------------------------------------------------------- scenes
def scene_cop31(draw, box):
    x0, y0, x1, y1 = box
    scene_box(draw, box, (24, 48, 84))
    # hall: long table, delegates, a document with a red X
    draw.rectangle([x0 + 14, y0 + 62, x1 - 14, y1 - 14], fill=(90, 64, 40))
    for i in range(7):
        cx = x0 + 30 + i * 38
        draw.ellipse([cx - 9, y0 + 30, cx + 9, y0 + 48], fill=(220, 200, 160))
        draw.rectangle([cx - 11, y0 + 48, cx + 11, y0 + 62], fill=(70, 90, 130))
    draw.rectangle([x0 + 96, y0 + 66, x0 + 168, y0 + 92], fill=(255, 255, 255))
    draw.line([x0 + 104, y0 + 72, x0 + 160, y0 + 86], fill=RED, width=4)
    draw.line([x0 + 160, y0 + 72, x0 + 104, y0 + 86], fill=RED, width=4)
    draw.text((x0 + 10, y0 + 6), "NO DEAL", font=F_SANSB(16), fill=(255, 90, 70))


def scene_ukraine(draw, box):
    x0, y0, x1, y1 = box
    scene_box(draw, box, (12, 16, 42))
    # skyline with lit windows, drones as yellow crosses, one tilted block
    for i, (bx, bw, bh) in enumerate([(8, 34, 52), (48, 26, 70), (80, 40, 44), (126, 30, 62),
                                      (162, 36, 50), (204, 28, 66), (238, 34, 46), (278, 26, 58)]):
        draw.rectangle([x0 + bx, y1 - 14 - bh, x0 + bx + bw, y1 - 14], fill=(40, 44, 70))
        for wy in range(y1 - 14 - bh + 6, y1 - 18, 12):
            for wx in range(x0 + bx + 5, x0 + bx + bw - 4, 10):
                if (wx + wy) % 20 < 10:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
    # tilted damaged block
    draw.polygon([(x0 + 96, y1 - 30), (x0 + 140, y1 - 44), (x0 + 148, y1 - 14), (x0 + 104, y1 - 14)],
                 fill=(90, 60, 50))
    for cx, cy in [(60, 22), (150, 14), (240, 26), (300, 16)]:
        draw.line([x0 + cx - 6, y0 + cy, x0 + cx + 6, y0 + cy], fill=(255, 210, 90), width=2)
        draw.line([x0 + cx, y0 + cy - 6, x0 + cx, y0 + cy + 6], fill=(255, 210, 90), width=2)


def scene_bahrain(draw, box):
    x0, y0, x1, y1 = box
    scene_box(draw, box, (16, 22, 52))
    # two radar dishes + flame bursts
    for cx in (86, 220):
        draw.polygon([(x0 + cx - 26, y0 + 52), (x0 + cx + 26, y0 + 52), (x0 + cx, y0 + 26)],
                     outline=(200, 200, 200), width=3)
        draw.line([x0 + cx, y0 + 52, x0 + cx, y0 + 78], fill=(200, 200, 200), width=3)
        draw.rectangle([x0 + cx - 22, y0 + 78, x0 + cx + 22, y1 - 12], fill=(70, 74, 80))
    for fx, fh in [(40, 26), (150, 34), (262, 22)]:
        draw.polygon([(x0 + fx - 12, y1 - 12), (x0 + fx, y1 - 12 - fh), (x0 + fx + 12, y1 - 12)],
                     fill=(255, 140, 40))
        draw.polygon([(x0 + fx - 6, y1 - 12), (x0 + fx, y1 - 12 - fh + 10), (x0 + fx + 6, y1 - 12)],
                     fill=(255, 220, 90))


def scene_generic(draw, box, kind):
    """Small pictogram scenes for panels 4-13."""
    x0, y0, x1, y1 = box
    bgs = {"ship": (28, 60, 90), "vote": (90, 60, 30), "sport": (30, 90, 50),
           "city": (60, 60, 80), "plane": (40, 80, 110), "power": (80, 70, 20),
           "aid": (120, 40, 40), "flag": (30, 70, 100)}
    scene_box(draw, box, bgs.get(kind, (50, 60, 80)))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "ship":
        draw.rectangle([x0 + 20, cy - 4, x1 - 20, cy + 12], fill=(40, 40, 46))
        draw.polygon([(x0 + 52, cy - 26), (x0 + 62, cy - 26), (x0 + 58, cy - 4)], fill=(200, 200, 200))
        for fx in (x0 + 40, x0 + 110, x1 - 46):
            draw.polygon([(fx - 9, cy - 4), (fx, cy - 22), (fx + 9, cy - 4)], fill=(255, 140, 40))
        draw.rectangle([x0, y1 - 10, x1, y1 - 1], fill=(20, 50, 90))
    elif kind == "vote":
        draw.rectangle([cx - 26, cy - 8, cx + 26, cy + 20], fill=(250, 250, 250))
        draw.rectangle([cx - 26, cy - 8, cx + 26, cy + 2], fill=(169, 28, 28))
        draw.line([cx - 14, cy + 12, cx - 4, cy + 20], fill=(30, 120, 60), width=3)
        draw.line([cx - 4, cy + 20, cx + 18, cy - 2], fill=(30, 120, 60), width=3)
    elif kind == "cricket":
        draw.rectangle([cx - 30, cy + 8, cx + 30, cy + 14], fill=(120, 90, 40))
        draw.polygon([(cx - 4, cy - 20), (cx + 6, cy - 20), (cx + 2, cy + 8), (cx - 8, cy + 8)],
                     fill=(200, 160, 100))
        draw.ellipse([cx + 14, cy - 16, cx + 26, cy - 4], fill=(200, 40, 40))
        draw.rectangle([cx - 26, cy + 16, cx - 14, cy + 20], fill=(250, 250, 250))
        draw.rectangle([cx - 2, cy + 16, cx + 10, cy + 20], fill=(250, 250, 250))
        draw.rectangle([cx + 14, cy + 16, cx + 26, cy + 20], fill=(250, 250, 250))
    elif kind == "f1":
        for r in range(2):
            for c in range(5):
                if (r + c) % 2 == 0:
                    draw.rectangle([x0 + 14 + c * 12, y0 + 8 + r * 12,
                                    x0 + 26 + c * 12, y0 + 20 + r * 12], fill=(20, 20, 20))
        draw.polygon([(x0 + 90, cy + 16), (x1 - 30, cy + 16), (x1 - 44, cy + 2),
                      (x0 + 110, cy + 2)], fill=(200, 30, 30))
        draw.ellipse([x0 + 104, cy + 10, x0 + 116, cy + 22], fill=(20, 20, 20))
        draw.ellipse([x1 - 46, cy + 10, x1 - 34, cy + 22], fill=(20, 20, 20))
    elif kind == "football":
        draw.ellipse([cx - 20, cy - 16, cx + 20, cy + 16], fill=(250, 250, 250),
                     outline=(30, 30, 30), width=2)
        draw.polygon([(cx, cy - 8), (cx + 8, cy - 2), (cx + 5, cy + 8), (cx - 5, cy + 8),
                      (cx - 8, cy - 2)], fill=(30, 30, 30))
        for dx, dy in [(-14, -8), (14, -8), (-16, 8), (16, 8), (0, -14)]:
            draw.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=(30, 30, 30))
    elif kind == "tennis":
        draw.ellipse([cx - 20, cy - 16, cx + 20, cy + 16], fill=(190, 220, 60),
                     outline=(120, 150, 40), width=2)
        draw.arc([cx - 20, cy - 16, cx + 20, cy + 16], 300, 60, fill=(250, 250, 250), width=3)
        draw.arc([cx - 20, cy - 16, cx + 20, cy + 16], 120, 240, fill=(250, 250, 250), width=3)
    elif kind == "sport":
        draw.ellipse([cx - 26, cy - 18, cx + 26, cy + 18], fill=(250, 250, 250),
                     outline=(30, 30, 30), width=2)
        draw.arc([cx - 26, cy - 18, cx + 26, cy + 18], 20, 160, fill=(30, 30, 30), width=2)
        draw.arc([cx - 26, cy - 18, cx + 26, cy + 18], 200, 340, fill=(30, 30, 30), width=2)
    elif kind == "plane":
        draw.polygon([(x0 + 30, cy), (x1 - 30, cy - 12), (x1 - 30, cy + 12)], fill=(230, 230, 230))
        draw.polygon([(cx - 8, cy - 4), (cx + 8, cy - 4), (cx + 2, cy - 22)], fill=(200, 200, 200))
    elif kind == "power":
        draw.polygon([(cx + 6, y0 + 8), (cx - 12, cy + 4), (cx + 2, cy + 4), (cx - 6, y1 - 10),
                      (cx + 14, cy - 6), (cx, cy - 6)], fill=(255, 220, 60))
    elif kind == "aid":
        draw.rectangle([cx - 24, cy - 12, cx + 24, cy + 14], fill=(250, 250, 250))
        draw.rectangle([cx - 6, cy - 22, cx + 6, cy + 24], fill=(200, 40, 40))
        draw.rectangle([cx - 16, cy - 2, cx + 16, cy + 8], fill=(200, 40, 40))
    else:  # city / flag fallback: skyline
        for i, bh in enumerate([26, 38, 22, 34, 28]):
            bx = x0 + 14 + i * 32
            draw.rectangle([bx, y1 - 12 - bh, bx + 24, y1 - 12], fill=(30, 34, 52))
            draw.rectangle([bx + 8, y1 - 12 - bh + 6, bx + 16, y1 - 12 - bh + 12],
                           fill=(255, 210, 90))


PANEL_SCENES = {4: "ship", 5: "ship", 6: "vote", 7: "cricket", 8: "f1",
                9: "football", 10: "tennis", 11: "aid", 12: "power", 13: "plane"}
HERO_SCENES = {1: scene_cop31, 2: scene_ukraine, 3: scene_bahrain}


# ---------------------------------------------------------------- layout
def hero_block(draw, x, y, w, hero):
    scene_h = 90
    HERO_SCENES[hero["n"]](draw, (x, y, x + w, y + scene_h))
    y += scene_h + 4
    # dateline banner: badge right-aligned INSIDE the banner, tag truncated to fit
    label, color = hero["badge"]
    bf = F_SANSB(10)
    bw = int(draw.textlength(label, font=bf) + 12)
    draw.rectangle([x, y, x + w, y + 17], fill=RED)
    tag = f"{hero['n']} · {hero['tag']}"
    while draw.textlength(tag, font=F_SANSB(10)) > w - bw - 14 and len(tag) > 10:
        tag = tag[:-2]
    draw.text((x + 5, y + 3), tag, font=F_SANSB(10), fill=(255, 255, 255))
    draw.rounded_rectangle([x + w - bw, y + 1, x + w, y + 16], radius=2, fill=color)
    draw.text((x + w - bw + 6, y + 3), label, font=bf, fill=(255, 255, 255))
    y += 21
    # headline
    y = draw_lines(draw, x, y, wrap(draw, hero["head"], F_SANSB(17), w), F_SANSB(17),
                   fill=INK, leading=20)
    y += 2
    # body
    y = draw_lines(draw, x, y, wrap(draw, hero["body"], F_SANS(12), w), F_SANS(12),
                   fill=(50, 50, 50), leading=15)
    draw.text((x, y + 2), f"({hero['src']})", font=F_SANS(10), fill=GREY)
    return y + 16


def panel_block(draw, x, y, w, panel):
    scene_h = 40
    scene_generic(draw, (x, y, x + w, y + scene_h), PANEL_SCENES[panel["n"]])
    y += scene_h + 3
    draw.rectangle([x, y, x + w, y + 14], fill=RED)
    draw.text((x + 4, y + 2), f"{panel['n']} · {panel['tag']}", font=F_SANSB(9),
              fill=(255, 255, 255))
    y += 17
    y = draw_lines(draw, x, y, wrap(draw, panel["head"], F_SANSB(13), w), F_SANSB(13),
                   fill=INK, leading=14)
    y = draw_lines(draw, x, y, wrap(draw, panel["body"], F_SANS(11), w), F_SANS(11),
                   fill=(50, 50, 50), leading=12)
    draw.text((x, y + 1), f"({panel['src']})", font=F_SANS(9), fill=GREY)
    return y + 11


# Rough world map: schematic continents in a lat/lon-ish box.
CONTINENTS = [
    [(0.03, 0.18), (0.10, 0.08), (0.20, 0.10), (0.27, 0.20), (0.24, 0.32), (0.16, 0.42),
     (0.10, 0.38), (0.04, 0.30)],  # North America
    [(0.20, 0.52), (0.27, 0.48), (0.31, 0.60), (0.28, 0.78), (0.23, 0.72), (0.19, 0.60)],
    [(0.46, 0.10), (0.52, 0.06), (0.57, 0.14), (0.55, 0.26), (0.48, 0.28), (0.45, 0.18)],
    [(0.46, 0.32), (0.54, 0.30), (0.58, 0.42), (0.55, 0.62), (0.49, 0.66), (0.46, 0.48)],
    [(0.58, 0.08), (0.72, 0.06), (0.86, 0.10), (0.94, 0.22), (0.88, 0.38), (0.78, 0.44),
     (0.68, 0.36), (0.60, 0.26), (0.57, 0.16)],  # Asia
    [(0.82, 0.62), (0.90, 0.60), (0.93, 0.72), (0.86, 0.78), (0.81, 0.70)],  # Australia
]
# (lon -180..180, lat -60..85) -> map coords; pins for pictured stories 1-13
PINS = {1: (28, 41), 2: (31, 50), 3: (51, 26), 4: (57, 26), 5: (24, 60), 6: (114, 22),
        7: (175, -41), 8: (-115, 36), 9: (-3, 53), 10: (7, 45), 11: (34, 31),
        12: (51, 36), 13: (77, 29)}


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(198, 222, 235), outline=(60, 60, 60), width=1)
    for poly in CONTINENTS:
        pts = [(x + px * w, y + py * h) for px, py in poly]
        draw.polygon(pts, fill=(232, 216, 180), outline=(150, 130, 100))
    for n, (lon, lat) in PINS.items():
        px = x + (lon + 180) / 360 * w
        py = y + (85 - lat) / 145 * h
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
        t = str(n)
        draw.text((px - draw.textlength(t, font=F_SANSB(8)) / 2, py - 5), t,
                  font=F_SANSB(8), fill=(255, 255, 255))


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0
    y = header(d, y)
    y = number_strip(d, y + 4)
    y = region_bar(d, y + 6)
    y = utc_strip(d, y + 6)
    y += 8
    # heroes: 3 columns — use the tallest hero's real bottom
    gap, col_w = 12, (W - 48 - 24) // 3
    hx = 24
    hy = y
    hero_bottom = hy
    for hero in HEROES:
        hero_bottom = max(hero_bottom, hero_block(d, hx, hy, col_w, hero))
        hx += col_w + gap
    y = hero_bottom + 4
    # section header
    d.text((24, y), "MORE FROM THE DAY", font=F_SANSB(13), fill=RED)
    y += 16
    # panels: 5 columns x 2 rows
    pcol = (W - 48 - 4 * 10) // 5
    py = y
    for row in range(2):
        px = 24
        row_bottom = py
        for panel in PANELS[row * 5:(row + 1) * 5]:
            bottom = panel_block(d, px, py, pcol, panel)
            row_bottom = max(row_bottom, bottom)
            px += pcol + 10
        py = row_bottom + 2
    y = py + 2
    # map + list
    d.text((24, y), "WHERE IT HAPPENED", font=F_SANSB(12), fill=RED)
    d.text((340, y), "ALSO ON SUNDAY 22 NOVEMBER — 23 MORE STORIES",
           font=F_SANSB(12), fill=RED)
    y += 16
    map_h = 132
    draw_map(d, 24, y, 300, map_h)
    # list in two columns, one line per story
    lx, lw = 340, 330
    ly = y
    half = (len(LISTED) + 1) // 2
    for col_i, chunk in enumerate([LISTED[:half], LISTED[half:]]):
        cx = lx + col_i * (lw + 10)
        cy = ly
        for n, region, text, src in chunk:
            line = f"{n}  {text} ({src})"
            lines = wrap(d, line, F_SANS(10), lw)
            cy = draw_lines(d, cx, cy, lines, F_SANS(10), leading=11)
    y = ly + map_h + 6
    # DATE CHECK — 4 lines of text
    d.rectangle([24, y, W - 24, y + 69], outline=RED, width=2)
    d.text((32, y + 4), "DATE CHECK", font=F_SANSB(11), fill=RED)
    draw_lines(d, 32, y + 19, wrap(d, DATE_CHECK, F_SANS(10.5), W - 64), F_SANS(10.5),
               leading=12)
    y += 73
    # footer: one line
    d.text((24, y), "Every story here happened, or was first reported, on Sunday 22 November 2026. "
                    "Sources named beside each story · original drawings",
           font=F_SANS(10), fill=GREY)
    cert = ("CERTAINTY: CONFIRMED = settled by 2+ outlets · REPORTED = carried by the day\u2019s "
            "wires · CLAIM = one side\u2019s account, labelled as such")
    d.text((W - 24 - d.textlength(cert, font=F_SANS(9)), y + 14), cert,
           font=F_SANS(9), fill=GREY)
    # bottom navy bar
    d.rectangle([0, H - 22, W, H], fill=NAVY)
    d.text((24, H - 17), "THE WORLD IN ONE DAY", font=F_SANSB(11), fill=(255, 255, 255))
    tail = "SUNDAY 22 NOVEMBER 2026 · ONE PAGE"
    d.text((W - 24 - d.textlength(tail, font=F_SANSB(11)), H - 17), tail,
           font=F_SANSB(11), fill=(255, 255, 255))
    return img


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = draw_page()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, optimize=True)
    print(f"wrote {path} {img.size} {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
