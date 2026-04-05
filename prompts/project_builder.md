# Project Memory 生成模板

## 结构说明

Project Memory 负责保存这个甲方所处项目的真实上下文，让 Persona 的反馈不只是“像”，而且“对路”。

## 模板

```markdown
# {name} — Project Memory

## 项目概览
- 行业 / 项目：{project_type}
- 公司 / 团队：{company}
- 当前阶段：{stage}
- 甲方角色：{role}

---

## 核心目标
- 明面目标：{surface_goal}
- 真实优先级：{real_goal}
- 成功标准：{success_metrics}

---

## 审批链
- 日常接口人：{daily_contact}
- 真正拍板人：{final_approver}
- 隐性 stakeholder：{hidden_stakeholders}

---

## 风格偏好
- 喜欢的方向：{liked_directions}
- 讨厌的方向：{disliked_directions}
- 高频关键词：{keywords}
- 常提 benchmark：{benchmarks}

---

## 红线与禁区
1. {redline_1}
2. {redline_2}
3. {redline_3}

---

## 修改历史
| 阶段 | 变更 |
|------|------|
| {date_or_stage} | {change_summary} |

---

## 风险档案
- 最容易返工的点：{rework_risks}
- 常见延误原因：{delay_reasons}
- 最危险的误判：{dangerous_assumptions}

---

## 经典反馈原话
- "{quote_1}"
- "{quote_2}"
- "{quote_3}"

---

## Correction 记录
（由进化模式自动追加）
```

## 填充规则

1. 信息优先基于真实材料，不凭空美化
2. 如果同一个项目有多个阶段，保留阶段差异
3. 如果“口头要求”和“正式文档”冲突，两个都要写
4. 信息不足就写 `[待补充]`
