# Offline Real-time Speech-to-Text (SenseVoice)

基于 Sherpa-onnx 和 SenseVoice 的离线中英混合语音识。支持实时麦克风听写、自动标点和高精度识别。

1. 运行环境 (Requirements)

本项目需要 Python 3.10+。请直接安装以下依赖库：

```pip install sherpa-onnx sounddevice soundfile numpy```


(注：Mac 用户如果遇到麦克风报错，可能需要运行 brew install portaudio)

2. 模型下载 (Model Setup)

请在项目根目录下运行以下命令，下载并解压 SenseVoice 模型（约 400MB）：

# 创建目录并下载
```
mkdir -p models
cd models
curl -L -O [https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2](https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2)

# 解压并清理
tar xvf sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2
rm sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2
cd ..
```

最终文件结构确认：
```
Project/
├── models/
│   └── sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/
│       ├── model.int8.onnx
│       └── tokens.txt
├── main.py
└── README.md
```

3. 运行 (Usage)

确保麦克风连接正常，运行脚本：
```
python main.py
```

操作指南：

程序启动后显示 听写已开始。

说话：支持中英文混说。

上屏：说完一句话后停顿约 1 秒，文字即会自动识别上屏。

4. 参数配置 (Configuration)

在 main.py 中可根据环境微调：

SILENCE_THRESHOLD: 静音阈值。环境吵杂请调大（如 0.1），环境安静可调小（如 0.02）。

PAUSE_LIMIT: 停顿判定时间。默认 35 (约0.8秒)。说话慢容易被切断请调大此值。