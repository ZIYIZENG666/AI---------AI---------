# Product Requirements

## Purpose

This document defines the main product requirements for the MVP.

The product should help users build a company sales knowledge base, create
product cards, run campaigns, discover leads, evaluate customer fit, and
generate Gmail draft outreach emails.

## Main User Journey

The user should be able to:

1. Create a company profile.
2. Add company information.
3. Let AI extract structured knowledge.
4. Review and confirm the knowledge.
5. Create product cards.
6. Create a campaign based on a product card.
7. Search for potential customer companies.
8. Analyze candidate company websites.
9. Score whether each company is a good customer match.
10. Review recommended and non-recommended leads.
11. Approve leads for outreach.
12. Generate Gmail draft emails.
13. Manually review and send emails in Gmail.

## Core Features

### 1. Company Profile

The system should allow the user to create and manage basic company information.

Company information may include:

- Company name
- Website
- Industry
- Description
- Target market
- Value proposition

### 2. Company Information Input

The system should support company information input through simple MVP-friendly
methods.

Current implemented backend scope:

- Website URL
- Plain text
- Manual form input saved as text

The system should store source information for later reference.

Current backend boundary:

- The current source input backend slice stores text and URL source records only.
- A URL source records the URL and optional user-provided content; it does not
  mean a crawler has fetched or processed the page.
- Uploaded documents, PDF parsing, Word parsing, image OCR, file storage,
  document parsing, and crawler processing are future scope unless explicitly
  requested later.

### 3. AI Knowledge Draft

The system should use AI to extract structured knowledge from company materials.

The draft should include useful sales knowledge such as:

- What the company does
- Main products or services
- Target customers
- Pain points solved
- Key strengths
- Differentiation
- Use cases
- Sales talking points

The draft must be reviewed by the user before becoming confirmed knowledge.

### 4. Confirmed Knowledge Base

The user should be able to confirm, edit, or reject AI-generated knowledge.

Only confirmed knowledge should be used as reliable input for product cards,
campaigns, scoring, and outreach drafts.

### 5. Product Card

The system should allow the user to create product cards based on confirmed knowledge.

A product card may include:

- Product name
- Product description
- Target customer
- Problems solved
- Use cases
- Key benefits
- Differentiation
- Proof points

### 6. Campaign

The system should allow the user to create a sales campaign from a confirmed
Product Card that belongs to the same company / workspace scope.

A campaign may include:

- Selected product card
- Product Card snapshot captured at confirmation
- Target country or region
- Target industry
- Target company type
- Target customer role
- Search keywords
- Qualification criteria
- Number of leads to discover
- Outreach angle

The AI may suggest a campaign, but AI suggestions start as draft content and
must be reviewed by the user.

Campaign status values are limited to:

- `draft`
- `confirmed`
- `archived`

Campaign lifecycle requirements:

- New Campaigns default to `draft`.
- Draft Campaigns can be viewed, edited, deleted, or confirmed.
- Draft Campaigns cannot be used for formal Lead Discovery before confirmation.
- Confirming a Campaign requires Product Card validation: the Product Card must
  exist, belong to the same company / workspace scope, and have
  `status = confirmed`.
- Confirming a Campaign saves `product_card_snapshot` so future Lead Discovery
  uses the product meaning that was confirmed at that time.
- Confirmed Campaigns can be viewed, archived, and used for Lead Discovery.
- Confirmed Campaigns cannot be edited, deleted, or returned to draft.
- Repeating confirm on an already confirmed Campaign is idempotent and should
  keep the Campaign confirmed.
- Archived Campaigns are read-only history. They cannot be edited, deleted,
  restored, or used for new Lead Discovery. They may appear in the default
  Campaign list / `全部` view alongside draft and confirmed Campaigns, and the
  UI may also provide an explicit archived filter.
- Reusing a similar confirmed Campaign should use duplicate / copy as draft. The
  copy gets a new ID, starts as draft, can be edited, and must revalidate the
  current Product Card when later confirmed.

