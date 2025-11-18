# Offline Real-time Speech-to-Text (SenseVoice)
这是一个基于 Sherpa-onnx 和 SenseVoice 模型的离线语音识别项目。 它支持实时麦克风听写，具备以下特点：

完全离线：无需联网，数据安全。

中英混合：无需切换语言，支持中英文无缝混说。

自动标点：自动根据语气添加逗号、句号和问号。

高精度：基于阿里达摩院的 SenseVoiceSmall 模型。

1. 环境准备 (Environment Setup)
建议使用 Conda 创建一个干净的 Python 3.10 环境。

创建虚拟环境
Bash

# 创建名为 sensevoice 的环境
conda create -n sensevoice python=3.10

# 激活环境
conda activate sensevoice
安装依赖包
只需要安装推理引擎 sherpa-onnx 和音频处理库 sounddevice。

Bash

pip install sherpa-onnx sounddevice soundfile numpy
(注：如果是 Mac 用户，可能需要先运行 brew install portaudio 以支持麦克风调用)

2. 模型下载 (Model Download)
本项目使用 SenseVoiceSmall 多语言模型。请按照以下步骤下载并解压模型文件。

方式 A：命令行下载 (Mac/Linux)
在项目根目录下执行：

Bash

# 1. 创建存放模型的目录
mkdir -p models
cd models

# 2. 下载模型压缩包 (约 400MB)
curl -L -O https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2

# 3. 解压
tar xvf sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2

# 4. 删除压缩包 (可选)
rm sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2

# 5. 返回项目根目录
cd ..
方式 B：浏览器手动下载 (Windows/通用)
点击链接下载：sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2

在项目根目录下新建 models 文件夹。

将下载的文件解压到 models 文件夹中。

3. 目录结构 (Directory Structure)
安装完成后，您的项目目录应该长这样：

Plaintext

Project/
├── models/
│   └── sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/
│       ├── model.int8.onnx
│       └── tokens.txt
├── main.py            # 您的主程序脚本
└── README.md
4. 运行 (Usage)
确保麦克风已连接，直接运行 Python 脚本：

Bash

python main.py
使用说明：
程序启动后会显示 听写已开始。

说话：对着麦克风说话（中文、英文均可）。

停顿：说完一句话后，停顿约 0.8 秒。

上屏：程序会自动识别并打印带标点的文字。

5. 常见问题配置
如果识别效果不理想，可以在代码中调整以下参数：

无法检测到说话？

调低 SILENCE_THRESHOLD (例如改为 0.02)。

环境太吵，一直显示乱码？

调高 SILENCE_THRESHOLD (例如改为 0.1)。

说话慢，总被切断？

调大 PAUSE_LIMIT (例如改为 50)。