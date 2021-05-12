import time
import tensorflow as tf
from detectors.cell_detection.centroidtracker import CentroidTracker
import numpy as np
import cv2


class Detector:
    def __init__(self, threshold):
        self.model = None
        self.ct = None
        self.threshold = threshold

    def init_detector(self):
        self.model = load_model()
        self.ct = CentroidTracker(maxDisappeared=3)

    def detect(self, img):

        (H, W) = img.shape[:2]
        image_np = np.array(img)
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image_np)

        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # input_tensor = np.expand_dims(image_np, 0)
        detections = self.model(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        rects = []
        for (ymin, xmin, ymax, xmax), score in zip(detections['detection_boxes'], detections['detection_scores']):
            if score > self.threshold:
                rects += [(xmin, ymin, xmax, ymax) * np.array([W, H, W, H])]
                left, right, top, bottom = get_bounding_boxes(img, ymin, xmin, ymax, xmax)
                cv2.rectangle(img, (int(left), int(bottom)), (int(right), int(top)), (255, 0, 0), 1)

        objects, rects = self.ct.update(rects)

        # loop over the tracked objects
        for (objectID, centroid) in objects.items():
            # draw both the ID of the object and the centroid of the
            # object on the output frame
            text = "{}".format(objectID)
            cv2.putText(img, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 255), 1)
            cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        return img



# Saved model path
PATH_TO_SAVED_MODEL = r'C:\Users\viktor_koukouliev\models\research\cell_detector_igraph/saved_model'

# CLIPS_TO_DETECT_PATH = 'clips'
# DETECTED_CLIPS_PATH = 'detected_clips'
# IMAGE_PATH = os.path.join('image', 'example.tif')


def get_bounding_boxes(image,
                           ymin,
                           xmin,
                           ymax,
                           xmax):
  im_height, im_width, _ = image.shape
  return (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)


def load_model():
    print('Loading model...', end='')
    start_time = time.time()

    # Load saved model and build the detection function
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done! Took {} seconds'.format(elapsed_time))

    return detect_fn


def image_to_8bit_equalized(image):
    ratio = np.amax(image) / 256
    img8 = (image / ratio).astype('uint8')

    return img8


# flags = tf.compat.v1.flags
# flags.DEFINE_integer('x_cord', None, 'X coordinate', required=True)
# flags.DEFINE_integer('y_cord', None, 'Y coordinate', required=True)
# flags.DEFINE_integer('offset', None, 'Offset from the point', required=True)
# flags.DEFINE_integer('frame_start', None, 'Frame to start from', required=True)
# FLAGS = flags.FLAGS

# ct = CentroidTracker(maxDisappeared=3)
# (H, W) = (None, None)
#
# if not os.path.exists(DETECTED_CLIPS_PATH):
#     os.makedirs(DETECTED_CLIPS_PATH)
#
# img = io.imread(IMAGE_PATH)
# print(img.shape)
# detect_fn = load_model()
#
# for frame_num, image in enumerate(img[FLAGS.frame_start:]):
#     frame = image_to_8bit_equalized(np.dstack((np.zeros((len(image[0]), len(image[0][0]))), image[1], image[0])))
#
#     x = FLAGS.x_cord
#     y = FLAGS.y_cord
#     offset = FLAGS.offset
#
#     (H, W) = frame.shape[:2]
#
#     if x-offset < 0 or y-offset < 0 or x+offset > W or y+offset > H:
#         print('Coordinates or offset out of bounds')
#         break
#
#     frame = frame[x-offset:x+offset, y-offset:y+offset]
#     (H, W) = frame.shape[:2]
#
#     image_np = np.array(frame)
#
#     # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
#     input_tensor = tf.convert_to_tensor(image_np)
#
#     # The model expects a batch of images, so add an axis with `tf.newaxis`.
#     input_tensor = input_tensor[tf.newaxis, ...]
#
#     # input_tensor = np.expand_dims(image_np, 0)
#     detections = detect_fn(input_tensor)
#
#     num_detections = int(detections.pop('num_detections'))
#     detections = {key: value[0, :num_detections].numpy()
#                   for key, value in detections.items()}
#     detections['num_detections'] = num_detections
#
#     # detection_classes should be ints.
#     detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
#
#     rects = []
#     for (ymin, xmin, ymax, xmax), score in zip(detections['detection_boxes'], detections['detection_scores']):
#         if score > 0.10:
#             rects += [(xmin, ymin, xmax, ymax) * np.array([W, H, W, H])]
#             left, right, top, bottom = get_bounding_boxes(frame, ymin, xmin, ymax, xmax)
#             cv2.rectangle(frame, (int(left), int(bottom)), (int(right), int(top)), (0, 0, 255), 1)
#
#     objects = ct.update(rects)
#
#     # loop over the tracked objects
#     for (objectID, centroid) in objects.items():
#         # draw both the ID of the object and the centroid of the
#         # object on the output frame
#         text = "{}".format(objectID)
#         cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 2)
#         cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
#
#     # show the output frame
#     cv2.imshow("Frame", frame)
#     key = cv2.waitKey(1) & 0xFF
#
#     # if the `q` key was pressed, break from the loop
#     if key == ord("q"):
#         break


def create_category_index(categories):
  """Creates dictionary of COCO compatible categories keyed by category id.

  Args:
    categories: a list of dicts, each of which has the following keys:
      'id': (required) an integer id uniquely identifying this category.
      'name': (required) string representing category name
        e.g., 'cat', 'dog', 'pizza'.

  Returns:
    category_index: a dict containing the same entries as categories, but keyed
      by the 'id' field of each category.
  """
  category_index = {}
  for cat in categories:
    category_index[cat['id']] = cat
  return category_index