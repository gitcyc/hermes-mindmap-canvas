# Hermes Mindmap Canvas v0.2 PRD
# Hermes 脑图 Canvas v0.2 产品需求文档

## 1. Background
## 1. 背景

Hermes Mindmap Canvas is a real-time web canvas for Hermes Agent.
Hermes Mindmap Canvas 是一个为 Hermes Agent 服务的实时 Web 脑图画布。

Users can update mindmap nodes through conversation, and the browser canvas updates live through WebSocket.
用户可以通过和 Agent 对话来更新脑图节点，浏览器画布会通过 WebSocket 实时刷新。

The v0.1 version already supports:
v0.1 版本已经支持：

- FastAPI backend
- FastAPI 后端

- React Flow frontend
- React Flow 前端画布

- WebSocket real-time updates
- WebSocket 实时更新

- JSON persistence
- JSON 文件持久化存储

- Hermes helper command
- Hermes 辅助命令 `hermes-mindmap`

- Basic node creation, status update, layout, and connection
- 基础节点创建、状态更新、自动布局和节点连接

## 2. Goal
## 2. 目标

v0.2 focuses on making the canvas usable as a real product workspace.
v0.2 的重点是让 Canvas 从演示原型变成真正可用的产品工作区。

Main goals:
主要目标：

1. Display node notes directly on cards.
1. 在节点卡片上直接显示 notes。

2. Show a right-side detail panel when a node is selected.
2. 点击节点后，在右侧显示详情面板。

3. Allow editing node metadata from the UI.
3. 允许在网页 UI 中编辑节点元数据。

4. Add node search.
4. 增加节点搜索功能。

5. Add basic tag metadata: priority, type, owner, source.
5. 增加基础标签字段：priority、type、owner、source。

6. Display attachment names on node cards.
6. 在节点卡片上显示附件名称。

7. Export a mindmap as Markdown.
7. 支持将脑图导出为 Markdown。

## 3. Non-goals
## 3. 非目标

v0.2 will not include:
v0.2 暂不包含：

- Multi-map dropdown
- 多脑图下拉切换

- Discord thread auto-binding
- Discord thread 自动绑定脑图

- Advanced dagre/elk layout
- 高级 dagre / elk 自动布局算法

- Login/auth
- 登录和权限系统

- Hermes Dashboard embedding
- 嵌入 Hermes Dashboard

- Excel export
- Excel 导出

- Obsidian Canvas export
- Obsidian Canvas 导出

- History rollback
- 历史版本和回滚

These are reserved for later versions.
这些功能保留到后续版本开发。

## 4. User Stories
## 4. 用户故事

### 4.1 View notes
### 4.1 查看 notes

As a user, I want node notes to be visible on the canvas so that I can understand context without opening raw JSON.
作为用户，我希望节点 notes 能直接显示在画布上，这样不需要打开 JSON 文件也能理解上下文。

### 4.2 Inspect node details
### 4.2 查看节点详情

As a user, I want to click a node and see details in a right panel, including label, status, notes, priority, type, owner, source, and attachments.
作为用户，我希望点击节点后能在右侧面板看到 label、status、notes、priority、type、owner、source 和 attachments 等信息。

### 4.3 Edit node details
### 4.3 编辑节点详情

As a user, I want to edit node label, status, notes, priority, type, owner, and source directly in the browser.
作为用户，我希望能直接在浏览器中编辑节点的 label、status、notes、priority、type、owner 和 source。

### 4.4 Search nodes
### 4.4 搜索节点

As a user, I want to search nodes by label, notes, owner, type, or status.
作为用户，我希望可以按 label、notes、owner、type 或 status 搜索节点。

### 4.5 Export Markdown
### 4.5 导出 Markdown

As a user, I want to export the mindmap to a Markdown outline for documentation and sharing.
作为用户，我希望能把脑图导出成 Markdown 大纲，方便写文档和分享。

### 4.6 Display attachment names
### 4.6 显示附件名称

