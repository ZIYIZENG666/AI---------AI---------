# Data Model

## Purpose

This document defines the main data entities for the MVP.

The database should use PostgreSQL from the beginning.

Use Alembic for all database migrations.

## General Rules

1. Use UUID or stable IDs for main entities.
2. Include `created_at` and `updated_at` where appropriate.
3. Keep future account support in mind.
4. Where reasonable, include `owner_id` or `workspace_id` as nullable MVP placeholders.
5. Do not design around SQLite.
6. Do not store secrets in the database without proper protection.

## Constraint Naming and PostgreSQL Authority

Database constraints are part of the stable schema contract.

Rules:

1. A SQLAlchemy `CheckConstraint` and the Alembic migration that creates it must
   resolve to the same database constraint name.
2. Use `ck_<table_name>_<column_name>` for new status, type, and other enum-like
   checks, for example `ck_product_cards_status`.
3. Do not use one constraint name in ORM metadata and another in migration code.
4. Existing constraint declarations should be audited and normalized as Phase 3
   foundation hardening; this documentation update does not claim the code audit
   is complete.
5. PostgreSQL is authoritative for JSON/JSONB behavior, foreign keys, indexes,
   constraint names, and migration ordering.
6. SQLite `Base.metadata.create_all()` or in-memory tests do not validate the
   real Alembic/PostgreSQL schema.

## Main Entities

## company_profiles

Stores the user's own company information.

Main fields:

- `id`
- `owner_id`
- `workspace_id`
- `name`
- `website`
- `industry`
- `description`
- `target_market`
- `created_at`
- `updated_at`

Relationship:

- One company profile can have many sources.
- One company profile can have many knowledge items.
- One company profile can have many product cards.

## company_sources

Stores raw company input materials.

Main fields:

- `id`
- `company_id`
- `source_type`
- `title`
- `url`
- `raw_content`
- `status`
- `created_at`
- `updated_at`

Phase 1B supports these `source_type` values:

- `url`
- `text`

Source rules for Phase 1B:

- Text sources require `raw_content` and do not use `url`.
- URL sources require `url`; `raw_content` is optional because no crawler runs in this phase.
- New source records use `status = ready`.
- Uploaded documents, PDF parsing, Word parsing, image OCR, file storage,
  document parsing, and crawler processing are deferred.
- The current backend does not define document, PDF, Word, image, or uploaded
  file `source_type` values.

## knowledge_items

Stores AI-generated and user-confirmed knowledge.

Main fields:

- `id`
- `company_id`
- `source_id`
- `category`
- `title`
- `content`
- `status`
- `confidence`
- `created_at`
- `updated_at`

Possible `status`:

- `draft`
- `confirmed`
- `rejected`

Only confirmed knowledge should be used as reliable input for product cards,
campaigns, scoring, and outreach.

Phase 1B knowledge rules:

- Drafts created from a source keep that source in `source_id`.
- The current deterministic generator copies available source content without calling an LLM or crawler.
- `confidence` remains null for deterministic drafts because no AI confidence is inferred.
- Only a `draft` item may transition to `confirmed` or `rejected`.
- Company knowledge lists may be filtered by status so confirmed knowledge remains separate from unreviewed drafts.

## product_cards

Stores product or service cards.

Main fields:

- `id`
- `company_id`
- `name`
- `description`
- `target_customer`
- `pain_points`
- `value_proposition`
- `use_cases`
- `differentiators`
- `source_knowledge_item_ids`
- `source_type`
- `status`
- `created_at`
- `updated_at`

Possible `status`:

- `draft`
- `confirmed`

Allowed `source_type`:

- `ai_generated`
- `manual`

`confirmed` 表示用户已确认，可用于后续 Campaign 与 Outreach。

Phase 2 product card rules:

- Product cards are generated only from the company's confirmed knowledge items.
- Draft and rejected knowledge items must not appear in
  `source_knowledge_item_ids` or generated content.
