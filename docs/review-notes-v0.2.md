# v0.2 Review Notes from windsurf-docs / claude-opus-4-7-high
# v0.2 windsurf-docs / Claude 审核记录

## Verdict
## 结论

Conditionally approved to enter implementation.

有条件批准进入编码阶段。

## Required fixes before or during first implementation pass
## 第一轮实现必须优先处理的问题

1. Backend update_node must preserve unknown fields.
1. 后端 update_node 必须保留未知字段。

2. Backend update_node must support priority, type, owner, source, and attachments.
2. 后端 update_node 必须支持 priority、type、owner、source 和 attachments。

3. Add Markdown export endpoint.
3. 增加 Markdown 导出接口。

4. Frontend must display notes, tags, owner, and attachment names.
4. 前端必须显示 notes、标签、owner 和附件名称。

5. Add detail panel, search box, and double-click quick edit.
5. 增加详情面板、搜索框和双击快速编辑。

## Recommended implementation order
## 建议实现顺序

1. Fix update_node field preservation.
1. 修复 update_node 字段保留逻辑。

2. Add Markdown export endpoint.
2. 增加 Markdown 导出接口。

3. Add frontend node card display improvements.
3. 增强前端节点卡片显示。

4. Add right-side detail panel.
4. 增加右侧详情面板。

5. Add search.
5. 增加搜索。

6. Add double-click quick edit.
6. 增加双击快速编辑。

7. Test and deploy to Unraid.
7. 测试并部署到 Unraid。

## Risk notes
## 风险记录

Low risk:
低风险：

- Architecture is simple and clear.
- 架构简单清晰。

- FastAPI + React Flow is suitable.
- FastAPI + React Flow 组合合适。

- JSON persistence is simple and reliable.
- JSON 文件持久化简单可靠。

Medium risk:
中风险：

- Current update_node may drop future fields.
- 当前 update_node 可能丢失未来字段。

- Single-file frontend will grow larger in v0.2.
- 单文件前端在 v0.2 会变大。

- Input validation is limited.
- 输入校验有限。

## Approval

Approved to start coding with the condition that backend field preservation is fixed first.

批准开始编码，但必须先修复后端字段保留问题。
