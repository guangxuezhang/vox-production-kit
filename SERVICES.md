# 统一服务配置

Windows 新设备先运行 `./bootstrap.ps1 -InstallMissing`：通过 winget 安装缺少的 Node、Python、FFmpeg，再安装 pnpm，进入 setup.ps1 安装工程依赖并调用 configure.py。系统安装可能出现 Windows 权限提示。已有环境也可单独运行 `python configure.py`。

配置提示：豆包 API Key、FriModel API Key、IMA Client ID、IMA API Key。IMA 不使用时可留空。凭据只保存在被 Git 忽略的 .private 中。按回车保留已有配置。

```powershell
python vox.py check
python vox.py image --prompt-file work/prompt.txt --output outputs/image.png --state-file outputs/image-state.json
python vox.py tts work/own-framework/narration-final.txt outputs/new-narration
python vox.py ima openapi/list_docs work/request.json
```

check 是本地检查，不代表接口鉴权已通过。image 和 tts 是付费生产操作，安装时不会执行。TTS 使用原速生成，后续由 build_final.py 保调变速与重排 cue。TTS 输出目录有独占标记，状态不明时不得重复请求。IMA 正文从 JSON 文件读取，入口仅支持读操作。

这里的 configure.py 替代旧 .env.example 配置说明。三个接口的执行代码均已随仓库交付，不依赖原电脑的绝对路径。bootstrap 负责 Windows 缺失软件安装，setup 负责工程依赖。Windows 新设备真实安装及付费接口验收尚未完成，不得宣称全部已验证。
