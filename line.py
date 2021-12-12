# Using http://trystans.blogspot.com/2011/09/roguelike-tutorial-08-vision-line-of.html
def get_line(x0, y0, x1, y1):
  points = []
  
  dx = abs(x1 - x0)
  dy = abs(y1 - y0)
  
  sx = 1 if x0 < x1 else -1
  sy = 1 if y0 < y1 else -1
  err = dx - dy

  while True:
    points.append((x0, y0))
    if x0 == x1 and y0 == y1:
      break

    e2 = err * 2

    if e2 > -dy:
      err -= dy
      x0 += sx
    if e2 < dx:
      err += dx
      y0 += sy
  return points

def get_line_no_diagonal(x0, y0, x1, y1):
  points = []
  
  dx = abs(x1 - x0)
  dy = abs(y1 - y0)
  
  sx = 1 if x0 < x1 else -1
  sy = 1 if y0 < y1 else -1
  err = dx - dy

  while True:
    points.append((x0, y0))
    if x0 == x1 and y0 == y1:
      break

    e2 = err * 2

    if e2 >= -dy:
      err -= dy
      x0 += sx
    elif e2 < dx:
      err += dx
      y0 += sy
  return points
