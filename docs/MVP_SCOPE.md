# MVP Scope

## Purpose

This document defines what belongs to the first version and what must be excluded.

The goal is to keep the MVP focused, buildable, testable, and deployable.

## MVP Goal

The MVP should prove one core value:

A user can provide company information, create a product-based campaign, discover potential B2B leads, receive AI customer-fit judgments with reasons, approve leads, and generate Gmail draft outreach emails.

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

### 3. AI Knowledge Draft

- Generate structured knowledge draft from source information
- Save draft result
- Allow user review

### 4. Confirmed Knowledge

- Allow user to confirm useful knowledge
- Confirmed knowledge becomes the reliable input for later steps

### 5. Product Card

- Generate Product Cards from confirmed knowledge and allow users to add products manually
- Link product card to company
- Use confirmed knowledge as reference
- Keep only `draft` and `confirmed` Product Card statuses; deletion does not create `rejected`
- Allow draft cards to be edited, confirmed, or deleted
- Allow confirmed cards to be edited, used by Campaign, or deleted only when no Campaign has referenced them
- Keep edit-save behavior separate from `draft -> confirmed` confirmation

### 6. Campaign

- Create campaign from a confirmed product card
- Define target market, target industry, target customer type, and search criteria
- Allow AI to suggest campaign content
- Allow user to edit and confirm campaign

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

### 12. Task Status

- Record background task status
- Show whether tasks are pending, running, completed, or failed

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
- LinkedIn automation
- LinkedIn browser-extension automation
- Automatic LinkedIn messaging, connection requests, profile scraping, or contact downloading
- Google Sheets workflow
- Multi-agent architecture
- LangGraph workflow
- Complex RAG system as a hard dependency
- Advanced analytics dashboard
- Complex email reply tracking

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

## AI Rule

AI can suggest, draft, classify, score, and explain.

AI cannot make final outreach decisions.

The user must review and approve leads and email drafts.

## LinkedIn Rule

LinkedIn is out of scope for MVP automation.

- The MVP must not use the LinkedIn API.
- The MVP must not perform automated LinkedIn crawling or scraping.
- The MVP must not use Playwright, Selenium, browser extensions, or bots to automatically access LinkedIn.
- A LinkedIn URL may only be manually provided by the user or stored as a manual review reference.
- A LinkedIn URL or LinkedIn contact reference must not be used as Gmail Draft eligibility or as a Gmail Draft recipient.
