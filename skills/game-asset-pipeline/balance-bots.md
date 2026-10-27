# Balance with bots

Tune by simulation, then confirm with one real play-test number. Two patterns from the user's games:

## 1. Economy and season sim
- Load the game's **real rule files** into a Node `vm` sandbox, so the sim runs the same code as the game, not a copy.
- Define skill profiles: `weak`, `avg`, `good`. Each has a reaction delay, how far ahead it looks, input noise, tap rate, aim time, hit chance, and how often it goes for the best target.
- The fight bot plays the real fight step: it looks at a marker seen `delay` seconds ago, imagines holding or not for `look` seconds, and picks the closer one.
- Model what you can't simulate cheaply (aiming, throwing) with measured numbers, and comment where each came from ("a served customer is replaced about 8.5 s after the catch lands, measured in game").
- Give the bot a sensible greedy shop order.
- Print per day: quota met %, coins, the day each upgrade is owned. Target lines such as: average player meets the quota 90%+ on days 1 to 10; owns everything around day 11 to 14; weak players struggle late.
- `CURVE=1` mode: land rate per species per gear setup ("let go always loses; full gear lands everything").

## 2. Whole-stage bots
- Bots press real inputs into the real simulation step: a skilled bot (dodges tells, picks up heals when hurt, steps off hazards), a button-masher (never dodges), and a mode-specific bot (a rider).
- Run 6 to 10 seeds each and assert **ranges**:
  - a skilled clear averages 2 to 5 bot minutes (bots are about 3x faster than people);
  - a masher does not always clear (at most 8 of 10);
  - a rider clears at least 5 of 6.
- Comment why each floor is what it is, and lower it with a note when the author makes a fight harder on purpose.

## 3. Deterministic rule checks (every game's `verify.js`)
Parry and dodge windows, combo routing, odds tables (70/24/6), save migration, exactly-once payouts, fairness rules (orders never ask for locked items), each fish or boss beatable within its time on full gear and never with no input.
