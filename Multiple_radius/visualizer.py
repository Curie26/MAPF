import numpy as np
import time
import cv2
from copy import deepcopy
import yaml

from cbs_mapf_radius.planner import Planner

class Simulator:
    def __init__(self):
        self.canvas = np.ones((1080, 1920, 3), np.uint8) * 255
        self.draw_rect(np.array([np.array(v) for v in RECT_OBSTACLES.values()]))
        static_obstacles = self.vertices_to_obsts(RECT_OBSTACLES)
        
        self.planner = Planner(GRID_SIZE, ROBOT_RADIUS, static_obstacles)
        print("GRID_SIZE: ", GRID_SIZE)                    
        print("ROBOT_RADIUS: ", ROBOT_RADIUS)              
        print("START: ", START)                            
        print("GOAL: ", GOAL)                               
        before = time.time()
        self.path = self.planner.plan(START, GOAL, debug=False)
        after = time.time()
        print('Time elapsed:', "{:.4f}".format(after-before), 'second(s)')

        self.colours = self.assign_colour(len(self.path))

        if self.path is None or self.path == []:
            print("Path is empty, check planner class")
            return

        d = dict()

        for i, path in enumerate(self.path):
            self.draw_path(self.canvas, path, i, 10)  # Draw the path on canvas
            d[i] = path
        self.path = d
   
    '''
    Press any key to start.
    Press 'q' to exit.
    '''     
    def start(self):
        wait = True
        try:
            i = 0
            while True:
                frame = deepcopy(self.canvas)
                for id_ in self.path:
                    x, y = tuple(self.path[id_][i])
                    cv2.circle(frame, (x, y), ROBOT_RADIUS[id_]-5, self.colours[id_], 5)
                cv2.imshow('frame', frame)
                if wait:
                    cv2.waitKey(0)
                    wait = False
                k = cv2.waitKey(100) & 0xFF 
                if k == ord('q'):
                    break
                i += 1
        except Exception:
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    '''
    Transform opposite vertices of rectangular obstacles into obstacles
    '''
    @staticmethod
    def vertices_to_obsts(obsts):
        def drawRect(v0, v1):
            o = []
            base = abs(v0[0] - v1[0])
            side = abs(v0[1] - v1[1])
            for xx in range(0, base, 30):
                o.append((v0[0] + xx, v0[1]))
                o.append((v0[0] + xx, v0[1] + side - 1))
            o.append((v0[0] + base, v0[1]))
            o.append((v0[0] + base, v0[1] + side - 1))
            for yy in range(0, side, 30):
                o.append((v0[0], v0[1] + yy))
                o.append((v0[0] + base - 1, v0[1] + yy))
            o.append((v0[0], v0[1] + side))
            o.append((v0[0] + base - 1, v0[1] + side))
            return o
        static_obstacles = []
        for vs in obsts.values():
            static_obstacles.extend(drawRect(vs[0], vs[1]))
        return static_obstacles
    '''
    Randomly generate colours
    '''
    @staticmethod
    def assign_colour(num):
        def colour(x):
            x = hash(str(x+42))
            return ((x & 0xFF, (x >> 8) & 0xFF, (x >> 16) & 0xFF))
        colours = dict()
        for i in range(num):
            colours[i] = colour(i)
        return colours

    def draw_rect(self, pts_arr: np.ndarray) -> None:
        for pts in pts_arr:
            cv2.rectangle(self.canvas, tuple(pts[0]), tuple(pts[1]), (0, 0, 255), thickness=3)

    def draw_path(self, frame, xys, i, radius):
        for x, y in xys:
            cv2.circle(frame, (int(x), int(y)), radius, self.colours[i], -1)


def load_scenario(fd):
    with open(fd, 'r') as f:
        global GRID_SIZE, ROBOT_RADIUS, RECT_OBSTACLES, START, GOAL
        data = yaml.load(f, Loader=yaml.FullLoader)
        GRID_SIZE = data['GRID_SIZE']
        ROBOT_RADIUS = data['ROBOT_RADIUS']
        RECT_OBSTACLES = data['RECT_OBSTACLES']
        START = data['START']
        GOAL = data['GOAL']
            

if __name__ == '__main__':
    load_scenario("Multiple_radius/scenario.yaml")
    r = Simulator()
    r.start()
