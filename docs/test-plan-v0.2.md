# Hermes Mindmap Canvas v0.2 Test Plan
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
