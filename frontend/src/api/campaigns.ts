export type CampaignStatus = "draft" | "confirmed" | "archived";
export type ProductCardStatus = "draft" | "confirmed";
export type ProductCardSourceType = "ai_generated" | "manual";

export interface PaginationMeta {
  total: number;
  limit: number;
  offset: number;
}

export interface Company {
  id: string;
  owner_id: string | null;
  workspace_id: string | null;
  name: string;
  website: string | null;
  industry: string | null;
  description: string | null;
  target_market: string | null;
  value_proposition: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProductCard {
  id: string;
  company_id: string;
  name: string;
  description: string;
  target_customer: string;
  pain_points: string[];
  value_proposition: string;
  use_cases: string[];
  differentiators: string[];
  source_knowledge_item_ids: string[];
  source_type: ProductCardSourceType;
  status: ProductCardStatus;
  created_at: string;
  updated_at: string;
}

export interface ProductCardSnapshot {
  product_card_id?: string;
  company_id?: string;
  name?: string;
  description?: string;
  target_customer?: string;
  pain_points?: string[];
  value_proposition?: string;
  use_cases?: string[];
  differentiators?: string[];
  source_type?: ProductCardSourceType;
}

export interface Campaign {
  id: string;
  company_id: string;
  product_card_id: string;
  product_card_snapshot: ProductCardSnapshot | null;
  name: string;
  target_country: string | null;
  target_region: string | null;
  target_industry: string | null;
  target_company_type: string | null;
  target_role: string | null;
  search_keywords: string[];
  qualification_criteria: string[];
  outreach_angle: string | null;
  lead_limit: number;
  status: CampaignStatus;
  created_at: string;
  updated_at: string;
}

export interface CampaignPayload {
  product_card_id: string;
  name: string;
  target_country: string | null;
  target_region: string | null;
  target_industry: string | null;
  target_company_type: string | null;
  target_role: string | null;
  search_keywords: string[];
  qualification_criteria: string[];
  outreach_angle: string | null;
  lead_limit: number;
}

export interface CampaignUpdatePayload {
  name?: string;
  target_country?: string | null;
  target_region?: string | null;
  target_industry?: string | null;
  target_company_type?: string | null;
  target_role?: string | null;
  search_keywords?: string[];
  qualification_criteria?: string[];
  outreach_angle?: string | null;
  lead_limit?: number;
}

interface Envelope<T> {
  data: T;
  message: string;
}

interface Collection<T> {
  items: T[];
  pagination: PaginationMeta;
}

export class ApiError extends Error {
  status: number;
  code?: string;

  constructor(message: string, status: number, code?: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

const API_PREFIX = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_PREFIX}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
    ...init,
  });

  const contentType = response.headers.get("content-type") ?? "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    const message =
      payload?.error?.message ??
      payload?.detail?.[0]?.msg ??
      "请求失败，请稍后重试。";
    const code = payload?.error?.code;
    throw new ApiError(message, response.status, code);
  }

  return payload as T;
}

function buildQuery(params: Record<string, string | number | undefined>) {
  const search = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) {
      search.set(key, String(value));
    }
  });
  const query = search.toString();
  return query ? `?${query}` : "";
}

export async function listCompanies() {
  const response = await request<Envelope<Collection<Company>>>(
    `/companies${buildQuery({ limit: 100, offset: 0 })}`,
  );
  return response.data;
}

export async function listCampaigns(
  companyId: string,
  status?: CampaignStatus,
) {
  const response = await request<Envelope<Collection<Campaign>>>(
    `/companies/${companyId}/campaigns${buildQuery({
      status,
      limit: 100,
      offset: 0,
    })}`,
  );
  return response.data;
}

export async function listConfirmedProductCards(companyId: string) {
  const response = await request<Envelope<Collection<ProductCard>>>(
    `/companies/${companyId}/product-cards${buildQuery({
      status: "confirmed",
      limit: 100,
      offset: 0,
    })}`,
  );
  return response.data;
}

export async function createCampaign(
  companyId: string,
  payload: CampaignPayload,
) {
  const response = await request<Envelope<Campaign>>(
    `/companies/${companyId}/campaigns`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
  return response.data;
}

export async function updateCampaign(
  campaignId: string,
  payload: CampaignUpdatePayload,
) {
  const response = await request<Envelope<Campaign>>(`/campaigns/${campaignId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  return response.data;
}

export async function deleteCampaign(campaignId: string) {
  const response = await request<Envelope<{ id: string; deleted: boolean }>>(
    `/campaigns/${campaignId}`,
    {
      method: "DELETE",
    },
  );
  return response.data;
}

export async function confirmCampaign(campaignId: string) {
  const response = await request<Envelope<Campaign>>(
    `/campaigns/${campaignId}/confirm`,
    {
      method: "POST",
    },
  );
  return response.data;
}

export async function archiveCampaign(campaignId: string) {
  const response = await request<Envelope<Campaign>>(
    `/campaigns/${campaignId}/archive`,
    {
      method: "POST",
    },
  );
  return response.data;
}

export async function duplicateCampaign(campaignId: string) {
  const response = await request<Envelope<Campaign>>(
    `/campaigns/${campaignId}/duplicate`,
    {
      method: "POST",
    },
  );
  return response.data;
}
