#!/usr/bin/env python3
"""Regenerate the site icons from assets/img/portrait.jpg.

    python3 tools/make-favicon.py

Why this exists rather than a one-line Hugo pipeline: a dim photograph of a
face is unreadable at 16px. Straight grayscale produced a grey smudge in the
tab. The icons need a much harder levels curve than the on-page portrait --
enough to blow the background to white and hold the head as a dark shape --
so the two are generated separately from the same source.

Requires macOS `sips` for the JPEG decode and crop; everything after that is
stdlib. Run it after changing assets/img/portrait.jpg, then commit static/.
"""
import os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets/img/portrait.jpg")
OUT = os.path.join(ROOT, "static")

# Head crop within portrait.jpg (which is itself head-and-shoulders). The icon
# needs the head to fill the tile; the on-page portrait does not.
CROP = dict(top=23, left=122, size=250)

# Levels: lift the midtones hard and clip the background to white. Chosen by
# rendering 16/32px candidates against both a light and a dark tab strip.
ICON_LEVELS = dict(lo=18, hi=132, gamma=0.75, sharpen=0.25)   # 16px, 32px
TOUCH_LEVELS = dict(lo=8, hi=155, gamma=0.85, sharpen=0.0)    # 180px, detail survives

import zlib, struct

def read_png(path):
    d = open(path,'rb').read(); assert d[:8]==b'\x89PNG\r\n\x1a\n'
    i=8; idat=b''; w=h=ct=None
    while i < len(d):
        ln = struct.unpack('>I', d[i:i+4])[0]; typ=d[i+4:i+8]; body=d[i+8:i+8+ln]
        if typ==b'IHDR': w,h,bd,ct = struct.unpack('>IIBB', body[:10])
        elif typ==b'IDAT': idat += body
        i += 12+ln
    raw = zlib.decompress(idat); ch={0:1,2:3,4:2,6:4}[ct]; stride=w*ch
    rows=[]; prev=bytearray(stride); p=0
    for y in range(h):
        f=raw[p]; p+=1; line=bytearray(raw[p:p+stride]); p+=stride
        for x in range(stride):
            a=line[x-ch] if x>=ch else 0; b=prev[x]; c=prev[x-ch] if x>=ch else 0
            if f==1: line[x]=(line[x]+a)&255
            elif f==2: line[x]=(line[x]+b)&255
            elif f==3: line[x]=(line[x]+(a+b)//2)&255
            elif f==4:
                pa=abs(b-c); pb=abs(a-c); pc=abs(a+b-2*c)
                pr=a if(pa<=pb and pa<=pc) else (b if pb<=pc else c)
                line[x]=(line[x]+pr)&255
        rows.append(bytes(line)); prev=line
    g=bytearray(w*h)
    for y,line in enumerate(rows):
        for x in range(w):
            px=line[x*ch:(x+1)*ch]
            g[y*w+x] = px[0] if ch<3 else int(0.299*px[0]+0.587*px[1]+0.114*px[2])
    return w,h,bytes(g)

def write_png_gray(path,w,h,px):
    def chunk(t,d):
        return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    raw=b''.join(b'\x00'+px[y*w:(y+1)*w] for y in range(h))
    out=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack(">IIBBBBB",w,h,8,0,0,0,0))
    out+=chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
    open(path,'wb').write(out); return len(out)

def resize_box(src,sw,sh,dw,dh):
    out=bytearray(dw*dh)
    for y in range(dh):
        y0=y*sh//dh; y1=max(y0+1,(y+1)*sh//dh)
        for x in range(dw):
            x0=x*sw//dw; x1=max(x0+1,(x+1)*sw//dw)
            s=n=0
            for yy in range(y0,y1):
                r=yy*sw
                for xx in range(x0,x1): s+=src[r+xx]; n+=1
            out[y*dw+x]=s//n
    return bytes(out)

def percentile(px,p):
    h=[0]*256
    for v in px: h[v]+=1
    tgt=len(px)*p/100.0; c=0
    for v in range(256):
        c+=h[v]
        if c>=tgt: return v
    return 255

def levels(px,lo,hi,gamma=1.0):
    lut=[]
    for v in range(256):
        t=(v-lo)/max(1,(hi-lo)); t=min(1.0,max(0.0,t))
        lut.append(int(round((t**gamma)*255)))
    return bytes(lut[v] for v in px)

def sharpen(px,w,h,amt):
    out=bytearray(px)
    for y in range(1,h-1):
        for x in range(1,w-1):
            i=y*w+x
            lap=5*px[i]-px[i-1]-px[i+1]-px[i-w]-px[i+w]
            v=int(px[i]+amt*(lap-px[i]))
            out[i]=0 if v<0 else (255 if v>255 else v)
    return bytes(out)

def main():
    tmp = tempfile.mkdtemp()
    flat = os.path.join(tmp, "crop.png")
    subprocess.run(["sips", "-c", str(CROP["size"]), str(CROP["size"]),
                    "--cropOffset", str(CROP["top"]), str(CROP["left"]),
                    SRC, "--out", flat, "-s", "format", "png"],
                   check=True, capture_output=True)
    w, h, g = read_png(flat)

    def render(size, cfg):
        big = levels(g, cfg["lo"], cfg["hi"], cfg["gamma"])
        px = resize_box(big, w, h, size, size)
        if cfg["sharpen"]:
            px = sharpen(px, size, size, cfg["sharpen"])
        return px

    p16 = render(16, ICON_LEVELS)
    p32 = render(32, ICON_LEVELS)
    p180 = render(180, TOUCH_LEVELS)
    write_png_gray(os.path.join(OUT, "favicon-16x16.png"), 16, 16, p16)
    write_png_gray(os.path.join(OUT, "favicon-32x32.png"), 32, 32, p32)
    write_png_gray(os.path.join(OUT, "apple-touch-icon.png"), 180, 180, p180)

    # PNG-payload ICO (Vista+). Every current browser decodes it; verified by
    # rendering the file in Chrome rather than trusting the header alone.
    import struct
    blobs = [(16, open(os.path.join(OUT, "favicon-16x16.png"), "rb").read()),
             (32, open(os.path.join(OUT, "favicon-32x32.png"), "rb").read())]
    off = 6 + 16 * len(blobs)
    head = struct.pack("<HHH", 0, 1, len(blobs))
    ents = b""
    for n, b in blobs:
        ents += struct.pack("<BBBBHHII", n, n, 0, 0, 1, 32, len(b), off)
        off += len(b)
    with open(os.path.join(OUT, "favicon.ico"), "wb") as f:
        f.write(head + ents + b"".join(b for _, b in blobs))
    print("wrote favicon.ico, favicon-16x16.png, favicon-32x32.png, apple-touch-icon.png")

if __name__ == "__main__":
    main()
