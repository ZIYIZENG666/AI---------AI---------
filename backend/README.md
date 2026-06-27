# Backend

Current implemented backend slices:

- `company`: company profile create, list, get, and update
- `sources`: company-owned text/URL source create, list, and get
- `knowledge`: deterministic source-to-draft creation, status-filtered listing, confirm, and reject
- `products`: confirmed-knowledge-only deterministic Product Card generation, manual Product Card creation, list, get, patch/edit, confirm, and delete

The backend is no longer only the company minimum slice. The implemented backend
surface currently covers `company`, `sources`, `knowledge`, and `products`.

Current Product Card backend behavior:

- Product Cards support create, list, get, patch/edit, confirm, and delete.
- Product Cards support only `draft` and `confirmed` statuses.
- `rejected` is not a valid Product Card status, and there is no Product Card reject endpoint.
- Delete replaces the legacy reject/rejected behavior.
- AI-generated Product Cards are created from confirmed company knowledge and start with `status = draft` and `source_type = ai_generated`.
- Manual Product Cards are created through `POST /api/v1/product-cards`, belong to a company, and start with `status = draft` and `source_type = manual`.
- PATCH edits only user-editable Product Card fields and must not change status, source type, source knowledge, or company ownership.
- Confirm is idempotent: confirming an already confirmed Product Card returns the current confirmed record.
- Draft Product Cards can be deleted. Confirmed Product Cards can be deleted only when no Campaign has ever referenced them; otherwise deletion returns HTTP `409`.
- Campaign is still a later phase. Only confirmed Product Cards may be selected by Campaign when that module is implemented.

Current not implemented:

- Campaign
- Lead Discovery
- Contacts
- Outreach and Gmail Draft workflow
- Frontend workflow pages

Phases 1B and 2 intentionally do not include document parsing, OCR, crawling,
real LLM calls, external integrations, or frontend workflow pages.
