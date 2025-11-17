import cv2
import os
import base64
import requests
from pathlib import Path
'''
这个项目暂时用已有视频抽帧
'''

VIDEO_PATH = "/Users/kilobao/Desktop/GSA/Monitor/calibration_videos/human_behavior.mp4"
OUTPUT_DIR = "frames"
INTERVAL_SEC = 2.0  # 每 2 秒抽取一帧


# -----------------------------
#  抽帧（按时间间隔）
# -----------------------------
def extract_frames(video_path, out_dir, interval_sec=2.0):
    os.makedirs(out_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_interval = int(fps * interval_sec)
    timestamps = []

    frame_id = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % frame_interval == 0:
            out_path = f"{out_dir}/frame_{saved:04d}.jpg"
            cv2.imwrite(out_path, frame)

            time_sec = frame_id / fps
            timestamps.append((out_path, time_sec))
            saved += 1

        frame_id += 1

    cap.release()
    return timestamps


# -----------------------------
#  调用 Ollama 的 Qwen3-VL:30B
# -----------------------------
def qwen_vl_infer(image_path):
    url = "http://localhost:11434/api/generate"

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    prompt = (
        "请描述图片中的人物正在做什么行为，用一句自然语言回答。"
        "同时给一个能代表该行为的 emoji（仅一个）。"
        "格式：描述: xxx, Emoji: 😄"
    )

    payload = {
        "model": "qwen3-vl:30b",
        "prompt": prompt,
        "images": [img_b64],
        "stream": False,
        "options": {"temperature": 0.2}
    }

    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json().get("response", "")


# -----------------------------
#  主流程
# -----------------------------
def main():
    print("[1] 抽取视频帧…")
    timestamps = extract_frames(VIDEO_PATH, OUTPUT_DIR, INTERVAL_SEC)
    print(f"已抽取 {len(timestamps)} 帧")

    print("\n[2] Qwen3-VL 推理开始…\n")

    for frame_path, ts in timestamps:
        print(f"时间 {ts:.1f}s, 帧 {Path(frame_path).name}")
        out = qwen_vl_infer(frame_path)
        print(out)
        print("-" * 40)


if __name__ == "__main__":
    main()
