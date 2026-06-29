# Module Boundaries

## Purpose

This document defines the responsibilities and boundaries of each backend module.

The goal is to keep the codebase modular, understandable, and easy to change.

## General Rule

Each module should own its own business logic.

A module should not directly modify another module's internal data unless done
through a service or clear interface.

Routes should call services.

Services may coordinate with other services.

Repositories should only handle database access.

Providers should handle external service calls.

## Modules

## company

### Responsibility

The company module manages the user's own company profile.

It handles:

- Company profile creation
- Company profile update
- Company website
- Company description
- Basic company metadata

### Not Responsible For

It should not handle:

- AI knowledge extraction
- Lead discovery
- Campaign logic
- Gmail drafts

## sources

### Responsibility

The sources module manages raw company input materials.

Current implemented backend scope:

- Source text
- Source URL
- Source processing status

Future scope unless explicitly requested later:

- Uploaded document metadata
- PDF or Word document parsing
- Image OCR
- File storage
- Crawler processing of URL contents

### Not Responsible For

It should not decide final knowledge.

It should not run customer scoring.

It should not parse uploaded files, run OCR, store file blobs, or crawl URLs in
the current backend slice.

## knowledge

### Responsibility

The knowledge module manages AI-generated and user-confirmed company knowledge.

It handles:

- AI knowledge draft
- Knowledge review status
- Confirmed knowledge
- Rejected knowledge
- Knowledge categories

### Not Responsible For

It should not handle lead discovery.

It should not create outreach emails directly.

## products

### Responsibility

The products module manages product cards.

It handles:

- Product card generation from confirmed knowledge and manual creation
- Product card ownership by company
- Product card `draft -> confirmed` lifecycle
- Product card editing and deletion rules
- Product positioning
- Target customer description
- Pain points solved
- Benefits
- Differentiation

### Not Responsible For

It should not search leads directly.

It should not send emails.

### Scope Ownership

The `products` module owns Product Card scope validation.

- The current Phase 2 slice is single-user and stores `company_id` on every Product Card.
- ID-only get, patch, confirm, and delete lookups are not the final authorization model.
- Planned hardening should first require `product_card_id + company_id` in
  repository/service lookup semantics.
- Future workspace support should extend this to `product_card_id + company_id + workspace_id`.
- Campaign and later modules must not consume a Product Card from another company or workspace.
- The `products` service must protect Campaign references before deletion; route
  handlers must not perform the reference query or deletion decision directly.
- Product Card reject/rejected behavior is outside this module contract. Deletion is the only removal operation.
- This boundary does not require implementing accounts or workspace permissions in the current documentation task.

## campaigns

### Responsibility

The campaigns module manages sales campaigns.

It handles:

- Campaign creation
- Campaign criteria
- Target country or region
- Target industry
- Search keywords
- Qualification criteria
- Outreach angle
- Campaign status

### Not Responsible For

It should not crawl websites directly.

It should not generate Gmail drafts directly.

## discovery

### Responsibility

The discovery module finds candidate leads.

It handles:

- Search query generation
- Search provider usage
- Candidate company collection
- Source URL collection
- Initial lead creation

### Not Responsible For

It should not perform final AI scoring.

It should not approve leads.

It should not generate outreach drafts.

## intelligence

### Responsibility

The intelligence module collects and processes lead website information.

It handles:

- Website crawling
- Website text extraction
- Company website summary
- Evidence extraction
- Content sufficiency check

### Not Responsible For

It should not decide final lead approval.

It should not generate Gmail drafts.

## qualification

### Responsibility

The qualification module scores and judges lead fit.

It handles:

- AI lead scoring
- Matching reasons
- Risk notes
- Recommendation level
- Fit explanation
- Evidence-based judgment

### Not Responsible For

It should not search new leads.

It should not create Gmail drafts directly.

It should not approve leads on behalf of the user.

## reviews

### Responsibility

The reviews module manages user review decisions.

It handles:

- Lead approval
- Lead rejection
- Manual review status
- Review notes

### Not Responsible For

It should not calculate AI scores.

It should not crawl websites.

## contacts

### Responsibility

The contacts module manages lead contact information.

It handles:

- Email contact records
- Contact page URL
- Contact person information if available
- Contact source
- Contact validation status
- User-provided LinkedIn URL as a manual reference only

Gmail Draft eligibility must be based on a selected valid email contact:

- the frontend passes `contact_id`
- the backend verifies that `contact_id` belongs to the approved lead
- `contacts.contact_type = email`
- `contacts.status = valid`
- `outreach_drafts.contact_id` stores the selected contact after validation

Contact forms, phone numbers, LinkedIn references, manual review contacts,
invalid email contacts, unselected contacts, and lead-level email-like fields
must not be treated as Gmail Draft recipients.

### Not Responsible For

It should not send emails.

It should not score leads.

It should not use LinkedIn API, scraping, crawler, bot, browser automation,
browser extension automation, automated login, automated search, automated
profile extraction, automated contact downloading, automated messaging, or
automated connection requests.

## outreach

### Responsibility

The outreach module manages outreach draft generation.

It handles:

- Email draft generation
- Gmail draft creation
- Draft status
- Draft subject and body
- Gmail draft ID

It may create Gmail drafts only for approved leads with a selected valid email
contact.

### Not Responsible For

It should not automatically send emails.

It should not read or sync the inbox, track replies, monitor replies, move,
delete, label, or modify existing Gmail messages.

Gmail Draft creation is not complete Gmail integration or email automation.

It should not approve leads.

It should not discover new leads.

It should not use a LinkedIn reference, contact form, phone number, manual
review contact, invalid email contact, unselected contact, or lead-level
email-like field as Gmail Draft eligibility.

## LinkedIn Boundary

The MVP must not contain a LinkedIn Provider, LinkedIn Adapter, LinkedIn
Crawler, LinkedIn Scraper, LinkedIn Bot, or LinkedIn Automation module.

Discovery, intelligence (crawler behavior), contacts, outreach, and AI services
must not automatically access LinkedIn.

The MVP must not perform:

- LinkedIn API access
- LinkedIn scraping
- LinkedIn crawler behavior
- LinkedIn bot behavior
- LinkedIn browser automation
- LinkedIn browser extension automation
- Automated LinkedIn login
- Automated LinkedIn search
- Automated LinkedIn profile extraction
- Automated LinkedIn contact downloading
- Automated LinkedIn messaging
- Automated LinkedIn connection requests

Allowed boundary:

- Only the `contacts` module may store a user-provided LinkedIn URL as a manual reference.
- Only the frontend may display a LinkedIn URL for human review.
- A LinkedIn URL must not be used as a Gmail Draft recipient or as Gmail Draft
  eligibility.

## tasks

### Responsibility

The tasks module manages background task tracking.

It handles:

- Task creation
- Task status
- Task logs
- Error messages
- Started and finished timestamps

### Not Responsible For

It should not contain business-specific logic from other modules.

## Cross-module Rules

1. A campaign can use product and knowledge data.
2. Discovery can use campaign criteria.
3. Intelligence can process leads created by discovery.
4. Qualification can use campaign, product, knowledge, and intelligence data.
5. Outreach can only generate drafts for approved leads.
6. Tasks can track long-running operations from any module.
7. User review must remain separate from AI scoring.
