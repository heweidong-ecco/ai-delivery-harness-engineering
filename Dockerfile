FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
RUN pip install --upgrade pip && pip install -e ".[dev]"

COPY . .

# 这里**刻意不装** pre-commit 钩子:
#   · `.dockerignore` 排除了 `.git`,而 `pre-commit install` 需要一个 git 仓库 ——
#     所以它在这个镜像里**必然失败**;
#   · 原先写的是 `RUN pre-commit install --install-hooks || true`,用 `|| true` 把
#     这个必然失败吞掉了(H12 同类:让"检查"永不失败的写法)。
# 容器只负责跑 `make gate`,不需要提交钩子;钩子由 `make hooks` 或
# `scripts/dev-setup.sh` 在**开发机**上装。
CMD ["make", "gate"]
