# Hermes Mindmap Canvas v0.2 Use Cases
# Hermes 脑图 Canvas v0.2 使用场景

## Use Case 1: Conversational project planning
## 使用场景 1：对话式项目规划

The user asks Hermes to create or update a project mindmap.
用户通过对话要求 Hermes 创建或更新项目脑图。

Example:
示例：

“在脑图 hermes 里添加 v0.2 开发计划，包括 notes 显示、详情面板、搜索、Markdown 导出。”

Expected behavior:
预期行为：

- Hermes reads the current mindmap.
- Hermes 读取当前脑图。

- Hermes finds or creates the correct parent node.
- Hermes 找到或创建正确的父节点。

- Hermes calls the mindmap API through the helper command.
- Hermes 通过 helper 命令调用脑图 API。

- The browser canvas updates in real time.
- 浏览器 Canvas 实时更新。

## Use Case 2: Inspecting node context
## 使用场景 2：查看节点上下文

The user clicks a node to inspect detailed information.
用户点击某个节点查看详细信息。

Expected behavior:
预期行为：

- A right-side detail panel opens.
- 右侧详情面板打开。

- The panel shows label, status, notes, priority, type, owner, source, and attachments.
- 面板显示 label、status、notes、priority、type、owner、source 和 attachments。

## Use Case 3: Editing node details in browser
## 使用场景 3：在浏览器中编辑节点详情

The user edits a node directly in the web UI.
用户直接在 Web UI 中编辑节点。

Expected behavior:
预期行为：

- The user changes label, notes, or metadata.
- 用户修改 label、notes 或元数据。

- The frontend sends an update_node operation.
- 前端发送 `update_node` 操作。

- The backend saves the change to JSON.
- 后端将修改保存到 JSON。

- WebSocket broadcasts the updated map.
- WebSocket 广播更新后的脑图。

## Use Case 4: Searching nodes
## 使用场景 4：搜索节点

The user searches for a keyword.
用户搜索关键词。

Expected behavior:
预期行为：

- Matching nodes are highlighted.
- 匹配的节点被高亮。

- Search checks label, notes, status, priority, type, owner, source, and attachment names.
- 搜索范围包括 label、notes、status、priority、type、owner、source 和附件名称。

## Use Case 5: Exporting Markdown
## 使用场景 5：导出 Markdown

The user exports a mindmap as Markdown.
用户将脑图导出为 Markdown。

Expected behavior:
预期行为：

- The backend generates a tree-style Markdown outline.
- 后端生成树状 Markdown 大纲。

- Node metadata and notes are included when useful.
- 必要时包含节点元数据和 notes。

- The result can be copied into documentation.
- 结果可以复制到文档中使用。

## Use Case 6: Displaying attachment names
## 使用场景 6：显示附件名称

The user or Hermes adds attachment metadata to a node.
用户或 Hermes 为节点添加附件元数据。

Expected behavior:
预期行为：

- Attachment names appear on the node card.
- 附件名称显示在节点卡片上。

- Attachment names also appear in the detail panel.
- 附件名称也显示在详情面板中。

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
