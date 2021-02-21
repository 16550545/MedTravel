# Flask imports
from flask import render_template, request, Response
from . import main
from ..models import User
from .utils import *

# Face swapping imports
import cv2
import numpy as np
import dlib
import time
from pathlib import Path

cwd = Path.cwd()

cap = cv2.VideoCapture(0)
time.sleep(2.0)

def extract_index_nparray(nparray):
    index = None
    for num in nparray[0]:
        index = num
        break
    return index

def gen(value):
    global ran
    # This range represents the facial landmarks of the mouth
    ran = range(48,68)
    # Teeth whitening
    if  value == "1":
        img = cv2.imread(str(cwd) + "/app/main/res/img/smile_male.jpg")
    # This one is a simple smile
    elif value == "2":
        img = cv2.imread(str(cwd) + "/app/main/res/img/new_smile.jpg")
    # This is braces
    elif value == "3":
        img = cv2.imread(str(cwd) + "/app/main/res/img/braces_female_6.jpg")
    # Else, swap for a smile
    else:
        img = cv2.imread(str(cwd) + "/app/main/res/img/smile_male.jpg")


    landmarks_points2 = []
    #FIXED: used cwd to calculate rel path
    # cv2.imshow('image', img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(img_gray)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(str(cwd) + "/app/main/res/shape_predictor_68_face_landmarks.dat")

    indexes_triangles = []

    # Face 1
    faces = detector(img_gray)
    for face in faces:
        landmarks = predictor(img_gray, face)
        landmarks_points = []

        for n in ran:
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmarks_points.append((x, y))

            # cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

        points = np.array(landmarks_points, np.int32)
        convexhull = cv2.convexHull(points)
        # cv2.polylines(img, [convexhull], True, (255, 0, 0), 3)
        cv2.fillConvexPoly(mask, convexhull, 255)

        # Delaunay triangulation
        rect = cv2.boundingRect(convexhull)
        subdiv = cv2.Subdiv2D(rect)
        subdiv.insert(landmarks_points)
        triangles = subdiv.getTriangleList()
        triangles = np.array(triangles, dtype=np.int32)

        indexes_triangles = []
        for t in triangles:
            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])

            index_pt1 = np.where((points == pt1).all(axis=1))
            index_pt1 = extract_index_nparray(index_pt1)

            index_pt2 = np.where((points == pt2).all(axis=1))
            index_pt2 = extract_index_nparray(index_pt2)

            index_pt3 = np.where((points == pt3).all(axis=1))
            index_pt3 = extract_index_nparray(index_pt3)

            if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
                triangle = [index_pt1, index_pt2, index_pt3]
                indexes_triangles.append(triangle)

    while True:
        _, img2 = cap.read()
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        img2_new_face = np.zeros_like(img2)

        # Face 2
        faces2 = detector(img2_gray)
        for face in faces2:
            landmarks = predictor(img2_gray, face)
            landmarks_points2 = []
            for n in ran:
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                landmarks_points2.append((x, y))

            # cv2.circle(img2, (x, y), 3, (0, 255, 0), -1)
            points2 = np.array(landmarks_points2, np.int32)
            convexhull2 = cv2.convexHull(points2)

        # Triangulation of both faces
        for triangle_index in indexes_triangles:
            # Triangulation of the first face
            tr1_pt1 = landmarks_points[triangle_index[0]]
            tr1_pt2 = landmarks_points[triangle_index[1]]
            tr1_pt3 = landmarks_points[triangle_index[2]]
            triangle1 = np.array([tr1_pt1, tr1_pt2, tr1_pt3], np.int32)

            rect1 = cv2.boundingRect(triangle1)
            (x, y, w, h) = rect1
            cropped_triangle = img[y: y + h, x: x + w]
            cropped_tr1_mask = np.zeros((h, w), np.uint8)

            points = np.array([[tr1_pt1[0] - x, tr1_pt1[1] - y],
                            [tr1_pt2[0] - x, tr1_pt2[1] - y],
                            [tr1_pt3[0] - x, tr1_pt3[1] - y]], np.int32)

            cv2.fillConvexPoly(cropped_tr1_mask, points, 255)

            # Triangulation of second face
            tr2_pt1 = landmarks_points2[triangle_index[0]]
            tr2_pt2 = landmarks_points2[triangle_index[1]]
            tr2_pt3 = landmarks_points2[triangle_index[2]]
            triangle2 = np.array([tr2_pt1, tr2_pt2, tr2_pt3], np.int32)

            rect2 = cv2.boundingRect(triangle2)
            (x, y, w, h) = rect2

            cropped_tr2_mask = np.zeros((h, w), np.uint8)

            points2 = np.array([[tr2_pt1[0] - x, tr2_pt1[1] - y],
                                [tr2_pt2[0] - x, tr2_pt2[1] - y],
                                [tr2_pt3[0] - x, tr2_pt3[1] - y]], np.int32)

            cv2.fillConvexPoly(cropped_tr2_mask, points2, 255)



            # Warp triangles
            points = np.float32(points)
            points2 = np.float32(points2)
            M = cv2.getAffineTransform(points, points2)
            warped_triangle = cv2.warpAffine(cropped_triangle, M, (w, h))
            warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=cropped_tr2_mask)


            # Reconstructing destination face
            img2_new_face_rect_area = img2_new_face[y: y + h, x: x + w]
            img2_new_face_rect_area_gray = cv2.cvtColor(img2_new_face_rect_area, cv2.COLOR_BGR2GRAY)
            _, mask_triangles_designed = cv2.threshold(img2_new_face_rect_area_gray, 1, 255, cv2.THRESH_BINARY_INV)
            warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=mask_triangles_designed)

            img2_new_face_rect_area = cv2.add(img2_new_face_rect_area, warped_triangle)
            img2_new_face[y: y + h, x: x + w] = img2_new_face_rect_area


        # Face swapped (putting 1st face into 2nd face)
        img2_face_mask = np.zeros_like(img2_gray)
        img2_head_mask = cv2.fillConvexPoly(img2_face_mask, convexhull2, 255)
        img2_face_mask = cv2.bitwise_not(img2_head_mask)


        img2_head_noface = cv2.bitwise_and(img2, img2, mask=img2_face_mask)
        result = cv2.add(img2_head_noface, img2_new_face)

        (x, y, w, h) = cv2.boundingRect(convexhull2)
        center_face2 = (int((x + x + w) / 2), int((y + y + h) / 2))

        seamlessclone = cv2.seamlessClone(result, img2, img2_head_mask, center_face2, cv2.MIXED_CLONE)

        key = cv2.waitKey(1)
        if key == 27:
            break

        cv2.imwrite('pic.jpg', seamlessclone)
        # This might be a problem, no matter the scale of the app
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')

    cap.release()


@main.route('/', methods = ['GET'])
def index():
    global option
    """Video streaming"""
    if request.method == 'GET':
        # Get the selected option via query params
        option = request.args.get('value')
        return render_template('index.html', option=option)
    else:
        return render_template('index.html')

@main.route('/email', methods=['POST'])
def email():
    pname = request.form['name']
    plastname = request.form['lastname']
    pemail = request.form['email']
    pphone = request.form['phone']
    pprocedure = request.form['procedure']

    sbj = 'Nueva Solicitud: '+ pname + ' ' +plastname
    cnt =  'Hola soy '+pname+' '+plastname+' me gustaría saber mas sobre el procedimiento: '+pprocedure+'<br>Esta es mi información: <br><strong>Correo: </strong>'+pemail+'<br><strong>Telefono: </strong>'+pphone

    send_email(sbj, cnt)

    return ('Your message has been sent. Thank you!')


@main.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # Pass the option to the main function to change images based on the value
    return Response(gen(option),
                mimetype='multipart/x-mixed-replace; boundary=frame')
