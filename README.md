[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ASEP9929/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/ASEP9929/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World in One Day — 20 November 2026

One image summing up the world news of Friday, 20 November 2026,
drawn procedurally for make.fun's `news-image-20261120` bounty.

## What the day held

- **Three leaders, one table** — Trump, Xi and Putin hold the
  first-ever three-way summit in Shenzhen, China, talking nuclear arms
  control, energy security and Ukraine.
- **Court: Myanmar committed genocide** — the UN's top court rules
  Myanmar committed genocide against the Rohingya minority.
- **Cyclone Akvan hits India's coast** — the storm makes landfall in
  Odisha; 300,000 evacuated, 423 rescue teams deployed.
- **Voyager 1, one light-day away** — NASA confirms the probe is a
  full light-day from Earth, the farthest human-made object ever.
- **GTA VI passes $1.8 billion** — a day after launch, GTA 6 sales
  already top The Odyssey's $1.8bn global box-office run.
- **Embassies hit in Kyiv strikes** — Russian strikes damage the
  Austrian and Dutch embassies in Kyiv, officials say.

## How it is built

`gen_image.py` draws the front page with PIL (flat vector style,
DejaVu fonts): a masthead naming the day and six panels, one per story,
each with a short headline, a two-to-three-line summary and a small drawn
pictogram. `main.ts` (Node, standard library only, no network) copies
the resulting `entry.png` to `/output/entry.png`, so two runs write the
same bytes. The image is 1024×1024 PNG, 99,177 bytes — under the 1 MiB
cap — and two runs of `main.ts` produce byte-identical output (verified
locally).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see `LICENSE`.
