import sherpa_onnx
import soundfile as sf
import re

def format_time(seconds):
    minutes = int(seconds // 60)
    rem_seconds = seconds % 60
    return f"{minutes:02d}:{rem_seconds:06.3f}"

def main():
    # 1. 配置 SenseVoice 模型
    model_dir = "./models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17"
    print(f"正在加载 SenseVoice 模型: {model_dir} ...")

    try:
        recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
            model=f"{model_dir}/model.int8.onnx",
            tokens=f"{model_dir}/tokens.txt",
            num_threads=1,
            use_itn=True, # 启用逆文本标准化 (把"一二三"转为"123")
            decoding_method="greedy_search",
        )
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return

    # 2. 读取音频
    audio_file = "2/output.wav" 
    print(f"正在读取音频: {audio_file} ...")

    try:
        audio, sample_rate = sf.read(audio_file, dtype="float32")
    except Exception as e:
        print(f"无法读取音频: {e}")
        return

    if sample_rate != 16000:
        print("❌ 错误：采样率必须是 16000 Hz")
        return

    # 3. 识别
    print("正在识别 (支持中英混合 + 标点 + 情感)...")
    stream = recognizer.create_stream()
    stream.accept_waveform(sample_rate, audio)
    recognizer.decode_stream(stream)
    
    result = stream.result
    
    # SenseVoice 的 result.tokens 是正常的汉字/单词，且带有精确时间戳
    # 即使是英文，它也不会像 Zipformer 那样乱码
    
    tokens = result.tokens
    timestamps = result.timestamps

    if len(tokens) == 0:
        print("未识别到内容")
        return

    # 4. 智能断句 (基于标点符号)
    # SenseVoice 会自动输出标点 (，。？！)
    # 我们可以利用标点来完美切分时间轴
    
    sentences = []
    current_text = ""
    start_t = timestamps[0]
    
    # 定义标点符号集合
    punctuations = set(['，', '。', '？', '！', ',', '.', '?', '!'])

    for i, token in enumerate(tokens):
        t = timestamps[i]
        
        # 累加文本
        current_text += token
        
        # 如果当前字是标点，或者这是最后一个字，就切分一句
        if token in punctuations or i == len(tokens) - 1:
            # 记录这一句
            sentences.append({
                "start": start_t,
                "end": t, # 这一句结束于当前标点的时间
                "text": current_text.strip()
            })
            
            # 重置下一句
            current_text = ""
            # 下一句的开始时间是下一个 token 的时间 (如果存在)
            if i < len(tokens) - 1:
                start_t = timestamps[i+1]

    # 5. 打印结果
    print("\n" + "="*40)
    print(f"  SenseVoice 最终结果 (中英混合+标点)")
    print("="*40)
    
    for s in sentences:
        t_start = format_time(s['start'])
        t_end = format_time(s['end'])
        # 清理一下文本中的 HTML 标签 (SenseVoice 有时会输出情感标签如 <|HAPPY|>)
        clean_text = re.sub(r'<\|.*?\|>', '', s['text'])
        if clean_text.strip():
            print(f"[{t_start} --> {t_end}]  {clean_text}")

if __name__ == "__main__":
    main()