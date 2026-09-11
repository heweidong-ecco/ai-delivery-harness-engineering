"""依赖漏洞审计 —— 语义为"硬",但必须**跑得过**。

反外审 H11:原先 CI 里是 `pip-audit --strict || true`(软),与本脚本(硬 fail)
语义矛盾 —— 统一为硬。但在补齐验证时实测发现:直接改成 `--strict` 会让
**这一步永远红**,因为本仓把自己用 `-e .` 装成了一个**不在 PyPI 上的包**:

    ERROR: ai-delivery-harness-engineering: Dependency not found on PyPI
           and could not be audited

`--strict` 的含义是「**依赖收集**失败即整体失败」(见 `pip-audit --help`),
而不是「发现漏洞才失败」—— **发现漏洞时无论如何都返回非零**。
所以正确写法是去掉 `--strict`、改用 `--skip-editable`:
  · 有漏洞   → 仍然 fail(硬语义不变,这才是 H11 要的);
  · 本仓自身是 editable 本地包 → 按 `--skip-editable` 跳过,不再误判为失败。
"""

import subprocess

# `--skip-editable` 而非 `--strict`:理由见模块 docstring。
PIP_AUDIT_ARGS = ["pip-audit", "--skip-editable"]


def main() -> None:
    result = subprocess.run(
        PIP_AUDIT_ARGS,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)
    print("Dependency audit passed")


if __name__ == "__main__":
    main()
