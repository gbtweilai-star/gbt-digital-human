# digital_human · 视频域能力位

> **用途一句话**：数字人「以图生视频」

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
<img alt="capability" src="https://img.shields.io/badge/capability-322%20%2F%20341-orange">
</p>

这是 **GBT V8 的 341 个原生能力位中的第 322 个**（视频域 · `video`），
单独抽出来做成的独立仓库：可安装、可测试、零运行时依赖。

---

## 一、这一位是什么

> 数字人「以图生视频」（本地 SadTalker，零账号/零验证）：**一张照片 + 一段配音 ⇒ 带头部动作与口型同步的说话视频**。ops：status/probe 只读（引擎·权重·venv 缺件如实报）· capabilities 读边界 · render 写（异步出片回 task_id；写面自收窄在 outputs/dh-talk/ 与 state/digital_human/）· task/jobs 读任务账 · socket start/stop/status 把本能力包成 **OpenAI 兼容端点**（只监听回环），主脑用 omni_plug.ai_control（远端 https）或 _local_ai_call（回环）反向调用 —— **对面跑的是我们自己的权重，借的只是 CPU/GPU**，换远端只改 base_url。实测边界（2026-10-19）：成片画质上限由**取景**决定（脸在画面里越小口型越看不清 ⇒ 传头肩景，如 outputs/ref/face-tight.png）；本机纯 CPU 约 13.6 s/帧（14.8s 配音≈80 分钟），GPU 通常 1~2 分钟。

上面这句是**注册表原文**，逐字复制，没有改写。`tests/test_spec.py` 会把它钉死——
描述漂移会让测试失败，而不是悄悄发版。

---

## 二、用途：它解决什么问题

### 2.1 这一域在管什么

成片工程：拍摄与运动（actioncam）、剪辑（edit_pipeline / libtv_workflow）、调色与音轨（look_grade / audio_mix / audio_extract）、数字人与生成（digital_human / h3_video_gen）、以及版权与发布（media_license / media_stamp / media_publish）。

### 2.2 为什么这么设计

视频域所有能力位都遵循同一条约束：**产物必须落盘且可复算**。渲染参数、帧率、码率、时长都写进产物元数据，别人拿到文件能复现出同一个结果，而不是只有一张截图。

### 2.3 具体到 `digital_human`

**该用它的时候**：

- 你的任务可以概括为「数字人「以图生视频」」，并且
- 它不需要任何必填参数，可以直接调用，并且
- 你确认它是**可逆**动作（注册表 `safe: true`，不需要逐次授权）。

**不该用它的时候**：

- 你只是想要一个「大概能做这件事」的模糊入口 —— 这一位有明确契约，不是万能入口。
- 你需要它**替你做决定**。它执行，不做价值判断；要不要执行是调用方的事。
- 你希望它自带模型/密钥/机器。它不自带，见 4.5 节接后端。

---

## 三、安装

```bash
git clone https://github.com/gbtweilai-star/gbt-digital-human.git
cd gbt-digital-human
python -m pip install -e ".[dev]"
```

零运行时依赖，只有 `pytest` 是开发期依赖。

---

## 四、使用方式

### 4.1 看它是什么（人类可读）

```bash
python -m gbt_digital_human info
```

真实输出（本机捕获，非示意）：

```text
digital_human  (video)  v1.0.0
----------------------------------------
数字人「以图生视频」（本地 SadTalker，零账号/零验证）：**一张照片 + 一段配音 ⇒ 带头部动作与口型同步的说话视频**。ops：status/probe 只读（引擎·权重·venv 缺件如实报）· capabilities 读边界 · render 写（异步出片回 task_id；写面自收窄在 outputs/dh-talk/ 与 state/digital_human/）· task/jobs 读任务账 · socket start/stop/status 把本能力包成 **OpenAI 兼容端点**（只监听回环），主脑用 omni_plug.ai_control（远端 https）或 _local_ai_call（回环）反向调用 —— **对面跑的是我们自己的权重，借的只是 CPU/GPU**，换远端只改 base_url。实测边界（2026-10-19）：成片画质上限由**取景**决定（脸在画面里越小口型越看不清 ⇒ 传头肩景，如 outputs/ref/face-tight.png）；本机纯 CPU 约 13.6 s/帧（14.8s 配音≈80 分钟），GPU 通常 1~2 分钟。

gated      : False
external   : False
multi-op   : True
params     : (none)
values     : start, stop, status
```

### 4.2 看它的契约（机器可读）

```bash
python -m gbt_digital_human spec --json
```

输出是一个 JSON 对象，字段与注册表一一对应：`name` / `domain` / `desc` / `handler` /
`safe` / `gated` / `external` / `requires_params` / `params` / `params_hint` /
`multi_op` / `ops` / `ops_hint`。下游可以直接拿它做能力发现，不需要读文档。

### 4.3 只校验、不执行

```bash
python -m gbt_digital_human check --payload '{}'
```

