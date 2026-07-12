import dlib
import numpy as np
import face_recognition_models
import streamlit as st
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector,sp,facerec

def get_face_embeddings(image_np):
    detector,sp, facerec = load_dlib_models()
    faces = detector(image_np,1)

    encodings = []
    for face in faces:
        shape = sp(image_np,face)
        face_descriptor = facerec.compute_face_descriptor(image_np,shape,1) # 128 embeddings created

        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:

        embedding = student.get("face_embedding")

        if embedding:
            X.append(np.array(embedding))
            y.append(student["student_id"])

    if len(X) == 0:
        return None

    return {
        "X": X,
        "y": y
    }

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)

    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    THRESHOLD = 0.70

    for encoding in encodings:

        best_student = None
        best_distance = float("inf")

        for sid, stored_embedding in zip(y_train, X_train):

            stored_embedding = np.array(stored_embedding)

            distance = np.linalg.norm(stored_embedding - encoding)

            if distance < best_distance:
                best_distance = distance
                best_student = sid

        print(f"Best Match: {best_student}")
        print(f"Distance : {best_distance:.4f}")

        if best_distance <= THRESHOLD:
            detected_student[int(best_student)] = True

    return detected_student, all_students, len(encodings)