export type SourceType = "text" | "url";
export type SourceStatus = "ready";
export type KnowledgeStatus = "draft" | "confirmed" | "rejected";

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

export interface CompanyPayload {
  name: string;
  website?: string | null;
  industry?: string | null;
  description?: string | null;
  target_market?: string | null;
  value_proposition?: string | null;
}

export interface CompanySource {
  id: string;
  company_id: string;
  source_type: SourceType;
  title: string;
  url: string | null;
  raw_content: string | null;
  status: SourceStatus;
  created_at: string;
  updated_at: string;
}

export interface SourcePayload {
  source_type: SourceType;
  title: string;
  url?: string | null;
  raw_content?: string | null;
}

export interface KnowledgeItem {
  id: string;
  company_id: string;
  source_id: string | null;
  category: string;
  title: string;
  content: string;
  status: KnowledgeStatus;
  confidence: number | null;
  created_at: string;
  updated_at: string;
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
    const validationMessage =
      payload?.error?.details?.[0]?.msg ?? payload?.detail?.[0]?.msg;
    const message =
      payload?.error?.message ??
      validationMessage ??
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

export async function createCompany(payload: CompanyPayload) {
  const response = await request<Envelope<Company>>("/companies", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return response.data;
}

export async function updateCompany(
  companyId: string,
  payload: Partial<CompanyPayload>,
) {
  const response = await request<Envelope<Company>>(`/companies/${companyId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  return response.data;
}

export async function listSources(companyId: string) {
  const response = await request<Envelope<Collection<CompanySource>>>(
    `/companies/${companyId}/sources${buildQuery({ limit: 100, offset: 0 })}`,
  );
  return response.data;
}

export async function createSource(companyId: string, payload: SourcePayload) {
  const response = await request<Envelope<CompanySource>>(
    `/companies/${companyId}/sources`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
  return response.data;
}

export async function createKnowledgeDraft(sourceId: string) {
  const response = await request<Envelope<KnowledgeItem>>(
    `/sources/${sourceId}/knowledge-drafts`,
    {
      method: "POST",
    },
  );
  return response.data;
}

export async function listKnowledge(
  companyId: string,
  status?: KnowledgeStatus,
) {
  const response = await request<Envelope<Collection<KnowledgeItem>>>(
    `/companies/${companyId}/knowledge${buildQuery({
      status,
      limit: 100,
      offset: 0,
    })}`,
  );
  return response.data;
}

export async function confirmKnowledge(knowledgeId: string) {
  const response = await request<Envelope<KnowledgeItem>>(
    `/knowledge/${knowledgeId}/confirm`,
    {
      method: "POST",
    },
  );
  return response.data;
}

export async function rejectKnowledge(knowledgeId: string) {
  const response = await request<Envelope<KnowledgeItem>>(
    `/knowledge/${knowledgeId}/reject`,
    {
      method: "POST",
    },
  );
  return response.data;
}
