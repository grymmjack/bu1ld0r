#!/usr/bin/python3
"""m0d3l's picture helpers: an atlas laid out at 256 x 256 (K = 1 pixels) and drawn at K x that.

    from paint import Atlas
    a = Atlas(K=2, seed=11, here=HERE)          # here: the model's folder (its renders)
    RED = a.load('red.png')
    img = a.tinted(RED, 122.4, 44.2, (190, 26, 32))   # sizes in K = 1 pixels
    img = a.text(img, 'TRAUMA KIT', 7, (0, 2, 122.4, 12), (246, 246, 242))
    a.put((0, 0), img); a.save(OUT)

Every size and place is in K = 1 pixels (the 256 layout); the class multiplies by K. Material
renders come from pixelmon (the AI paints surfaces, code draws structure): `tinted` keeps a
render's light and shade on a colour of our choosing; `white` is painted metal made from any
render's fine texture. Text uses DIN Bold Condensed (stencil-like) when it's installed.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = os.path.expanduser('~/.local/share/fonts/d/DINNeuzeitGroteskStd_BdCond.otf')
if not os.path.exists(FONT):
    FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'


def lum(a):
    return a @ np.array([0.299, 0.587, 0.114], np.float32)


class Atlas:
    def __init__(self, K=2, seed=1, here='.', size=256, fill=(128, 128, 128)):
        self.K = K
        self.rng = np.random.default_rng(seed)
        self.here = here
        self.img = np.zeros((size * K, size * K, 3), np.float32)
        self.img[:] = fill

    # -- sources --------------------------------------------------------------------------
    def load(self, name, rows=None):
        a = np.asarray(Image.open(os.path.join(self.here, name)).convert('RGB'), np.float32)
        return a[rows[0]:rows[1]] if rows else a

    def _crop(self, src, w, h):
        y = int(self.rng.integers(0, src.shape[0] - h)) if src.shape[0] > h else 0
        x = int(self.rng.integers(0, src.shape[1] - w)) if src.shape[1] > w else 0
        c = src[y:y + h, x:x + w]
        if c.shape[0] < h or c.shape[1] < w:                     # (a source smaller than asked: stretched)
            c = np.asarray(Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)).resize((w, h), Image.LANCZOS), np.float32)
        return c

    def px(self, v):
        return max(1, round(v * self.K))

    # -- surfaces (sizes in K = 1 pixels) -------------------------------------------------
    def detail(self, src, w, h, amt):
        """w x h (real pixels) of src's fine texture: its luminance less a blur of it, x amt."""
        p = Image.fromarray(np.clip(lum(self._crop(src, w, h)), 0, 255).astype(np.uint8))
        hp = np.asarray(p, np.float32) - np.asarray(p.filter(ImageFilter.GaussianBlur(6 * self.K)), np.float32)
        return hp * amt

    def tinted(self, src, w, h, rgb, amt=1.0):
        """src's light and shade on colour rgb."""
        w, h = self.px(w), self.px(h)
        l = lum(self._crop(src, w, h))
        l = 1 + (l / max(l.mean(), 1) - 1) * amt
        return np.array(rgb, np.float32) * l[..., None]

    def painted(self, src, w, h, rgb, amt=1.6, scuffs=1.0, scuff_k=(0.88, 0.95)):
        """Flat paint of colour rgb with src's fine texture (orange peel) and a few scuffs."""
        w, h = self.px(w), self.px(h)
        out = np.ones((h, w, 3), np.float32) * np.array(rgb, np.float32)
        out += self.detail(src, w, h, amt)[..., None]
        r = self.rng
        for _ in range(int(scuffs * w * h / (900 * self.K * self.K)) + 1):
            x, y = r.integers(0, w), r.integers(0, h)
            L, a = r.integers(3 * self.K, 12 * self.K), r.uniform(0, np.pi)
            k = r.uniform(*scuff_k)
            for t in range(int(L)):
                xx, yy = int(x + np.cos(a) * t), int(y + np.sin(a) * t)
                if 0 <= xx < w and 0 <= yy < h:
                    out[yy, xx] *= k
        return out

    def edge_dark(self, img, px=3, k=0.86):
        """Darker toward the edges (dirt where hands don't reach)."""
        h, w = img.shape[:2]
        px *= self.K
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)).astype(np.float32)
        return img * (k + (1 - k) * np.clip(d / px, 0, 1))[..., None]

    # -- marks (places in K = 1 pixels, on an image made here) -----------------------------
    def rect(self, img, box, rgb, a=1.0):
        x0, y0, x1, y1 = [round(v * self.K) for v in box]
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + np.array(rgb, np.float32) * a
        return img

    def cross(self, img, cx, cy, size, arm, rgb):
        self.rect(img, (cx - arm / 2, cy - size / 2, cx + arm / 2, cy + size / 2), rgb)
        self.rect(img, (cx - size / 2, cy - arm / 2, cx + size / 2, cy + arm / 2), rgb)
        return img

    def text(self, img, s, px, box, rgb=(30, 30, 32), align='c', alpha=0.92):
        """Text s, px tall, in box (x0, y0, x1, y1): drawn 6x and shrunk (clean edges)."""
        h, w = img.shape[:2]
        big = 6
        m = Image.new('L', (w * big, h * big), 0)
        d = ImageDraw.Draw(m)
        f = ImageFont.truetype(FONT, max(1, int(px * self.K * big)))
        x0, y0, x1, y1 = [v * self.K * big for v in box]
        l, t, r, b = d.textbbox((0, 0), s, font=f)
        tx = {'c': (x0 + x1) / 2 - (r - l) / 2, 'l': x0, 'r': x1 - (r - l)}[align] - l
        d.text((tx, (y0 + y1) / 2 - (b - t) / 2 - t), s, font=f, fill=255)
        a = np.asarray(m.resize((w, h), Image.LANCZOS), np.float32)[..., None] / 255 * alpha
        return img * (1 - a) + np.array(rgb, np.float32) * a

    def barcode(self, img, box, seed):
        r = np.random.default_rng(seed)
        x0, y0, x1, y1 = box
        x = x0
        while x < x1:
            bw = r.choice([0.35, 0.35, 0.7, 1.05])
            if r.random() < 0.55:
                self.rect(img, (x, y0, min(x + bw, x1), y1), (20, 20, 22))
            x += bw
        return img

    def label(self, img, box, lines, seed, paper=(247, 247, 240), bars=True):
        """An inventory sticker: paper, thin border, lines of (text, px), a barcode under them."""
        x0, y0, x1, y1 = box
        self.rect(img, box, paper)
        for b in ((x0, y0, x1, y0 + 0.5), (x0, y1 - 0.5, x1, y1), (x0, y0, x0 + 0.5, y1), (x1 - 0.5, y0, x1, y1)):
            self.rect(img, b, (120, 120, 120))
        y = y0 + 1.5
        for s, p in lines:
            img = self.text(img, s, p, (x0 + 1, y, x1 - 1, y + p + 0.6))
            y += p + 1
        if bars:
            self.barcode(img, (x0 + 3, y + 0.5, x1 - 3, y1 - 2), seed)
        return img

    def latch(self, img_w, img_h, alu, rgb=(176, 180, 186)):
        """An over-centre latch's face: hinge barrel across the top, lever below, pull lip."""
        w, h = img_w, img_h
        l = self.tinted(alu, w, h, rgb, 0.9)
        b = h * 0.19
        self.rect(l, (0, 0, w, b), (120, 124, 130))
        self.rect(l, (0, b * 0.2, w, b * 0.45), (222, 225, 230), 0.8)
        self.rect(l, (0, b, w, b + h * 0.035), (60, 62, 66))
        self.rect(l, (w * 0.09, b, w * 0.13, h * 0.9), (225, 228, 232), 0.7)
        self.rect(l, (w * 0.87, b, w * 0.91, h * 0.9), (90, 92, 98), 0.7)
        self.rect(l, (w * 0.18, h * 0.83, w * 0.82, h), (140, 144, 150))
        self.rect(l, (w * 0.18, h * 0.83, w * 0.82, h * 0.865), (230, 232, 236), 0.7)
        return self.edge_dark(l, 1.2, 0.8)

    # -- the atlas ------------------------------------------------------------------------
    def put(self, at, img):
        x0, y0 = round(at[0] * self.K), round(at[1] * self.K)
        h = min(img.shape[0], self.img.shape[0] - y0)
        w = min(img.shape[1], self.img.shape[1] - x0)
        self.img[y0:y0 + h, x0:x0 + w] = img[:h, :w]

    def save(self, out):
        Image.fromarray(np.clip(self.img, 0, 255).astype(np.uint8)).save(out)
        print(out)
