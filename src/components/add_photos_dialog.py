import time
from PIL import Image
import streamlit as st

@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance")

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(2)
    with t1:
        type_camera = ("primary" if st.session_state.photo_tab == "camera" else "tertiary") 

        if st.button("Camera",type=type_camera,width="stretch"):
            st.session_state.photo_tab = "camera"
    with t2:
        type_upload = ("primary" if st.session_state.photo_tab == "upload" else "tertiary")

        if st.button("Upload photos",type=type_upload,width="stretch"):
            st.session_state.photo_tab = "upload"

    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take Snapshot",key="dialog_cam")
        if cam_photo:
            img = Image.open(cam_photo).convert("RGB")

            if "last_camera_image" not in st.session_state or \
            st.session_state.last_camera_image != cam_photo.name:

                st.session_state.attendance_images.append(img)
                st.session_state.last_camera_image = cam_photo.name
            st.toast("Photo captured")

    if st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader(
            "Upload Your Files",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="upload_dialog"
        )

    st.divider()

    if st.button("Done", type="primary", width="stretch"):
        if st.session_state.photo_tab == "upload" and uploaded_files:
            existing_hashes = st.session_state.get("uploaded_hashes", set())
            for file in uploaded_files:
                file_bytes = file.getvalue()
                if file_bytes not in existing_hashes:
                    img = Image.open(file).convert("RGB")
                    st.session_state.attendance_images.append(img)
                    existing_hashes.add(file_bytes)

            st.session_state.uploaded_hashes = existing_hashes

        st.rerun()