import turtle
import random
import math

# SETUP
sc = turtle.Screen()
sc.setup(1100, 700)
sc.bgcolor("#000010")
sc.title("Moonlit Night")
turtle.colormode(1.0)
t = turtle.Turtle()
turtle.tracer(0, 0)
t.hideturtle()
t.speed(0)

W, H = 550, 350 

# HELPERS 

def rect(x, y, w, h, c):
    """Filled rectangle, bottom-left corner at (x, y)."""
    t.color(c); t.penup(); t.goto(x, y); t.setheading(0)
    t.begin_fill()
    t.forward(w);  t.setheading(90)
    t.forward(h);  t.setheading(180)
    t.forward(w);  t.setheading(270)
    t.forward(h)
    t.end_fill()

def tri(p1, p2, p3, c):
    """Filled triangle given three (x,y) tuples."""
    t.color(c); t.penup(); t.goto(p1)
    t.begin_fill()
    t.goto(p2); t.goto(p3); t.goto(p1)
    t.end_fill()

# NIGHT SKY

def gradient_sky():
    rows = 45
    band = (H + 175) / rows
    for i in range(rows):
        r = i / rows
        t.color(r * 0.03, r * 0.04, 0.06 + r * 0.17)
        y = H - i * band
        t.penup(); t.goto(-W, y); t.setheading(0)
        t.begin_fill()
        t.forward(W*2);  t.setheading(270); t.forward(band + 1)
        t.setheading(180); t.forward(W*2); t.setheading(90); t.forward(band + 1)
        t.end_fill()

# MOON 


def moon():
    t.penup()
    t.color("grey")
    t.goto(400,200)
    t.pendown()
    t.begin_fill()
    t.circle(80)
    t.end_fill()

#  STARS 

stars = []

def create_stars(n=250):
    for _ in range(n):
        while True:
            x = random.randint(-W, W)
            y = random.randint(-55, H)
            # Leave space around the moon
            if not (220 < x < 370 and 80 < y < 295):
                break
        stars.append({
            "x": x, "y": y,
            "base": random.uniform(1.0, 2.8),
            "ph":   random.uniform(0, math.tau),
            "sp":   random.uniform(0.04, 0.13),
        })

def draw_stars(f):
    for s in stars:
        br = 0.45 + 0.55 * abs(math.sin(f * s["sp"] + s["ph"]))
        sz = s["base"] + 0.7 * math.sin(f * s["sp"] * 0.7 + s["ph"])
        t.color(br, br, min(1.0, br + 0.12))
        t.penup(); t.goto(s["x"], s["y"]); t.dot(max(1, sz))

#  SHOOTING STARS 

shooters = []

def update_shooters():
    if len(shooters) < 2 and random.random() < 0.012:
        shooters.append({
            "x":     random.randint(-W + 50, W - 100),
            "y":     random.randint(100, H - 30),
            "trail": random.randint(9, 18),
            "spd":   random.uniform(10, 20),
        })
    for s in list(shooters):
        for i in range(s["trail"]):
            a = (s["trail"] - i) / s["trail"]
            t.color(a, a, a * 0.9 + 0.1)
            t.penup(); t.goto(s["x"] - i * 5, s["y"] + i * 5)
            t.dot(max(1, a * 3.5))
        s["x"] += s["spd"]; s["y"] -= s["spd"]
    shooters[:] = [s for s in shooters if s["y"] > -H and s["x"] < W + 100]

#  GROUND & HILLS

def draw_ground():
    # Distant rolling hills
    t.color(0.04, 0.10, 0.04)
    t.penup(); t.goto(-W, -118)
    t.begin_fill()
    for x in range(-W, W + 8, 8):
        y = -118 + 48 * math.sin((x + 140) * math.pi / 270) \
                 + 20 * math.sin(x * math.pi / 120)
        t.goto(x, y)
    t.goto(W, -H); t.goto(-W, -H)
    t.end_fill()
    # Mid-ground gentle wave
    t.color(0.05, 0.13, 0.05)
    t.penup(); t.goto(-W, -188)
    t.begin_fill()
    for x in range(-W, W + 8, 8):
        y = -188 + 13 * math.sin((x + 70) * math.pi / 185)
        t.goto(x, y)
    t.goto(W, -H); t.goto(-W, -H)
    t.end_fill()
    # Flat foreground
    rect(-W, -H, W * 2, H - 210, (0.04, 0.12, 0.04))