`check` 永远不会抛异常，只返回「哪里不满足契约」。适合在花掉一次模型调用之前，
先把缺的参数摆给用户看。退出码：`0` 通过、`1` 契约不满足、`2` JSON 本身不合法。

### 4.4 执行

```bash
python -m gbt_digital_human run --payload '{}'
```

默认后端是 **stub**，所以你会拿到这样的信封：

```json
{
  "cap": "digital_human",
  "status": "validated",
  "backend": "stub",
  "data": { "executed": false, "reason": "no backend wired" },
  "note": "payload checked against the contract; nothing was executed."
}
```

注意 `status` 是 `"validated"` 而**不是** `"ok"`。这是刻意的：一个把 stub 报成成功的库，
会让调用方停止寻找真正的实现。`bool(result)` 对 stub 结果是 `False`。

### 4.5 接上你自己的后端

```python
from gbt_digital_human import SPEC, run

class MyBackend:
    name = "my-backend"

    def invoke(self, cap, payload):
        # 这里才是真实实现：调模型、调浏览器、调你的服务
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"      # 真实后端才会是 ok
print(result.as_dict())
```

也可以进程级注册一次，之后所有 `run()` 都走它：

```python
from gbt_digital_human.backend import register_backend
register_backend(MyBackend())
```

`Backend` 是一个 `Protocol`，只需要 `name` 属性和 `invoke(cap, payload) -> dict`。
不继承任何基类，你的实现不需要依赖本包。

### 4.6 作为库用

```python
from gbt_digital_human import SPEC, run
from gbt_digital_human.core import check

print(SPEC.name, SPEC.domain, SPEC.gated)

problems = check({})
if problems:
    for p in problems:
        print("缺:", p)
else:
    print(run({}).as_dict())
```

---

## 五、参数

| 参数 | 必填 | 说明 |
|---|---|---|
| — | 否 | 注册表未标注必填参数 |

> 注册表原话（`params_hint`）：（空）

**注册表登记的取值 / 子动作（3 个）**：`start`、`stop`、`status`


**为什么表里只有「必填/否」两档**：注册表只标注了哪些参数是必填的，没有标注类型与取值范围。
本包没有替它编造类型 —— 编造出来的类型比没有类型更危险，因为调用方会相信它。

---

## 六、返回值

`run()` 返回一个不可变的 `Result`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `cap` | `str` | 能力位名，恒等于 `digital_human` |
| `status` | `str` | `validated`（stub 校验通过）/ `ok`（真实后端执行）/ `error` |
| `backend` | `str` | 实际执行后端的 `name` |
| `data` | `dict` | 后端返回的原始字典 |
| `note` | `str` | 人类可读的补充说明（stub 会在这里说明自己没执行） |
| `elapsed_ms` | `float` | 后端耗时 |

`Result.as_dict()` 可直接 `json.dumps`。

---

## 七、边界与注意

- **多位一体**（注册表 `multi_op: true`）。同一个能力名下挂着多个子动作，调用前必须读清楚 `op` 的含义，否则「调对了能力、用错了动作」是最常见的误用。
- **本包不含真实实现**。这是刻意设计：真实实现依附于原运行时（模型、密钥、机器）。本包发布的是契约、校验、CLI 与类型接缝；接上你自己的 `Backend` 就能跑。

---

## 八、它不会做什么

- **不会假装执行成功**。默认 stub 的 `status` 是 `validated`，`executed` 是 `false`。
- **不会替你决定要不要执行**。授权是人的动作，不是库的动作。
- **不会编造参数类型**。注册表没写的，本包也不写。
- **不会静默吞掉错误**。后端抛异常就往上抛，返回非 dict 就报 `CapError`。
- **不会联网**。零运行时依赖，`run()` 只调用你给的后端。

---

## 九、测试

```bash
python -m pytest
```

真实输出：

```text
20 passed, 3 skipped in 0.11s
```

测试里有一条**漂移守卫**：`test_description_is_verbatim` 把 `SPEC.desc` 与注册表快照逐字比对。
描述被改了一个字，构建立刻失败。

---

## 十、出处与核对

| 项 | 值 |
|---|---|
| 能力位名 | `digital_human` |
| 域 | `video`（视频域，共 341 位 / 30 域中的一位） |
| 注册表 handler | `digital_human` |
| `safe` | `True` → gated = `False` |
| `external` | `False` |
| `multi_op` | `True` |
| 索引页 | [video/digital_human](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/video/digital_human.md) |
| 全量图谱 | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

**关于 341 这个数**：父仓 README 写的是 348，但按 AST 解析注册表实际可枚举的是
`341 个能力位 + 0 个未实现 + 0 个已禁用 = 341`。差出来的 7 个是历史重名/已合并条目。
本仓库按 341 编号，编号与 `gbt-caps` 的索引一致，可逐条核对。

---

## License

MIT。见 [LICENSE](LICENSE)。