- `pain_points`, `use_cases`, `differentiators`, and
  `source_knowledge_item_ids` are stored as JSON lists.
- The deterministic generator maps recognized knowledge categories into
  structured fields and does not call an LLM or external API.
- AI-generated Product Cards start with `source_type = ai_generated` and `status = draft`.
- User-created Product Cards start with `source_type = manual` and `status = draft`.
- User-created Product Cards must include `company_id`, and the backend must
  verify that the company exists. Product Cards must not exist without a
  company.
- A Product Card may transition only from `draft` to `confirmed`; repeating
  confirmation on `confirmed` leaves it unchanged.
- Editing a Product Card does not change its status. Unsaved edits are frontend
  state and must not create database statuses such as `editing`, `modified`, or
  `pending_changes`.
- Editing a Product Card must not change `company_id`, `source_type`, `status`,
  or `source_knowledge_item_ids`.
- Deleting a Product Card does not create a `rejected` record or status.
- Only confirmed product cards should become inputs for the later campaign workflow.
- A confirmed Product Card may be physically deleted only when no Campaign has
  ever referenced it.
- `ck_product_cards_status` must allow only `draft` and `confirmed`; a
  source-type check constraint must allow only `ai_generated` and `manual`.

Product Card scope plan:

- The current Product Card model belongs to a company through `company_id` in
  the single-user MVP.
- Campaign creation and confirmation already consume Product Cards through
  same-company validation: a Campaign may use only a confirmed Product Card
  from its own company.
- Product Card deletion checks whether a Campaign has referenced the Product
  Card before physical deletion.
- Product Card route-level get, patch, confirm, and delete lookups are still
  ID-only in the current single-user MVP contract. They are provisional and
  must not be treated as the final ownership model.
- Planned route-level repository/service lookups should require
  `product_card_id + company_id` for get, patch, confirm, and delete operations.
- Future workspace support should add and enforce `workspace_id`, producing
  `product_card_id + company_id + workspace_id` scope semantics.
- No route-level Product Card company/workspace authorization, workspace
  ownership field, or multi-tenant authorization is claimed as implemented yet.

Product Card AI output mapping note:

- AI output may include fields such as `product_name`, `unsuitable_customers`,
  `keywords`, or `evidence_sources`.
- Those fields describe the AI output schema, not direct database columns unless
  they are listed in this `product_cards` section.
- Service logic must map AI output into the Product Card draft fields before
  persistence.
- The persisted Product Card status remains only `draft` or `confirmed`; there
  is no `rejected` Product Card status and no Product Card reject endpoint.

## campaigns

Stores sales campaigns.

Main fields:

- `id`
- `company_id`
- `product_card_id`
- `product_card_snapshot`
- `name`
- `target_country`
- `target_region`
- `target_industry`
- `target_company_type`
- `target_role`
- `search_keywords`
- `qualification_criteria`
- `outreach_angle`
- `lead_limit`
- `status`
- `created_at`
- `updated_at`

Possible `status`:

- `draft`
- `confirmed`
- `archived`

`confirmed` 表示用户已确认，可进入 lead discovery。

`archived` 表示只读历史记录。Archived Campaigns cannot be edited, deleted,
restored, or used for new Lead Discovery.

Campaign field rules:

- `product_card_id` is the required Product Card link.
- `product_card_snapshot` is a JSON/JSONB historical copy saved when a Campaign
  transitions from `draft` to `confirmed`. It is not a foreign key and should
  contain only core Product Card business fields that affect matching or
  outreach generation, such as product name, description, target customer / ICP,
  value proposition, pain points, use cases, differentiators, industry /
  category, and other confirmed Product Card fields directly used downstream.
- `target_country` and `target_region` are separate fields. Do not use
  `target_country_or_region` as a database field.
- AI suggestion fields such as `campaign_goal`,
  `target_customer_profile`, `exclusion_rules`, and `scoring_focus` are not
  database columns unless a later migration explicitly adds them. They must be
  mapped into the Campaign draft fields by service logic.
