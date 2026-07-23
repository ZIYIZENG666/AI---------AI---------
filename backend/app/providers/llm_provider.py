"""Provider contracts and mocks for future large language model integrations."""

from typing import Any


class LLMProvider:
    """Abstract-ish provider surface for text generation capabilities."""

    def generate_text(self, prompt: str) -> str:
        raise NotImplementedError("LLM integration is not implemented in the skeleton.")


class LeadScoringProvider:
    """Provider contract for AI customer-fit scoring."""

    provider_name = "llm_provider"
    model_name = "llm_model"

    def score_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Return structured Lead Scoring output for a validated Lead."""

        raise NotImplementedError("Lead scoring integration is not implemented.")


class MockLeadScoringProvider(LeadScoringProvider):
    """Deterministic provider used for Phase 6 Lead Scoring development."""

    provider_name = "mock_llm"
    model_name = "mock_lead_scoring_v1"

    def score_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        lead = payload["lead"]
        campaign = payload["campaign"]
        intelligence = payload["intelligence"]
        product_snapshot = campaign.get("product_card_snapshot") or {}

        evidence = self._build_evidence(intelligence.get("evidence") or [])
        score = 35
        matching_reasons: list[str] = []
        risk_notes: list[str] = []
        uncertainty_notes: list[str] = []
        text_blob = self._text_blob(lead, campaign, intelligence, product_snapshot)

        if evidence:
            score += 15
            matching_reasons.append(
                "The Lead has traceable website evidence available for fit scoring."
            )
        else:
            risk_notes.append("No traceable website evidence was available.")
            uncertainty_notes.append("The mock scorer could not verify website claims.")

        target_industry = str(campaign.get("target_industry") or "").strip().lower()
        lead_industry = str(lead.get("industry") or "").strip().lower()
        if target_industry and (
            target_industry in lead_industry or target_industry in text_blob
        ):
            score += 15
            matching_reasons.append(
                "The Lead industry context aligns with the Campaign target industry."
            )
        elif target_industry:
            score -= 5
            risk_notes.append(
                "The Lead industry context is not clearly aligned with the Campaign."
            )
        else:
            uncertainty_notes.append("The Campaign target industry is not explicit.")

        if self._has_keyword_overlap(campaign, intelligence, product_snapshot):
            score += 15
            matching_reasons.append(
                "The Lead website intelligence overlaps with Campaign and Product Card terms."
            )
        else:
            uncertainty_notes.append(
                "The mock scorer found limited keyword overlap with the Campaign."
            )

        if intelligence.get("products_or_services") and intelligence.get(
            "target_customers"
        ):
            score += 10
            matching_reasons.append(
                "The Lead has a clear product and customer profile in website intelligence."
            )
        else:
            risk_notes.append("The Lead product or customer profile is incomplete.")

        target_country = str(campaign.get("target_country") or "").strip().lower()
        lead_country = str(lead.get("country") or "").strip().lower()
        if target_country and lead_country == target_country:
            score += 5
            matching_reasons.append("The Lead country matches the Campaign target country.")
        elif target_country and lead_country:
            score -= 5
            risk_notes.append("The Lead country differs from the Campaign target country.")
        elif target_country:
            uncertainty_notes.append("The Lead country is not available for verification.")

        if intelligence.get("content_quality") != "sufficient":
            score -= 20
            risk_notes.append("Website intelligence quality is not marked sufficient.")

        fit_score = max(0, min(100, score))
        if not risk_notes:
            risk_notes.append("No critical blocker was found in the mock evidence.")
        if not uncertainty_notes:
            uncertainty_notes.append(
                "The score is based on bounded mock intelligence, not a real LLM call."
            )

        return {
            "fit_score": fit_score,
            "recommendation": self._recommendation_for_score(fit_score),
            "matching_reasons": matching_reasons,
            "risk_notes": risk_notes,
            "uncertainty_notes": uncertainty_notes,
            "evidence": evidence,
            "suggested_outreach_angle": self._suggested_outreach_angle(campaign),
        }

    @staticmethod
    def _build_evidence(evidence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        for item in evidence_items[:5]:
            source_url = str(item.get("source_url") or "").strip()
            snippet = str(
                item.get("evidence_text") or item.get("snippet") or ""
            ).strip()
            if not source_url or not snippet:
                continue
            normalized.append(
                {
                    "claim": "Website evidence used for fit scoring.",
                    "evidence_text": snippet,
                    "source_url": source_url,
                    "confidence": "medium",
                    "explanation": "Evidence returned by the crawler provider.",
                }
            )
        return normalized

    @staticmethod
    def _text_blob(
        lead: dict[str, Any],
        campaign: dict[str, Any],
        intelligence: dict[str, Any],
        product_snapshot: dict[str, Any],
    ) -> str:
        values: list[str] = []
        for source in (lead, campaign, intelligence, product_snapshot):
            for value in source.values():
                if isinstance(value, list):
                    values.extend(str(item) for item in value)
                elif isinstance(value, dict):
                    values.extend(str(item) for item in value.values())
                elif value is not None:
                    values.append(str(value))
        return " ".join(values).lower()

    def _has_keyword_overlap(
        self,
        campaign: dict[str, Any],
        intelligence: dict[str, Any],
        product_snapshot: dict[str, Any],
    ) -> bool:
        terms: list[str] = []
        for key in ("search_keywords", "qualification_criteria"):
            terms.extend(str(item) for item in campaign.get(key) or [])
        for key in ("name", "target_customer", "value_proposition"):
            value = product_snapshot.get(key)
            if value:
                terms.extend(str(value).split())

        text = self._text_blob({}, {}, intelligence, {})
        return any(term.lower() in text for term in terms if len(term.strip()) >= 4)

    @staticmethod
    def _recommendation_for_score(score: int) -> str:
        if score >= 80:
            return "recommended"
        if score >= 60:
            return "maybe"
        if score >= 40:
            return "needs_manual_review"
        return "not_recommended"

    @staticmethod
    def _suggested_outreach_angle(campaign: dict[str, Any]) -> str | None:
        outreach_angle = str(campaign.get("outreach_angle") or "").strip()
        if outreach_angle:
            return outreach_angle
        return "Use the validated website evidence to open a focused sales conversation."