As a user, I want attachment names to be displayed near nodes so that I can see what files are related to a node.
作为用户，我希望节点旁边显示附件名称，这样可以知道该节点关联了哪些文件。

## 5. Data Model
## 5. 数据模型

Each node may include:
每个节点可以包含：

- id
- 节点唯一 ID

- label
- 节点标题

- status: todo | doing | done | blocked
- 节点状态：todo / doing / done / blocked

- notes
- 节点详细说明

- x
- 节点横向坐标

- y
- 节点纵向坐标

- priority: low | medium | high | urgent
- 优先级：low / medium / high / urgent

- type: idea | task | decision | fact | issue | resource
- 类型：idea / task / decision / fact / issue / resource

- owner
- 负责人

- source
- 信息来源，比如 Discord、Hermes、manual

- attachments: array of objects
- 附件列表，对象数组

Attachment object:
附件对象：

- name
- 附件名称

- url
- 附件链接，可以先为空

## 6. Backend Requirements
## 6. 后端需求

### 6.1 Update node
### 6.1 更新节点

The update_node operation must support label, status, notes, x, y, priority, type, owner, source, and attachments.
`update_node` 操作必须支持 label、status、notes、x、y、priority、type、owner、source 和 attachments。

Unknown existing node fields should be preserved.
已有但当前接口不认识的字段也应该保留，避免破坏旧数据或未来扩展字段。

### 6.2 Markdown export
### 6.2 Markdown 导出

Add endpoint: GET /api/maps/{name}/export/markdown
增加接口：`GET /api/maps/{name}/export/markdown`

It should return a Markdown document with a tree-style outline.
该接口应该返回一个树状大纲格式的 Markdown 文档。

### 6.3 Backward compatibility
### 6.3 向后兼容

Existing v0.1 JSON files must continue working.
现有 v0.1 的 JSON 文件必须继续可用。

## 7. Frontend Requirements
## 7. 前端需求

### 7.1 Node card
### 7.1 节点卡片

Node cards should display label, status, node id, optional notes preview, optional priority/type/owner badges, and optional attachment names.
节点卡片应该显示 label、status、node id，可选显示 notes 摘要、priority/type/owner 标签以及附件名称。

### 7.2 Detail panel
### 7.2 详情面板

When a node is selected, show a right-side panel with editable fields.
选中节点后，在右侧显示可编辑详情面板。

Editable fields include label, status, notes, priority, type, owner, source, and attachments.
可编辑字段包括 label、status、notes、priority、type、owner、source 和 attachments。

### 7.3 Search
### 7.3 搜索

Add a search box. Matching nodes should be visually highlighted.
增加搜索框。匹配到的节点应该有视觉高亮。

Search should match label, notes, status, priority, type, owner, source, and attachment names.
搜索范围包括 label、notes、status、priority、type、owner、source 和附件名称。

### 7.4 Markdown export button
### 7.4 Markdown 导出按钮

Add an Export Markdown button. Clicking it should open or download the Markdown export.
增加 Export Markdown 按钮，点击后打开或下载 Markdown 导出结果。

## 8. Acceptance Criteria
## 8. 验收标准

v0.2 is complete when:
满足以下条件时，v0.2 完成：

- Notes are visible on node cards.
- 节点卡片能显示 notes。

- Clicking a node opens a detail panel.
- 点击节点能打开右侧详情面板。

- Editing node fields from the detail panel updates the backend and refreshes the canvas.
- 在详情面板编辑节点字段后，后端数据更新，Canvas 实时刷新。

- Search can find nodes by label and notes.
- 搜索可以通过 label 和 notes 找到节点。

- Attachment names are visible when present.
- 如果节点有附件，附件名称可以显示。

- Markdown export works.
- Markdown 导出可用。

- Existing hermes.json still loads correctly.
- 现有 `hermes.json` 仍然能正常加载。

- The app still runs in Unraid Docker on port 9321.
- 应用仍然可以在 Unraid Docker 中通过 9321 端口运行。