- Campaign creation must verify that the referenced Product Card belongs to the
  same company and has `status = confirmed`.
- A Campaign must not be created from a draft, deleted, or rejected Product
  Card. Product Cards do not have a current `rejected` status.
- New Campaigns default to `draft`.
- A `draft` Campaign may be viewed, edited, deleted, or confirmed, but it cannot
  be used for formal Lead Discovery before confirmation.
- A `confirmed` Campaign may be viewed, archived, and used for Lead Discovery.
  It cannot be edited, deleted, or returned to `draft`.
- Repeating confirm on an already `confirmed` Campaign is idempotent and leaves
  it confirmed.
- A `confirmed` Campaign must preserve historical meaning through
  `product_card_snapshot`; downstream Lead Discovery should use the snapshot
  captured at confirmation time instead of rereading a later edited Product Card
  as the source of Campaign meaning.
- Planned Campaign status transitions are only `draft -> confirmed` and
  `confirmed -> archived`.
- Duplicate / copy as draft creates a new `draft` Campaign with a new `id` from
  a source Campaign. The source Campaign is not modified, and the new draft must
  revalidate the current Product Card when it is later confirmed.
- Archived Campaigns are not restorable. If future reuse is needed, it must be
  handled through duplicate / copy as draft rather than restore.
- Only a `confirmed` Campaign may enter Lead Discovery.
- Campaign status must not store Lead Discovery execution status. Future
  LeadDiscoveryJob, CampaignJob, or background task models should own execution
  states such as `pending`, `running`, `paused`, `completed`, `failed`, and
  `cancelled`.
- Campaign is not a CRM sequence and must not perform automatic follow-up, bulk
  sending, or automatic email sending.

## leads

Stores discovered candidate companies.

Main fields:

- `id`
- `campaign_id`
- `company_name`
- `website`
- `normalized_name`
- `normalized_website`
- `description`
- `country`
- `industry`
- `source_url`
- `discovery_status`
- `validation_status`
- `review_status`
- `created_at`
- `updated_at`

Possible `validation_status`:

- `pending`
- `valid`
- `invalid`
- `duplicate`
- `insufficient_content`

Possible `review_status`:

- `unreviewed`
- `approved`
- `rejected`
- `needs_manual_review`

Review status rules:

- `review_status` is a human review workflow state.
- AI scoring must not set `review_status` directly.
- Only `review_status = approved` can proceed to Outreach Draft or Gmail Draft
  creation.

## lead_intelligence

Stores website analysis and extracted evidence for leads.

Main fields:

- `id`
- `lead_id`
- `website_summary`
- `products_or_services`
- `target_customers`
- `business_model`
- `pain_points`
- `evidence`
- `content_quality`
- `crawl_status`
- `error_message`
- `created_at`
- `updated_at`

## lead_scores

Stores AI customer matching judgment.

Main fields:

- `id`
- `lead_id`
- `campaign_id`
- `fit_score`
- `recommendation`
- `matching_reasons`
- `risk_notes`
- `evidence`
- `suggested_outreach_angle`
- `model_name`
- `created_at`
- `updated_at`

Possible `recommendation`:

- `recommended`
- `maybe`
- `not_recommended`
- `needs_manual_review`

Recommendation rules:

- `recommendation` is produced by AI scoring.
- `recommended`, `maybe`, and `not_recommended` must not be mixed with human
  approval states.
- `needs_manual_review` may appear here as an AI uncertainty signal, while
  `leads.review_status = needs_manual_review` is a human workflow state.

## contacts

Stores lead contact information.

Main fields:

- `id`
- `lead_id`
- `contact_type`
- `value`
- `source`
- `confidence`
- `status`
- `created_at`
- `updated_at`

Possible `contact_type`:

- `email`
- `contact_form`
- `phone`
- `linkedin`
- `manual`

Possible `status`:

- `unverified`
- `valid`
- `invalid`
- `blocked`

`contact_type = linkedin` 仅表示人工发现的公开联系人渠道或资料引用，不表示
LinkedIn API integration。

