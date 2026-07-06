# Workflow

## Purpose

This document defines the main end-to-end workflow of the system.

The workflow should remain simple and focused for MVP.

## Main Workflow

### Step 1: Create Company Profile

The user creates a company profile.

The company profile stores basic information such as:

- Company name
- Website
- Industry
- Description
- Target market

### Step 2: Add Company Information

The user adds company information.

Current implemented backend inputs:

- Website URL
- Text description
- Manual notes saved as text

Future source-input scope unless explicitly requested later:

- Uploaded documents
- PDF or Word document parsing
- Image OCR
- File storage
- Crawler processing of URL contents

The system stores the input as source data.

The current backend source slice stores text and URL records only. A stored URL
does not imply that a crawler has fetched or parsed the website.

### Step 3: Generate AI Knowledge Draft

The system uses AI to analyze the company source information.

The AI generates a structured knowledge draft.

The draft may include:

- Company summary
- Products or services
- Target customers
- Pain points solved
- Differentiation
- Sales talking points
- Use cases

### Step 4: User Reviews Knowledge

The user reviews the AI-generated knowledge draft.

The user can:

- Confirm useful knowledge
- Edit knowledge
- Reject incorrect knowledge

Only confirmed knowledge should be used in later steps.

### Step 5: Create and Review Product Card

A Product Card may be generated from confirmed knowledge or added manually by
the user.

The frontend must keep a permanent `手动添加产品` entry; AI generation is not the
only creation path. Both sources start in `draft`, and only a `confirmed`
Product Card may be used by a Campaign.

The product card explains:

- What the product is
- Who it is for
- What problem it solves
- Why customers may care
- Key selling points

Product Card lifecycle and editing rules:

- A draft Product Card may be edited, confirmed, or deleted.
- A confirmed Product Card may be edited, deleted when unreferenced, or used by a
  Campaign; it must not show a confirmation button.
- Repeating the confirm request for an already confirmed Product Card is idempotent and leaves it confirmed.
- Selecting a Product Card opens a details dialog where fields can be edited directly.
- When fields have changed, the dialog shows `取消` and `保存修改`.
- `取消` discards unsaved frontend state and does not call the save API.
- `保存修改` calls `PATCH /api/v1/product-cards/{id}` and does not change Product Card status.
- `确认产品卡片` means `draft -> confirmed`; it is separate from saving edited fields.
- Deletion never creates a Product Card `rejected` status.
- A confirmed Product Card already referenced by a Campaign cannot be physically
  deleted and returns HTTP `409`.

Product Card scope note:

- The current MVP is a single-user prototype, and each Product Card belongs to a company.
- Campaign creation and confirmation already validate that the selected Product
  Card is confirmed and belongs to the same company as the Campaign.
- Product Card route-level get, patch, confirm, and delete company/workspace
  authorization remains planned hardening.
- Future workspace or multi-tenant support must extend this boundary to workspace ownership.
- This is not a claim that Product Card route-level account or workspace
  authorization is already implemented.

### Step 6: Create Campaign

The user selects a confirmed product card and creates a sales campaign.

The campaign defines:

- Target country or region
- Target industry
- Target company type
- Target customer role
- Search criteria
- Qualification criteria
- Outreach angle
- Number of leads to find

AI may suggest campaign content, but it starts as a `draft` Campaign and must be
reviewed by the user.

Campaign lifecycle rules:

- A new Campaign defaults to `draft`.
- A `draft` Campaign can be viewed, edited, deleted, or confirmed.
- A `draft` Campaign cannot be used for formal Lead Discovery before it is
  confirmed.
- Confirming a `draft` Campaign requires the backend to revalidate that the
  linked Product Card exists, belongs to the same company / workspace scope, and
  has `status = confirmed`.
- When a Campaign becomes `confirmed`, the backend saves
  `product_card_snapshot` as a historical copy of the confirmed Product Card
  business fields that affect matching or outreach generation.
- A `confirmed` Campaign can be viewed, archived, and used for Lead Discovery.
- A `confirmed` Campaign cannot be edited, deleted, or returned to `draft`.
- Repeating confirm on an already `confirmed` Campaign is idempotent and leaves
  it confirmed.
- An `archived` Campaign is a read-only historical record. It may appear in the
  default Campaign list / `全部` view or through an explicit archived filter, but
  it cannot be edited or deleted, cannot be restored, and cannot be used for new
  Lead Discovery.
- If the user wants to reuse a similar `confirmed` Campaign, the workflow is
  duplicate / copy as draft. The copied Campaign receives a new `id`, starts as
  `draft`, can be edited, and must revalidate the current Product Card when it
  is confirmed.

Campaign status is limited to `draft`, `confirmed`, and `archived`. Runtime
states such as `pending`, `running`, `paused`, `completed`, `failed`, and
`cancelled` belong to future Lead Discovery / Campaign Job records, not to the
Campaign configuration itself.

