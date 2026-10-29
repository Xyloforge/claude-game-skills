# Genre guide: sims and economies

Read this on top of the core rules in [../SKILL.md](../SKILL.md) for any game built around a money or resource loop:
days or seasons, a shop, upgrades, orders, customers, quotas, collecting (fishing, farming, cooking, running a
stall or a town). Example numbers are in [../reference.md](../reference.md).

## 1. The loop

- **Goals told up front:** a goal card at the start of each day or season with two or three star goals, progress in
  the pause menu, and a first-day hint that points at the first goal.
- **Days or seasons have their own character:** seeded content that is the same on reload, morning and night (or
  seasons) with their own roster, light grade, ambience and music.
- **Orders and quotas grow with the player's gear,** so nothing becomes free late, and **never ask for what the
  player cannot have yet**.
- **Customers have patience you can see:** a speech bubble with a fuse that burns amber, then red, then the customer
  sighs and leaves.

## 2. Fairness

- **Never take away earned progress.** A mechanic that steals what the player already won (a thief that grabs the
  catch) feels like punishment. Use optional risk the player chooses instead: a bonus for speed, a chance at more.
- **Missing a goal costs a streak or a bonus, never money already earned.**
- **Letting go always loses the current attempt, and full gear always wins within its tier's time,** so skill and
  upgrades both matter and neither is a lottery.
- **A failure costs a bounded, recoverable amount** (a share of carried money that can be picked up again).

## 3. Upgrades and collecting

- **Upgrades come in levels** (for example three, plus a gated legendary fourth) and are **visible in the world:** a
  new part on the tool, the stall showing what was caught, a hat that changes prices.
- **Price the strongest lines highest,** and say why in a comment ("not too strong: expensive but balanced").
- **Rarity tiers on everything collectable,** legendaries strange rather than bigger and truly rare (about 1% base,
  more with a charm), arriving with a shimmer, a sound and a banner, and leaving if ignored.
- **A journal:** silhouettes for undiscovered things, flavor text, times found, records, and a NEW or BIGGEST card
  with a count-up.

## 4. Feel of the core action

- **Feedback scales with the size of what was won:** a small catch gets a small shake and freeze; a huge one gets a
  zoom, a long freeze, a splash and a banner.
- **The struggle has a gauge that grows out of the thing it measures** (a catch bar coming out of the fish), with tick
  marks, a glow when in the zone, a flash in danger and a shake when losing.
- **Diegetic UI:** a chalkboard quota in the world, a wanted poster stamped PAID, orders on paper slips.

## 5. Balance by simulation

- **Model the economy before tuning by feel.** A simulator loads the game's real rule files (for example in a Node
  `vm` sandbox) and plays whole days with weak, average and good bots: reaction delay, input noise, aim time, hit
  chance and a sensible greedy shop order.
- **Print per day:** goal pass rate, money, and the day each upgrade is owned. Tune prices to target times ("an
  average player meets the quota 90%+ on days 1 to 10 and owns everything around day 11 to 14; weak players
  struggle late").
- **A curve mode** that prints the success rate per catch, order or target for each gear setup.
- **Comment where every measured number came from** ("a served customer is replaced about 8.5 s after the sale,
  measured in game").

## Checklist

- [ ] Goals shown up front; days or seasons differ; orders grow with gear and never ask for locked things.
- [ ] Nothing confiscates earned progress; failures cost a bounded, recoverable amount.
- [ ] Upgrades in levels, visible in the world; rarity tiers; a journal with silhouettes.
- [ ] The core action's feedback and gauge scale with what is at stake.
- [ ] A bot simulation with weak, average and good players supports the prices and quotas.
