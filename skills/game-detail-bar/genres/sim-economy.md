# Genre guide: sims and economies

Read this on top of the core rules in [../SKILL.md](../SKILL.md) for any game built around a money or resource loop:
days or seasons, a shop, upgrades, orders, customers, quotas, collecting (fishing, farming, cooking, running a
stall or a town), and incremental or idle games whose numbers grow forever (section 6). Example numbers are in [../reference.md](../reference.md).

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

## 6. Incremental and idle loops

For games whose numbers grow forever (clickers, idle games, simulator-style "train, upgrade, rebirth" loops). Their
pull is anticipation of the next bigger thing, not fear of losing.

- **No loss at all.** The main action always pays; luck only varies upward (a bad roll is a common item, never a
  loss); there is no deadline, only the next visible goal. Mixing in a fail state halfway loses both kinds of pull.
- **The first action is the main reward.** Name the peak the loop builds toward (smashing the boss, opening the
  egg), hand the player the tool for it at spawn and put the target straight ahead, so the first thing they ever do
  is the payoff. Supporting systems (selling, a shop, a collection) are taught only when the player needs them.
- **Show something better than what the player has, in the first minute and in view:** a rival with a bigger item, a
  later tier in use, a locked area with something happening in it. Desire comes from seeing it, not from a text goal.
  Computer rivals are labelled as such; never pass them off as real players.
- **Make late-game scale absurd,** and visible in the world: the thing that grows starts normal and ends ridiculous
  (grow length much faster than width so the player is never hidden; cap it where there is no room), and the base or
  workshop changes look with each tier so progress reads from a distance.
- **Space the big rewards like a level curve.** The wait between two big rewards grows by a small step each time and
  never multiplies; check it with a pacing simulation that caps the longest wait in the first 20 minutes.
- **More levels, not pricier levels.** When an upgrade maxes out too early, give it more levels with smaller steps
  instead of steeper prices; each level is a small purchase beat, a steep price is a wall.
- **Boosts are optional offers.** A short boost appears where the player is looking and is taken with one tap; if
  ignored, the normal effect still happens, so an idle player is never punished and nothing interrupts the loop.
- **Time away always progresses:** income while away (capped, the cap shown), collected on one welcome-back claim
  that pays even if closed; a hidden tab plays out its time when the player returns. Menus never pause the world.

## Checklist

- [ ] Goals shown up front; days or seasons differ; orders grow with gear and never ask for locked things.
- [ ] Nothing confiscates earned progress; failures cost a bounded, recoverable amount.
- [ ] Upgrades in levels, visible in the world; rarity tiers; a journal with silhouettes.
- [ ] The core action's feedback and gauge scale with what is at stake.
- [ ] A bot simulation with weak, average and good players supports the prices and quotas.
- [ ] Incremental games: no loss; the first action is the main reward; something better is visible in the first
      minute; late scale is absurd and shows in the world; big rewards spaced like a level curve; more levels rather
      than pricier ones; boosts are optional; time away progresses.