#  POND 

def draw_pond(f):
    px, py, a, b = 220, -255, 80, 20
    # Water body
    t.color(0.01, 0.05, 0.16)
    t.penup(); t.goto(px + a, py)
    t.begin_fill()
    for deg in range(0, 362, 4):
        rad = math.radians(deg)
        t.goto(px + a * math.cos(rad), py + b * math.sin(rad))
    t.end_fill()

#  PINE TREE

def pine(x, y, h=110, scale=1.0):
    th = int(h * 0.22 * scale)
    tw = max(5, int(9 * scale))
    rect(x - tw // 2, y, tw, th, (0.22, 0.12, 0.04))
    bw = h * 0.54 * scale
    for i in range(3):
        ratio = i / 2
        ly = y + th + i * h * 0.20 * scale
        lw = bw * (1 - ratio * 0.42)
        lh = h * 0.38 * scale
        d  = 0.04 + 0.07 * ratio
        tri((x - lw / 2, ly), (x + lw / 2, ly), (x, ly + lh),
            (d, 0.22 + 0.09 * ratio, d))

#  WINDOW 

def draw_window(wx, wy, f):
    # Warm candlelight flicker
    g = 0.62 + 0.28 * abs(math.sin(f * 0.08 + wx * 0.05))
    rect(wx, wy, 32, 32, (g, g * 0.62, 0.07))
    # Frame and cross-dividers
    t.color(0.27, 0.13, 0.04)
    t.penup(); t.goto(wx, wy); t.pendown(); t.width(2); t.setheading(0)
    for _ in range(4):
        t.forward(32); t.left(90)
    t.penup(); t.goto(wx + 16, wy); t.pendown()
    t.setheading(90);  t.forward(32)
    t.penup(); t.goto(wx, wy + 16); t.pendown()
    t.setheading(0);   t.forward(32)
    t.penup(); t.width(1)

#  HOUSE 

HX, HY = -155, -215
HW, HH =  150,  120

SMOKE_CX = HX + 32    # centre of chimney top
SMOKE_CY = HY + 174   # top of chimney cap

def draw_house(f):
    hx, hy, w, h = HX, HY, HW, HH

    # ── Chimney base drawn BEFORE roof so roof covers lower portion ──
    rect(hx + 22, hy + 110, 20, 60, (0.32, 0.14, 0.07))

    # ── Walls ──
    rect(hx,          hy, w,      h, (0.40, 0.20, 0.09))
    rect(hx + w - 10, hy, 10,     h, (0.32, 0.16, 0.07))   # right shadow

    # ── Door ──
    rect(hx + 55, hy, 40, 72, (0.17, 0.08, 0.02))
    t.color(0.30, 0.14, 0.06)
    t.penup(); t.goto(hx + 55, hy); t.pendown(); t.width(2)
    t.setheading(90); t.forward(72)
    t.right(90);      t.forward(40)
    t.right(90);      t.forward(72)
    t.penup(); t.width(1)
    t.color(0.88, 0.75, 0.10)
    t.penup(); t.goto(hx + 92, hy + 32); t.dot(5)

    # ── Porch step ──
    rect(hx + 46, hy - 8, 58, 8, (0.30, 0.14, 0.06))

    # ── Windows ──
    draw_window(hx + 8,   hy + 38, f)
    draw_window(hx + 100, hy + 38, f)

    # ── Roof (covers chimney base) ──
    tri((hx - 14,      hy + h),
        (hx + w + 14,  hy + h),
        (hx + w // 2,  hy + h + 62),
        (0.28, 0.07, 0.07))
    # Right-slope shadow
    tri((hx + w // 2,     hy + h + 62),
        (hx + w + 14,     hy + h),
        (hx + w // 2 + 4, hy + h + 62),
        (0.22, 0.05, 0.05))
    # Roof ridge line
    t.color(0.20, 0.04, 0.04)
    t.penup(); t.goto(hx - 14, hy + h); t.pendown(); t.width(2)
    t.goto(hx + w // 2, hy + h + 62)
    t.goto(hx + w + 14, hy + h)
    t.penup(); t.width(1)

    # ── Chimney cap (above roof) ──
    rect(hx + 19, hy + 169, 26, 5, (0.27, 0.11, 0.05))

# FENCE 

def draw_fence(x0, y0, length, n=10):
    if length <= 0 or n <= 0:
        return
    sp  = length / n
    col = (0.50, 0.40, 0.26)
    # Horizontal rails
    for ry in [y0 + 12, y0 + 30]:
        t.color(col); t.penup(); t.goto(x0, ry); t.pendown(); t.width(2)
        t.setheading(0); t.forward(length)
        t.penup(); t.width(1)
    # Pointed pickets
    for i in range(n + 1):
        px = x0 + i * sp
        t.color(col); t.penup(); t.goto(px - 3, y0)
        t.begin_fill()
        t.setheading(90); t.forward(36)
        t.right(45);  t.forward(4.5)
        t.right(90);  t.forward(4.5)
        t.right(45);  t.forward(36)
        t.right(90);  t.forward(6.4)
        t.right(90)
        t.end_fill()

# PATH 

def draw_path():
    cx = HX + 75   # door centre x
    t.color(0.22, 0.18, 0.10)
    t.penup(); t.goto(cx - 18, HY)
    t.begin_fill()
    t.goto(cx + 18, HY)
    t.goto(cx + 65, HY - 160)
    t.goto(cx - 65, HY - 160)
    t.end_fill()
    # Stone-row marks
    for row in range(5):
        ry = HY - 22 - row * 28
        hw = 20 + row * 9
        t.color(0.28, 0.23, 0.14)
        t.penup(); t.goto(cx - hw, ry); t.pendown(); t.width(1)
        t.setheading(0); t.forward(hw * 2)
        t.penup(); t.goto(cx, ry); t.pendown()
        t.setheading(270); t.forward(22)
        t.penup(); t.width(1)

#  CHIMNEY SMOKE 

smoke = []

def update_smoke():
    if random.random() < 0.18:
        smoke.append({
            "x":    SMOKE_CX + random.uniform(-2, 2),
            "y":    SMOKE_CY,
            "vx":   random.uniform(-0.4, 0.4),
            "vy":   random.uniform(1.3, 2.6),
            "life": 1.0,
            "size": random.uniform(5, 9),
        })
    for p in smoke:
        g = p["life"] * 0.33
        t.color(g, g, g + 0.06)
        t.penup(); t.goto(p["x"], p["y"])
        t.dot(max(1, p["size"] * p["life"]))
        p["x"] += p["vx"] + random.uniform(-0.08, 0.08)
        p["y"] += p["vy"]
        p["life"] -= 0.013
        p["size"] += 0.22
    smoke[:] = [p for p in smoke if p["life"] > 0]



#  MAIN LOOP 

create_stars()
frame = 0

while True:
    t.clear()

    gradient_sky()
    draw_stars(frame)
    moon()
    update_shooters()
    draw_ground()
    draw_pond(frame)

    # Left fence (right up to house edge) and right fence (from house to tree line)
    draw_fence(-W,          HY - 4, HX + W - 5,              13)
    draw_fence(HX + HW + 5, HY - 4, W - (HX + HW + 5) - 55, 11)

    draw_path()

    # Left pine cluster
    pine(-460, HY,      125)
    pine(-410, HY -  8,  95, 0.88)
    pine(-490, HY +  5,  85, 0.80)

    # Right pine cluster
    pine( 170, HY,      115)
    pine( 225, HY -  5,  98, 0.92)
    pine( 290, HY +  6, 138, 1.08)
    pine( 365, HY -  2, 105, 0.95)

    draw_house(frame)
    update_smoke()
    turtle.update()
    frame += 1
