
"""
    This is a solution to the problem:

    Given a list of cartesian coordinates (2D so x,y), find all of the permutations
    of four points which form a rectangle/square.

    The solution checks all permutations of four points to detect that the points
    form two right angle triangles across perpendicular lines.
    Perpendicular testing requires a bit of overhead to prevent divide-by-zero,
    but the rest of the approach leverages computational geometry (distance, Slope
    and orthogonality) to avoid the need to sort.
    The solution does not concern itself with rectangle orientation as it relies
    on angles and lengths between points.

    I saw this on youtube one day, and spent a lot longer than the video trying to
    solve it myself.
"""

import logging
import math

def length(p1, p2):
    """ what is the linear distance between two points of x,y
        @NOTE calculated using pythagoreus
    """
    rise = abs(p1[1]-p2[1])
    run = abs(p1[0]-p2[0])
    return math.sqrt(math.pow(rise,2)+math.pow(run,2))

def slope(p1, p2):
    """ return that slope of a line formed by two points of x,y
        @NOTE does not check for divide-by-zero
        @SEE is_slope_infinite for divide-by-zero checks
    """
    return abs(p1[1]-p2[1])/abs(p1[0]-p2[0])

def is_slope_infinite(p1, p2):
    """ do two points of x,y form a line with infinite slope """
    return p1[0]==p2[0]

def is_perpendicular(l1, l2):
    """ Are two lines, each from two points of x,y, perpendicular """
    assert len(l1) == 2 and len(l1[0]) == 2 and len(l1[1]) == 2, "l1 is supposed to be a set of two points of x,y"
    assert len(l2) == 2 and len(l2[0]) == 2 and len(l2[1]) == 2, "l2 is supposed to be a set of two points of x,y"

    # first priority, avoid divide by zeros in slope (do this here to avoid complicated slope method)
    # if both lines are of infinite slope, then they are parrallel
    if is_slope_infinite(l1[0], l1[1]) and is_slope_infinite(l2[0], l2[1]):
        return False
    # if one line has infinite slope, then the other is perp only if it has
    # a slope of 1
    elif is_slope_infinite(l1[0], l1[1]):
        return slope(l2[0], l2[1]) == 0
    elif is_slope_infinite(l2[0], l2[1]):
        return slope(l1[0], l1[1]) == 0
    # all other cases, the two slope should be inverse.  slope(l1) = 1/slope(l2)
    # which we re-arrange in order to avoid divide-by-zero again.
    else:
        return slope(l1[0], l1[1]) * slope(l2[0], l2[1]) == 1

def unit_point():
    """ Some unit tests for point and line comparisons """
    assert math.isclose(length((0, 0),(0, 5)), 5.0, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((1, 1),(10, 1)), 9.0, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((0, 0),(3, 4)), 5.0, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((5, 3),(1, 13)), 10.770330, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((1, 1),(1, 13)), 12.000000, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((1, 1),(5, 3)), 4.472136, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((1, 1),(8, 13)), 13.892444, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((5, 3),(10, 13)), 11.180340, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((1, 1),(10, 13)), 15.000000, rel_tol=1e-6), "Wrong length"
    assert math.isclose(length((5, 3),(14, 14)), 14.212670, rel_tol=1e-6), "Wrong length"

    assert not math.isclose(length((2, 3),(11, 14)), 1, rel_tol=1e-6), "Wrong length"

    assert not is_slope_infinite((1,2), (2,3)), "Slope should not be infinite"
    assert is_slope_infinite((1,2), (1,4)), "Slope should be infinite"
    assert slope((3,3), (6,6)) == 1, "Slope should be 1"
    assert is_perpendicular(((1,1), (1,4)), ((0,3), (7,3))), "Lines should be perpendicular"
    assert is_perpendicular(((1,1), (4,4)), ((1,4), (4,1))), "Lines should be perpendicular"
    assert not is_perpendicular(((1,1), (1,4)), ((3,1), (3,4))), "Lines should not be perpendicular"
    assert not is_perpendicular(((1,8), (6,2)), ((3,5), (2,7))), "Lines should not be perpendicular"

def is_ra_triangle(start, ra, finish):
    """ prove that three points of x,y form a right angle triangle from a->b and b->c """
    return math.isclose(math.pow(length(start, ra),2) + math.pow(length(ra, finish),2), math.pow(length(start, finish),2), rel_tol=1e-9)

def is_rectangle(a, b, c, d):
    """ Do four points form a rectangle?
        Any four points of x,y from three lines from any one of the points
           EL = ((a,b) , (a,c) , (a,d))
        to prove we have a rectangle, the following needs to be proven:
        1. we should be able to form two right-angle triangles around the longest line
        2. the two shorter lines will be perpendicular (it suffices to prove that two lines are perp)
    """
    if is_perpendicular((a,b), (a,c)):
        # a,b and a,c are perpendicular, so a,d is the only possible hyp
        return is_ra_triangle(a, b, d) and is_ra_triangle(a, c, d)
    elif is_perpendicular((a,b), (a,d)):
        # a,b and a,d are perpendicular, so a,c is the only possible hyp
        return is_ra_triangle(a, b, c) and is_ra_triangle(a, d, c)
    else:
        # if none of our lines are perpendicular then we can't have a rectangle
        return False

