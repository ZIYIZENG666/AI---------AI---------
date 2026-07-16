import { ApiError, PaginationMeta } from "./campaigns";

export type TaskStatus =
  | "pending"
  | "running"
  | "completed"
  | "failed"
  | "cancelled";

export type TaskType = "lead_discovery" | "lead_validation";
export type RelatedEntityType = "campaign" | "lead";

export type DiscoveryStatus = "discovered";
export type ValidationStatus =
  | "pending"
  | "valid"
  | "invalid"
  | "duplicate"
  | "insufficient_content";
export type ReviewStatus =
  | "unreviewed"
  | "approved"
  | "rejected"
  | "needs_manual_review";

export interface LeadDiscoveryStartData {
  task_id: string;
  status: "pending";
  task_type: "lead_discovery";
  campaign_id: string;
}

export interface LeadValidationStartData {
  task_id: string;
  status: "pending";
  task_type: "lead_validation";
  lead_id: string;
}

export interface TaskRun {
  id: string;
  task_type: TaskType;
  related_entity_type: RelatedEntityType;
  related_entity_id: string;
  search_query: string | null;
  input_url: string | null;
  provider_name: string;
  status: TaskStatus;
  progress: number;
  error_message: string | null;
  started_at: string | null;
  finished_at: string | null;
  created_at: string;
  updated_at: string;
}

export type CrawlStatus =
  | "completed"
  | "failed"
  | "insufficient_content"
  | "skipped";

export interface LeadIntelligence {
  id: string;
  lead_id: string;
  task_run_id: string;
  source_url: string;
  provider_name: string;
  website_summary: string | null;
  products_or_services: string[];
  target_customers: string[];
  business_model: string | null;
  pain_points: string[];
  evidence: Array<Record<string, unknown>>;
  content_quality: string;
  crawl_status: CrawlStatus;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface Lead {
  id: string;
  campaign_id: string;
  task_run_id: string;
  company_name: string;
  website: string;
  normalized_name: string;
  normalized_website: string;
  description: string | null;
  country: string | null;
  industry: string | null;
  source_url: string;
  search_query: string;
  raw_snippet: string | null;
  discovery_reason: string | null;
  provider_name: string;
  discovery_status: DiscoveryStatus;
  validation_status: ValidationStatus;
  review_status: ReviewStatus;
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

export async function startLeadDiscovery(campaignId: string) {
  const response = await request<Envelope<LeadDiscoveryStartData>>(
    `/campaigns/${campaignId}/lead-discovery`,
    {
      method: "POST",
    },
  );
  return response.data;
}

export async function getTask(taskId: string) {
  const response = await request<Envelope<TaskRun>>(`/tasks/${taskId}`);
  return response.data;
}

export async function listLeadDiscoveryTasks(
  campaignId: string,
  limit = 20,
  offset = 0,
) {
  const response = await request<Envelope<Collection<TaskRun>>>(
    `/campaigns/${campaignId}/lead-discovery/tasks${buildQuery({
      limit,
      offset,
    })}`,
  );
  return response.data;
}

export async function listCampaignLeads(
  campaignId: string,
  limit = 100,
  offset = 0,
) {
  const response = await request<Envelope<Collection<Lead>>>(
    `/campaigns/${campaignId}/leads${buildQuery({ limit, offset })}`,
  );
  return response.data;
}

export async function startLeadValidation(leadId: string) {
  const response = await request<Envelope<LeadValidationStartData>>(
    `/leads/${leadId}/validation`,
    {
      method: "POST",
    },
  );
  return response.data;
}

export async function listLeadValidationTasks(
  leadId: string,
  limit = 20,
  offset = 0,
) {
  const response = await request<Envelope<Collection<TaskRun>>>(
    `/leads/${leadId}/validation/tasks${buildQuery({ limit, offset })}`,
  );
  return response.data;
}

export async function listLeadIntelligence(
  leadId: string,
  limit = 20,
  offset = 0,
) {
  const response = await request<Envelope<Collection<LeadIntelligence>>>(
    `/leads/${leadId}/intelligence${buildQuery({ limit, offset })}`,
  );
  return response.data;
}