Campaign runtime execution states such as running, paused, completed, failed,
or cancelled belong to future Lead Discovery / Campaign Job records. They must
not be mixed into Campaign status.

### 7. Lead Discovery

The system should search for candidate companies based on the confirmed campaign.

The MVP may use search APIs and crawler providers through abstraction.

The system should collect basic lead information such as:

- Company name
- Website
- Description
- Country or region
- Industry
- Source URL

### 8. Lead Validation

Before AI scoring, the system should perform basic validation.

Validation may include:

- Company name normalization
- Website normalization
- Duplicate checking
- Website availability check
- Basic content sufficiency check
- Obvious mismatch filtering

Only valid leads should continue to AI scoring.

### 9. Customer Matching Score

The system should use AI to score whether a lead is a good match for the selected product and campaign.

The score should include:

- Fit score
- Matching reasons
- Evidence from website or source
- Risk notes
- Recommended action

The score must not be a black box.

### 10. Lead Review

The user should be able to review leads before outreach.

AI recommendation and human review status must be treated as separate concepts.

AI recommendation may include:

- Recommended
- Maybe
- Not recommended
- Needs manual review

Human review status may include:

- Unreviewed
- Approved
- Rejected
- Needs manual review

The AI recommendation is generated by the system to help the user understand whether a lead appears suitable for the campaign.

The human review status represents the user's final decision on whether the lead can proceed to outreach.

Only leads with human review status = Approved can proceed to outreach draft generation or Gmail Draft creation.

Recommended leads are not automatically approved. The user must explicitly approve a lead before outreach.

### 11. Outreach Draft

For approved leads, the system should generate a Gmail draft.

Gmail Draft eligibility must be based on a selected valid email contact:

- the frontend passes `contact_id`
- the backend verifies that `contact_id` belongs to the approved lead
- `contacts.contact_type = email`
- `contacts.status = valid`
- `outreach_drafts.contact_id` stores the selected contact after validation

A LinkedIn reference, contact form, phone, manual review contact, or lead-level
email-like field must not be used as Gmail Draft eligibility.

The email draft should be based on:

- Confirmed company knowledge
- Product card
- Campaign
- Lead information
- Website evidence
- Matching reasons

The system must not automatically send emails.

Gmail Draft does not mean email automation or complete Gmail integration. The
system must not read or sync the inbox, track replies, monitor replies, move,
delete, label, or modify existing Gmail messages, or request `gmail.send` or
`gmail.modify` permissions. OAuth scope must be limited to the minimum
draft-creation permission, such as `gmail.compose`.

### 12. Task Tracking

The system should record task execution status.

Useful task information includes:

- Task type
- Task status
- Started time
- Finished time
- Error message
- Related campaign
- Related lead

## MVP UI Requirements

The MVP should provide a simple web dashboard.

The dashboard should support:

- Company profile management
- Knowledge review
- Product card management
- Campaign creation
- Campaign list and detail behavior that follows `draft`, `confirmed`, and
  `archived` permissions
- Lead results page
- Lead detail page
- Outreach draft status

The UI does not need to be highly complex, but it should be clear and usable.

All user-facing Campaign UI text, including page titles, buttons, status labels,
empty states, errors, success messages, and confirmation dialogs, must be
Chinese.

## Out of Scope for MVP

The MVP should not include:

- Full account registration and login system
- Team permission management
- Full CRM pipeline
- Automatic email sending
- Email reply tracking, reply monitoring, inbox sync, or follow-up automation
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
- Google Sheets integration
- Complex analytics dashboard
- Payment system
- Multi-agent workflow

Allowed LinkedIn boundary:

- A user may manually paste a public LinkedIn URL as a reference only.
- The system may store that URL as a manual reference.
- The system must not access, scrape, automate, enrich, or extract data from LinkedIn.
- A LinkedIn URL must not be used as a Gmail Draft recipient or as Gmail Draft
  eligibility.
