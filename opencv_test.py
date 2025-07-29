import cv2
import os
import pickle
import face_recognition
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("人脸识别系统")

        # 创建按钮
        self.register_btn = tk.Button(root, text="录入人脸", command=self.register_face)
        self.register_btn.pack(pady=10)

        self.recognize_btn = tk.Button(root, text="人脸识别", command=self.recognize_face)
        self.recognize_btn.pack(pady=10)

        # 创建标签显示摄像头画面
        self.label = tk.Label(root)
        self.label.pack()

        # 初始化变量
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        if os.path.exists("faces.dat"):
            with open("faces.dat", "rb") as f:
                self.known_face_encodings, self.known_face_names = pickle.load(f)

    def save_known_faces(self):
        with open("faces.dat", "wb") as f:
            pickle.dump((self.known_face_encodings, self.known_face_names), f)

    def register_face(self):
        name = tk.simpledialog.askstring("输入", "请输入姓名:")
        if name:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if ret:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    face_locations = face_recognition.face_locations(rgb_frame)

                    if face_locations:
                        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                        self.known_face_encodings.append(face_encoding)
                        self.known_face_names.append(name)
                        self.save_known_faces()

                        # 保存照片
                        if not os.path.exists("faces"):
                            os.makedirs("faces")
                        cv2.imwrite(f"faces/{name}.jpg", frame)
                        messagebox.showinfo("成功", f"{name}的人脸已录入!")
                        break

                    # 显示摄像头画面
                    img = Image.fromarray(rgb_frame)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.label.imgtk = imgtk
                    self.label.configure(image=imgtk)
                    self.root.update()

            cap.release()

    def recognize_face(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)

                if face_locations:
                    face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "未知"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_face_names[first_match_index]

                    # 在画面上显示名字
                    cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # 显示摄像头画面
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
                self.root.update()

                # 按q退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
