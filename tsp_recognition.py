import cv2
import numpy as np
import math
from tsp_instances import tum_logo, spanning_tree


# (ORB) feature based alignment      
def featureAlign(im1, im2, max_features=10000, feature_retention=0.01):
  
  # Convert images to grayscale
  im1Gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
  im2Gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    
  # Detect ORB features and compute descriptors.
  orb = cv2.ORB_create(max_features)
  keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
  keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
  
  # Match features.
  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
  matches = list(matcher.match(descriptors1, descriptors2, None))
#   print(matches)
  # Sort matches by score
  matches.sort(key=lambda x: x.distance, reverse=False)

  # Remove not so good matches
  numGoodMatches = int(len(matches) * feature_retention)
  matches = matches[:numGoodMatches]

  # Draw top matches
  imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
  #cv2.imwrite("matches.jpg", imMatches)
  
  # Extract location of good matches
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)

  for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt
  
  # Find homography
  h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

  # Use homography
  height, width, channels = im2.shape
  im1Reg = cv2.warpPerspective(im1, h, (width, height))
  
  return im1Reg, h 


def local_search(bitmap, start_v, start_h, end_v, end_h, max_distance) -> bool:
  """
  Use BFS (potentially with skipping) to find a path from the start node to the end node.
  If the path is found, return True.
  Otherwise, return False.
  """
  assert bitmap[start_h][start_v] == 255
  # Find all adjacent pixels
  pixel_queue = [(start_h, start_v)]
  visited = set()
  while pixel_queue:
    h, v = pixel_queue.pop(0)
    visited.add((h, v))
    if end_h == h and end_v == v:
       return True
    for dh, dv in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1),
                   (0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (2, -2), (-2, 2), (-2, -2), 
                   (1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]:
      nh, nv = h + dh, v + dv
      if nh < 0 or nv < 0 or nh >= len(bitmap) or nv >= len(bitmap[0]):
        continue
      if (nh, nv) in visited or (nh, nv) in pixel_queue:
        continue
      if bitmap[nh][nv] > 100:
        if distance_from_line(h, v, start_h, start_v, end_h, end_v) <= max_distance:
          pixel_queue.append((nh, nv))
  return False


def distance_from_line(x, y, x1, y1, x2, y2) -> int:
    # Calculate the distance from the point (x, y) to the line segment from (x1, y1) to (x2, y2)
    a = x - x1
    b = y - y1
    c = x2 - x1
    d = y2 - y1
    dot = a * c + b * d
    len_sq = c * c + d * d
    param = -1
    if len_sq != 0:
        param = dot / len_sq
    if param < 0:
       xx = x1
       yy = y1
    elif param > 1:
       xx = x2
       yy = y2
    else:
       xx = x1 + param * c
       yy = y1 + param * d
    dx = x - xx
    dy = y - yy
    return int(math.sqrt(dx * dx + dy * dy))


def get_edged_image(image_1, image_2, max_features=10000, feature_retention=0.01):
  """
  Align the user image to the instance image. 
  Find the edges of the user image.
  """
  im1 =  cv2.imread(image_1);

  lab= cv2.cvtColor(im1, cv2.COLOR_BGR2LAB)
  l_channel, a, b = cv2.split(lab)

  # Applying CLAHE to L-channel
  # feel free to try different values for the limit and grid size:
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2,2))
  cl = clahe.apply(l_channel)

  # merge the CLAHE enhanced L-channel with the a and b channel
  limg = cv2.merge((cl,a,b))

  # Converting image from LAB Color model to BGR color spcae
  im1 = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

  # cv2.imshow('im1', im1)
  # cv2.waitKey(0)
  
  im2 =  cv2.imread(image_2);

  aligned, warp_matrix = featureAlign(im1, im2, max_features=max_features, feature_retention=feature_retention)
  cv2.imwrite("aligned.jpg", aligned, params=[cv2.IMWRITE_JPEG_QUALITY, 90])
  print(warp_matrix)

  # Contours

  image = cv2.imread('aligned.jpg') 
  image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)
    
  # Grayscale 
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    
  # Find Canny edges 
  edged = cv2.Canny(gray, 30, 100) 
  return edged


def find_connections(edged, tsp_points):
  connections = []
  for point_1 in tsp_points:
    tsp_points_2 = tsp_points.copy()
    tsp_points_2 = sorted(tsp_points_2, key=lambda x: (x[0] - point_1[0])**2 + (x[1] - point_1[1])**2)
    connected: list[tuple[int, int]] = []
    for point_2 in tsp_points_2:
      if point_1 == point_2:
        continue
      if local_search(edged, *point_1, *point_2, 20):
        colinear = False
        for prev_point in connected:
          if distance_from_line(*prev_point, *point_1, *point_2) <= 40:
            colinear = True
            print("Found colinear points:", tsp_points.index(point_1), tsp_points.index(point_2))
            break
        if colinear:
          continue
        connected.append(point_2)
        if (point_1, point_2) not in connections and (point_2, point_1) not in connections:
          print("Found a connection:", tsp_points.index(point_1), tsp_points.index(point_2))
          connections.append((point_1, point_2))
  return connections


def get_score(user_img, instance_type, user_img_name):
  tsp_points, file_name = tum_logo(create_file=False)
  if int(instance_type) == 2:
    tsp_points, file_name = spanning_tree(create_file=False)

  image_1 = user_img
  image_2 = file_name

  edged = get_edged_image(image_1, image_2)
    
  # Insert known points
  for point in tsp_points:
    edged = cv2.circle(edged, point, 15, 255, -1)

  # Brute force search for connections
  connections = find_connections(edged, tsp_points)

  # Show the point indices
  for point in tsp_points:
    edged = cv2.putText(edged, f'{tsp_points.index(point)}', (point[0]-5, point[1]+6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 100, 2)

  # Calculate the score
  score: float = 0
  for p_1, p_2 in connections:
    score += math.sqrt((p_1[0] - p_2[0])**2 + (p_1[1] - p_2[1])**2)
    edged = cv2.line(edged, p_1, p_2, 100, 2)
  print(f'Score: {score}')
  cv2.imwrite(f"contour/contour-{user_img_name}", edged)
  # cv2.imshow('Canny Edges After Contouring', edged) 

  # cv2.waitKey(0) 
  return score
  


if __name__ == '__main__':
  get_score("user_input/1 Annaluisa.jpg", 1, "tsp_instances/tum_logo.jpg")