import os

import cv2


def object_movement(ID):
    """
    :param ID: ID of the object that is being moved
    """
    load_reference_images(ID)
    pass


def load_reference_images(ID):
    """
    Retrieve the images of the object that is being moved
    :param ID: ID of the object that is being moved
    """

    # Create an empty list to store the images
    images = []
    # Get the absolute path of the folder
    folder_path = os.path.dirname(os.path.abspath(__file__)) + "/objects/" + ID + "/"
    for filename in os.listdir(folder_path):
        img = cv2.imread(os.path.join(folder_path, filename))
        if img is not None:
            images.append(img)

    return images


def feature_matching(image):
    # Scale Invariant Feature Transform (SIFT): extract keypoints and compute its descriptors
    pass


"""
Request the data from unity and analyze scene
"""
if __name__ == '__main__':
    object_movement("01")
