项目简介：
基于开源的语音转文字模型whisper，实现麦克风输入，实时语音转文字的功能。将文字作为输入传入百度大模型中，并返回输出结果。

环境配置参照：
https://gitcode.com/ufal/whisper_streaming/overview?utm_source=artical_gitcode&isLogin=1

改进方案：
1、原来的模型在声音很弱的时候会有乱码的情况发生（模型训练的问题）。对输出乱码的情况作了滤波处理，基本能解决该问题。
2、语音输入 5858|五八五八|58|五八|你好 作为开始提示语，谢谢 作为结束语，中间的字段作为大模型语音输入。

运行指令：
(whisperstream) yqh@yqh-ThinkStation-P520:~/yqh/llm_process/src/llm_asr$ python3 test_llm_asr.py --language zh --model_dir faster-whisper-medium --min-chunk-size 1 
(whisperstream) yqh@yqh-ThinkStation-P520:~/yqh/llm_process/src/llm_asr$ arecord -f S16_LE -c1 -r 16000 -t raw -D default | nc localhost 43099
(ysm) 离线测试 $ python3 whisper_online.py record_test.wav  --offline  --model medium  --model_dir faster -whisper-medium  --language zh   --min-chunk-size 4 > output.txt 
