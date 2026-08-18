import os
import re
import subprocess
from pathlib import Path

# Paths
audio_dir = Path("assets/narration")
html_file = Path("index.html")
temp_dir = Path("temp_padded")
temp_dir.mkdir(exist_ok=True)

# 1. Get raw audio durations using ffprobe
def get_raw_duration(f_path):
    cmd = [
        "ffprobe", "-i", str(f_path),
        "-show_entries", "format=duration",
        "-v", "quiet", "-of", "csv=p=0"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        try:
            return float(res.stdout.strip())
        except ValueError:
            return 0.0
    return 0.0

# 2. Parse slide durations from index.html
content = html_file.read_text(encoding="utf-8")
pattern = r"i:\s*(\d+),\s*dur:\s*([\d\.]+),\s*sub:"
matches = re.findall(pattern, content)
slide_durs = {int(i): float(dur) for i, dur in matches}
print("Slide durations from index.html:", slide_durs)

# 3. Create padded audio for each page
mp3_files = sorted(list(audio_dir.glob("page-*.mp3")))
padded_files = []

for f in mp3_files:
    m = re.search(r"page-(\d+)\.mp3", f.name)
    if not m:
        continue
    idx = int(m.group(1))
    
    if idx not in slide_durs:
        print(f"Warning: page-{idx:02d}.mp3 not in index.html PAGES!")
        continue
        
    raw_dur = get_raw_duration(f)
    target_dur = slide_durs[idx]
    silence_dur = max(0.1, target_dur - raw_dur)
    
    out_padded = temp_dir / f"padded-{idx:02d}.mp3"
    padded_files.append(out_padded)
    
    # Run ffmpeg to pad silence to reach exact target duration
    # We use aevalsrc to generate silence of silence_dur length and concat it
    cmd = [
        "ffmpeg", "-y", "-i", str(f),
        "-filter_complex", f"aevalsrc=0:d={silence_dur:.3f}[silence];[0:a][silence]concat=n=2:v=0:a=1[out]",
        "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", str(out_padded)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Padded page-{idx:02d}.mp3: raw={raw_dur:.3f}s, silence={silence_dur:.3f}s, target={target_dur:.1f}s")

# 4. Concat all padded files into master_audio.mp3
concat_list = temp_dir / "concat_list.txt"
with open(concat_list, "w", encoding="utf-8") as file:
    for pf in padded_files:
        # Use absolute path or relative path with forward slashes for ffmpeg concat
        file.write(f"file '{pf.resolve().as_posix()}'\n")

renders_dir = Path("renders")
renders_dir.mkdir(exist_ok=True)
master_audio = renders_dir / "master_audio.mp3"

cmd_concat = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", str(concat_list),
    "-c", "copy", str(master_audio)
]
subprocess.run(cmd_concat)
print(f"\nCreated master audio at: {master_audio.resolve()}")

# Clean up temp files
for pf in padded_files:
    try:
        pf.unlink()
    except:
        pass
try:
    concat_list.unlink()
    temp_dir.rmdir()
except:
    pass

print("Done!")
