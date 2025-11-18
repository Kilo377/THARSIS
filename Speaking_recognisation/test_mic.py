import sherpa_onnx
import sounddevice as sd
import numpy as np
import queue
import sys
import re

def main():
    # ==========================================
    # 1. 配置 SenseVoice 模型
    # ==========================================
    model_dir = "./models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17"
    
    # 为了界面更干净，我们把加载日志也简化一下
    print("-" * 50)
    print(f"正在加载模型 SenseVoice ...", end="", flush=True)

    try:
        recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
            model=f"{model_dir}/model.int8.onnx",
            tokens=f"{model_dir}/tokens.txt",
            num_threads=1,
            use_itn=True,
            decoding_method="greedy_search",
        )
        print(" [完成]")
    except Exception as e:
        print(f"\n❌ 模型加载失败: {e}")
        return

    # ==========================================
    # 2. 麦克风参数
    # ==========================================
    SAMPLE_RATE = 16000
    SILENCE_THRESHOLD = 0.03  # 灵敏度 (环境吵就调大，比如 0.05)
    PAUSE_LIMIT = 35          # 停顿判定 (约 0.8-1.0秒)
    
    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            pass # 忽略底层警告，保持界面干净
        audio_queue.put(indata.copy())

    print("-" * 50)
    print("  📝  听写已开始 (请说话，说完停顿即可上屏)")
    print("-" * 50)

    with sd.InputStream(channels=1, dtype="float32", samplerate=SAMPLE_RATE, callback=callback):
        buffer = []
        silent_frames = 0
        is_speaking = False
        
        while True:
            frame = audio_queue.get()
            volume = np.linalg.norm(frame) * 10
            
            # === 状态机逻辑 ===
            if volume > SILENCE_THRESHOLD:
                # 正在说话
                is_speaking = True
                silent_frames = 0
                buffer.append(frame)
                # [修改处]：去掉了这里的 print(".", ...)
                
            else:
                # 当前静音
                if is_speaking:
                    buffer.append(frame)
                    silent_frames += 1
                    
                    # 判定一句结束
                    if silent_frames > PAUSE_LIMIT: 
                        # 打印一个临时的状态，告诉用户正在算
                        # \r 可以让光标回到行首，避免换行
                        print("\r[正在识别...]", end="", flush=True)
                        
                        # 1. 识别
                        full_audio = np.concatenate(buffer)
                        stream = recognizer.create_stream()
                        stream.accept_waveform(SAMPLE_RATE, full_audio)
                        recognizer.decode_stream(stream)
                        
                        # 2. 获取文本
                        text = stream.result.text
                        text = re.sub(r'<\|.*?\|>', '', text).strip()
                        
                        # 清除 "[正在识别...]" 这行字 (用空格覆盖)
                        print("\r" + " " * 20 + "\r", end="", flush=True)
                        
                        if len(text) > 0:
                            # 3. 打印结果
                            print(f"> {text}")
                        
                        # 重置
                        buffer = []
                        is_speaking = False
                        silent_frames = 0
                else:
                    pass

if __name__ == "__main__":
    main()