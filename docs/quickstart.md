# 快速开始

## 1. 克隆

```bash
git clone <repo>
cd ai-delivery-harness-engineering
```

## 2. 安装

```bash

python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
## 3. 安装钩子

```bash

pre-commit install
```
## 4. 跑门禁

```bash

make gate
```
## 5. 开始填充

见 `docs/fill-guide.md`。

## 6. 第一个需求

```bash

mkdir -p harness/changes/REQ-0001
cp harness/changes/_template/*.md harness/changes/REQ-0001/
./scripts/check-gates.sh harness/changes/REQ-0001
```