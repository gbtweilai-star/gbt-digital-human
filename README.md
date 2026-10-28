# digital_human

**One capability bit from GBT V8, packaged standalone.** No. 322 of 341,
`video` domain (Video).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> 数字人「以图生视频」（本地 SadTalker，零账号/零验证）：**一张照片 + 一段配音 ⇒ 带头部动作与口型同步的说话视频**。ops：status/probe 只读（引擎·权重·venv 缺件如实报）· capabilities 读边界 · render 写（异步出片回 task_id；写面自收窄在 outputs/dh-talk/ 与 state/digital_human/）· task/jobs 读任务账 · socket start/stop/status 把本能力包成 **OpenAI 兼容端点**（只监听回环），主脑用 omni_plug.ai_control（远端 https）或 _local_ai_call（回环）反向调用 —— **对面跑的是我们自己的权重，借的只是 CPU/GPU**，换远端只改 base_url。实测边界（2026-10-19）：成片画质上限由**取景**决定（脸在画面里越小口型越看不清 ⇒ 传头肩景，如 outputs/ref/face-tight.png）；本机纯 CPU 约 13.6 s/帧（14.8s 配音≈80 分钟），GPU 通常 1~2 分钟。

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-digital-human.git
cd gbt-digital-human
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_digital_human info                  # capability card
python -m gbt_digital_human spec --json           # machine-readable contract
python -m gbt_digital_human check --payload '{}'
python -m gbt_digital_human run   --payload '{}'
```

Real `info` output from this machine:

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

Wire a real implementation:

```python
from gbt_digital_human import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

**注册表登记的取值 / 子动作（3 个）**：`start`、`stop`、`status`

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Not gated: the registry marks this bit `safe: true`.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.11s
```

## Provenance

| field | value |
|---|---|
| capability | `digital_human` |
| domain | `video` |
| handler | `digital_human` |
| safe | `True` (gated = `False`) |
| external | `False` |
| atlas page | [video/digital_human](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/video/digital_human.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
