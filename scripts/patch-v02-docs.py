from pathlib import Path

root = Path.cwd()

prd = root / "docs/prd-v0.2.md"
use_cases = root / "docs/use-cases-v0.2.md"
tech = root / "docs/technical-design-v0.2.md"
review = root / "docs/review-prompts/claude-review-v0.2.md"
plan = root / "docs/v0.2-plan.md"
test_plan = root / "docs/test-plan-v0.2.md"

# 1. Make v0.2-plan bilingual
plan.write_text("""# v0.2 Plan: UI and Export Upgrade
# v0.2 计划：UI 和导出能力升级

## Goals
## 目标

- Show notes on node cards
- 在节点卡片上显示 notes

- Add right-side detail panel
- 增加右侧详情面板

- Enable node editing from UI
- 支持从网页 UI 编辑节点

- Enable double-click quick edit
- 支持双击节点快速编辑

- Add node search
- 增加节点搜索

- Add color/tag metadata: priority, type, owner, source
- 增加颜色/标签元数据：priority、type、owner、source

- Show attachment names on node cards
- 在节点卡片上显示附件名称

- Add Markdown export
- 增加 Markdown 导出

## Non-goals
## 非目标

- Multi-map dropdown
- 多脑图下拉切换

- Discord thread auto-binding
- Discord thread 自动绑定脑图

- Advanced auto-layout
- 高级自动布局

- Login/auth
- 登录/权限系统

- Hermes dashboard embedding
- 嵌入 Hermes Dashboard

## Data model additions
## 数据模型新增字段

Each node may support:
每个节点可以支持：

- notes
- 节点说明

- priority: low | medium | high | urgent
- 优先级：low / medium / high / urgent

- type: idea | task | decision | fact | issue | resource
- 类型：idea / task / decision / fact / issue / resource

- owner
- 负责人

- source
- 来源

- attachments: array of {name, url}
- 附件数组：{name, url}

## Backend additions
## 后端新增能力

- Preserve unknown node fields during updates
- 更新节点时保留未知字段

- Add Markdown export endpoint
- 增加 Markdown 导出接口

- Add richer update_node operation fields
- 扩展 update_node 支持更多字段

## Frontend additions
## 前端新增能力

- Notes display
- notes 显示

- Detail panel
- 详情面板

- Editable label/status/notes/priority/type/owner/source
- 可编辑 label/status/notes/priority/type/owner/source

- Double-click quick edit
- 双击快速编辑

- Search box
- 搜索框

- Attachment name display
- 附件名称显示

- Export Markdown button
- Markdown 导出按钮
""", encoding="utf-8")

# 2. PRD: add double-click goal if missing
s = prd.read_text(encoding="utf-8")
if "Allow double-click quick editing on nodes." not in s:
    s = s.replace(
"""7. Export a mindmap as Markdown.
7. 支持将脑图导出为 Markdown。""",
"""7. Export a mindmap as Markdown.
7. 支持将脑图导出为 Markdown。

8. Allow double-click quick editing on nodes.
8. 支持双击节点快速编辑。"""
    )

if "### 4.7 Double-click quick edit" not in s:
    s = s.replace(
"""### 4.6 Display attachment names
### 4.6 显示附件名称

As a user, I want attachment names to be displayed near nodes so that I can see what files are related to a node.
作为用户，我希望节点旁边显示附件名称，这样可以知道该节点关联了哪些文件。""",
"""### 4.6 Display attachment names
### 4.6 显示附件名称

As a user, I want attachment names to be displayed near nodes so that I can see what files are related to a node.
作为用户，我希望节点旁边显示附件名称，这样可以知道该节点关联了哪些文件。

### 4.7 Double-click quick edit
### 4.7 双击快速编辑

As a user, I want to double-click a node and quickly edit its label or notes.
作为用户，我希望可以双击节点并快速编辑它的标题或 notes。"""
    )

if "Double-clicking a node allows quick editing." not in s:
    s = s.replace(
"""- Markdown export works.
- Markdown 导出可用。""",
"""- Markdown export works.
- Markdown 导出可用。

- Double-clicking a node allows quick editing.
- 双击节点可以进行快速编辑。"""
    )
prd.write_text(s, encoding="utf-8")

# 3. Use cases: add double-click use case
s = use_cases.read_text(encoding="utf-8")
if "## Use Case 7: Double-click quick edit" not in s:
    s += """
## Use Case 7: Double-click quick edit
## 使用场景 7：双击快速编辑

The user double-clicks a node to quickly edit its label or notes.
用户双击节点，快速编辑节点标题或 notes。

Expected behavior:
预期行为：

- A quick edit UI appears.
- 出现快速编辑界面。

- The user can update label or notes.
- 用户可以更新 label 或 notes。

- The frontend sends an update_node operation.
- 前端发送 `update_node` 操作。

- The canvas updates in real time.
- Canvas 实时更新。
"""
use_cases.write_text(s, encoding="utf-8")

