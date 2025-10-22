import math

def draw_card(canvas, card, colors):
    shape, color_idx, shading, number = card
    color = colors[color_idx]
    count = number + 1

    spacing = 15
    shape_h = 35
    total_h = count * shape_h + (count - 1) * spacing
    start_y = (150 - total_h) / 2 + shape_h / 2

    for i in range(count):
        y = start_y + i * (shape_h + spacing)
        if shape == 0:
            draw_diamond(canvas, 55, y, 40, 18, color, shading)
        elif shape == 1:
            draw_oval(canvas, 55, y, 45, 18, color, shading)
        else:
            draw_squiggle(canvas, 55, y, 50, 18, color, shading)

# =============== SHAPE FUNCTIONS ===============

def draw_diamond(canvas, x, y, w, h, color, shading):
    pts = [x, y-h, x+w, y, x, y+h, x-w, y]
    if shading == 0:
        canvas.create_polygon(pts, fill=color, outline=color, width=2)
    elif shading == 1:
        canvas.create_polygon(pts, fill='', outline=color, width=2)
        step = 3
        for i in range(-w, w+1, step):
            y_top = y - h * (1 - abs(i) / w)
            y_bottom = y + h * (1 - abs(i) / w)
            canvas.create_line(x+i, y_top, x+i, y_bottom, fill=color)
    else:
        canvas.create_polygon(pts, fill='', outline=color, width=2)

def draw_oval(canvas, x, y, w, h, color, shading):
    if shading == 0:
        canvas.create_oval(x-w, y-h, x+w, y+h, fill=color, outline=color, width=2)
    elif shading == 1:
        step = 4
        for sx in range(int(x-w), int(x+w), step):
            dx = (sx - x) / w
            if abs(dx) > 1:
                continue
            dy = (1 - dx*dx)**0.5 * h
            canvas.create_line(sx, y-dy, sx, y+dy, fill=color)
        canvas.create_oval(x-w, y-h, x+w, y+h, outline=color, width=2)
    else:
        canvas.create_oval(x-w, y-h, x+w, y+h, fill='', outline=color, width=2)

def draw_squiggle(canvas, x, y, w, h, color, shading):
    points = [
        x, y - h*0.3,
        x + w*0.3, y - h*1.1,
        x + w*0.8, y - h*0.8,
        x + w, y - h*0.3,
        x + w*0.8, y + h*0.2,
        x + w*0.3, y,
        x, y + h*0.3,
        x - w*0.3, y + h*1.1,
        x - w*0.8, y + h*0.8,
        x - w, y + h*0.3,
        x - w*0.8, y - h*0.2,
        x - w*0.3, y,
    ]
    if shading == 0:
        canvas.create_polygon(points, fill=color, outline=color, width=2, smooth=True)
    elif shading == 1:
        draw_striped_polygon(canvas, points, color, step=4)
        canvas.create_polygon(points, fill='', outline=color, width=2, smooth=True)
    else:
        canvas.create_polygon(points, fill='', outline=color, width=2, smooth=True)

# =============== STRIPE HELPERS ===============

def draw_striped_polygon(canvas, points, color, step=4):
    ys = points[1::2]
    if not ys:
        return
    y_min = math.floor(min(ys))
    y_max = math.ceil(max(ys))

    for y in range(y_min, y_max + 1, step):
        xs = polygon_scanline_intersections(points, y)
        for i in range(0, len(xs)-1, 2):
            canvas.create_line(xs[i], y, xs[i+1], y, fill=color)

def polygon_scanline_intersections(points, y):
    xs = []
    n = len(points) // 2
    for i in range(n):
        x1, y1 = points[2*i], points[2*i + 1]
        x2, y2 = points[2*((i+1) % n)], points[2*((i+1) % n) + 1]
        if y1 == y2:
            continue
        y_min, y_max = min(y1, y2), max(y1, y2)
        if y_min <= y < y_max:
            t = (y - y1) / (y2 - y1)
            xi = x1 + t * (x2 - x1)
            xs.append(xi)
    xs.sort()
    return xs
