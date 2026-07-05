# MVP Scope

## Purpose

This document defines what belongs to the first version and what must be excluded.

The goal is to keep the MVP focused, buildable, testable, and deployable.

## MVP Goal

The MVP should prove one core value:

A user can provide company information, create a product-based campaign,
discover potential B2B leads, receive AI customer-fit judgments with reasons,
approve leads, and generate Gmail draft outreach emails.

## Must Have

The MVP must include the following:

### 1. Company Profile

- Create company profile
- Store basic company information
- Store company website and description

### 2. Source Input

- Add company source information
- Support simple text or URL input
- Store source records
- Treat uploaded documents, PDF parsing, Word parsing, image OCR, file storage,
  document parsing, and crawler processing as future scope unless explicitly
  requested later

### 3. AI Knowledge Draft

- Generate structured knowledge draft from source information
- Save draft result
- Allow user review

### 4. Confirmed Knowledge

- Allow user to confirm useful knowledge
- Confirmed knowledge becomes the reliable input for later steps

### 5. Product Card

- Generate Product Cards from confirmed knowledge and allow users to add
  products manually
- Link product card to company
- Use confirmed knowledge as reference
- Keep only `draft` and `confirmed` Product Card statuses; deletion does not create `rejected`
- Allow draft cards to be edited, confirmed, or deleted
- Allow confirmed cards to be edited, used by Campaign, or deleted only when no Campaign has referenced them
- Keep edit-save behavior separate from `draft -> confirmed` confirmation

### 6. Campaign

- Create campaign from a confirmed product card
- Require the Product Card to belong to the same company / workspace scope
- Define target market, target industry, target customer type, and search criteria
- Allow AI to suggest campaign content
- Keep Campaign status limited to `draft`, `confirmed`, and `archived`
- Allow draft Campaigns to be viewed, edited, deleted, or confirmed
- Save `product_card_snapshot` when a draft Campaign is confirmed
- Allow confirmed Campaigns to be viewed, archived, and used for Lead Discovery
- Do not allow confirmed Campaigns to be edited, deleted, or returned to draft
- Treat repeated confirm on an already confirmed Campaign as idempotent
- Treat archived Campaigns as read-only history that cannot be edited, deleted,
  restored, or used for new Lead Discovery
- Support duplicate / copy as draft for Campaign reuse instead of editing a
  confirmed Campaign or restoring an archived Campaign

### 7. Lead Discovery

- Search for candidate companies based on campaign
- Store discovered leads
- Store source URL and website

### 8. Lead Validation

- Normalize company name and website
- Remove duplicates
- Check website availability
- Filter obvious invalid leads

### 9. Lead Scoring

- Score valid leads with AI
- Generate fit score
- Generate matching reasons
- Generate risk notes
- Generate recommendation status

### 10. Lead Review

- Show lead results to user
- Allow user to approve or reject leads
- Allow user to view score reasons and evidence

### 11. Gmail Draft

- Generate email draft for approved leads
- Create Gmail draft only
- Store draft status
- User manually reviews and sends from Gmail
- Use only the minimum OAuth scope needed to create Gmail drafts, such as
  `gmail.compose`
- Do not read, sync, move, delete, label, or modify the user's existing mailbox
  contents

### 12. Task Status

- Record background task status
- Show whether tasks are pending, running, completed, or failed
- Keep task execution status separate from Campaign status. Runtime states such
  as running, paused, completed, failed, or cancelled belong to future
  LeadDiscoveryJob / CampaignJob / task records, not to `campaigns.status`

## Should Have

The MVP should include if practical:

- Simple dashboard
- Lead detail page
- Basic error messages
- Basic task logs
- AI provider abstraction
- Search provider abstraction
- Crawler provider abstraction
- Gmail provider abstraction
- Basic automated tests

## Could Have

These features are optional for MVP:

- More advanced filtering
- Simple analytics
- Export lead list
- Manual note field for leads
- Contact form detection
- Email finder integration

## Must Not Have

The MVP must not include:

- Full account system
- Team workspace permission system
- Payment system
- Full CRM pipeline
- Automatic email sending
- Bulk email sending
- LinkedIn API
- LinkedIn scraping
- LinkedIn crawler
- LinkedIn bot
- LinkedIn browser automation
- LinkedIn browser extension automation
- Automated LinkedIn login
- Automated LinkedIn search
- Automated LinkedIn profile extraction
- Automated LinkedIn contact downloading
- Automated LinkedIn messaging
- Automated LinkedIn connection requests
- Google Sheets workflow
- Multi-agent architecture
- LangGraph workflow
- Complex RAG system as a hard dependency
- Advanced analytics dashboard
- Email reply tracking, reply monitoring, inbox sync, or follow-up automation

## Account System Rule

The first version is a single-user MVP / prototype.

However, database and backend design should keep future expansion in mind.

Where reasonable, keep fields such as:

- `owner_id`
- `workspace_id`
- `created_by`

These fields may be nullable or simple placeholders in MVP.

Do not build full authentication unless explicitly requested.

## Database Rule

The MVP uses PostgreSQL from the beginning.

Do not use SQLite as the main database.

Use Alembic for migrations.

## Email Rule

The MVP only creates Gmail drafts.

The system must not send emails automatically.

Gmail Draft is not full email automation and not a complete Gmail integration.
The system must not request `gmail.send`, `gmail.modify`, mailbox read, inbox
sync, move, delete, label, reply tracking, or reply monitoring permissions or
features.

## AI Rule

AI can suggest, draft, classify, score, and explain.

AI cannot make final outreach decisions.

The user must review and approve leads and email drafts.

## LinkedIn Rule

LinkedIn is out of scope for MVP automation.

- The MVP must not use the LinkedIn API.
- The MVP must not perform LinkedIn scraping, LinkedIn crawling, LinkedIn bot
  behavior, LinkedIn browser automation, or LinkedIn browser extension
  automation.
- The MVP must not perform automated LinkedIn login, automated LinkedIn search,
  automated LinkedIn profile extraction, automated LinkedIn contact downloading,
  automated LinkedIn messaging, or automated LinkedIn connection requests.
- A LinkedIn URL may only be manually provided by the user or stored as a manual
  review reference.
- A LinkedIn URL or LinkedIn contact reference must not be used as Gmail Draft
  eligibility or as a Gmail Draft recipient.
