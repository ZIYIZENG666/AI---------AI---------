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

export interface ProductCardPayload {
  company_id: string;
  name: string;
  description: string;
  target_customer: string;
  pain_points: string[];
  value_proposition: string;
  use_cases: string[];
  differentiators: string[];
}

export type ProductCardUpdatePayload = Partial<
  Omit<ProductCardPayload, "company_id">
>;

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

export async function listProductCards(
  companyId: string,
  status?: ProductCardStatus,
) {
  const response = await request<Envelope<Collection<ProductCard>>>(
    `/companies/${companyId}/product-cards${buildQuery({
      status,
      limit: 100,
      offset: 0,
    })}`,
  );
  return response.data;
}

export async function createManualProductCard(payload: ProductCardPayload) {
  const response = await request<Envelope<ProductCard>>("/product-cards", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return response.data;
}

export async function generateProductCard(companyId: string) {
  const response = await request<Envelope<ProductCard>>(
    `/companies/${companyId}/product-cards`,
    {
      method: "POST",
    },
  );
  return response.data;
}

export async function updateProductCard(
  productCardId: string,
  payload: ProductCardUpdatePayload,
) {
  const response = await request<Envelope<ProductCard>>(
    `/product-cards/${productCardId}`,
    {
      method: "PATCH",
      body: JSON.stringify(payload),
    },
  );
  return response.data;
}

export async function confirmProductCard(productCardId: string) {
  const response = await request<Envelope<ProductCard>>(
    `/product-cards/${productCardId}/confirm`,
    {
      method: "POST",
    },
  );
  return response.data;
}

export async function deleteProductCard(productCardId: string) {
  const response = await request<Envelope<{ id: string; deleted: boolean }>>(
    `/product-cards/${productCardId}`,
    {
      method: "DELETE",
    },
  );
  return response.data;
}
