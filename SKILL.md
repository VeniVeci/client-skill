---
name: create-client
description: Distill a client into an AI Skill. Import chat logs, briefs, meeting notes, comments, and generate Project Memory + Approval Persona with continuous evolution. | 把甲方蒸馏成 AI Skill，导入聊天记录、方案、会议纪要和批注，生成 Project Memory + Approval Persona，支持持续进化。
argument-hint: [client-name-or-slug]
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.
>
> 本 Skill 支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。

# 甲方.skill 创建器（Claude Code 版）

## 触发条件

当用户说以下任意内容时启动：

- `/create-client`
- "帮我创建一个甲方 skill"
- "我想蒸馏一个甲方"
- "新建甲方"
- "给我做一个客户的 skill"
- "我想模拟一下这个客户会怎么改需求"

当用户对已有甲方 Skill 说以下内容时，进入进化模式：

- "我又找到新的聊天记录了" / "追加" / "更新一下这个甲方"
- "不对" / "这个甲方不会这样说" / "他真正会卡的是..."
- `/update-client {slug}`

当用户说 `/list-clients` 时列出所有已生成的甲方。

---

## 工具使用规则

本 Skill 运行在 Claude Code 环境，使用以下工具：

| 任务 | 使用工具 |
|------|----------|
| 读取 PDF / 图片 / 文本 | `Read` 工具 |
| 解析聊天记录 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/chat_parser.py` |
| 解析 PRD / brief / proposal | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/brief_parser.py` |
| 解析会议纪要 / 转写 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/meeting_parser.py` |
| 解析批注 / 评论汇总 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/comment_parser.py` |
| 写入 / 更新 Skill 文件 | `Write` / `Edit` 工具 |
| 版本管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 列出已有 Skill | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list` |

**基础目录**：Skill 文件写入 `./clients/{slug}/`（相对于本项目目录）。

---

## 安全边界（⚠️ 重要）

本 Skill 在生成和运行过程中严格遵守以下规则：

1. **仅用于内部协作、培训、预演与复盘**
2. **不冒充真实甲方**：生成的 Skill 用于模拟反馈，不等于真实授权
3. **不替代正式审批**：任何上线、签字、付款都必须走真实流程
4. **隐私保护**：所有数据默认本地存储，不上传任何服务器
5. **Layer 0 硬规则**：生成的甲方 Skill 不会凭空给出超出证据范围的明确结论

---

## 主流程：创建新甲方 Skill

### Step 1：基础信息录入（3 个问题）

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md` 的问题序列，只问 3 个问题：

1. **甲方代号 / 身份**（必填）
2. **项目背景**（一句话）
3. **沟通 / 决策风格**（一句话）

除代号外均可跳过。收集完后汇总确认再进入下一步。

### Step 2：原材料导入

向用户展示以下输入方式：

```text
[A] 聊天记录
[B] PRD / brief / proposal
[C] 会议纪要 / 语音转写
[D] 批注 / 评论汇总
[E] 直接粘贴 / 口述
```

如果用户说“没有文件”或“跳过”，仅凭 Step 1 的手动信息生成 Skill。

### Step 3：分析原材料

将收集到的所有原材料和用户填写的基础信息汇总，按以下两条线分析：

**线路 A（Project Memory）**

- 参考 `${CLAUDE_SKILL_DIR}/prompts/project_analyzer.md`
- 提取：项目目标、交付节点、审批链、红线、偏好、风险、修改历史

**线路 B（Approval Persona）**

- 参考 `${CLAUDE_SKILL_DIR}/prompts/approval_analyzer.md`
- 将用户输入的标签翻译为具体的反馈与决策规则
- 提取：说话风格、决策优先级、常见打回理由、协作行为

### Step 4：生成并预览

参考 `${CLAUDE_SKILL_DIR}/prompts/project_builder.md` 生成 Project Memory。  
参考 `${CLAUDE_SKILL_DIR}/prompts/approval_builder.md` 生成 Persona（5 层结构）。

向用户展示两个摘要并确认是否生成。

### Step 5：写入文件

生成目录结构：

```text
clients/{slug}/
  project.md
  persona.md
  meta.json
  SKILL.md
  versions/
  sources/
```

生成后告知用户：

```text
✅ 甲方 Skill 已创建！

文件位置：clients/{slug}/
触发词：/{slug}
        /{slug}-project
        /{slug}-persona
```

---

## 进化模式：追加材料

用户提供新的聊天记录、会议纪要、批注或方案时：

1. 读取新内容
2. 读取现有 `clients/{slug}/project.md` 和 `persona.md`
3. 参考 `${CLAUDE_SKILL_DIR}/prompts/merger.md` 分析增量内容
4. 先调用版本备份：

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./clients
```

5. 追加到对应文件
6. 重新生成 `SKILL.md`
7. 更新 `meta.json`

---

## 进化模式：对话纠正

用户表达“不是这样”“这个甲方不会这么说”“他真正会卡的是...”时：

1. 参考 `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md`
2. 判断属于 Project Memory 还是 Persona
3. 生成 correction 记录
4. 更新对应文件
5. 重新生成 `SKILL.md`

---

## 管理命令

`/list-clients`

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./clients
```

`/client-rollback {slug} {version}`

```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./clients
```

`/delete-client {slug}`

确认后删除 `clients/{slug}`。

`/close-project {slug}`

`/delete-client` 的委婉别名。
