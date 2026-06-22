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

Possible inputs:

- Website URL
- Text description
- Uploaded document
- Manual notes

The system stores the input as source data.

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

### Step 5: Create Product Card

The user creates a product card based on confirmed knowledge.

The product card explains:

- What the product is
- Who it is for
- What problem it solves
- Why customers may care
- Key selling points

### Step 6: Create Campaign

The user selects a product card and creates a sales campaign.

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

### Step 15: Record Status

The system records statuses such as:

- Lead discovered
- Lead scored
- Lead approved
- Draft generated
- Draft failed
- User rejected

## Workflow Rules

1. AI-generated knowledge must be reviewed before becoming confirmed knowledge.
2. Campaigns must be based on product cards.
3. Lead scoring must be based on confirmed campaign and product information.
4. Invalid leads should not be scored by AI.
5. Email drafts can only be generated for approved leads.
6. Gmail draft creation must not automatically send email.
7. All major steps should store status and error information.