Gmail Draft generation must not rely on a lead-level public email field or any
lead-level email-like field. It must use a selected contact record with:

- `contacts.contact_type = email`
- `contacts.status = valid`

Contact form, phone, LinkedIn, manual review, invalid email, unverified email,
blocked email, unselected contact, or missing contact records must not be
treated as eligible Gmail Draft recipients.

Contact selection rule:

- Do not add a `contacts.selected` field or selected boolean.
- When the user chooses a contact for Outreach Draft or Gmail Draft creation,
  the frontend passes `contact_id`.
- The backend must verify that `contact_id` exists, belongs to the current
  approved lead, has `contact_type = email`, and has `status = valid`.
- The backend must reject blocked, invalid, unverified, LinkedIn, phone,
  contact form, or manual-review-only contacts for Gmail Draft creation.
- The chosen contact is stored on `outreach_drafts.contact_id` after validation.

`contact_type = linkedin` only represents a manually provided or manually
reviewed public LinkedIn reference.

It does not represent:

- LinkedIn API integration
- LinkedIn scraping
- LinkedIn crawler, bot, browser automation, or browser extension automation
- automated LinkedIn login, search, profile extraction, contact downloading,
  messaging, or connection requests
- a verified email contact
- permission to generate Gmail Draft
- permission to send LinkedIn messages

For MVP, Gmail Draft must use a selected valid email contact:

- `contacts.contact_type = email`
- `contacts.status = valid`

A lead with only a LinkedIn contact and no valid email contact is not eligible
for Gmail Draft creation.

## outreach_drafts

Stores generated outreach draft records.

Main fields:

- `id`
- `lead_id`
- `campaign_id`
- `contact_id`
- `subject`
- `body`
- `status`
- `gmail_draft_id`
- `error_message`
- `created_at`
- `updated_at`

Possible `status`:

- `pending`
- `generated`
- `gmail_draft_created`
- `failed`

Important rule:

The system creates Gmail drafts only. It must not automatically send emails.

Gmail Draft creation is not email automation and not complete Gmail integration.
The system must not read or sync the inbox, track replies, monitor replies,
move, delete, label, or modify existing Gmail messages. OAuth scope must be
limited to the minimum draft-creation permission, such as `gmail.compose`.

Gmail draft eligibility should be evaluated from:

- `lead.review_status = approved`
- `outreach_drafts.contact_id`
- the selected contact belonging to the same lead
- `contact.contact_type = email`
- `contact.status = valid`
- the absence of an existing `gmail_draft_created` record for the same lead,
  campaign, selected contact, and outreach draft

LinkedIn references must not be used as Gmail Draft recipients. Gmail Draft
eligibility requires a selected valid email contact.

## task_runs

Stores background task status.

Task execution status is separate from Campaign configuration status. A task run
may track Lead Discovery or future Campaign Job execution, but these values must
not be stored in `campaigns.status`.

Main fields:

- `id`
- `task_type`
- `related_entity_type`
- `related_entity_id`
- `status`
- `progress`
- `error_message`
- `started_at`
- `finished_at`
- `created_at`
- `updated_at`

Possible `status`:

- `pending`
- `running`
- `completed`
- `failed`
- `cancelled`

## Relationship Summary

- Company profile has many sources.
- Company profile has many knowledge items.
- Company profile has many product cards.
- Product card has many campaigns.
- Campaign has many leads.
- Lead has one or many intelligence records.
- Lead has one or many scores.
- Lead has many contacts.
- Lead has many outreach drafts.
- Task runs can be linked to campaigns, leads, or outreach drafts.

## Data Integrity Rules

1. A product card must belong to a company.
2. A campaign must belong to a product card.
3. A lead must belong to a campaign.
4. Lead scoring should only happen after validation.
5. Outreach draft should only happen after user approval.
6. Gmail draft should only be created from an outreach draft.
7. Confirmed knowledge should be separated from draft knowledge.
