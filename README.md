# 甲方.skill

**把爱改需求的甲方，蒸馏成一个真正会提意见的 AI Skill。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

 

提供甲方的原材料: 微信/飞书聊天记录、邮件、会议纪要、PRD、批注截图、你的主观描述。\
生成一个**真正像甲方的 AI Skill**。\
它会用甲方的口气改需求，记得谁才是真正拍板的人，知道什么叫"简单大气但不能太普通"。

⚠️ **本项目用于内部对齐、培训、演练和复盘，不用于冒充真人、欺骗签字或绕过真实审批。**

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [English](README_EN.md)

***

> **April 5th Update：** 新增了一个示例甲方，在 `clients/example_brand_director/` 目录下，clone 后可直接体验。

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/VeniVeci/client-skill .claude/skills/create-client

# 或安装到全局（所有项目都能用）
git clone https://github.com/VeniVeci/client-skill ~/.claude/skills/create-client
```

### OpenClaw

```bash
git clone https://github.com/VeniVeci/client-skill ~/.openclaw/workspace/skills/create-client
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

***

## 使用

在 Claude Code 中输入：

```text
/create-client
```

按提示输入甲方代号、项目背景、沟通风格，然后选择数据来源。所有字段都可以跳过，只靠描述也能生成一个可运行的甲方 Skill。

生成完成后，用 `/{slug}` 调用该甲方 Skill。

### 管理命令

| 命令                                  | 说明                                            |
| ----------------------------------- | --------------------------------------------- |
| `/list-clients`                     | 列出所有甲方 Skill                                  |
| `/{slug}`                           | 调用完整 Skill（Project Memory + Approval Persona） |
| `/{slug}-project`                   | 仅项目记忆                                         |
| `/{slug}-persona`                   | 仅甲方人格                                         |
| `/client-rollback {slug} {version}` | 回滚到历史版本                                       |
| `/delete-client {slug}`             | 删除                                            |
| `/close-project {slug}`             | `delete` 的委婉别名                                |

***

## 效果示例

> 输入：`新消费护肤品牌总监，审美驱动，喜欢说高级感，预算敏感，老板经常临时插话，做 618 活动页`

**场景一：看设计稿**

```text
用户      ❯ 这一版落地页你看看能不能过

甲方.skill ❯ 先说结论，方向比上一版好。
             但是还不够高级，太像互联网促销页了。
             第一屏字还是太多，产品没有被托起来。
             你先别切开发，再给我一个更克制的版本。
```

**场景二：需求变更**

```text
用户      ❯ 这个需求昨天不是已经定了吗

甲方.skill ❯ 昨天定的是昨天的信息。
             今天老板看了，说赠品那块要再强调一下。
             你先别纠结对错，我们先把结果做出来。
```

**场景三：压预算**

```text
用户      ❯ 如果加这个动画，开发周期要多两天

甲方.skill ❯ 两天不行，节点不能动。
             你看看有没有更轻一点的实现方式。
             效果要有，但不要做成成本很高的那种。
```

**场景四：模糊反馈**

```text
用户      ❯ 你说的“再高级一点”具体是哪里

甲方.skill ❯ 不是单个点的问题，是整体气质不对。
             现在太满、太吵、太想卖东西。
             我要的是克制一点，但不是冷。
             你先按这个感觉出一版，我再看。
```

***

## 功能特性

### 支持的数据来源

| 来源                   | 格式                     | 备注             |
| -------------------- | ---------------------- | -------------- |
| 微信 / 飞书 / Slack 聊天记录 | txt / json / md / 导出文本 | 最能还原甲方语气       |
| 邮件线程                 | `.eml` / 纯文本转存         | 适合提取正式反馈和审批节点  |
| PRD / 方案 / Wiki      | md / txt / pdf         | 提取业务目标、禁区、交付标准 |
| 会议纪要 / 语音转写          | md / txt               | 适合提取隐性决策和临时变更  |
| 批注 / 评论汇总            | txt / json / 截图转文字     | 提取审美偏好和常见意见    |
| 直接粘贴文字               | 纯文本                    | 你的经验总结与踩坑记录    |

### 生成的 Skill 结构

每个甲方 Skill 由两部分组成，共同驱动输出：

| 部分                            | 内容                                    |
| ----------------------------- | ------------------------------------- |
| **Part A — Project Memory**   | 项目背景、目标、审批链、修改历史、禁区、偏好、风险档案           |
| **Part B — Approval Persona** | 5 层性格结构：硬规则 → 身份 → 表达风格 → 决策逻辑 → 协作行为 |

