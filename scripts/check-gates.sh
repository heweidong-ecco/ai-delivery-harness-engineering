#!/usr/bin/env bash
# check-gates —— 阶段产出物门(增量版)。
#
# 反外审 H5(2026-09-11):原实现**一次性检查全部 6 个产出物**,
# 且 grep 全仓它**未挂进 Makefile / CI / pre-commit 任何一处** ——
# 于是门禁只可能压在"最后一次提交",长任务中途断了 = 前面全白费。
#
# 现在:① 支持 `--stage <n>` 增量门(每阶段结束就能跑);
#       ② 产出物清单**单一来源** = harness/state/stages.json(与 scripts/stage_gate.py 共用),
#          不再在本脚本里重复列举 —— 顺带修掉原先**漏检 review-record-v1.md** 的缺口;
#       ③ 挂进了 Makefile(`make gates`)与 CI。
#
# 用法:
#   ./scripts/check-gates.sh REQ-0001              # 检查阶段 1..9 = 变更七件套齐备
#   ./scripts/check-gates.sh REQ-0001 --stage 4    # 增量门:只要求阶段 1..4 的产出物
#   ./scripts/check-gates.sh harness/changes/REQ-0001   # 兼容原写法(取 basename 作为需求号)
#
# 退出码:0 = 通过;1 = 门禁未过;2 = 用法错误。
set -euo pipefail

# 变更七件套齐备 = 阶段 1..9;阶段 10(用户确认)是人工检查点,需显式 --stage 10 才要求。
DEFAULT_UPTO=9

usage() {
  echo "Usage: $0 <REQ|REQ_DIR> [--stage <1..10>]" >&2
}

if [ $# -lt 1 ]; then
  usage
  exit 2
fi

REQ_ARG="$1"
shift
REQ="$(basename "$REQ_ARG")"

UPTO="$DEFAULT_UPTO"
while [ $# -gt 0 ]; do
  case "$1" in
    --stage)
      [ $# -ge 2 ] || { usage; exit 2; }
      UPTO="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

case "$UPTO" in
  ''|*[!0-9]*) echo "--stage 必须是数字,收到: $UPTO" >&2; exit 2 ;;
esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/scripts/stage_gate.py" check --req "$REQ" --upto "$UPTO"
