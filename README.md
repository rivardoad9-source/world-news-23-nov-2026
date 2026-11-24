# world-news-23-nov-2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rivardoad9-source/world-news-23-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/rivardoad9-source/world-news-23-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One 1024×1024 image summing up the world news of Monday 23 November 2026: COP31 ends with no deal, Ukraine's claim that its sea drone sank a Russian warship in Libya, more ships hit in the Strait of Hormuz, aid workers killed in Gaza, Democrats reaching 259 US House seats, the Banten factory fire, student protests across Europe and the Zanzibar hotel fires.

![entry](entry.png)

The illustrations are hand-written SVG (`design/scenes.py`), laid out as a bento grid (`design/build.py`) and rendered once with a headless browser. `main.py` copies the committed `entry.png` to `/output/entry.png` (standard library only, no network, same bytes every run).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python main.py && python -m unittest test_main
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=a8dvmwfr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
