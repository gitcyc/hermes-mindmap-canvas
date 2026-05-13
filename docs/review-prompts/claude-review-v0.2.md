# Claude Review Prompt for Hermes Mindmap Canvas v0.2
# Hermes 脑图 Canvas v0.2 的 Claude 审核提示词

You are reviewing the Hermes Mindmap Canvas v0.2 design and implementation.
你正在审核 Hermes Mindmap Canvas v0.2 的设计和实现。

Project context:
项目背景：

- The app is a small FastAPI + React Flow web canvas.
- 该应用是一个小型 FastAPI + React Flow Web Canvas。

- It runs in Docker on Unraid.
- 它运行在 Unraid 的 Docker 中。

- It is controlled by Hermes Agent through HTTP API.
- Hermes Agent 通过 HTTP API 控制它。

- The frontend is currently a single static/index.html file using React and React Flow from CDN.
- 当前前端是单个 `static/index.html` 文件，通过 CDN 使用 React 和 React Flow。

- Runtime data is stored as JSON under /data/mindmaps.
- 运行时数据以 JSON 形式存储在 `/data/mindmaps` 下。

- The user wants conversational updates from Hermes and real-time browser updates through WebSocket.
- 用户希望通过 Hermes 对话更新脑图，并通过 WebSocket 在浏览器中实时显示。

Please review:
请审核：

1. Product requirements
1. 产品需求

2. Data model
2. 数据模型

3. API design
3. API 设计

4. Frontend state management
4. 前端状态管理

5. Backward compatibility
5. 向后兼容性

6. Security and deployment risk
6. 安全和部署风险

7. Maintainability
7. 可维护性

8. Test plan
8. 测试计划

Files to review:
需要审核的文件：

- docs/prd-v0.2.md
- docs/use-cases-v0.2.md
- docs/technical-design-v0.2.md
- app.py
- static/index.html

Please provide:
请输出：

- High-level assessment
- 总体评价

- Critical issues
- 关键问题

- Suggested changes before coding
- 编码前建议先修改的问题

- Suggested changes after coding
- 编码后可以继续优化的问题

- A concise implementation checklist
- 简明实现 checklist
