# UI Requirements

This project uses Stitch as the primary UI design source for the frontend
dashboard.

## UI Source of Truth

Stitch-generated screens define the visual direction, layout, component
placement, spacing, and overall user experience of the frontend.

However, Stitch does not define backend behavior, business rules, database
rules, API contracts, or product workflow rules.

`AGENTS.md` remains the top-level authority for all Codex work. The priority
order below applies only to frontend UI implementation details after `AGENTS.md`
and project-level rules have already been applied.

For frontend UI implementation details, when there is a conflict, the priority
order is:

1. `docs/API_CONTRACT.md`
2. `docs/DATA_MODEL.md`
3. `docs/WORKFLOW.md`
4. `docs/MVP_SCOPE.md`
5. `docs/CODING_STANDARDS.md`
6. `docs/UI_REQUIREMENTS.md`
7. Stitch-generated UI design and frontend code

## Stitch to Codex Workflow

Frontend implementation should follow this workflow:

1. Generate or update the UI screens in Stitch.
2. Connect Stitch context to Codex through MCP when available.
3. Ask Codex to implement the frontend based on the Stitch UI.
4. Codex must compare the Stitch design with existing project rules before coding.
5. Codex must not blindly copy Stitch-generated code if it conflicts with project architecture.
6. Codex must keep API calls, state handling, validation, and error handling
   consistent with backend contracts.
7. After implementation, Codex must run frontend checks and provide a summary of
   completed pages.

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

English may only be used in code, API fields, database fields, logs, and developer-facing documentation.

## Frontend Implementation Rules

The frontend must use:

- React
- TypeScript
- Vite

Codex must preserve the modular frontend structure and must not put all page logic into a single file.

Each major dashboard area should have its own page or feature folder.

## MVP Dashboard Pages

The MVP dashboard should include UI screens for:

1. Company Profile
2. Source Input for current text and URL backend scope
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

## Stitch Design Consistency

When implementing a Stitch-generated screen, Codex must preserve:

- Page layout
- Main navigation structure
- Card/table/dialog structure
- Button placement
- Visual hierarchy
- Spacing intention
- User flow

Codex may adjust implementation details only when required by:

- API contract
- TypeScript correctness
- accessibility
- responsive behavior
- project coding standards

## Completion Check

After frontend implementation, Codex must report:

- Which Stitch screens were implemented
- Which frontend files were changed
- Which API endpoints are connected
- Which UI text is shown in Chinese
- Which checks or tests passed
- Any mismatch between Stitch design and implemented UI
