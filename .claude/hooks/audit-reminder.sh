#!/bin/sh
# audit-reminder —— 会话启动即把"未修的外审缺陷工单"推到上下文(SessionStart)。
#
# 目的:本仓有一份**外部出具、尚未修正**的缺陷工单。若不主动提示,
#   后来的 Agent(与人类)会**默认这套门禁是好的** —— 而它当前实质失效(H1)。
#   本 hook 用 SessionStart 的 `additionalContext` 把它变成"**开工第一眼就看到**"的事实,
#   而不是"藏在某个目录里等人翻"。
#
# 本文件放在 `.claude/`(不在 `docs/freeze.md` 声明的冻结范围内),不违反骨架冻结规则。
#
# opt-in:设 AUDIT_REMINDER=1 才生效(注册处内联);移除注册即关闭。

[ "$AUDIT_REMINDER" = "1" ] || exit 0

ROOT=$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd) || exit 0
DOC="$ROOT/.claude/AUDIT-外审记录与修正建议.md"
[ -f "$DOC" ] || exit 0

# 已修正则不再打扰:工单头部出现 [已修] 即静默
grep -q '\[已修\]' "$DOC" 2>/dev/null && exit 0

cat <<'JSON'
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"⚠ 本仓有一份【尚未修正】的外审缺陷工单:.claude/AUDIT-外审记录与修正建议.md —— 开工前先读它。\n其中 P0 三条(门禁体系当前实质失效,必须优先处理):\n  H1 scripts/check_harness_docs.py:1 是 markdown 围栏 → SyntaxError → 该脚本【永不执行】,而它被 Makefile:76 与 harness-ci.yml:55 调用 → `make gate` 与 CI 从未绿过。\n  H2 同文件的 REQUIRED 清单里还有 6 个不存在的路径(修好 H1 后仍会失败)。\n  H3 tests/test_scripts.py:316-326 用 pytest.skip 给坏门禁兜底 —— 「门禁坏了就跳过它」。\n处理顺序建议:H1→H3(先把坏门禁救活,并保证再坏会被发现)→ H2 → H5→H4(增量阶段门+真状态机)→ 其余。\n修完后:在工单头部加 [已修] 即可关闭本提示。"}}
JSON
exit 0
