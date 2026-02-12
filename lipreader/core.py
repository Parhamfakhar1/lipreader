import cv2
import numpy as np
import json
import os

class LipReader:
    def __init__(self, data_path="lip_data.json"):
        self.data_path = data_path
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load Haar Cascade classifier.")

    def extract_lip_ratio(self, frame, x, y, w, h):
        face_roi = frame[y:y + h, x:x + w]
        if face_roi.size == 0:
            return None
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 100:
                x_l, y_l, w_l, h_l = cv2.boundingRect(largest)
                return w_l / (h_l + 1e-6)
        return None

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")
        ratios = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) > 0:
                x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
                ratio = self.extract_lip_ratio(frame, x, y, w, h)
                if ratio is not None:
                    ratios.append(ratio)
        cap.release()
        if not ratios:
            raise ValueError("No lip region detected in video.")
        return {
            "avg_ratio": float(np.mean(ratios)),
            "ratio_std": float(np.std(ratios)),
            "min_ratio": float(np.min(ratios)),
            "max_ratio": float(np.max(ratios)),
            "frame_count": len(ratios)
        }

    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_data(self, data):
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def train(self, video_path, word):
        stats = self.process_video(video_path)
        stats["video"] = os.path.basename(video_path)
        data = self.load_data()
        if word not in data:
            data[word] = {"samples": [stats]}
        else:
            data[word]["samples"].append(stats)
        self.save_data(data)
        return stats

    def predict(self, video_path):
        test_stats = self.process_video(video_path)
        data = self.load_data()
        if not data:
            raise ValueError("No trained words found. Train first with `.train()`.")

        def similarity(test_avg, test_std, sample):
            dist = abs(test_avg - sample["avg_ratio"])
            std_diff = abs(test_std - sample["ratio_std"])
            return max(0, 1.0 - (dist / 2.0) - (std_diff / 1.0))

        scores = {}
        for word, word_data in data.items():
            score = np.mean([
                similarity(test_stats["avg_ratio"], test_stats["ratio_std"], s)
                for s in word_data["samples"]
            ])
            scores[word] = score

        total = sum(scores.values())
        if total == 0:
            return None, {}
        probabilities = {w: (s / total) * 100 for w, s in scores.items()}
        prediction = max(probabilities, key=probabilities.get)
        return prediction, probabilities