
import cv2
import numpy as np


def create_canvas(document_width: int = 794, document_height: int = 1123) -> np.ndarray:
    canvas = np.zeros((document_height, document_width, 3), dtype=np.uint8)

    margin = 65
    cv2.rectangle(canvas, (0, 0), (document_width, document_height), (255, 255, 255), -1)
    cv2.rectangle(canvas, (margin, margin), (margin+30, margin+30), (0, 0, 255), -1)
    cv2.rectangle(canvas, (margin+15, margin+15), (margin+45, margin+45), (0, 255, 0), -1)
    cv2.rectangle(canvas, (margin+30, margin+30), (margin+60, margin+60), (255, 0, 0), -1)
    tum_logo = cv2.imread("assets/TUM_logo.jpg")
    tum_logo_scaling = .15
    tum_logo = cv2.resize(tum_logo, (int(740 * tum_logo_scaling), int(390 * tum_logo_scaling)))
    # write the logo to the canvas
    x_offset, y_offset = document_width - tum_logo.shape[1] - margin, margin
    canvas[y_offset:y_offset+tum_logo.shape[0], x_offset:x_offset+tum_logo.shape[1]] = tum_logo

    dfg_logo = cv2.imread("assets/logo.jpg")
    dfg_logo_scaling = .3
    dfg_logo = cv2.resize(dfg_logo, (int(1057 * dfg_logo_scaling), int(135 * dfg_logo_scaling)))
    x_offset, y_offset = margin, document_height - dfg_logo.shape[0] - margin
    canvas[y_offset:y_offset+dfg_logo.shape[0], x_offset:x_offset+dfg_logo.shape[1]] = dfg_logo
    return canvas


def draw_nodes(canvas: np.ndarray, nodes: list[tuple[int, int]]) -> np.ndarray:
    for node in nodes:
        cv2.circle(canvas, node, 10, 0, -1)
    return canvas


if __name__ == "__main__":
    canvas = create_canvas()
    cv2.imwrite("test.jpg", canvas)