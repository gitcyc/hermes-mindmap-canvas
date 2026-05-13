# Hermes Mindmap Canvas v0.2 Technical Design
# Hermes 脑图 Canvas v0.2 技术设计

## Architecture
## 架构

Current architecture:
当前架构：

- FastAPI backend
- FastAPI 后端

- WebSocket update broadcasting
- WebSocket 更新广播

- React Flow frontend
- React Flow 前端

- JSON file persistence
- JSON 文件持久化

- Docker deployment on Unraid
- 部署在 Unraid Docker 中

## Backend Changes
## 后端修改

### update_node
### 更新节点

Extend update_node to accept these fields:
扩展 `update_node`，支持以下字段：

- label
- status
- notes
- x
- y
- priority
- type
- owner
- source
- attachments

The update operation should not drop unknown fields.
更新操作不应该删除未知字段，保证数据兼容性。

### Markdown export
### Markdown 导出

Add endpoint:
增加接口：

GET /api/maps/{name}/export/markdown

The endpoint should build a tree from edges and output Markdown.
该接口应该根据 edges 构造树，并输出 Markdown。

Example output:
示例输出：

# Map Title
# 脑图标题

- Root
- 根节点
  - Child A
  - 子节点 A
  - Child B
  - 子节点 B

Each node may include status, priority, type, owner, and notes.
每个节点可以包含 status、priority、type、owner 和 notes。

## Frontend Changes
## 前端修改

The current static/index.html will be enhanced without adding a build system.
当前继续增强 `static/index.html`，暂时不引入前端构建系统。

Reason:
原因：

- v0.2 should remain easy to deploy.
- v0.2 应该保持容易部署。

- The app currently uses React and React Flow through CDN.
- 当前应用通过 CDN 使用 React 和 React Flow。

- Docker image remains simple.
- Docker 镜像保持简单。

## Detail Panel
## 详情面板

Maintain selectedNodeId in React state.
在 React state 中维护 `selectedNodeId`。

When selectedNodeId changes, derive selected node from rawMap.nodes.
当 `selectedNodeId` 变化时，从 `rawMap.nodes` 中派生当前选中节点。

Editable fields are saved by calling:
可编辑字段通过以下接口保存：

POST /api/maps/{map}/ops

Payload:
请求数据：

{
  "op": "update_node",
  "id": "node-id",
  "label": "...",
  "notes": "...",
  "status": "...",
  "priority": "...",
  "type": "...",
  "owner": "...",
  "source": "..."
}

## Search
## 搜索

Maintain searchQuery in React state.
在 React state 中维护 `searchQuery`。

A node matches if the search query appears in label, notes, status, priority, type, owner, source, or attachment names.
如果搜索词出现在 label、notes、status、priority、type、owner、source 或附件名称中，则认为该节点匹配。

Matched nodes should get a stronger border or glow.
匹配节点应该显示更明显的边框或发光效果。

## Risk
## 风险

The static single-file frontend may become large.
单文件前端可能变得比较大。

This is acceptable for v0.2 but should be revisited in v0.4.
这在 v0.2 阶段可以接受，但 v0.4 后应该考虑拆分前端代码。