# 4. Technical design: add attachments in payload example and improve Markdown example
s = tech.read_text(encoding="utf-8")
if '"attachments": [' not in s:
    s = s.replace(
'''"source": "..."
}''',
'''"source": "...",
  "attachments": [
    {"name": "需求表截图.png", "url": ""}
  ]
}'''
    )

old_md = """# Map Title
# 脑图标题

- Root
- 根节点
  - Child A
  - 子节点 A
  - Child B
  - 子节点 B"""
new_md = """# Hermes Agent

- Hermes Agent [doing]
  - Mindmap Canvas on Unraid [done]
    - React Flow 实时刷新 [done]
  - Discord Gateway [done]"""
if old_md in s:
    s = s.replace(old_md, new_md)

if "## Double-click Quick Edit" not in s:
    s = s.replace(
"""## Search
## 搜索""",
"""## Double-click Quick Edit
## 双击快速编辑

Double-clicking a node should open a lightweight quick edit UI.
双击节点时应该打开轻量级快速编辑 UI。

The quick edit UI should support updating label and notes first.
快速编辑 UI 第一版先支持更新 label 和 notes。

The implementation can reuse the same update_node API used by the detail panel.
实现上可以复用详情面板使用的同一个 `update_node` API。

## Search
## 搜索"""
    )

tech.write_text(s, encoding="utf-8")

# 5. Add test plan
test_plan.write_text("""# Hermes Mindmap Canvas v0.2 Test Plan
# Hermes 脑图 Canvas v0.2 测试计划

## 1. API health test
## 1. API 健康检查

Command:
命令：

curl http://192.168.0.6:9321/api/health

Expected:
预期：

- Returns ok=true
- 返回 ok=true

## 2. Load existing map
## 2. 加载现有脑图

Test:
测试：

- Open http://192.168.0.6:9321
- 打开 http://192.168.0.6:9321

Expected:
预期：

- Existing hermes map loads correctly.
- 现有 hermes 脑图正常加载。

- Existing v0.1 nodes still render.
- 现有 v0.1 节点仍然正常渲染。

## 3. Update node metadata
## 3. 更新节点元数据

Test:
测试：

- Update label, status, notes, priority, type, owner, source, attachments.
- 更新 label、status、notes、priority、type、owner、source、attachments。

Expected:
预期：

- JSON file preserves all fields.
- JSON 文件保留所有字段。

- Unknown fields are not dropped.
- 未知字段不会被删除。

## 4. WebSocket realtime update
## 4. WebSocket 实时更新

Test:
测试：

- Keep browser page open.
- 保持浏览器页面打开。

- Update a node through API or Hermes helper.
- 通过 API 或 Hermes helper 更新节点。

Expected:
预期：

- Browser updates without manual refresh.
- 浏览器无需手动刷新即可更新。

## 5. Notes display
## 5. notes 显示

Expected:
预期：

- Notes preview appears on node card.
- 节点卡片显示 notes 摘要。

- Full notes appear in detail panel.
- 详情面板显示完整 notes。

## 6. Detail panel editing
## 6. 详情面板编辑

Expected:
预期：

- Selecting a node opens the detail panel.
- 选中节点会打开详情面板。

- Editing fields saves to backend.
- 编辑字段后保存到后端。

- Canvas updates after save.
- 保存后 Canvas 更新。

## 7. Double-click quick edit
## 7. 双击快速编辑

Expected:
预期：

- Double-clicking a node opens quick edit.
- 双击节点打开快速编辑。

- Label or notes can be changed.
- 可以修改 label 或 notes。

## 8. Search
## 8. 搜索

Expected:
预期：

- Search matches label, notes, status, priority, type, owner, source, and attachment names.
- 搜索匹配 label、notes、status、priority、type、owner、source 和附件名称。

- Matching nodes are highlighted.
- 匹配节点被高亮。

## 9. Markdown export
## 9. Markdown 导出

Endpoint:
接口：

GET /api/maps/{name}/export/markdown

Expected:
预期：

- Markdown tree is generated.
- 生成 Markdown 树状大纲。

- Status and notes are included when useful.
- 必要时包含 status 和 notes。

## 10. Docker build and Unraid deploy
## 10. Docker 构建和 Unraid 部署

Expected:
预期：

- Docker image builds successfully.
- Docker 镜像成功构建。

- Container starts through Dockge.
- 容器可以通过 Dockge 启动。

- App remains available on port 9321.
- 应用仍然通过 9321 端口访问。
""", encoding="utf-8")

# 6. Update Claude review prompt file list
s = review.read_text(encoding="utf-8")
if "docs/test-plan-v0.2.md" not in s:
    s = s.replace(
"""- docs/technical-design-v0.2.md
- app.py""",
"""- docs/technical-design-v0.2.md
- docs/test-plan-v0.2.md
- app.py"""
    )
review.write_text(s, encoding="utf-8")

print("v0.2 docs patched successfully.")
