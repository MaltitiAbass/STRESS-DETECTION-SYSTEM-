import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from web_functions import predict

# Load the trained model for real-time detection
model = tf.keras.models.load_model('stress_detection_model.h5')

def preprocess_image(image):
    """Preprocess the image for model input."""
    resized_image = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)  # Resize to 64x64
    normalized_image = resized_image / 255.0
    return normalized_image.reshape(1, 64, 64, 3)  # Reshape to (1, 64, 64, 3)

def preprocess_frame(frame):
    """Preprocess the frame for model input."""
    resized_frame = cv2.resize(frame, (64, 64), interpolation=cv2.INTER_AREA)  # Resize to 64x64
    normalized_frame = resized_frame / 255.0
    return normalized_frame.reshape(1, 64, 64, 3)  # Reshape to (1, 64, 64, 3)

def predict_class(features):
    """Predict function for image input."""
    prediction = model.predict(features)
    predicted_class = (prediction > 0.5).astype("int32")[0][0]
    return predicted_class

def app(df, X, y):
    """Create the prediction page"""

    st.title("Acquah StressPredict")

    st.markdown(
        """
            <p style="font-size:25px">
    This app uses <b style="color:green">three methods for stress analysis</b>: <b style="color:blue">manual input</b>, <b style="color:orange">uploaded images</b>, and <b style="color:red">real-time video capturing</b> to predict stress.
</p>
        """, unsafe_allow_html=True)
    
    mode = st.selectbox("Choose input mode", ["Manual Input", "Upload Picture", "Real-Time Capturing"])

    if mode == "Manual Input":
        st.subheader("Manual Input for Stress Detection")

        st.markdown(
            """
            <p style="font-size:18px">
                This input uses <b style="color:green">Decision Tree Classifier</b> for the prediction of stress.
            </p>
            """, unsafe_allow_html=True)

        # Manual input sliders
        features = {
            "Snoring Rate (snoring events per hour)": st.slider("Snoring Rate (snoring events per hour)", 0, 100, value=45),
            "Respiration Rate (breaths per minute)": st.slider("Respiration Rate (breaths per minute)", 12, 30, value=16),
            "Body Temperature (in °F)": st.slider("Body Temperature (in °F)", 95, 100, value=98),
            "Limb Movement (number of movements per hour)": st.slider("Limb Movement (number of movements per hour)", 0, 30, value=10),
            "Blood Oxygen Saturation (%)": st.slider("Blood Oxygen Saturation (%)", 80, 100, value=95),
            "Rapid Eye Movement (minutes per hour)": st.slider("Rapid Eye Movement (minutes per hour)", 0, 60, value=20),
            "Sleeping Hours (hours)": st.slider("Sleeping Hours (hours)", 0, 12, value=7),
            "Heart Rate (beats per minute)": st.slider("Heart Rate (beats per minute)", 50, 100, value=70)
        }

        st.write("### Feature Summary")
        st.table(features)  # Display features in a table

        if st.button("Predict"):
            # Get prediction and model score
            prediction, score = predict(X, y, list(features.values()))
            if prediction == 0:
                st.success("No stress detected 🙂")
            else:
                st.warning("Stress detected 😐")
            st.write(f"The model has an accuracy of {score * 100:.2f}%")

    elif mode == "Upload Picture":
        st.subheader("Upload Picture for Stress Detection")

        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Resize the image to a more appropriate size for display
            st.image(cv2.resize(image_rgb, (400, 400)), caption='Uploaded Image', use_column_width=False)

            features = preprocess_image(image_rgb)
            predicted_class = predict_class(features)

            if predicted_class == 0:
                st.success("No stress detected 🙂")
            else:
                st.warning("Stress detected 😐")

    elif mode == "Real-Time Capturing":
        st.subheader("Real-Time Capturing")

        if 'run' not in st.session_state:
            st.session_state.run = False

        if 'last_prediction' not in st.session_state:
            st.session_state.last_prediction = None

        run_button = st.button('Start/Stop')

        if run_button:
            st.session_state.run = not st.session_state.run

        FRAME_WINDOW = st.image([])
        camera = cv2.VideoCapture(0)

        while st.session_state.run:
            ret, frame = camera.read()
            if not ret:
                st.error("Failed to grab frame")
                break

            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                # Face detected, perform prediction
                features = preprocess_frame(frame)
                predicted_class = predict_class(features)

                if predicted_class == 1:
                    text = "********** Stress detected **********"
                    color = (0, 0, 255)  # Red
                    cv2.putText(frame_rgb, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
            else:
                # No face detected, do not update detection
                pass

            FRAME_WINDOW.image(frame_rgb)
            st.session_state.last_prediction = predicted_class if len(faces) > 0 else None

        camera.release()

    if 'camera' in locals():
        camera.release()
