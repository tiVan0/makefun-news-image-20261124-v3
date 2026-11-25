# The World Today — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/tiVan0/makefun-news-image-20261124-v3/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/tiVan0/makefun-news-image-20261124-v3/reward.svg)](https://make.fun/bounty/news-image-20261124)

One image that sums up the world's news of **Tuesday 24 November 2026**:
an improved newspaper front page — masthead with the giant date,
three picture-led leads, a labelled world map with 13 numbered pins,
35 stories across 7 regions plus the world, a DATE CHECK strip, and a
BY THE NUMBERS strip in which every figure carries its label.

## What changed since v1 and v2

- **Tighter curation, not more stories.** v1 (35 stories, newspaper)
  scored 0.656078 / 0.619464; v2 (50 stories, dense broadsheet) scored
  0.550748 — density alone hurt. v3 keeps 35 stories and drops v1's
  weakest: the CrowdStrike–Zscaler deal (announced Monday 23 Nov),
  the FIFA 2031 hosts (named Monday 23 Nov) and the Venezuela pivot
  (18 Nov). They are named in the DATE CHECK strip as left out, not
  presented as Tuesday news.
- **Better map.** v1's Middle East pin labels collided and its
  continents were crude sketches. v3 draws recognisable multi-point
  continent shapes and uses numbered pins with leader lines where
  badges would touch (Paris/Brussels, Zaporizhzhia/Antalya/Gaza),
  plus a two-column legend — no two labels can collide.
- **Tuesday's own numbers.** Every market figure is the official
  close: Dow 50,018.70 (+0.85%, first close above 50,000), Nasdaq
  23,733.54 (−1.48%), S&P 500 7,201.09 (−0.50%), Nvidia −5.9% on
  Tuesday after +31.5% on Monday — never an intraday snapshot.

## Leads

1. **Nvidia** — Huang's comeback fades in a day: −5.9% Tuesday after
   the record +31.5% Monday rally (bar chart drawn in).
2. **Sanofi** buys Insmed for $41bn in cash, $175 a share — the
   year's biggest pharma deal (pill drawn in).
3. **Ukraine** sinks the Russian corvette Merkury off Benghazi with
   7 sea drones and hits the cargo ship Angara (ship drawn in).

## How it is made

`render.py` draws the whole page deterministically with Pillow
(DejaVu fonts) and writes `entry.png` (1024×1024, under 1 MiB).
`main.py` is a stdlib-only copier: it copies `entry.png` into
`$MAKEFUN_OUTPUT_DIR/entry.png`, checks the copy is a complete PNG
of the same size, and sets mode 0644. No network, no randomness —
running the program twice writes byte-identical output.

## Facts

Every story was checked against primary sources dated 24 November
2026: Reuters, BBC, AP, Al Jazeera, UN News, Sanofi's own press
release, WSJ and Morningstar. Claims the wires flagged as
unverified (Iran's Hormuz tanker claim, Houthi casualty claims) are
labelled as claims in the paper. COP31 closed on Sunday 22 Nov; the
paper carries the UN reaction published Tuesday 24 Nov, and the
DATE CHECK strip says so.

## Stories (35, 7 regions + world)

Leads: Nvidia, Sanofi–Insmed, Merkury. Then: North America
(Washington, New York, Florida, Austin), Europe (Zaporizhzhia,
Brussels, Belgium, Paris, Moscow, NATO), Middle East (Hormuz, Gaza,
Riyadh, Antalya, Jerusalem), Africa (Dakar, Kinshasa, Abuja),
Asia (Tokyo, Seoul, Hanoi, Kuala Lumpur, Jakarta, Islamabad,
Lahore), Oceania (Honiara), Latin America (Cúcuta), World
(US measles count).

## License

MIT — see [LICENSE](LICENSE).
