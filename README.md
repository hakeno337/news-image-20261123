# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/hakeno337/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/hakeno337/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world's news of Monday 23 November 2026, set as an illustrated broadsheet front page under a full-width date band: the COP31 climate talks in Antalya ending without a deal (drawn globe and thermometer), the AI sell-off rattling world markets (Nikkei −5.06%), the Russian strike on Dymer, Ukraine, the Democrats' largest US House majority since 1992, tankers ablaze near Hormuz — each grid story with its own small icon — plus a ticker with the Banten factory fire, Márquez's eighth MotoGP title and Alcaraz's ATP Finals crown.

## Run it

```sh
node main.ts
```

The program copies the repository's `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR/entry.png` outside the grader), after checking it against the gate's limits (PNG or JPEG, at most 1 MiB, at most 1024 by 1024). Node 22, standard library only.

The image itself is composed by `compose.py` (Python + PIL): the day's stories, researched from 23 November's reporting, drawn and set as a legible illustrated front page at 1024 by 1024. Rebuild it with `python3 compose.py`.
