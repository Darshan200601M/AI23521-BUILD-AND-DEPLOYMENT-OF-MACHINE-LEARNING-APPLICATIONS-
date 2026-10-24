import os
import numpy as np
from PIL import Image, ImageDraw

os.makedirs('static/image', exist_ok=True)

# 1. stock_icon.png (Sleek dark badge with glowing cyan upward trend line)
icon = Image.new('RGBA', (120, 120), color=(15, 23, 42, 255))
draw = ImageDraw.Draw(icon)
# Rounded outline
draw.rounded_rectangle([4, 4, 116, 116], radius=24, outline=(99, 102, 241, 200), width=3)
# Upward soaring line
points = [(22, 92), (48, 62), (72, 72), (98, 28)]
draw.line(points, fill=(6, 182, 212, 255), width=6)
for p in points:
    draw.ellipse([p[0]-6, p[1]-6, p[0]+6, p[1]+6], fill=(16, 185, 129, 255), outline=(255, 255, 255, 255), width=2)
# Arrow head
draw.polygon([(98, 18), (86, 32), (108, 32)], fill=(6, 182, 212, 255))
icon.save('static/image/stock_icon.png')
print("Updated stock_icon.png")

# 2. stock.png (Hero section banner: 700x500 dark mode fintech)
hero = Image.new('RGB', (700, 500), color=(11, 15, 25))
draw = ImageDraw.Draw(hero)

# Subtle grid
for y in range(40, 460, 45):
    draw.line([(50, y), (650, y)], fill=(24, 32, 50), width=1)
for x in range(50, 660, 60):
    draw.line([(x, 40), (x, 450)], fill=(24, 32, 50), width=1)

# Sleek Candlesticks
candles = [
    (90, 330, 270, 350, 250, True),
    (145, 280, 240, 300, 220, True),
    (200, 250, 270, 280, 240, False),
    (255, 260, 210, 270, 200, True),
    (310, 220, 190, 230, 180, True),
    (365, 200, 230, 240, 190, False),
    (420, 220, 170, 230, 160, True),
    (475, 180, 150, 190, 140, True),
    (530, 160, 180, 190, 150, False),
    (585, 170, 120, 180, 110, True),
    (640, 130, 85, 140, 75, True),
]

for x, o, c, l_wick, h_wick, is_green in candles:
    color = (16, 185, 129) if is_green else (244, 63, 94)
    draw.line([(x, h_wick), (x, l_wick)], fill=color, width=2)
    top_box = min(o, c)
    bot_box = max(o, c)
    draw.rectangle([x-10, top_box, x+10, bot_box], fill=color)

# Smooth moving average line
trend_line = [(90, 310), (145, 260), (200, 255), (255, 235), (310, 205),
              (365, 215), (420, 195), (475, 165), (530, 170), (585, 145), (640, 105)]
draw.line(trend_line, fill=(99, 102, 241), width=4)

hero.save('static/image/stock.png')
print("Updated stock.png")

# 3. stock_llllll.avif & stock_llllll.png & stock_about.jpg
about = Image.new('RGB', (600, 400), color=(15, 23, 42))
draw = ImageDraw.Draw(about)
draw.rounded_rectangle([30, 30, 570, 370], radius=16, fill=(24, 34, 56), outline=(99, 102, 241), width=2)
# Draw mini trend
mini_pts = [(60, 310), (130, 280), (200, 290), (270, 240), (340, 220), (410, 235), (540, 160)]
draw.line(mini_pts, fill=(6, 182, 212), width=4)
for p in mini_pts:
    draw.ellipse([p[0]-5, p[1]-5, p[0]+5, p[1]+5], fill=(16, 185, 129))

about.save('static/image/stock_llllll.png')
about.save('static/image/stock_about.jpg')
about.save('static/image/stock_llllll.avif', format='JPEG')
print("Updated stock_llllll.*")

# 4. reg.jpg (Sleek dark gradient badge)
reg = Image.new('RGB', (600, 600), color=(15, 23, 42))
draw = ImageDraw.Draw(reg)
for y in range(30, 570, 35):
    draw.line([(30, y), (570, y)], fill=(30, 41, 65), width=1)
for x in range(30, 570, 35):
    draw.line([(x, 30), (x, 570)], fill=(30, 41, 65), width=1)

draw.ellipse([140, 120, 460, 440], fill=(24, 34, 60), outline=(99, 102, 241), width=3)
# Rocket arrow
arrow_pts = [(300, 180), (370, 300), (330, 290), (330, 380), (270, 380), (270, 290), (230, 300)]
draw.polygon(arrow_pts, fill=(6, 182, 212))

reg.save('static/image/reg.jpg', format='JPEG')
print("Updated reg.jpg")

print("[OK] All professional assets updated!")
