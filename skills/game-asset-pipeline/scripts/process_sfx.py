"""Trim, fade, normalise and encode downloaded sound effects for a web game.

Usage: python3 process_sfx.py <raw-dir> <out-dir> <spec.json> [--bitrate 64k]
spec.json maps each output key to its cut, e.g.
  {
    "clang1": {"max": 1.1, "fade": 0.5, "peak": -2},
    "fireLoop": {"max": 7.5, "fade": 0, "peak": -6, "loop": true},
    "door": {"max": 1.4, "fade": 0.4, "peak": -3, "start": 0.35, "lowpass": 3000}
  }
<raw-dir>/<key>.mp3 (or .wav/.ogg) is the untouched download. Steps per sound (FFmpeg):
  1. cut from `start` (default 0), then remove leading silence below -50 dBFS (not for loops)
  2. keep at most `max` seconds with a `fade`-second fade-out (loops get a 30 ms fade only, at the seam)
  3. optional `lowpass` / `highpass` Hz (a dull waterlogged hit, a thin radio)
  4. mono 44.1 kHz, peak-normalised to `peak` dBFS, MP3 at the bitrate (64k effects, 96k music or long ambience)
Prints a byte table (raw, runtime, reduction) to paste into AUDIO.md.
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"


def peak_db(path, filters):
    res = subprocess.run([FFMPEG, "-hide_banner", "-i", str(path), "-af", filters + ",volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True)
    m = re.search(r"max_volume: (-?[\d.]+) dB", res.stderr)
    return float(m.group(1)) if m else 0.0


def process(src, dst, spec, bitrate):
    chain = []
    if spec.get("start"):
        chain.append(f"atrim=start={spec['start']},asetpts=PTS-STARTPTS")
    if not spec.get("loop"):
        chain.append("silenceremove=start_periods=1:start_threshold=-50dB")
    length = spec.get("max", 2.0)
    chain.append(f"atrim=end={length}")
    fade = 0.03 if spec.get("loop") else spec.get("fade", 0.2)
    if fade:
        chain.append(f"afade=t=out:st={max(0, length - fade)}:d={fade}")
    if spec.get("lowpass"):
        chain.append(f"lowpass=f={spec['lowpass']}")
    if spec.get("highpass"):
        chain.append(f"highpass=f={spec['highpass']}")
    chain.append("aformat=channel_layouts=mono:sample_rates=44100")
    base = ",".join(chain)
    gain = spec.get("peak", -2) - peak_db(src, base)
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", str(src), "-af", f"{base},volume={gain:.2f}dB",
                    "-codec:a", "libmp3lame", "-b:a", bitrate, str(dst)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw"); ap.add_argument("out"); ap.add_argument("spec")
    ap.add_argument("--bitrate", default="64k")
    a = ap.parse_args()
    raw, out = Path(a.raw), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    spec = json.loads(Path(a.spec).read_text())
    before = after = 0
    print("| Runtime file | Raw bytes | Runtime bytes |\n| --- | ---: | ---: |")
    for key, s in spec.items():
        src = next((p for p in (raw / f"{key}{ext}" for ext in (".mp3", ".wav", ".ogg")) if p.exists()), None)
        if not src:
            print(f"| missing: {key} | | |"); continue
        dst = out / f"{key}.mp3"
        process(src, dst, s, s.get("bitrate", a.bitrate))
        before += src.stat().st_size; after += dst.stat().st_size
        print(f"| `{dst.name}` | {src.stat().st_size:,} | {dst.stat().st_size:,} |")
    if before:
        print(f"\nTotal {before:,} -> {after:,} bytes ({100 * (1 - after / before):.1f}% smaller)")


if __name__ == "__main__":
    main()
