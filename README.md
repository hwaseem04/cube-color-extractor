# Cube-color-extractor
Pet project to extract rubiks cube color using OpenCV. Working [demo]() in youtube.

## File structure and Overview
- `main.py` - This is the main file that reads video frames and detect cube faces. The following operations are performed in this file:
    - Opening the video frame and gray scaling it.
    - Edges are detected after gaussian blurring with canny edge detector.
    - For clear visibiity of edges, dilution and erosion are performed.
    - Bounding circles over 9 individual square pieces in the current face of the cube is detected and drawn.
    - After capturing 9 small squares in a face, a small cube is drawn at top of the output video frame upon pressing letter `e`.
    - Press letter `q` to quit the video frame. 
- `hsv_color_range` - This file contains hsv color range for each of the six colors in the cube. It also has function to detect color of a region based on its mean hsv values.
- `utilities` - This file holds all other additional utilities for manipulation.

## Dependencies
- Python 3.10 used.
- Main dependencies are listed [here](requirements1.txt).
- Enable conda/other python environment and install the dependencies

## How to use
- Show one face of the cube at a time in front of the camera.
- Press `e` to capture and draw its face colors.
- After capturing 6 faces, press `e` again to recapture from beginning.
- Press `q` to quit.
- For more clarity, watch this [demo]().

## Future directions
- Use the captured 6 faces to generate a 3D model of cube.
