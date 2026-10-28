"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "digital_human",
 "domain": "video",
 "desc": "数字人「以图生视频」（本地 SadTalker，零账号/零验证）：**一张照片 + 一段配音 ⇒ 带头部动作与口型同步的说话视频**。ops：status/probe 只读（引擎·权重·venv 缺件如实报）· capabilities 读边界 · render 写（异步出片回 task_id；写面自收窄在 outputs/dh-talk/ 与 state/digital_human/）· task/jobs 读任务账 · socket start/stop/status 把本能力包成 **OpenAI 兼容端点**（只监听回环），主脑用 omni_plug.ai_control（远端 https）或 _local_ai_call（回环）反向调用 —— **对面跑的是我们自己的权重，借的只是 CPU/GPU**，换远端只改 base_url。实测边界（2026-10-19）：成片画质上限由**取景**决定（脸在画面里越小口型越看不清 ⇒ 传头肩景，如 outputs/ref/face-tight.png）；本机纯 CPU 约 13.6 s/帧（14.8s 配音≈80 分钟），GPU 通常 1~2 分钟。",
 "handler": "digital_human",
 "safe": true,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": true,
 "ops": [
  "start",
  "stop",
  "status"
 ],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
