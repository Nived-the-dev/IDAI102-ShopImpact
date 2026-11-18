"""A shared Turtle-style path for the browser badge and Python Turtle preview."""

LEAF = [(22, 91), (27, 56), (51, 34), (93, 25), (87, 60), (65, 86), (22, 91)]
VEIN = [(22, 91), (53, 65), (72, 49)]

def leaf_svg():
    """Render the same path as SVG on headless Streamlit hosts."""
    points = lambda path: " ".join(f"{x},{y}" for x, y in path)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 116 116">'
            f'<circle cx="58" cy="58" r="56" fill="#e4f5e8"/>'
            f'<polygon points="{points(LEAF)}" fill="#33845b"/>'
            f'<polyline points="{points(VEIN)}" fill="none" stroke="#e4f5e8" '
            f'stroke-width="3" stroke-linecap="round"/></svg>')

if __name__ == "__main__":
    import turtle

    pen = turtle.Turtle()
    pen.speed(4)
    for path, color, filled in [(LEAF, "#33845b", True), (VEIN, "#aee0bc", False)]:
        pen.penup()
        pen.goto(path[0][0] - 58, 58 - path[0][1])
        pen.color(color)
        pen.pensize(3)
        pen.pendown()
        if filled:
            pen.begin_fill()
        for x, y in path[1:]:
            pen.goto(x - 58, 58 - y)
        if filled:
            pen.end_fill()
    pen.hideturtle()
    turtle.done()

