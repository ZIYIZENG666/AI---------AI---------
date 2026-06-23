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
- `raw_text`
- `file_path`
- `status`
- `error_message`
- `created_at`
- `updated_at`

Possible `source_type`:

- `url`
- `text`
- `document`
- `manual`

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

Only confirmed knowledge should be used as reliable input for product cards, campaigns, scoring, and outreach.

## product_cards

Stores product or service cards.

Main fields:

- `id`
- `company_id`
- `name`
- `description`
- `target_customer`
- `pain_points`
- `benefits`
- `differentiation`
- `use_cases`
- `proof_points`
- `status`
- `created_at`
- `updated_at`

Possible `status`:

- `draft`
- `confirmed`
- `archived`

`confirmed` 表示用户已确认，可用于后续 Campaign 与 Outreach。

## campaigns

Stores sales campaigns.

Main fields:

- `id`
- `company_id`
- `product_card_id`
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
- `running`
- `completed`
- `failed`
- `archived`

`confirmed` 表示用户已确认，可进入 lead discovery。

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

`contact_type = linkedin` 仅表示人工发现的公开联系人渠道或资料引用，不表示 LinkedIn API integration。

For MVP, Gmail draft generation should mainly use valid public email when available.

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

Gmail draft eligibility should be evaluated from:

- `lead.review_status`
- the selected `contacts` record
- the absence of an existing completed `outreach_drafts` record for the same lead, campaign, and contact

## task_runs

Stores background task status.

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