### Step 7: Discover Candidate Leads

The system searches for potential customer companies based on the confirmed
campaign. Lead Discovery should use the Campaign configuration and the
`product_card_snapshot` captured at Campaign confirmation time.

The system may use:

- Search provider
- Crawler provider
- Company website parser

The system stores candidate leads.

### Step 8: Validate Leads

The system performs basic lead validation before AI scoring.

Validation includes:

- Normalize company name
- Normalize website URL
- Remove duplicates
- Check whether website is reachable
- Check whether content is sufficient
- Filter obvious mismatch

Invalid leads should not be sent to AI scoring.

### Step 9: Analyze Lead Website

For valid leads, the system collects and summarizes useful website information.

The system should extract information such as:

- Company description
- Products or services
- Target customers
- Industry
- Business model
- Possible pain points
- Relevant evidence

### Step 10: AI Customer Matching Score

The system uses AI to compare the lead with:

- Confirmed company knowledge
- Product card
- Campaign criteria
- Lead website information

The AI generates:

- Fit score
- Recommendation level
- Matching reasons
- Website evidence
- Risk notes
- Suggested outreach angle

### Step 11: Show Lead Results

The system shows the user all useful lead results.

The user should be able to see:

- Recommended leads
- Maybe leads
- Not recommended leads
- Score
- Reasons
- Evidence
- Risk notes

The default view may prioritize recommended leads, but the user should be able to inspect other results.

### Step 12: User Reviews Leads

The user decides which leads should be contacted.

The user can mark leads as:

- Approved
- Rejected
- Needs manual review

Only approved leads can generate Gmail drafts.

### Step 13: Generate Outreach Draft

For approved leads, the system generates an outreach email draft.

Gmail Draft eligibility must use a selected valid email contact:

- the frontend passes `contact_id`
- the backend verifies that `contact_id` belongs to the approved lead
- `contacts.contact_type = email`
- `contacts.status = valid`
- `outreach_drafts.contact_id` stores the selected contact after validation

A LinkedIn reference, contact form, phone, manual review contact, or lead-level
email-like field must not make a lead eligible for Gmail Draft creation.

The draft should be based on:

- Product card
- Campaign
- Confirmed company knowledge
- Lead information
- Matching evidence
- Outreach angle

The system saves the draft and creates a Gmail draft.

### Step 14: User Sends Email Manually

The user reviews the draft in Gmail.

The user manually sends, edits, or deletes the email.

The system must not automatically send emails.

The system must not read or sync the inbox, track replies, monitor replies,
move, delete, label, or modify existing Gmail messages. Gmail Draft creation is
not complete Gmail automation.

### Step 15: Record Status

The system records statuses such as:

- Lead discovered
- Lead scored
- Lead approved
- Draft generated
- Draft failed
- User rejected

## Frontend and Backend Development Workflow

Backend and frontend work should move in synchronized phase numbers, while
keeping their responsibilities separate.

1. At the start of each phase, backend work defines the API contract, data model,
   business rules, validation rules, and allowed status transitions.
2. Frontend workflow design must be based on the current phase backend contract,
   data model, and business rules.
3. The user manually designs UI screens in Stitch.
4. Stitch is a visual and interaction reference. It does not define backend
   business logic or override project rules.
5. Backend implementation can continue independently of Stitch UI design once
   the API contract, data model, and business rules are clear.
6. Campaign frontend implementation requires Stitch Campaign design context.
   Without Stitch Campaign screens or authorized Stitch context, Codex must not
   implement a conservative fallback Campaign UI.
7. Codex implements frontend pages from project rules, current phase API
   contract, data model, business rules, `docs/UI_REQUIREMENTS.md`, and required
   Stitch design context.
8. Codex must not freely redesign UI unless explicitly requested.
9. Codex must not show or imply frontend features that the current backend API
   contract does not support.
10. Frontend and backend phases should be synchronized by phase number. For
    example, Backend Phase 3 is Campaign backend/API/data contract work, and
    Frontend Phase 3 is Campaign frontend UI work.
11. All user-facing frontend text must be Chinese.

## Workflow Rules

1. AI-generated knowledge must be reviewed before becoming confirmed knowledge.
2. Campaigns must be based on confirmed product cards from the same company /
   workspace scope.
3. Lead scoring must be based on confirmed campaign information and the
   Campaign's confirmed-time Product Card snapshot.
4. Invalid leads should not be scored by AI.
5. Email drafts can only be generated for approved leads with a selected valid
   email contact.
6. Gmail draft creation must not automatically send email.
7. Gmail access must stay limited to draft creation, with minimum OAuth scope
   such as `gmail.compose`.
8. All major steps should store status and error information.
