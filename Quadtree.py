from math import sqrt
import pprint


class Point:
    """Construct a 2D point (x,y)"""

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __str__(self):

        return "(%s, %s)" % (self.x, self.y)

class Rect:
    """Rectangle with central point (cx,cy), width=w and height=h"""

    def __init__(self, cx, cy, w, h):
        self.cx, self.cy = cx, cy
        self.w, self.h = w, h
        self.west_side, self.east_side = cx - w/2, cx + w/2
        self.north_side, self.south_side = cy - h/2, cy + h/2


    def contains(self, point):
        """Check if point is inside this Rect"""

        point_x, point_y = point.x, point.y


        if (point_x >= self.west_side and point_x <  self.east_side and
            point_y >= self.north_side and point_y < self.south_side):
            return True
        else:
            return False

    def intersects(self, other):
        """Check if Rect object "other" interesects this Rect"""
        if (other.west_side > self.east_side or other.east_side < self.west_side or
           other.north_side > self.south_side or other.south_side < self.north_side):
            return False
        else:
            return True


class Quadtree:
    def __init__(self, boundary, max_points=2):

        self.boundary = boundary
        self.max_points = max_points
        self.points = []
        self.divided = False #to check if a node has been divided

    def divide(self):
        """Split a node into four nodes(children)"""

        cx, cy = self.boundary.cx, self.boundary.cy
        w, h = self.boundary.w / 2, self.boundary.h / 2
        # The boundaries of the four children nodes are "northwest",
        # "northeast", "southeast" and "southwest" quadrants within the
        # boundary of the current node.
        self.nw = Quadtree(Rect(cx - w/2, cy - h/2, w, h),
                                    self.max_points)
        self.ne = Quadtree(Rect(cx + w/2, cy - h/2, w, h),
                                    self.max_points)
        self.se = Quadtree(Rect(cx + w/2, cy + h/2, w, h),
                                    self.max_points)
        self.sw = Quadtree(Rect(cx - w/2, cy + h/2, w, h),
                                    self.max_points)
        self.divided = True

    def insert(self, point):
        """Insert a Point into the tree"""

        if not self.boundary.contains(point):
            #point outside of the boundary
            return False
        if len(self.points) < self.max_points:
            # point can be inserted here,capacity is ok
            self.points.append(point)
            return True

        # Max_points exceeded: divide if needed and then check children.
        if not self.divided:
            self.divide()

        return (self.ne.insert(point) or
                self.nw.insert(point) or
                self.se.insert(point) or
                self.sw.insert(point))

    def query(self, boundary):
        """Find those points that lie within the boundary"""

        points_inside = []
        if not self.boundary.intersects(boundary):
            #abort if the searching range does not intersect this quad
            return False

        # Search this node's points to see if they lie within boundary
        for point in self.points:
            if boundary.contains(point):
                points_inside.append(point)
        # and if this node has children, search them too.
        if self.divided == True:
            self.nw.query(boundary)  #deleted found_points
            self.ne.query(boundary)
            self.se.query(boundary)
            self.sw.query(boundary)
        return points_inside

    def find_k_NN(self, point, k=1):
        """Find the nearest neighbour(k=1)"""

        def dist_points(new):
            return sqrt((point.x - new.x)**2 + (new.y - point.y)**2)

        neighbors = None
        for i in range(1, 10):
            area = Rect(point.x,point.y, (2**i)/2,(2**i)/2)
            neighbors = self.query(area)
            if len(neighbors) >= k:
                break
        return sorted(neighbors, key= dist_points)[:k] #sort according to distance

    def print__(self,point):
        """Print all the nodes of the tree."""

        for p in point.points:
            print("{}".format(p))
        if self.divided==True:
            if self.nw!= None:
               self.nw.print__(point.nw)
            if self.ne!= None:
               self.ne.print__(point.ne)
            if self.sw!= None:
               self.sw.print__(point.sw)
            if self.se!= None:
               self.se.print__(point.se)


r = Rect(5,2,100,100)
tree = Quadtree(r)
## Instert some points into the tree
tree.insert(Point(1,2))
tree.insert(Point(2,3))
tree.insert(Point(4,6))
tree.insert(Point(5,5))
tree.insert(Point(10,20))
tree.insert(Point(8,3))
tree.insert(Point(4,3))
point_interest = Point(2, 6)


print("\n Print all points:")
tree.print__(tree)

## Get the nearest neighbor to the point of interest
neigh = tree.find_k_NN(point_interest)
print("\n Nearest neighbor of point {}:".format(point_interest))
for point in neigh:
    print(point)

## View the points inside the specified rectangle
print("\n Points within the specified rectangle:")
for point in tree.query(r):
    print(point)

## Check if a point exists inside the specified rectangle
pt= Point(5,5)
r1 = Rect(pt.x,pt.y,50,50)
print("\n Let's check if point {} exists inside the rectangle with boundaries {}".format(pt,(r1.cx,r1.cy,r1.w,r1.h)))
if len(tree.query(r1))>0:
    print("\n Point {} exists".format(pt))
else:
    print("\n Point {} does not exist".format(pt))
