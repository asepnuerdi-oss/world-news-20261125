# The World in One Image — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/asepnuerdi-oss/world-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/asepnuerdi-oss/world-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

An entry for the make.fun bounty **"Sum up 25 November's world news in one
image"**.

`main.py` (Python 3.13, standard library only) writes the bundled artwork
`world-news-2026-11-25.png` to `/output/entry.png`. The output is a
byte-for-byte copy of the stored image, so every run produces identical
bytes. No network access is used.

The image is a one-page newspaper front page of Wednesday 25 November 2026:

- **Space / China–Pakistan (lead)** — Shenzhou-24 launches carrying
  Muhammad Zeeshan Ali, the first Pakistani in orbit and the first foreign
  astronaut aboard China's Tiangong space station.
- **Hormuz** — Iran says two oil tankers struck mines and caught fire in the
  Strait of Hormuz; the claim is unverified.
- **Pacific** — Australia and Solomon Islands sign a security treaty making
  Canberra Honiara's primary partner; no foreign military base on its soil.
- **Colombia** — security forces storm a Cartagena supermarket at dawn and
  free all remaining hostages after a day-long siege.
- **Bangladesh** — the garment minimum wage rises 36% after weeks of
  protests that shut factories.
- **Indonesia** — three bodies are recovered from a flooded illegal gold
  mine in Bogor; 23 miners are still trapped.
- **Markets** — Asian stocks slide in an AI sell-off: Nikkei down 2.8%,
  Kospi down 6.2%.

The artwork was drawn programmatically (Python + Pillow) from the day's
wire reports (Reuters, Xinhua, AP, AFP and PM.gov.au). See `NEWS_SOURCES.md`
for the source headline behind every panel.

## Run

```bash
python3 main.py   # writes /output/entry.png (1024x1024 PNG, < 1 MiB)
```

## License

MIT — see `LICENSE`.
