from math import sqrt
from random import seed,random
import pprint

def sqrt_dist(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return sqrt((x1-x2)**2 + (y1-y2)**2)

def build_tree(points,k=2, depth=0):
    """Function that takes the points and returns a kd tree
       k=2 because we have 2D points"""

    nPoints = len(points)

    if nPoints == 0: #if we don't have points there's no tree
        return None

    split_axis = depth % k

    sorted_points = sorted(points, key=lambda point: point[split_axis]) #sort the points by the axis

    return {
        'point': sorted_points[nPoints // 2], #splitting point is the middle point
        'left': build_tree(sorted_points[:nPoints // 2], depth + 1), #left subtree, contains points before the splitting point
        'right': build_tree(sorted_points[nPoints // 2 + 1:], depth + 1) #right subtree, contains points after the splitting point
        #every subtree increaments the depth
    }


def closest_distance(pivot,point1,point2):
    """Function to handle case where point1 is None or point2 is None
    and compare distance from pivot point"""

    if point1 is None:
        return point2

    if point2 is None:
        return point1

    dist1 = sqrt_dist(pivot, point1)
    dist2 = sqrt_dist(pivot, point2)

    if dist1 < dist2:
        return point1
    else:
        return point2


def kdtree_NN(root, point, k=2,depth=0):
    """Find nearest neighbours"""

    if root is None:
        return None

    axis = depth % k

    next_branch = None
    opposite_branch = None  #we want to check also opposite_branch if there's sth better there

    if point[axis] < root['point'][axis]: #if point smaller than splitting point then branch will be the left
        branch = root['left']
        opposite_branch = root['right']
    else:
        branch = root['right']
        opposite_branch = root['left']

    #check which point is closer to the point we search, the current splitting or the one from kdtree_NN
    #recursive call
    best = closest_distance(point,
                           kdtree_NN(branch,point,depth + 1),
                           root['point']) #current splitting point

    #search on the other side of the tree not to miss a better solution
    if sqrt_dist(point, best) > (point[axis] - root['point'][axis]) ** 2:
        best = closest_distance(point,
                               kdtree_NN(opposite_branch,point,depth + 1),
                               best) #previous best

    return best


def find_NN(all,target_point):
    """Use a simple function that finds NN just for comparison with our KDtree"""

    optimal_point = None
    optimal_dist = None

    for current_point in all:
        current_dist = sqrt_dist(current_point,target_point)

        if optimal_dist is None:  #for the first iteration
            optimal_dist=current_dist
            optimal_point=current_point

        if current_dist < optimal_dist:
            optimal_dist=current_dist
            optimal_point=current_point

    return optimal_point



## generate random 2D points
seed(1234) #to always get same results
def random_point(k):
    return [random() for i in range(k)]


def random_points(k, n):
    return [random_point(k) for i in range(n)]

generated_points = random_points(2,15)
pivot= generated_points[0]  #we search the NN for that point
points = [p for p in generated_points if p!= pivot] #all points minus pivot


tree = build_tree(points=points)
pp = pprint.PrettyPrinter(indent=4) #to have a better output of the tree
print("The KD-tree produced is: \n")
pp.pprint(tree)

expected_closest = find_NN(points,pivot)
closest_found = kdtree_NN(tree,pivot)
expected_distance = sqrt_dist(pivot, expected_closest)
found_distance = sqrt_dist(pivot, closest_found)

print("\n Pivot point is: {}".format(pivot))

print("\n Expected closest point is: {} (distance: {})".format(expected_closest, expected_distance))
print("\n Closest point found is: {} (distance: {})".format(closest_found, found_distance))

if found_distance == expected_distance:
    print("\n KD tree found correctly the nearest neighbor :)")
else:
    print("\n Error! Found a worse distance")


"""-------------------- Basic code Done! -----------------------
Below is an additional class with an insert method just to try inserting manually some nodes in a K-D tree
"""

class Point():
    ##constructor
    def __init__(self, x,y):
        self.left = None
        self.right= None
        self.x = x
        self.y = y

def insert_new(root, node):
    if root is None:
        root = node
    else:
        if root.x > node.x and root.y > node.y:
            if root.left is None:
                root.left = node
            else:
                insert_new(root.left, node)
        else:
            if root.right is None:
                root.right = node
            else:
                insert_new(root.right, node)


def print_nodes(root):
    if not root:
        return
    print(root.x,root.y)
    print_nodes(root.left)
    print_nodes(root.right)

r = Point(3,2)
insert_new(r, Point(7,2))
insert_new(r, Point(1,3))
insert_new(r, Point(5,5))

print("\n Nodes inserted:")
print_nodes(r)
