# Genre guide: real-time multiplayer

Read this on top of the core rules in [../SKILL.md](../SKILL.md) for any game where two or more players share one live
game over a network: co-op or versus, browser or native. It is about how the game is split between devices and how to
test it, whatever the genre. Example numbers are in [../reference.md](../reference.md).

## 1. Pick the model on purpose

| Model | How it works | Feels like | Use it for |
| --- | --- | --- | --- |
| Host streams a picture | One device runs everything and sends what it draws; others send buttons | Every action a guest takes waits a full round trip (150-300 ms online) | A quick prototype only |
| **Each player owns their own character** (recommended for co-op) | Each device runs its own character at once; one host owns the shared world | Your own actions are instant; others and enemies are slightly in the past | Co-op and casual versus games ("friend games") |
| Server-authoritative state with prediction | A server runs the world; clients predict their own movement and correct | Instant movement, corrections on disagreement | Competitive games, anything with strangers |
| Lockstep or rollback | Every device runs the same simulation from the same inputs | Exact; rollback hides delay | Fighting games, strategy games with many units |

The common first mistake is the picture stream: it is quick to build, but a guest's own character answers a round trip
late, and predicting movement alone is not enough, because attacks and abilities still lag. Decide the model before
building the game, because every ability's code has to respect it.

## 2. Owner-runs-their-character, in detail

**Who owns what:**
- **Each player's device:** its character's movement, dashes, ability casts, cooldowns, meters and the effects of
  its own abilities. They answer on the frame the key goes down.
- **The host (or server):** the shared world: enemies, health of every character, loot, doors and level changes,
  bosses, timers, the score.

**Hitting the world:**
- A player's abilities hit a **local mirror** of the enemies (positions, sizes, facing and status flags from the host),
  drawn where the player sees them. What you see is what you hit.
- The device sends **actions**, not results: "hit enemy 12 for 15 with these options", "launch enemy 7", "break prop
  4", "trigger the trap at x,y". The host applies them **in that player's name** (their relics, passives and bonuses)
  and quietly (no second spark), then sends back damage numbers and flashes.
- Anything an ability does to an enemy besides damage (a pull, a pin, a mark, a stun) is found by comparing the
  mirror before and after the abilities ran that frame, and sent as a small "effect" action.
- Effects that change the shared world (darkness over the whole room, a wall that blocks enemies) are sent as world
  actions, or the cast runs on the host entirely (mark such abilities with a flag).
- Local feedback (spark, freeze, camera kick, hit sound) plays at once on the player's own device.
- Give every enemy a stable network id when it is created, so actions can name it.

**Being hit:**
- Health stays with the host. Enemies attack the player's character where its owner last reported it, honouring the
  owner's dash and invulnerability, so a dodge on the owner's screen still counts.
- When a hit lands, the host tells the owner, who plays the knockback, the hurt pose and the invulnerable time
  locally. The host keeps its own short invulnerable timer too, so the same hit cannot land twice before the owner's
  next report arrives.
- **The host takes the character over only when it must:** while it is held or grabbed by an enemy, or while
  knocked down. The owner follows the host's position then, and gets control back at the host's position afterwards.
- Things the world does to the character (a wind gust, a conveyor, a snare, the floor slowing it) are measured on the
  host and sent in the owner's header, and the owner applies them.

**Moving between levels:** when the host places characters (a new room, back to the hub), it bumps a **move counter**.
The owner echoes the counter in its reports, and the host ignores reports from before the move, so a stale position
can never walk a character through a door in the new room.

**Showing other players' characters:** each owner records how its character and abilities look (or sends their
state) and the host shows them to everyone. In a draw-command stream, mark each player's part as an **owner block** so
that player skips it and draws its own live copy in its place, at the same depth in the scene.

## 3. Showing the world smoothly

- **Interpolate between snapshots:** draw the world a little behind the newest snapshot, sliding every object between
  the two around "now minus the delay".
- **An adaptive buffer:** start around one frame interval plus a little (about 45 ms at 30 snapshots a second), grow
  with measured jitter, and change slowly so playback never jumps.
- **Late snapshots do not freeze:** objects keep moving along their path for a short time (extrapolation, capped).
- **Events are queued, never dropped:** sounds, banners, menus and rewards run in order when their snapshot is shown.
  Only cosmetic events that are already stale (a sound or shake more than about 350 ms old) are skipped.
- **Measure bytes per snapshot** in a busy moment and keep it reasonable (a few KB at 30 a second is fine; tens of KB
  is not).

## 4. Feedback goes to the right player

- **Personal feedback goes only to its player:** their screen shake, their HUD bumps, their menus (a reward pick, a
  shop), their denied sounds. World events (a boss roar, a door slamming) go to everyone.
