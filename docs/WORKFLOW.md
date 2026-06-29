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
- Before Campaign and later downstream records rely on a Product Card, access should be hardened to preserve the same company boundary.
- Future workspace or multi-tenant support must extend this boundary to workspace ownership.
- This is planned hardening, not a claim that account or workspace authorization is already implemented.

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

AI may suggest campaign content, but the user must be able to edit and confirm it.

### Step 7: Discover Candidate Leads

The system searches for potential customer companies based on the confirmed campaign.

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

## Frontend Implementation Workflow

Major frontend pages should be designed in Stitch first when available, then
implemented by Codex according to `docs/UI_REQUIREMENTS.md` and existing project
rules.

## Workflow Rules

1. AI-generated knowledge must be reviewed before becoming confirmed knowledge.
2. Campaigns must be based on product cards.
3. Lead scoring must be based on confirmed campaign and product information.
4. Invalid leads should not be scored by AI.
5. Email drafts can only be generated for approved leads with a selected valid
   email contact.
6. Gmail draft creation must not automatically send email.
7. Gmail access must stay limited to draft creation, with minimum OAuth scope
   such as `gmail.compose`.
8. All major steps should store status and error information.