运行逻辑：`收到方案/问题 → Persona 判断甲方态度和优先级 → Project Memory 提供上下文 → 用甲方风格输出`

### 支持的标签

**沟通风格**：模糊型甲方 · 审美驱动 · 数据驱动 · 爱说人话但不给标准 · 只给感觉不给结论 · 喜欢临上线改需求 · 话少但一票否决 · 既要又要还要

**业务偏好**：高级感控 · 转化导向 · 品牌导向 · 老板意志代理人 · 预算敏感 · 时间焦虑 · 风险厌恶 · 喜欢 benchmark · 迷恋大厂感 · 讨厌互联网味

**协作行为**：不看文档 · 只看首页 · 喜欢拉新人进群 · 经常说“简单改一下” · 不愿意砍需求 · 喜欢最后一分钟拍板 · 多轮汇报型

### 进化机制

- **追加材料** → 导入新聊天记录 / 新会议纪要 / 新批注 → 增量 merge 到对应部分
- **对话纠正** → 说「这个甲方不会这样说」→ 写入 Correction 层，立即生效
- **版本管理** → 每次更新自动存档，支持回滚

***

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准：

```text
create-client/
├── SKILL.md                  # skill 入口（官方 frontmatter）
├── prompts/                  # Prompt 模板
│   ├── intake.md             #   对话式信息录入
│   ├── project_analyzer.md   #   项目记忆提取
│   ├── approval_analyzer.md  #   甲方决策人格提取
│   ├── project_builder.md    #   project.md 生成模板
│   ├── approval_builder.md   #   persona.md 五层结构模板
│   ├── merger.md             #   增量 merge 逻辑
│   └── correction_handler.md #   对话纠正处理
├── tools/
│   ├── chat_parser.py        # 聊天记录分析
│   ├── brief_parser.py       # PRD / 方案解析
│   ├── meeting_parser.py     # 会议纪要 / 转写解析
│   ├── comment_parser.py     # 批注 / 评论汇总解析
│   ├── skill_writer.py       # Skill 文件管理
│   └── version_manager.py    # 版本存档与回滚
├── clients/                  # 生成的甲方 Skill（默认 gitignored）
│   └── example_brand_director/
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

***

## 实验子项目

这个仓库里还额外放了一个正在孵化的 GitHub-native 方向：

- [maintainer-skill/README.md](maintainer-skill/README.md)

一句话 pitch：

> 把 maintainer 蒸馏成 AI Skill，让它在你发 PR 前先喷你一遍。

如果 `甲方.skill` 更偏内部协作和情绪共鸣，`maintainer.skill / reviewer.skill` 更偏 GitHub 传播和开源开发者场景。

***

## 示例甲方

仓库内置了一个可试玩样例：

- 路径：`clients/example_brand_director/`
- 设定：新消费品牌总监，审美驱动，预算敏感，老板意志强
- 适用场景：活动页、品牌视觉、营销文案、临上线改需求

你可以直接打开其中的 `SKILL.md` 看完整人格，也可以把里面的项目记忆和人格结构拿去做二次创作。

***

## 注意事项

- **原材料质量决定 Skill 质量**：真实聊天记录 + 会议纪要 > 只靠主观吐槽
- 建议优先提供：**拍板反馈** > **打回意见** > **临时变更记录** > 日常寒暄
- 生成的甲方 Skill 是一种协作模型，不是法律意义上的授权人
- 涉及客户隐私和商业机密时，请自行脱敏后再导入

***

## 致敬 & 灵感

这个项目沿用了“把真人协作对象蒸馏成 AI Skill”的思路：

- **[同事.skill](https://github.com/titanwings/colleague-skill)** 把职场知识和人物风格做成可调用的 Skill
- 私人关系场景证明了这种双层蒸馏结构不只适用于工作协作

而 **甲方.skill** 把这套方法迁移到更 GitHub-native、也更容易被开发者共鸣的场景里：
不是为了陪聊，是为了让你在提案、写文案、改设计、出方案之前，先被甲方提前毒打一遍。

***

### 写在最后

很多项目不是做死的，是猜死的。

你以为需求写在 PRD 里，实际上需求写在甲方那句“我也说不上来，但就感觉不对”里。\
你以为最大的风险是做不出来，实际上最大的风险是做出来了，但甲方说“不是我要的那个感觉”。\
你以为拍板人是群里最活跃的那个，实际上真正拍板的是那个从不说话、只在最后十分钟出现的人。

这个 Skill 做的事，就是把这些隐形规则，从空气里提取出来，变成一个你能提前对话、提前模拟、提前挨骂的对象。

你不一定会更喜欢甲方。\
但你大概率会更懂甲方。
