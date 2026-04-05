# 详细安装说明

## Claude Code 安装

### 项目级安装（推荐）

在你的 git 仓库根目录执行：

```bash
mkdir -p .claude/skills
git clone https://github.com/VeniVeci/client-skill .claude/skills/create-client
```

### 全局安装

```bash
git clone https://github.com/VeniVeci/client-skill ~/.claude/skills/create-client
```

### OpenClaw 安装

```bash
git clone https://github.com/VeniVeci/client-skill ~/.openclaw/workspace/skills/create-client
```

---

## 依赖安装

### 可选依赖

```bash
cd .claude/skills/create-client  # 或你的安装路径
pip3 install -r requirements.txt
```

当前没有硬性依赖。所有核心流程都可以在纯文本模式下运行。  
如果你要处理更复杂的本地文件格式，可以自行按需扩展 `tools/`。

---

## 推荐的原材料准备方式

### 1. 聊天记录

推荐导出并整理为 `txt`、`md` 或 `json`，来源可以是：

- 微信
- 飞书
- Slack
- 邮件线程导出后的纯文本

建议优先保留这些内容：

1. 甲方直接拍板的话
2. 甲方打回方案的原话
3. 临上线前新增需求
4. 关于预算、老板、节点、风险的表述

### 2. PRD / 提案 / 方案

把以下文档整理为 `md` 或 `txt` 最稳妥：

- PRD
- 活动 brief
- 创意提案
- 需求变更记录
- 对比稿说明

建议保留：

- 业务目标
- 不能碰的红线
- 明确说过“不要”的内容
- 对“高级感”“品牌感”“转化”的定义

### 3. 会议纪要 / 语音转写

如果有会议纪要或录音转写，优先保留：

- 谁真正拍板
- 谁只是在转述老板意见
- 哪些需求是“临时加的”
- 哪些地方表面同意，实际没过

### 4. 批注 / 评论

把设计批注、文案修改意见、飞书评论统一整理成一个文本文件，尤其关注：

- 高频形容词
- 否定方式
- 模糊反馈
- 反复出现的 benchmark

---

## 常见问题

### Q: 数据会上传到云端吗？
A: 不会。默认所有数据都在本地文件系统中处理和存储。

### Q: 可以同时创建多个甲方 Skill 吗？
A: 可以。每个甲方会生成独立的 `clients/{slug}/` 目录。

### Q: 创建后还能继续进化吗？
A: 可以。追加新的聊天记录、会议纪要或批注即可增量更新。说“这个甲方不会这么说”可以触发纠正流程。

### Q: 删除命令是什么？
A: 使用 `/delete-client {slug}`，或者用更委婉的 `/close-project {slug}`。
