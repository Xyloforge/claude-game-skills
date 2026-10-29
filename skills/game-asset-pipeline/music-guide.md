# Music guide (Suno)

The user makes the music in a generator such as Suno from prompts Claude writes. Claude then sets the loop and the mix.

## Writing the prompt

**Never list instruments.** Instrument lists were rejected ("just define the vibe and bpm and what we're doing, what it's for"). The generator chooses the instruments.

Describe only:
1. **What the game is and what the player is doing** at that moment (exploring a burning village, fighting a boss in a cathedral, fishing on a calm morning pier, a shop between tides).
2. **The vibe and theme** (dark gothic, cozy, tense, triumphant, eerie, melancholy, heroic, playful).
3. **The pace:** fast or slow, driving or laid-back, and a **bpm**.
4. **Its job:** "instrumental, seamless loop, background music for a game", and for a boss theme "epic boss battle theme, strong opening first bar".

Template:

```
Instrumental background music for a <genre> game: <what the player is doing, where>.
<vibe and theme words>, <fast / slow / steady>, <N> bpm.
<what it must make the player feel>. Instrumental, no vocals, seamless loop.
```

Example: "Instrumental background music for a gothic action game: a lone witch hunter fights through a burning village at night under a red moon. Dark, relentless, heroic, fast with forward momentum, 120 bpm. Should make the player feel hunted but unstoppable. Instrumental, no vocals, seamless loop."

Give one prompt per track: each stage, each boss, night and day variants, menus, shop, ending. Put them in `~/Downloads/<game>-music-prompts.md`, with the file name to save each result under.

## Looping

Suno songs are full songs with an intro and an outro, so looping the whole file cuts badly at the end. Loop a section the song itself repeats:

```sh
python3 ${CLAUDE_SKILL_DIR}/scripts/find_loop.py "<song>.mp3" --preview seam.wav
```

- It lists the three most likely repeat periods with the loop body for each. The top pick is not always the full section; a long verse can score a shorter phrase first.
- Listen to `seam.wav` (6 s before the jump, then 6 s after it) and use the candidate whose seam is inaudible.
- Play the intro once, then whenever playback passes the loop end, jump back by the period.
- Cut the runtime file about 2 s after the loop end. Encode stereo 96 kb/s.
- Stream long music through a media element, not a decoded buffer: 3 minutes decoded holds about 60 MB.
- Record the loop points, similarity, source bytes and runtime bytes in AUDIO.md.

## Mixing in game

- Duck the music for pause, menus and cinematics (about 35%), and for big catches or achievements; resume from the same position.
- Fade out at the end of a run, and pause it while the tab is hidden.
- **Boss entrance:** the stage music fades to silence, sound builds the scene (gates, heartbeat, bell, candles, organ), and the boss theme cuts in from its first bar exactly with the title card. After a death the theme starts at once, and the stage music returns at the checkpoint.
- Each time of day or area that changes the mood gets its own track (a morning tide and a night tide).