def unit_is_rectangle():
    """ Some unit testing for rectangle checking """
    assert is_ra_triangle((4, 6), (3, 11), (8, 12)), "right-angle triangle not detected"
    assert is_ra_triangle((4, 6), (9, 7), (8, 12)), "right-angle triangle not detected"
    assert is_ra_triangle((4, 6), (3, 7), (8, 12)), "right-angle triangle not detected"
    assert is_ra_triangle((3, 11), (1, 13), (2, 14)), "right-angle triangle not detected"

    assert not is_ra_triangle((1, 6), (3, 11), (8, 12)), "right-angle triangle false detected"
    assert not is_ra_triangle((4, 6), (1, 7), (8, 12)), "right-angle triangle false detected"

    assert is_rectangle((1,1), (1,4), (3,1), (3,4)), "Expected rectangle denied"
    assert is_rectangle((10, 12), (8, 13), (11, 14), (9, 15)), "Expected rectangle denied"
    assert is_rectangle((9, 14), (15, 14), (9, 15), (15, 15)), "Expected rectangle denied"

    assert not is_rectangle((2,1), (3,4), (1,1), (2,6)), "Unexpected rectangle accepted"
    assert not is_rectangle((1,1), (1,4), (2,1), (3,4)), "Unexpected rectangle accepted"
    assert not is_rectangle((1,1), (1,5), (3,1), (3,4)), "Unexpected rectangle accepted"
    assert not is_rectangle((1,1), (1,4), (3,1), (4,4)), "Unexpected rectangle accepted"
    assert not is_rectangle((6, 1), (1, 6), (14, 9), (3, 14)), "Unexpected rectangle accepted"
    assert not is_rectangle((2, 1), (9, 2), (15, 10), (4, 15)), "Unexpected rectangle accepted"
    assert not is_rectangle((6, 4), (10, 7), (9, 8), (5, 11)), "Unexpected rectangle accepted"

unit_point()
unit_is_rectangle()

# Lots of random points to play with
points = (
    (1,1),
    (2,1),
    (5,1),
    (6,1),
    (7,1),
    (11,1),
    (13,1),
    (1,2),
    (3,2),
    (5,2),
    (6,2),
    (9,2),
    (10,2),
    (14,2),
    (1,3),
    (4,3),
    (5,3),
    (8,3),
    (11,3),
    (14,3),
    (1,4),
    (2,4),
    (6,4),
    (12,4),
    (3,5),
    (7,5),
    (11,5),
    (15,5),
    (1,6),
    (2,6),
    (4,6),
    (5,6),
    (9,6),
    (12,6),
    (14,6),
    (1,7),
    (3,7),
    (4,7),
    (5,7),
    (8,7),
    (9,7),
    (10,7),
    (13,7),
    (15,7),
    (1,8),
    (2,8),
    (3,8),
    (8,8),
    (9,8),
    (10,8),
    (15,8),
    (10,9),
    (11,9),
    (12,9),
    (13,9),
    (13,9),
    (14,9),
    (15,9),
    (2,10),
    (10,10),
    (15,10),
    (1,11),
    (3,11),
    (4,11),
    (5,11),
    (6,11),
    (10,11),
    (1,12),
    (4,12),
    (5,12),
    (8,12),
    (10,12),
    (11,12),
    (13,12),
    (15,12),
    (1,13),
    (2,13),
    (3,13),
    (8,13),
    (10,13),
    (2,14),
    (3,14),
    (8,14),
    (9,14),
    (14,14),
    (11,14),
    (12,14),
    (15,14),
    (1,15),
    (2,15),
    (3,15),
    (4,15),
    (7,15),
    (9,15),
    (10,15),
    (15,15),
)

def find_all_rectangles(ps):
    """ Print all permutations of 4 points of x,y from the passed array which
        form a rectangle in any orientation """

    lim = len(ps)

    assert lim >= 4, "Not enough points to make a rectangle"
    print("Checking for rectangles across %d points" % (lim))

    """
        Pick 4 indexes of the ps array, moving forward only to limit ourselves
        to permutations of points.

        @NOTE we could try to eliminate sets early, but the cost saving isn't
            certain, so it might not actually perform any better

            1. no rectangle can exist with four points of the same X, or Y value
               so we could quick drop permutations that don't span across X or Y
               values.
    """
    checked = 0
    found = 0
    for i in range(0, lim-3):
        for j in range(i+1, lim-2):
            for k in range(j+1, lim-1):
                for l in range(k+1, lim):
                    checked += 1
                    if is_rectangle(ps[i], ps[j], ps[k], ps[l]):
                        print ("FOUND: (%d, %d, %d, %d) => %s, %s, %s, %s" % (i, j, k, l, ps[i], ps[j], ps[k], ps[l]))
                        found += 1

    print("FINISHED [Checked:%d][Found:%d]" % (checked, found))

find_all_rectangles(points)
