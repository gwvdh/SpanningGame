import cv2
from create_file import create_canvas, draw_nodes
import random
import math


def test_1(create_file: bool = False):
    tsp_points = [(409, 542), (445, 344), (606, 668), (160, 486), (214, 682), (374, 809), (642, 415), (231, 307)]
    file_name = "tsp_instances/test_instance_1.jpg"
    if create_file:
        canvas = create_canvas()
        canvas = draw_nodes(canvas, tsp_points)
        cv2.imwrite(file_name, canvas)
    return tsp_points, file_name


def tum_logo(create_file: bool = False):
    tsp_points = [(150, 400),                                     (350, 400), (400, 400),                                                 (650, 400),
                  (150, 450), (200, 450), (250, 450), (300, 450),                         (450, 450), (500, 450), (550, 450), (600, 450), 
                                                                  (350, 750), (400, 750), 
                              (200, 800), (250, 800), (300, 800),                         (450, 800), (500, 800), (550, 800), (600, 800), (650, 800)]
    file_name = "tsp_instances/tum_logo.jpg"
    if create_file:
        canvas = create_canvas()
        canvas = draw_nodes(canvas, tsp_points)
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY) 
        cv2.imwrite(file_name, canvas)
    return tsp_points, file_name


def spanning_tree(create_file: bool = False):
    tsp_points = [(269, 270), (642, 561), (459, 202), (489, 867), (445, 267), (615, 848), (551, 510), (289, 436), (381, 479), (622, 667), 
                  (124, 246), (105, 202), (306, 501), (203, 349), (427, 414), (388, 862), (344, 544), (314, 270), (337, 318), (451, 694), 
                  (120, 820), (250, 860)]
    file_name = "tsp_instances/spanning_tree.jpg"
    if create_file:
        canvas = create_canvas()
        canvas = draw_nodes(canvas, tsp_points)
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY) 
        cv2.imwrite(file_name, canvas)
        for point in tsp_points:
            cv2.putText(canvas, f'{tsp_points.index(point)}', (point[0]-5, point[1]+6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2)
        cv2.imshow('Spanning tree', canvas) 

        # cv2.waitKey(0)
    return tsp_points, file_name


def random_spanning_tree(create_file: bool = False):
    tsp_points = []
    for i in range(20):
        x = random.randint(100, 700)
        y = random.randint(200, 900)
        too_close = False
        for point in tsp_points:
            if math.sqrt((x - point[0])**2 + (y - point[1])**2) < 30:
                too_close = True
                break
        if not too_close:
            tsp_points.append((x, y))
    file_name = "tsp_instances/random_spanning_tree.jpg"
    if create_file:
        canvas = create_canvas()
        canvas = draw_nodes(canvas, tsp_points)
        cv2.imwrite(file_name, canvas)
        print(tsp_points)
        cv2.imshow('Random instance', canvas) 

        cv2.waitKey(0) 

    return tsp_points, file_name

if __name__ == "__main__":
    spanning_tree(create_file=True)