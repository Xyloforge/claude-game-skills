"""Find seamless loop points in a song that ends on an outro: a section the song itself repeats.

Usage: python3 find_loop.py <song.mp3> [--min 30] [--max 120] [--preview seam.wav]
Prints the best three candidate periods with the loop body for each. Play the intro once, then whenever playback
passes `end`, jump back by `length`. --preview writes 6 s before the seam followed by 6 s after the jump of the
best candidate, so the seam can be checked by ear before using it. Needs ffmpeg (PATH or /opt/homebrew/bin) and numpy.

How it works: decode to mono, build 12-band pitch-class (chroma) frames every 0.25 s, stack 4 s of frames into one
feature so it describes a passage, and for each period P average the similarity of every passage with the one P
later over a run of at least P/2. Tested on a 3-minute boss theme: it found an 80.0 s repeat.
Long verses that repeat with small changes can score a shorter period (a phrase) first; listen to the preview.
"""
import argparse
import shutil
import subprocess
import wave

import numpy as np

RATE = 11025
HOP = 0.25
STACK = 16  # frames per passage: 4 s


def ffmpeg():
    return shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"


def decode(path):
    raw = subprocess.check_output([ffmpeg(), "-v", "error", "-i", path, "-ac", "1", "-ar", str(RATE), "-f", "f32le", "-"])
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def chroma(x):
    n, hop = 4096, int(HOP * RATE)
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop]
    mag = np.abs(np.fft.rfft(frames * np.hanning(n), axis=1))
    freq = np.fft.rfftfreq(n, 1 / RATE)
    keep = (freq > 60) & (freq < 4000)
    pitch = (np.round(12 * np.log2(freq[keep] / 440)) % 12).astype(int)
    out = np.zeros((len(mag), 12))
    for k in range(12):
        out[:, k] = mag[:, keep][:, pitch == k].sum(axis=1)
    return out


def passages(c):
    f = np.array([c[i:i + STACK].ravel() for i in range(len(c) - STACK)])
    f -= f.mean(axis=1, keepdims=True)
    return f / (np.linalg.norm(f, axis=1, keepdims=True) + 1e-9)


def rank(f, lo, hi):
    found = []
    for lag in range(int(lo / HOP), int(hi / HOP)):
        sim = np.sum(f[lag:] * f[:-lag], axis=1)
        k = lag // 2
        if len(sim) < k:
            break
        avg = np.convolve(sim, np.ones(k) / k, "valid")
        i = int(np.argmax(avg))
        # extend the run while passages keep matching, to find where the repeat ends
        end = i + k
        while end < len(sim) and sim[end] > avg[i] - 0.15:
            end += 1
        found.append((float(avg[i]), lag * HOP, i * HOP, end * HOP))
    found.sort(reverse=True)
    picked = []
    for cand in found:  # drop near-duplicates of a better period
        if all(abs(cand[1] - p[1]) > 1.0 for p in picked):
            picked.append(cand)
        if len(picked) == 3:
            break
    return picked


def preview(x, end, period, path):
    pre, post = x[int((end - 6) * RATE):int(end * RATE)], x[int((end - period) * RATE):int((end - period + 6) * RATE)]
    data = np.clip(np.concatenate([pre, post]), -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes((data * 32767).astype(np.int16).tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song")
    ap.add_argument("--min", type=float, default=30)
    ap.add_argument("--max", type=float, default=120)
    ap.add_argument("--preview")
    a = ap.parse_args()
    x = decode(a.song)
    best = rank(passages(chroma(x)), a.min, a.max)
    print(f"duration {len(x) / RATE:.2f} s")
    dur = len(x) / RATE
    for n, (score, period, start, end) in enumerate(best, 1):
        # passages start..end match the ones a period later; each passage covers 4 s
        loop_end = min(end + 4.0 + period, dur)
        print(f"{n}. period {period:.2f} s, similarity {score:.2f}: {start:.2f}-{end + 4:.2f} s repeats at "
              f"{start + period:.2f}-{loop_end:.2f} s -> loop body {loop_end - period:.2f} -> {loop_end:.2f} s "
              f"(jump back {period:.2f} s when playback passes {loop_end:.2f} s)")
    if best and a.preview:
        _, period, _, end = best[0]
        preview(x, min(end + 4.0 + period, dur), period, a.preview)
        print(f"seam preview written to {a.preview}: 6 s before the jump, then 6 s after it")
    print("Refine the chosen period to the beat by ear or with a waveform editor, cut the file ~2 s past the loop end.")


if __name__ == "__main__":
    main()
