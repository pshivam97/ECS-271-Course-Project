"""(https://www.youtube.com/watch?v=yCQN096CwWM)
"""

# Library Imports

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import cv2
from matplotlib import pyplot as plt

# Global Variables
output_image_height = 128

# This function will display image given the numpy ndarray
def disp_image(M):
  plt.imshow(M)
  plt.show()

# This function will return maximum sum subarray
def kadane(A):
  A = np.array(A)
  n = len(A)
  k = 1
  y = A[0]
  t = A[0]
  l = 0
  r = 0
  ltmp = 0
  rtmp = 0
  while k != n:
    if t + A[k] > A[k] :
      t = t + A[k]
    else:
      t = A[k]
      ltmp = k
    rtmp += 1

    if t > y :
      y = t
      l = ltmp
      r = rtmp
    k = k + 1
  return y, l, r

# This function will return loosely maximum sum rectangle
def SubRectangularMatrixWithMaximumSumHorizontalAndVertical(M):
  M = np.array(M)
  H, W = M.shape

  _, max_L, max_R = kadane(np.sum(M,axis=0))
  _, max_U, max_D = kadane(np.sum(M,axis=1))

  return max_L, max_R, max_U, max_D

# This function will remove extra spaces in image from all four sides
def remove_space(M, weight_of_dark = -1, weight_of_light = 100):

  # Converting to np array
  M = np.array(M)
  height = M.shape[0]
  width = M.shape[1]

  # Converting picture to binary
  vf = np.vectorize(convert_to_binary)
  binary_image = vf(M)

  # Reweight matrix
  assign_weight = lambda x: weight_of_light if x == 0 else weight_of_dark

  vfw = np.vectorize(assign_weight)
  MW = vfw(binary_image) # Weighted matrix

  # Return result
  max_L, max_R, max_U, max_D = SubRectangularMatrixWithMaximumSumHorizontalAndVertical(MW)

  padding = height // 20

  # Add Padding
  if max_L > padding:
    max_L -= padding
  else:
    max_L = 0

  if max_R + padding < width :
    max_R += padding
  else:
    max_R = width - 1

  if max_U > padding:
    max_U -= padding
  else:
    max_U = 0

  if max_D + padding < height:
    max_D += padding
  else:
    max_D = height - 1

  return M[max_U:max_D+1,max_L:max_R+1]

def get_cutpoints_kmeans(M):
  M = np.array(M)
  Mdas = np.array(M)

  # Converting picture to binary
  vf = np.vectorize(convert_to_binary)
  M = vf(M)

  M = np.sum(M,axis=0) # Summing every column of image_array
  M = (max(M) - min(M)) - (M - min(M)) # Normalize

  threshold = np.average(M) / 5

  space_list = []
  start_point = 0
  s_counter = 0
  s_bool = False

  for i in range(len(M)):
    if M[i] >= threshold:
      if s_bool:
        space_list.append((start_point,s_counter))
      start_point = i
      s_counter = 0
      s_bool = False
    else:
      s_counter += 1
      s_bool = True

  if (len(space_list) < 2 ):
    return get_cutpoints(Mdas)

  from sklearn.cluster import KMeans
  list1 = [x[1] for x in space_list]
  km = KMeans(n_clusters = 2, random_state=90).fit(np.array(list1).reshape(-1,1))
  klabels = km.labels_

  list_0 = [space_list[x[0]][1] // 2 for x in enumerate(klabels) if x[1] == 0]
  list_1 = [space_list[x[0]][1] // 2 for x in enumerate(klabels) if x[1] == 1]

  if len(list_0) < 1 or len(list_1) < 1 :
    return get_cutpoints(Mdas)

  avg_0 = sum(list_0)/len(list_0)
  avg_1 = sum(list_1)/len(list_1)

  t_label = 1
  if avg_0 > avg_1 :
    t_label = 0

  cutpoint_list = [space_list[x[0]][0] + space_list[x[0]][1] // 2 for x in enumerate(klabels) if x[1] == t_label]

  return cutpoint_list

# This function will return a list points, where each point in a separate space between words
def get_cutpoints(M):
  gamma = int(M.shape[0] / 3)

  M = np.array(M)

  # Converting picture to binary
  vf = np.vectorize(convert_to_binary)
  M = vf(M)

  M = np.sum(M,axis=0) # Summing every column of image_array
  M = (max(M) - min(M)) - (M - min(M)) # Normalize

  threshold = np.average(M) / 5

  cutpoint_list = []

  counter = 0

  for i in range(len(M)):
    if counter == gamma:
      cutpoint_list.append(i)
    if M[i] < threshold:
      counter += 1
    else:
      counter = 0

  return cutpoint_list

# This function will return the images of words given the image of sentence and cutpoints
def get_words_image(M,cutpoint_list):
  M = np.array(M)
  cutpoint_list = [0] + cutpoint_list + [M.shape[1]]
  word_images = []
  for x in range(len(cutpoint_list)-1):
    word_images.append(M[:,cutpoint_list[x]:cutpoint_list[x+1]])

  return word_images

# Library Imports

import numpy as np
import pandas as pd
from PIL import Image
import cv2


# Convert individual grayscale pixel to binary
convert_to_binary = lambda x: 0 if x<128 else 255

# Input : Location of an image of a sentence
# Output : List containing the locations of images of words
#
# Other Work Done :
# It saves the images of words in current working directory
# It also displays the image of sentence and images of words

def split_sentence(image_location):
  # Variables
  blur_amount_factor = 50

  # Opening image
  current_image = cv2.imread(image_location)

  # Converting it to greyscale
  current_image = cv2.cvtColor(current_image,cv2.COLOR_BGR2GRAY)

  # Saving height and width
  orig_height , orig_width = current_image.shape

  # Apply filter to remove noise
  blur_amount = orig_height // blur_amount_factor
  if blur_amount % 2 == 0 :
    blur_amount += 1
  current_image = cv2.medianBlur(current_image, blur_amount)

  # Remove extra spaces around sentence
  current_image = remove_space(current_image)

  # Getting cutpoints
  cutpoint_list = get_cutpoints_kmeans(current_image)

  # Getting images of words
  word_images = get_words_image(current_image, cutpoint_list)

  # Remove extra space around words
  word_images = [remove_space(x) for x in word_images]

  # Resizing every word image to make height equal to 50
  word_images = [cv2.resize(x, (int(x.shape[1]*(output_image_height/x.shape[0])),int(x.shape[0]*(output_image_height/x.shape[0]))), interpolation = cv2.INTER_NEAREST) for x in word_images]

  # Saving word images in current directory
  paths = []
  for i in range(len(word_images)):
      cv2.imwrite('w'+str(i+1)+'.png',word_images[i])
      paths.append('w'+str(i+1)+'.png')

  return paths


if __name__ == '__main__':
  import sys
  splitted_words = split_sentence(sys.argv[1])
  print(splitted_words)