- **No echoes:** a sound a player's own character made plays on their device at once; when the host relays it to the
  others, it marks who made it, and that player skips it.
- **A player's freeze-frames never freeze the host's world.**
- **Menus:** decide which menus pause everyone (host menus) and which open only on one player's device (their
  loadout, their reward pick), and show the others a line saying who is in a menu.

## 5. Co-op game design

- **Scale challenge with the number of players** (for example enemy health ×(1 + 0.65 per extra player), waves
  ×(1 + 0.35 per extra player)) and let enemies chase the nearest player.
- **Downed, not dead:** a teammate standing beside a downed player revives them over a couple of seconds; clearing
  the area revives everyone at low health; the run ends only when everyone is down.
- **Shared and personal rewards:** decide what is shared (gold is easy to share) and what is personal (relics, picks:
  each player gets their own pick from a chest).
- **Joining rules:** a short room code without look-alike letters (no B/8, I/1, O/0, S/5, Z/2), join only in the hub
  or lobby, lock the room during a run.
- **Each player is told apart at a glance:** a colored ring or outline per player slot, names over heads, and party
  health bars in the HUD.

## 6. Plumbing

- **Version the protocol** and keep the server accepting the previous version, so old builds keep working while the
  new one rolls out; a room speaks only its host's version, and a mismatch shows a clear "update the game" message.
- **The relay or server checks every message:** size limits, a message-rate limit, and only the right senders for
  each message type. The host also clamps every number a guest sends (damage, positions, speeds) to a sane range.
- **Reconnection:** a dropped player gets a grace period (about 20 s) to come back to the same seat; the host leaving
  ends the room for everyone with a clear message.
- **A host in a background tab must keep running.** Browsers stop animation frames in hidden tabs; tick the game from
  a worker timer while hidden (worker timers keep running), and do not open the pause screen for the host while
  guests play.
- **Host the relay near the players** (for example Singapore for South-East Asia) and keep WebSocket support enabled
  on any reverse proxy in front of it.

## 7. Testing

- **Two or more headless browsers on one machine,** one hosting and the others joining by code, every mode and level
  played, 0 page errors on every page.
- **A lag simulator:** a small TCP proxy between the game and the relay that delays every chunk by a base plus
  jitter in each direction (for example 70 ± 25 ms), keeping order. Run every multiplayer test through it as well.
- **A phone-speed guest:** CPU throttling 4× on the guest's page while measuring.
- **Measure, don't guess:**
  - key press to own character moving on screen (target: one to three frames, under about 50 ms, with lag on);
  - an action reaching the host (enemy health drops after a guest's hits);
  - snapshot bytes and the interpolation delay and jitter under lag;
  - frame times on the guest during a busy fight.
- **Cover the rare paths:** being hit, grabbed and released, going down and being revived, a level change mid-action,
  an ability that changes the world, the host's tab hidden, a guest reconnecting.

## 8. Troubleshooting

- **"CORS request did not succeed", status `(null)`:** the browser never got an answer, so the server was down,
  restarting or unreachable. Check the server directly (a health endpoint and the matchmaking call with the game's
  origin) before changing code.
- **WebSocket upgrade returns 404 or 400:** the reverse proxy is not passing the upgrade; turn on its WebSocket
  support.
- **Measure the route:** time a few connections to the server from where the players are (the first one includes DNS
  and TLS setup); find the server's region from its IP.

## 9. Improving further

- **UDP-style transport** (WebRTC data channels, or a platform relay) for larger or competitive games: one lost
  WebSocket packet holds up everything behind it.
- **Send state, not pictures:** compact snapshots with deltas from the last acknowledged one cost far less than draw
  commands, at the price of every system drawing from state on each device. Worth it from day one in a new game, not
  as a retrofit.
- **Interest management:** send each player only what is near them.
- **Smoothing corrections:** when the host and the owner disagree, ease the difference out over a few frames instead
  of snapping, and snap only on teleports.
- **A debug overlay** with ping, jitter, buffer delay, snapshot size and dropped events.
- **A soak test with the maximum number of players** for several minutes.

## Checklist

- [ ] The model was chosen on purpose and written in the spec; each player's own actions answer within a few frames.
- [ ] Abilities hit a local mirror and send actions; the host applies them in the player's name, quietly.
- [ ] Health is the host's; dodges on the owner's screen count; takeovers only when held or downed; move counters on
      level changes.
- [ ] Interpolation with an adaptive buffer; late snapshots extrapolate; events never dropped.
- [ ] Personal feedback goes to its player only; no echoes.
- [ ] Protocol versioned; relay checks size, rate and senders; reconnection; hidden host tab keeps ticking.
- [ ] Tested with two or more browsers, a lag simulator and a throttled guest, with the numbers reported.
