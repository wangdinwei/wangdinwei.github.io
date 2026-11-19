#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成社交分享卡片 1200x630（微信/飞书/Twitter 分享时显示）。"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/data/workspace/app4/GitHub作品集/site/assets"
os.makedirs(OUT, exist_ok=True)
W, H = 1200, 630

CJK_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
CJK_M = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
EN_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
EN_R  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    try: return ImageFont.truetype(path, size)
    except Exception: return ImageFont.truetype(EN_R, size)

img = Image.new("RGB", (W, H), (8, 11, 18))
d = ImageDraw.Draw(img)

# 渐变背景
TOP, BOT = (11, 16, 26), (17, 24, 38)
for y in range(H):
    t = y / (H - 1)
    d.line([(0, y), (W, y)], fill=tuple(int(TOP[i] + (BOT[i] - TOP[i]) * t) for i in range(3)))

# 网格装饰
GRID = (24, 32, 47)
for x in range(0, W, 56):
    d.line([(x, 0), (x, H)], fill=GRID, width=1)
for y in range(0, H, 56):
    d.line([(0, y), (W, y)], fill=GRID, width=1)

# 左上角光晕
for r in range(420, 0, -12):
    a = int(16 * (1 - r / 420))
    d.ellipse([-r, -r, r, r], fill=(11 + a, 16 + a, 26 + a * 2))

# 强调斜线
ACC = (56, 189, 248)
d.line([(W - 150, H), (W - 20, 120)], fill=(37, 99, 235), width=3)
d.line([(W - 142, H), (W - 12, 120)], fill=ACC, width=2)

PAD = 72

# 顶部小标签
f_badge = F(CJK_M, 22)
d.rounded_rectangle([PAD, 64, PAD + 250, 108], radius=22, outline=(45, 58, 80), width=2)
d.ellipse([PAD + 20, 80, PAD + 32, 92], fill=(34, 197, 94))
d.text((PAD + 46, 73), "远程协作开放", font=f_badge, fill=(170, 185, 205))

# 主标题（两行，中文）
f_h1 = F(CJK_B, 62)
d.text((PAD, 150), "把 AI 从", font=f_h1, fill=(240, 245, 250))
bb = d.textbbox((PAD, 150), "把 AI 从", font=f_h1)
d.text((bb[2] + 12, 150), "demo", font=F(EN_B, 58), fill=(125, 211, 252))
bb2 = d.textbbox((bb[2] + 12, 150), "demo", font=F(EN_B, 58))
d.text((bb2[2] + 12, 150), "做到上线收钱", font=f_h1, fill=(240, 245, 250))

# 副标题
f_sub = F(CJK_M, 30)
d.text((PAD, 250), "AI 应用全栈开发 · 本地模型部署 · 自动化系统", font=f_sub, fill=(150, 168, 190))

# 三个数字
f_num = F(EN_B, 40)
f_lab = F(CJK_M, 19)
stats = [("64,752", "行 Python"), ("2,484", "个路由"), ("11", "个生产步骤")]
x = PAD
for n, lab in stats:
    d.text((x, 330), n, font=f_num, fill=(248, 250, 252))
    nb = d.textbbox((x, 330), n, font=f_num)
    d.text((x, 386), lab, font=f_lab, fill=(120, 138, 160))
    x = nb[2] + 64

# 分隔线
d.line([(PAD, 460), (PAD + 300, 460)], fill=(56, 189, 248), width=3)

# 底部：名字 + 站点
f_name = F(CJK_B, 28)
d.text((PAD, 496), "王丁炜", font=f_name, fill=(230, 238, 246))
nb = d.textbbox((PAD, 496), "王丁炜", font=f_name)
d.text((nb[2] + 16, 498), "Dingwei Wang", font=F(EN_R, 26), fill=(140, 158, 180))

f_url = F(EN_R, 22)
ub = d.textbbox((0, 0), "wangdinwei.github.io", font=f_url)
uw = ub[2] - ub[0]
ux = W - PAD - uw
d.rounded_rectangle([ux - 14, 494, W - PAD + 14, 540], radius=8, fill=(13, 19, 30))
d.text((ux, 504), "wangdinwei.github.io", font=f_url, fill=(160, 220, 255))

img.save(f"{OUT}/og-card.png", optimize=True)
print("og-card.png:", img.size, os.path.getsize(f"{OUT}/og-card.png")//1024, "KB")
