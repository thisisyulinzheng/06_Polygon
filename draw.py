from display import *
from matrix import *
from gmath import *

def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, color ):
    i = 0
    v = [0, 0, 1]
    while (i < len(polygons) - 2):
        n = calculate_normal(polygons, i)
        dot = dot_product(n, v)
        if (dot > 0):
            p0 = polygons[i]
            p1 = polygons[i+1]
            p2 = polygons[i+2]
            draw_line(p0[0], p0[1], p1[0], p1[1], screen, color)
            draw_line(p1[0], p1[1], p2[0], p2[1], screen, color)
            draw_line(p2[0], p2[1], p0[0], p0[1], screen, color)
        i+=3

def add_box( polygons, x, y, z, width, height, depth ):

    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #top
    add_polygon(polygons, x, y, z, x1, y, z1, x, y, z1)
    add_polygon(polygons, x, y, z, x1, y, z, x1, y, z1)
    #bottom
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    #front
    add_polygon(polygons, x, y, z, x, y1, z, x1, y, z)
    add_polygon(polygons, x, y1, z, x1, y1, z, x1, y, z)
    #back
    add_polygon(polygons, x, y, z1, x1, y, z1, x, y1, z1)
    add_polygon(polygons, x, y1, z1, x1, y, z1, x1, y1, z1)
    #left
    add_polygon(polygons, x, y, z, x, y, z1, x, y1, z1)
    add_polygon(polygons, x, y, z, x, y1, z1, x, y1, z)
    #right
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, steps ):
    points = generate_sphere(cx, cy, cz, r, steps)
    total = (len(points))
    steps += 1
    for slice in range(0, steps + 1):
        for semi in range(0, steps - 1):
            i0 = (slice * steps + semi) % total
            i1 = (slice * steps + semi + 1) % total
            i2 = (slice * steps + semi + steps + 1) % total
            i3 = (slice * steps + semi + steps) % total
            add_polygon(polygons,points[i0][0], points[i0][1], points[i0][2],
                        points[i1][0], points[i1][1], points[i1][2],
                        points[i2][0], points[i2][1], points[i2][2])
            if (semi != 0):
                add_polygon(polygons, points[i0][0], points[i0][1], points[i0][2],
                            points[i2][0], points[i2][1], points[i2][2],
                            points[i3][0], points[i3][1], points[i3][2])



def generate_sphere( cx, cy, cz, r, steps ):
    points = []

    rot_start = 0
    rot_stop = steps
    circ_start = 0
    circ_stop = steps

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(steps)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(steps)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, steps ):
    points = generate_torus(cx, cy, cz, r0, r1, steps)
    total = (len(points))
    for slice in range(0, steps):
        for cir in range(0, steps):
            i0 = (slice * steps + cir) % total
            i1 = (slice * steps + cir + 1) % total
            i2 = (slice * steps + cir + steps + 1) % total
            i3 = (slice * steps + cir + steps) % total
            add_polygon(polygons, points[i0][0], points[i0][1], points[i0][2],
                        points[i2][0], points[i2][1], points[i2][2],
                        points[i1][0], points[i1][1], points[i1][2])
            add_polygon(polygons,points[i0][0], points[i0][1], points[i0][2],
                        points[i3][0], points[i3][1], points[i3][2],
                        points[i2][0], points[i2][1], points[i2][2])

def generate_torus( cx, cy, cz, r0, r1, steps ):
    points = []
    rot_start = 0
    rot_stop = steps
    circ_start = 0
    circ_stop = steps

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(steps)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(steps)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, steps ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= steps:
        t = float(i)/steps
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, steps, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= steps:
        t = float(i)/steps
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )

def draw_line( x0, y0, x1, y1, screen, color ):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
