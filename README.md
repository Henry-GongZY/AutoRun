# AutoRun

一个集成飞书 (Feishu/Lark) 机器人和自动化批处理的 Python 项目。

## 功能特性

- **飞书集成**: 支持长连接 (WebSocket) 模式，通过 @ 机器人指令触发自动化任务。
- **自动化批处理**: 支持指定 Git 链接或本地目录，自动拉取更新并顺序执行 Shell 命令。
- **动态同步策略**: 根据工作时间自动调整 Git 轮询频率，节省资源。
- **校验规则扩展**: 采用抽象基类设计，可轻松添加自定义校验逻辑。
- **配置管理**: 使用 Pydantic Settings 进行环境变量管理。

## 快速开始

### 1. 环境准备

确保已安装 Python 3.10+。建议使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. 安装依赖

```bash
pip install .
```

或者使用开发模式安装：

```bash
pip install -e .
```

### 3. 配置环境变量

将 `.env.example` 复制为 `.env` 并填写相关凭据：

```bash
cp .env.example .env
```

### 4. 运行项目

```bash
python -m src.main
```

## 扩展校验规则

在 `src/validators/` 目录下创建新的 Python 文件，继承 `BaseValidator` 类并实现 `validate` 方法即可。
