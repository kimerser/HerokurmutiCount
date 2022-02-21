from flask import Flask
import cv2

app = Flask(__name__)
@app.route("/")
def index():
    print(cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml"))
    return "Hello MyProJect RMUTI!"

if __name__ == "__main__":
    app.run()
