import random
import copy

centers = []

UP = 0x01
DOWN = 0x02
LEFT = 0x04
RIGHT = 0x08

def find_centers(board):
    x = 0
    y = 0

    for row in board:
        for item in row:
            if item == "c":
                dir = 0;
                if board[y][x+1] == "b" and board[y][x-1] == "b":
                    if board[y+1][x] == "b":
                        dir = DOWN
                    if board[y-1][x] == "b":
                        dir = UP
                if board[y+1][x] == "b" and board[y-1][x] == "b":
                    if board[y][x+1] == "b":
                        dir = RIGHT
                    if board[y][x-1] == "b":
                        dir = LEFT
                centers.append((x,y,dir))
            x += 1
        x = 0
        y += 1

    return centers

def find_cell(board, cell):
    x = 0
    y = 0
    for row in board:
        for item in row:
            if item == cell:
                return (x,y)
            x += 1
        x = 0
        y += 1

def find_start(board):
    return find_cell(board, "s")

def find_end(board):
    return find_cell(board, "e")


def find_center(x, y, centers):
    for center in centers:
        if center[0] == x and center[1] == y:
            return center

def sort_centers(start, centers):
    hitcount = 0
    x = start[0]
    y = start[1]
    direction = RIGHT
    new_centers = []
    while hitcount < len(centers):
        if direction == RIGHT:
             x += 1
        if direction == LEFT:
             x -= 1
        if direction == UP:
             y -= 1
        if direction == DOWN:
             y += 1

        if board[y][x] == "c":
            center = find_center(x,y, centers)
            new_centers.append(center)
            direction = center[2]
            hitcount += 1
    return new_centers


INITIAL_DIST = 100000000

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self._edict = {}


    def add_vertex(self, vid):
        self.vertices.append(vid)

    def add_edge(self, vid1, vid2):
        if vid1 in self.vertices and vid2 in self.vertices:
            if not self._edict.has_key(vid1):
                self._edict[vid1] = []

            if not self._edict.has_key(vid2):
                self._edict[vid2] = []

            self._edict[vid1].append(vid2)
            self._edict[vid2].append(vid1)

            self.edges.append((vid1, vid2))

    def nearest_node(self, dist, q):
        min = INITIAL_DIST
        nearest = None
        for key in dist:
            if dist[key] < min and key in q:
                nearest = key
                min = dist[key]
        return nearest


    def neighbors(self, node):
        neighbors = []
        for vid in self._edict[node]:
            neighbors.append(vid)
        return neighbors

    def shortest_path(self, vid1, vid2):
        if vid1 in self.vertices and vid2 in self.vertices:
            dist = {}
            previous = {}
            for v in self.vertices:
                dist[v] = INITIAL_DIST
                previous[v] = None

            dist[vid1] = 0
            q = self.vertices[:]
            while len(q) > 0:
                u = self.nearest_node(dist, q)
                if u == None:
                    return dist
                q.remove(u)
                n = self.neighbors(u)
                for v in n:
                    alt = dist[u] + 1
                    if alt < dist[v]:
                        dist[v] = alt
                        previous[v] = u

            return dist



def cell_clear(board, x, y):
    if (y >= 0 and y < len(board) and x >= 0 and x < len(board[0])):
        val = board[y][x]
        return val == " " or val == "p" or val == "b" or val == "s" or val == "e" or val == "c"


def get_cell_name(x, y):
    return str(x) + "_" + str(y)

def board_to_graph(board):
    y = 0
    x = 0
    g = Graph()
    for row in board:
        for item in row:
            g.add_vertex(get_cell_name(x,y))
            x += 1
        x = 0
        y += 1

    x = 0
    y = 0
    for row in board:
        for item in row:
            if cell_clear(board, x, y):
                if cell_clear(board, x-1, y):
                    g.add_edge(get_cell_name(x,y), get_cell_name(x-1, y))
                if cell_clear(board, x+1, y):
                    g.add_edge(get_cell_name(x,y), get_cell_name(x+1, y))
                if cell_clear(board, x, y-1):
                    g.add_edge(get_cell_name(x,y), get_cell_name(x, y-1))
                if cell_clear(board, x, y+1):
                    g.add_edge(get_cell_name(x,y), get_cell_name(x, y+1))
            x += 1
        x = 0
        y += 1
    return g


def add_n_walls(board, n):
    x = 0
    y = 0
    height = len(board)
    width = len(board[0])
    placements = []
    for i in range(0, n):
        while board[y][x] != " " and board[y][x] != "p":
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
        if (board[y][x] == " " or board[y][x] == "p"):
            board[y][x] = "w"
            placements.append((x,y))
    return placements


def print_board(board):
    for row in board:
        print "".join(row)


def do_length(board, centers, start, end):
    g = board_to_graph(board)
    centers = sort_centers(start, centers)
    nc = []
    for center in centers:
        nc.append((center[0], center[1]))
    centers = nc
    centers.append(end)
    centers.insert(0, start)
    sum = 0
    for i in range(1, len(centers)):
        start = centers[i-1]
        end = centers[i]
        start_name = get_cell_name(start[0], start[1])
        end_name = get_cell_name(end[0], end[1])
        dist = g.shortest_path(start_name, end_name)[end_name]
        sum += dist
    return sum

if __name__ == "__main__":
    board_text = open("gem").read().strip()
    board = []
    for line in board_text.split("\n"):
        board.append(list(line))

    centers = find_centers(board)
    start = find_start(board)
    end = find_end(board)

    best_board = board
    print "initial shortest path start"
    best_length = do_length(board, centers, start, end)
    print best_length
    print "initial shortest path end"
    best_p = []

    while True:
        bprime = copy.deepcopy(board)
        p = add_n_walls(bprime, 30)
        print "loop shortest path start"
        candidate_length = do_length(bprime, centers, start, end)
        print "loop shortest path end", candidate_length, best_length
        if candidate_length > best_length and candidate_length != INITIAL_DIST:
            best_length = candidate_length
            best_board = bprime
            best_p = p
            print_board(bprime)
            print best_length
            print best_p
            print "____________________________________________________________"
