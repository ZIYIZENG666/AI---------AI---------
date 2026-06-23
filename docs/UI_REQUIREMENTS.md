# UI Requirements

This document defines frontend UI rules, Stitch-to-Codex workflow, dashboard page structure, and user-facing text requirements.

## UI Development Source

This project uses Stitch as the primary UI design source for the frontend dashboard.

Stitch-generated screens define:

- Visual direction
- Page layout
- Component placement
- Spacing intention
- User flow
- Overall frontend experience

However, Stitch does not define:

- Backend behavior
- Business rules
- Database rules
- API contracts
- Product workflow rules
- Permission rules
- Data validation rules

## Priority Order

When there is a conflict, follow this priority order:

1. API_CONTRACT.md
2. DATA_MODEL.md
3. WORKFLOW.md
4. MVP_SCOPE.md
5. CODING_STANDARDS.md
6. UI_REQUIREMENTS.md
7. Stitch-generated UI design and frontend code

Codex must not blindly copy Stitch-generated code if it conflicts with project architecture or confirmed project rules.

## Stitch-to-Codex Workflow

Frontend implementation should follow this workflow:

1. Generate or update the relevant UI screens in Stitch.
2. Provide the Stitch-generated design context to Codex through Stitch MCP when available.
3. Ask Codex to implement the frontend based on both project rules and Stitch UI design.
4. Codex must compare Stitch UI with existing project rules before coding.
5. Codex must preserve the visual direction and interaction structure from Stitch when possible.
6. Codex must keep API calls, state handling, validation, loading states, error states, and business logic consistent with backend contracts.
7. After implementation, Codex must run frontend checks and report completed pages, changed files, connected APIs, and any mismatch between Stitch design and implemented UI.

## Language Requirement

All user-visible frontend text must be Chinese.

This includes:

- Page titles
- Navigation labels
- Buttons
- Form labels
- Empty states
- Error messages
- Confirmation dialogs
- Status badges
- Table headers
- Tooltips
- Toast messages
- Modal titles
- Form validation messages

English may only be used in:

- Code
- API fields
- Database fields
- Logs
- Developer-facing documentation
- Internal variable names

## Frontend Technology

The frontend must use:

- React
- TypeScript
- Vite

Codex must preserve a modular frontend structure.

Codex must not put all page logic into a single file.

Each major dashboard area should have its own page, feature folder, reusable components, API client logic, and type definitions when appropriate.

## MVP Dashboard Pages

The MVP dashboard should include UI screens for:

1. Company Profile
2. Source Upload / Source Input
3. Knowledge Review
4. Product Card Management
5. Campaign Creation
6. Lead Discovery Results
7. Lead Detail Review
8. Outreach Draft Status

## Product Card UI Rules

The Product Card UI must support:

- Viewing product cards
- Manually adding a product card
- Editing draft or confirmed product cards
- Confirming draft product cards
- Deleting product cards when allowed

The UI must not show a confirm button for already confirmed product cards.

Product Card status labels must be displayed in Chinese:

- draft = 待确认
- confirmed = 已确认

The UI must not display rejected Product Cards because rejected is not a valid Product Card status.

Recommended Product Card UI text:

- 产品卡片
- 产品
- 待确认
- 已确认
- 手动添加产品
- 编辑
- 删除
- 确认产品卡片
- 保存修改
- 取消
- 已被获客任务使用

## Stitch Design Consistency

When implementing a Stitch-generated screen, Codex must preserve:

- Page layout
- Main navigation structure
- Card, table, dialog, and form structure
- Button placement
- Visual hierarchy
- Spacing intention
- User flow
- Empty state design
- Error state design
- Loading state design

Codex may adjust implementation details only when required by:

- API contract
- TypeScript correctness
- Accessibility
- Responsive behavior
- Existing project architecture
- Project coding standards

## Completion Check

After frontend implementation, Codex must report:

- Which Stitch screens were implemented
- Which frontend files were changed
- Which API endpoints are connected
- Which UI text is shown in Chinese
- Which checks or tests passed
- Any mismatch between Stitch design and implemented UI
- Any part still using mock data
- Any part not yet connected to backend API
