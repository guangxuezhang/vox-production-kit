# VOX Production Kit

最新安装与统一接口请先读 [SERVICES.md](SERVICES.md)。运行 `./bootstrap.ps1 -InstallMissing` 安装缺失环境并进入凭据配置。该入口替代下文旧版依赖外部服务 Skill 和 .env 的说明；三个接口执行脚本现已在 services 与 work 中随仓库交付。IMA 需要 Client ID 和 API Key。

已跑通的 VOX 工程源码与示例素材。包含真实 Remotion 4.0.523 + React 19.1.0 工程、原有逐镜动画、透明 PNG、背景、旁白、字幕时间线、Alpha 分离脚本、豆包请求脚本、音效引擎及 QA 脚本。

## 首次使用（Windows）

预先安装 Node.js、pnpm、Python 3.11 或 3.12、FFmpeg（含 ffprobe），并使其可从终端调用。

```powershell
./setup.ps1
pnpm --dir remotion dev
pnpm --dir remotion render
```

渲染输出：`outputs/own-framework/own-framework-finished-v2.mp4`。示例使用已有素材，无须调用付费 API。首次 Remotion 渲染可能下载浏览器。中文字体默认 Microsoft YaHei；其他系统请安装可用中文字体并修改字体声明。安装脚本目前面向 Windows，不能宣称已在所有设备测试。

## 已确认的制作方法

用户决定选题与来源 → 确认文案及按语义划分的镜头 → 男声旁白保调变速及最终时间戳 → 每镜参考图 → 每 3–5 件元素一张透明集合图及一张干净背景 → Alpha 分离与轮廓验收 → Create Storyboard 按词句编排的动作表 → 导演动作表校验 → Remotion 按表实现与渲染 → 按语义植入音效 → 观看、抽帧和技术验收。

背景固定；素材错峰进入后停稳，优先避免重叠，人物高于其他视觉素材，字幕独立顶层。每一步告知用户下一步并等待确认，除非用户授权整段自动推进。时长和镜头数由当次内容决定。

新选题必须先生成 `episode-plan.json`，按 `skills/vox-production/references/director-plan.md` 填写每件素材的旁白 cue、动作意义、入场/落点与镜间交接。用 `node scripts/render_episode.cjs <episode-plan.json> <composition-id> <output.mp4>` 渲染；缺动作表或校验失败时不会进入 Remotion。上方的 `pnpm --dir remotion render` 只复现仓库自带的旧示例。

## 包内脚本

- `work/own-framework/split_alpha.py`：读取 outputs/own-framework/shot??-assets-?.png，将 Alpha 连通素材分离到 remotion/public/cutouts。
- `work/own-framework/build_final.py`：已确认示例文案的逐字 cue 编译器与 1.3 倍变速。内含本集 8 镜排布，新选题必须重写动作表和对应编译数据，不能直接替换文字后套用。
- `work/own-framework/doubao_tts_corrected.mjs`：豆包旁白请求，接受本机 key 文件、输出项目目录、音色 ID、输出名称、语速参数、文案文件。不会自动读取 .env。默认使用明确传入的已确认男声 ID `zh_male_liufei_uranus_bigtts`。
- `work/own-framework/qa_final.py`：成片解码及抽帧报告；参数为输出文件名。
- `work/own-framework/qa_motion.py`：本集人物入场变化及固定背景角落检查。技术检查不能代替观看验收。
- `audio/render_soundscape.mjs`：确定性音效生成，命令如下。

```powershell
node audio/render_soundscape.mjs --config work/own-framework/sound-cues.json --output outputs/own-framework/soundscape.wav
python work/own-framework/qa_final.py own-framework-finished-v2.mp4
```

示例 Remotion 源码保留原有 paper-swish 音效；sound-cues.json 是后续已接受的 75.8 秒音效版本。为不同配音或重新渲染版本混音前必须核对时长，不要直接混入不匹配的音效轨。

## Skill 与服务配置

Skill 入口：skills/vox-production/SKILL.md。安装后首次调用应从 https://github.com/guangxuezhang/vox-production-kit.git 下载工程并运行 setup.ps1。

新片所需服务：豆包、外置生图，使用 IMA 来源时再配置 IMA。`.env.example` 仅是配置清单，不是已完成的统一 API 适配器。外置生图与 IMA 应接入设备上对应的 external-image-channel 与 ima-skill；仅填写三个 Key 并不能替代安装相应接口脚本、配置模型/地址及知识库权限。不要把密钥提交到仓库。

镜头设计使用 create-storyboard，动画实现使用 remotion-best-practices。仓库未复制这两个第三方 Skill；需在目标设备安装。已接受示例可直接渲染，新选题的自动生产仍需要这些 Skill 和服务接入。

## 验证边界

本仓库用于复用真实实现和示例，不保证新生成图片逐像素相同。已有素材决定画面复现，字体、音色权限和服务模型会影响跨设备结果。交付前检查画面、完整轮廓、背景静止、错峰动作、人物层级、字幕同步及真实音色听感。
