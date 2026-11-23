# Sunday 22 November 2026 — The World in One Day

One 1024×1024 image summing up Sunday 22 November 2026's world news: 36 stories across 7 regions, every one dated that Sunday — COP31 collapsing with no deal at all in Antalya, Russia firing 186 drones at Ukraine overnight (161 downed), and India declaring on a record 720-9 in Wellington.

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Iruwae/news-image-20261122-entry-r8/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Iruwae/news-image-20261122-entry-r8/reward.svg)](https://make.fun/bounty/news-image-20261122)

[View the bounty on make.fun](https://make.fun/bounty/news-image-20261122)

## How it is built

`draw.py` (Python 3 + PIL) draws `entry.png` from scratch: masthead, a "The Day in UTC" strip, a six-number strip (186 / 161 / 0 / 98.79% / 720-9 / 4–0), a region bar, 3 illustrated hero stories, 10 illustrated panels, a world map with numbered pins, a 23-item story list, and a date check that names what was deliberately left out (stories first reported Friday or Saturday) and what had not happened yet at the wire cutoff.

`main.ts` (Node, standard library only) runs `draw.py` with the output directory (`$MAKEFUN_OUTPUT_DIR`, default `/output`) and verifies `entry.png` was produced.

## Run it

```sh
python3 draw.py out                    # regenerate entry.png into out/
MAKEFUN_OUTPUT_DIR=out node main.ts    # regenerate + verify
```

All illustrations are original flat-vector drawings. No photos, no downloads, no copied images.
