"""
Author: Hima Bindu Krovvidi hk4233
This program finds the shortest path between two terrain points if there exists one.
AI lab1.py
"""

import math
from sys import argv
from PIL import Image

speeds = {}
mapColor = {}
pathway = []


class Lab1:

    def __init__(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.elevated = None
        self.kind = None
        self.val = float("inf")
        self.isVisited = None


def calcGValue(temp, i, val):
    if val == 0:
        dist = math.sqrt(((i.elevated - temp.elevated) * 10.29) ** 2)
    else:
        dist = math.sqrt(((i.elevated - temp.elevated) * 7.55) ** 2)
    return dist/(speeds[temp.kind] + (temp.elevNode - i.elevated) / 40)


def calcHValue(i, dest):
    return math.sqrt((i.x_coordinate - dest.x_coordinate) ** 2 + (i.y_coordinate - dest.y_coordinate) ** 2 + (
            i.elevated - dest.elevated) ** 2) / 2


def calcFValue(temp, i, destination):
    if temp.x_coordinate == i.x_coordinate:
        dist = calcGValue(temp, i, 0) + calcHValue(i, destination)
    else:
        dist = calcGValue(temp, i, 1) + calcHValue(i, destination)
    return dist


def mapConstruct(td, ed):
    temp = []
    for i in range(500):
        ln = []
        for j in range(395):
            l = Lab1(i, j)
            l.kind = mapColor[td[i][j][:3]]
            l.elevated = ed[i][j]
            ln.append(l)
        temp.append(ln)
    return temp


def path(mapUnit, start, destination):
    if speeds[start.kind] == 0:
        print("Wrong source")
        return
    if speeds[destination.kind] == 0:
        print("Wrong destination")
        return
    start.val = 0
    temp = start
    visit = [temp]
    visited = []
    while len(visit) != 0:
        minVal = float("inf")
        minNode = None
        for i in visit:
            if minVal > i.val:
                minNode = i
                minVal = i.val
        temp = minNode
        if temp == destination:
            while temp.isVisited:
                curr = [temp.x_coordinate, temp.y_coordinate]
                pathway.append(curr)
                temp = temp.isVisited
            curr = [temp.x_coordinate, temp.y_coordinate]
            pathway.append(curr)
            return pathway
        else:
            visited.append(temp)
            visit.remove(temp)
            for i in findNeighbors(temp, mapUnit):
                if i not in visited:
                    if i not in visit:
                        i.isVisited = temp
                        visit.append(i)
                        i.val = calcFValue(temp, i, destination)
                    else:
                        currF = calcFValue(temp, i, destination) < i.val
                        if i.val > currF:
                            i.val = currF
                            i.isVisited = temp
    print("Pathway not found")


def findNeighbors(temp, mapUnit):
    neighbors = []
    x = temp.x_coordinate
    y = temp.y_coordinate
    if x == 0:
        if y == 0:
            if speeds[mapUnit[x][y + 1].kind] != 0:
                neighbors.append(mapUnit[x][y + 1])
            if speeds[mapUnit[x + 1][y].kind] != 0:
                neighbors.append(mapUnit[x + 1][y])
        if 0 < y < 394:
            if speeds[mapUnit[x][y - 1].kind] != 0:
                neighbors.append(mapUnit[x][y - 1])
            if speeds[mapUnit[x][y + 1].kind] != 0:
                neighbors.append(mapUnit[x][y + 1])
            if speeds[mapUnit[x + 1][y].kind] != 0:
                neighbors.append(mapUnit[x + 1][y])
        if y == 394:
            if speeds[mapUnit[x][y - 1].kind] != 0:
                neighbors.append(mapUnit[x][y - 1])
            if speeds[mapUnit[x + 1][y].kind] != 0:
                neighbors.append(mapUnit[x + 1][y])
    elif x == 499:
        if y == 0:
            if speeds[mapUnit[x][y + 1].kind] != 0:
                neighbors.append(mapUnit[x][y + 1])
            if speeds[mapUnit[x - 1][y].kind] != 0:
                neighbors.append(mapUnit[x - 1][y])
        if 0 < y < 394:
            if speeds[mapUnit[x][y - 1].kind] != 0:
                neighbors.append(mapUnit[x][y - 1])
            if speeds[mapUnit[x][y + 1].kind] != 0:
                neighbors.append(mapUnit[x][y + 1])
            if speeds[mapUnit[x - 1][y].kind] != 0:
                neighbors.append(mapUnit[x - 1][y])
        if y == 394:
            if speeds[mapUnit[x][y - 1].kind] != 0:
                neighbors.append(mapUnit[x][y - 1])
            if speeds[mapUnit[x - 1][y].kind] != 0:
                neighbors.append(mapUnit[x - 1][y])
    elif 0 < x < 499:
        if y == 0:
            if speeds[mapUnit[x + 1][y].kind] != 0:
                neighbors.append(mapUnit[x + 1][y])
            if speeds[mapUnit[x][y - 1].kind] != 0:
                neighbors.append(mapUnit[x][y - 1])
            if speeds[mapUnit[x - 1][y].kind] != 0:
                neighbors.append(mapUnit[x - 1][y])
        if y == 394:
            if speeds[mapUnit[x + 1][y].kind] != 0:
                neighbors.append(mapUnit[x + 1][y])
            if speeds[mapUnit[x][y - 1].kind] != 0:
                neighbors.append(mapUnit[x][y - 1])
            if speeds[mapUnit[x - 1][y].kind] != 0:
                neighbors.append(mapUnit[x - 1][y])
    else:
        if speeds[mapUnit[x + 1][y].kind] != 0:
            neighbors.append(mapUnit[x + 1][y])
        if speeds[mapUnit[x][y - 1].kind] != 0:
            neighbors.append(mapUnit[x][y - 1])
        if speeds[mapUnit[x - 1][y].kind] != 0:
            neighbors.append(mapUnit[x - 1][y])
        if speeds[mapUnit[x][y + 1].kind] != 0:
            neighbors.append(mapUnit[x][y + 1])
    return neighbors


def init():
    speeds["open_land"] = 2.0
    speeds["rough_meadow"] = 0.25
    speeds["easy_movement_forest"] = 1.25
    speeds["slow_run_forest"] = 1.00
    speeds["walk_forest"] = 0.75
    speeds["impassible_vegetation"] = 0.00
    speeds["lake_swamp_marsh"] = 0.00
    speeds["paved_road"] = 2.00
    speeds["foot_path"] = 2.00
    speeds["out_of_bounds"] = 0.00

    mapColor[248, 148, 18] = "open_land"
    mapColor[255, 192, 0] = "rough_meadow"
    mapColor[255, 255, 255] = "easy_movement_forest"
    mapColor[2, 208, 60] = "slow_run_forest"
    mapColor[2, 136, 40] = "walk_forest"
    mapColor[5, 73, 24] = "impassible_vegetation"
    mapColor[0, 0, 255] = "lake_swamp_marsh"
    mapColor[71, 51, 3] = "paved_road"
    mapColor[0, 0, 0] = "foot_path"
    mapColor[205, 0, 101] = "out_of_bounds"

    terrainData = []
    pixels = Image.open(argv[1])
    pixelImg = list(pixels.getdata())
    rows = []
    cols = 0
    for i in pixelImg:
        rows.append(i)
        cols += 1
        if cols == 395:
            cols = 0
            terrainData.append(rows)
            rows = []

    elevationData = []
    rf = open(argv[2], 'r')
    for r in rf:
        ln = r.strip().split()
        ln2 = []
        for i in range(len(ln)):
            ln2.append(float(ln[i]))
        elevationData.append(ln2)

    paths = []
    rf2 = open(argv[3], 'r')
    for i in rf2:
        ln = i.strip().split()
        points = [int(ln[1]), int(ln[0])]
        paths.append(points)

    for i in range(len(paths) - 1):
        start = paths[i]
        destination = paths[i + 1]
        mapUnit = mapConstruct(terrainData, elevationData)
        path(mapUnit, mapUnit[start[0]][start[1]], mapUnit[destination[0]][destination[1]])
    dist2 = 0
    for i in range(len(pathway) - 1):
        pixels.putpixel((pathway[i][1], pathway[i][0]), (255, 0, 127))
        dist2 = dist2 + (math.sqrt(((pathway[i][0] - pathway[i + 1][0]) * 7.55) ** 2 +
                                   ((pathway[i][1] - pathway[i + 1][1]) * 10.29) ** 2 +
                                   (float(elevationData[pathway[i][1]][pathway[i][0]]) - float(
                                       elevationData[pathway[i + 1][1]][pathway[i + 1][0]])) ** 2))
    pixels.putpixel((pathway[len(pathway) - 1][1], pathway[len(pathway) - 1][0]), (255, 0, 127))
    pixels.save(argv[4])
    print(str(dist2))


if __name__ == '__main__':
    if len(argv) != 5:
        print("Wrong input")
    else:
        init()
