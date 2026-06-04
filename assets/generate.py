#!/usr/bin/env python3
"""Generate course example images via the local inemaimg server (ERNIE, open license)."""
import json, base64, urllib.request, os, time, sys

BASE = os.environ.get("INEMAIMG_URL", "http://localhost:8000")
MODEL = os.environ.get("INEMAIMG_MODEL", "ernie")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "img")
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(HERE, "prompts.json")) as f:
    data = json.load(f)

def post(path, payload, timeout=2400):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

print(f"[load] swapping to {MODEL} ...", flush=True)
t0 = time.time()
try:
    post("/models/load", {"model": MODEL})
    print(f"[load] ready in {time.time()-t0:.0f}s", flush=True)
except Exception as e:
    print(f"[load] warn: {e}", flush=True)

ok = 0
for item in data["images"]:
    fname = item["file"]
    dest = os.path.join(OUT, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"[skip] {fname} (exists)", flush=True)
        ok += 1
        continue
    payload = {
        "model": MODEL,
        "prompt": item["prompt"],
        "width": item["width"],
        "height": item["height"],
        "steps": 50,
    }
    t = time.time()
    try:
        res = post("/generate", payload)
        img_b64 = res["image"]
        if "," in img_b64[:64]:
            img_b64 = img_b64.split(",", 1)[1]
        with open(dest, "wb") as fp:
            fp.write(base64.b64decode(img_b64))
        ok += 1
        print(f"[ok] {fname} {time.time()-t:.0f}s -> {os.path.getsize(dest)//1024}KB", flush=True)
    except Exception as e:
        print(f"[ERR] {fname}: {e}", flush=True)

print(f"[done] {ok}/{len(data['images'])} images in {os.path.join('assets','img')}", flush=True)
