import type { ReactNode } from "react";
import { useEffect, useMemo, useState } from "react";

import { ApiError, Campaign } from "../../api/campaigns";
import {
  Lead,
  LeadIntelligence,
  TaskRun,
  TaskStatus,
  getTask,
  listCampaignLeads,
  listLeadDiscoveryTasks,
  listLeadIntelligence,
  listLeadValidationTasks,
  startLeadDiscovery,
  startLeadValidation,
} from "../../api/leadDiscovery";

const taskStatusLabels: Record<TaskStatus, string> = {
  pending: "待执行",
  running: "执行中",
  completed: "已完成",
  failed: "失败",
  cancelled: "已取消",
};

const validationStatusLabels: Record<Lead["validation_status"], string> = {
  pending: "待验证",
  valid: "验证有效",
  invalid: "验证无效",
  duplicate: "重复线索",
  insufficient_content: "内容不足",
};

const validationStatusTone: Record<Lead["validation_status"], string> = {
  pending: "mini-status--warning",
  valid: "mini-status--success",
  invalid: "mini-status--danger",
  duplicate: "mini-status--neutral",
  insufficient_content: "mini-status--warning",
};

const reviewStatusLabels: Record<Lead["review_status"], string> = {
  unreviewed: "未审查",
  approved: "后续阶段",
  rejected: "后续阶段",
  needs_manual_review: "后续阶段",
};

const blockingTaskStatuses: TaskStatus[] = ["pending", "running", "completed"];

function formatDate(value: string | null) {
  if (!value) {
    return "未记录";
  }

  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function formatOptional(value: string | null | undefined, fallback = "未填写") {
  return value?.trim() ? value : fallback;
}

function websiteHref(website: string) {
  return website.startsWith("http://") || website.startsWith("https://")
    ? website
    : `https://${website}`;
}

function getDiscoveryErrorMessage(error: unknown) {
  if (error instanceof ApiError) {
    if (error.code === "lead_discovery_already_exists") {
      return "该获客任务已经存在进行中或已完成的线索发现任务，请查看现有任务状态。";
    }
    if (error.code === "campaign_not_confirmed") {
      return "草稿获客任务不能启动线索发现，请先确认获客任务。";
    }
    if (error.code === "campaign_archived") {
      return "已归档获客任务不能启动新的线索发现。";
    }
    if (error.code === "campaign_not_found") {
      return "未找到当前获客任务，请刷新列表后重试。";
    }
    return error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "线索发现操作失败，请稍后重试。";
}

function getValidationErrorMessage(error: unknown) {
  if (error instanceof ApiError) {
    if (error.code === "lead_validation_already_exists") {
      return "该线索已经存在进行中或已完成的验证任务，请查看现有验证状态。";
    }
    if (error.code === "lead_already_validated") {
      return "该线索已经完成验证，不能重复启动。";
    }
    if (error.code === "lead_not_discovered") {
      return "该线索还不是已发现状态，不能启动验证。";
    }
    if (error.code === "campaign_not_confirmed") {
      return "该线索所属获客任务尚未确认，不能启动线索验证。";
    }
    if (error.code === "campaign_archived") {
      return "已归档获客任务下的线索不能启动新的验证。";
    }
    if (error.code === "lead_not_found") {
      return "未找到当前线索，请刷新候选线索列表后重试。";
    }
    return error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "线索验证操作失败，请稍后重试。";
}

function upsertTask(tasks: TaskRun[], task: TaskRun) {
  const existingIndex = tasks.findIndex((item) => item.id === task.id);
  if (existingIndex === -1) {
    return [task, ...tasks];
  }

  return tasks.map((item) => (item.id === task.id ? task : item));
}

function upsertTaskByLead(
  current: Record<string, TaskRun[]>,
  leadId: string,
  task: TaskRun,
) {
  return {
    ...current,
    [leadId]: upsertTask(current[leadId] ?? [], task),
  };
}

function isTerminalTask(status: TaskStatus) {
  return status === "completed" || status === "failed" || status === "cancelled";
}

function formatEvidenceValue(value: unknown) {
  if (typeof value === "string") {
    return value;
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  if (value === null || value === undefined) {
    return "未记录";
  }
  return JSON.stringify(value);
}

export default function LeadDiscoveryPanel({ campaign }: { campaign: Campaign }) {
  const [tasks, setTasks] = useState<TaskRun[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [activeTaskId, setActiveTaskId] = useState("");
  const [selectedLeadId, setSelectedLeadId] = useState("");
  const [validationTasksByLead, setValidationTasksByLead] = useState<
    Record<string, TaskRun[]>
  >({});
  const [intelligenceByLead, setIntelligenceByLead] = useState<
    Record<string, LeadIntelligence[]>
  >({});
  const [searchText, setSearchText] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [isValidationLoading, setIsValidationLoading] = useState(false);
  const [isStartingValidation, setIsStartingValidation] = useState(false);
  const [error, setError] = useState("");
  const [validationError, setValidationError] = useState("");
  const [message, setMessage] = useState("");
  const [validationMessage, setValidationMessage] = useState("");

  const activeTask = useMemo(
    () => tasks.find((task) => task.id === activeTaskId) ?? tasks[0] ?? null,
    [activeTaskId, tasks],
  );

  const blockingTask = useMemo(
    () => tasks.find((task) => blockingTaskStatuses.includes(task.status)) ?? null,
    [tasks],
  );

  const selectedLead = useMemo(
    () => leads.find((lead) => lead.id === selectedLeadId) ?? leads[0] ?? null,
    [leads, selectedLeadId],
  );

  const selectedValidationTasks = selectedLead
    ? (validationTasksByLead[selectedLead.id] ?? [])
    : [];
  const selectedValidationTask = selectedValidationTasks[0] ?? null;
  const selectedIntelligence = selectedLead
    ? (intelligenceByLead[selectedLead.id] ?? [])
    : [];
  const blockingValidationTask =
    selectedValidationTasks.find((task) =>
      blockingTaskStatuses.includes(task.status),
    ) ?? null;

  const filteredLeads = useMemo(() => {
    const query = searchText.trim().toLowerCase();
    if (!query) {
      return leads;
    }

    return leads.filter((lead) =>
      [
        lead.company_name,
        lead.website,
        lead.country,
        lead.industry,
        lead.search_query,
        lead.discovery_reason,
      ]
        .filter(Boolean)
        .some((value) => String(value).toLowerCase().includes(query)),
    );
  }, [leads, searchText]);

  async function refreshDiscoveryData(options?: {
    silent?: boolean;
    nextActiveTaskId?: string;
  }) {
    if (options?.silent) {
      setIsRefreshing(true);
    } else {
      setIsLoading(true);
    }
    setError("");

    try {
      const [taskResult, leadResult] = await Promise.all([
        listLeadDiscoveryTasks(campaign.id),
        listCampaignLeads(campaign.id),
      ]);

      setTasks(taskResult.items);
      setLeads(leadResult.items);
      const nextActiveTaskId = options?.nextActiveTaskId ?? activeTaskId;
      setActiveTaskId(nextActiveTaskId || taskResult.items[0]?.id || "");
      setSelectedLeadId((current) => {
        if (current && leadResult.items.some((lead) => lead.id === current)) {
          return current;
        }
        return leadResult.items[0]?.id ?? "";
      });
    } catch (requestError) {
      setError(getDiscoveryErrorMessage(requestError));
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }

  async function handleStartDiscovery() {
    setIsStarting(true);
    setError("");
    setMessage("");

    try {
      const started = await startLeadDiscovery(campaign.id);
      setActiveTaskId(started.task_id);
      setMessage("线索发现任务已启动，正在读取最新任务状态。");

      const task = await getTask(started.task_id);
      setTasks((current) => upsertTask(current, task));
      await refreshDiscoveryData({
        silent: true,
        nextActiveTaskId: started.task_id,
      });
    } catch (requestError) {
      setError(getDiscoveryErrorMessage(requestError));
      await refreshDiscoveryData({ silent: true });
    } finally {
      setIsStarting(false);
    }
  }

  async function refreshTask(taskId: string) {
    try {
      const task = await getTask(taskId);
      setTasks((current) => upsertTask(current, task));
      if (isTerminalTask(task.status)) {
        await refreshDiscoveryData({
          silent: true,
          nextActiveTaskId: task.id,
        });
      }
    } catch (requestError) {
      setError(getDiscoveryErrorMessage(requestError));
    }
  }

  async function refreshValidationData(leadId: string, options?: { silent?: boolean }) {
    if (!leadId) {
      return;
    }
    if (!options?.silent) {
      setIsValidationLoading(true);
    }
    setValidationError("");

    try {
      const [taskResult, intelligenceResult] = await Promise.all([
        listLeadValidationTasks(leadId),
        listLeadIntelligence(leadId),
      ]);
      setValidationTasksByLead((current) => ({
        ...current,
        [leadId]: taskResult.items,
      }));
      setIntelligenceByLead((current) => ({
        ...current,
        [leadId]: intelligenceResult.items,
      }));
    } catch (requestError) {
      setValidationError(getValidationErrorMessage(requestError));
    } finally {
      setIsValidationLoading(false);
    }
  }

  async function handleStartValidation(lead: Lead) {
    setSelectedLeadId(lead.id);
    setIsStartingValidation(true);
    setValidationError("");
    setValidationMessage("");

    try {
      const started = await startLeadValidation(lead.id);
      setValidationMessage("线索验证任务已启动，正在同步网站情报。");

      const task = await getTask(started.task_id);
      setValidationTasksByLead((current) =>
        upsertTaskByLead(current, lead.id, task),
      );
      await refreshValidationData(lead.id, { silent: true });
      await refreshDiscoveryData({
        silent: true,
        nextActiveTaskId: activeTaskId,
      });
    } catch (requestError) {
      setValidationError(getValidationErrorMessage(requestError));
      await refreshValidationData(lead.id, { silent: true });
      await refreshDiscoveryData({ silent: true, nextActiveTaskId: activeTaskId });
    } finally {
      setIsStartingValidation(false);
    }
  }

  async function refreshValidationTask(leadId: string, taskId: string) {
    try {
      const task = await getTask(taskId);
      setValidationTasksByLead((current) => upsertTaskByLead(current, leadId, task));
      if (isTerminalTask(task.status)) {
        await refreshValidationData(leadId, { silent: true });
        await refreshDiscoveryData({
          silent: true,
          nextActiveTaskId: activeTaskId,
        });
      }
    } catch (requestError) {
      setValidationError(getValidationErrorMessage(requestError));
    }
  }

  useEffect(() => {
    setTasks([]);
    setLeads([]);
    setActiveTaskId("");
    setSelectedLeadId("");
    setValidationTasksByLead({});
    setIntelligenceByLead({});
    setSearchText("");
    setMessage("");
    setValidationMessage("");
    void refreshDiscoveryData();
  }, [campaign.id]);

  useEffect(() => {
    if (selectedLead?.id) {
      void refreshValidationData(selectedLead.id);
    }
  }, [selectedLead?.id]);

  useEffect(() => {
    if (!activeTask || isTerminalTask(activeTask.status)) {
      return;
    }

    const timer = window.setInterval(() => {
      void refreshTask(activeTask.id);
    }, 2500);

    return () => window.clearInterval(timer);
  }, [activeTask?.id, activeTask?.status]);

  useEffect(() => {
    if (
      !selectedLead ||
      !selectedValidationTask ||
      isTerminalTask(selectedValidationTask.status)
    ) {
      return;
    }

    const timer = window.setInterval(() => {
      void refreshValidationTask(selectedLead.id, selectedValidationTask.id);
    }, 2500);

    return () => window.clearInterval(timer);
  }, [selectedLead?.id, selectedValidationTask?.id, selectedValidationTask?.status]);

  const canStartDiscovery = !blockingTask && !isStarting;
  const canStartSelectedLeadValidation =
    Boolean(selectedLead) &&
    selectedLead?.discovery_status === "discovered" &&
    selectedLead?.validation_status === "pending" &&
    !blockingValidationTask &&
    !isStartingValidation;
  const showZeroResult =
    activeTask?.status === "completed" && leads.length === 0 && !isLoading;

  return (
    <section className="lead-discovery-panel" aria-label="线索发现">
      <div className="lead-discovery-heading">
        <div>
          <span className="section-kicker">前端第四阶段</span>
          <h2>线索发现</h2>
          <p>
            基于已确认获客任务启动一次模拟线索发现，并展示任务状态与候选线索。
          </p>
        </div>
        <button
          className="secondary-button"
          disabled={isRefreshing}
          onClick={() => void refreshDiscoveryData({ silent: true })}
          type="button"
        >
          {isRefreshing ? "刷新中..." : "刷新状态"}
        </button>
      </div>

      {message ? <div className="notice notice--success">{message}</div> : null}
      {error ? (
        <div className="notice notice--error">
          <strong>线索发现未完成</strong>
          <span>{error}</span>
        </div>
      ) : null}

      <div className="lead-discovery-grid">
        <CampaignDiscoverySummary campaign={campaign} />

        <div className="lead-action-card surface-panel">
          <div className="lead-action-icon" aria-hidden="true">
            <span />
          </div>
          <h3>{blockingTask ? "已有发现任务" : "准备就绪"}</h3>
          <p>
            当前仅调用后端已验证的模拟搜索提供方，不执行真实搜索、真实爬虫或网站情报分析。
          </p>
          <button
            className="primary-button"
            disabled={!canStartDiscovery}
            onClick={() => void handleStartDiscovery()}
            type="button"
          >
            {isStarting
              ? "正在启动..."
              : blockingTask
                ? "已有发现任务"
                : "开始发现线索"}
          </button>
          {blockingTask ? (
            <small>
              已存在状态为「{taskStatusLabels[blockingTask.status]}」的任务，后端会阻止重复启动。
            </small>
          ) : null}
        </div>
      </div>

      <div className="lead-rule-strip">
        <span>草稿任务不能启动线索发现</span>
        <span>已归档任务不能启动新发现</span>
        <span>发现结果仍是待验证、未审查的候选线索</span>
      </div>

      <TaskStatusPanel task={activeTask} />

      <LeadResultsSection
        filteredLeads={filteredLeads}
        isLoading={isLoading}
        leads={leads}
        searchText={searchText}
        selectedLeadId={selectedLead?.id ?? ""}
        showZeroResult={showZeroResult}
        onSelectLead={setSelectedLeadId}
        onSearchTextChange={setSearchText}
        onStartValidation={(lead) => void handleStartValidation(lead)}
      />

      {leads.length > 0 ? (
        <LeadValidationSection
          canStartValidation={canStartSelectedLeadValidation}
          intelligenceItems={selectedIntelligence}
          isLoading={isValidationLoading}
          isStarting={isStartingValidation}
          lead={selectedLead}
          message={validationMessage}
          task={selectedValidationTask}
          tasks={selectedValidationTasks}
          validationError={validationError}
          onRefresh={() =>
            selectedLead ? void refreshValidationData(selectedLead.id) : undefined
          }
          onStartValidation={() =>
            selectedLead ? void handleStartValidation(selectedLead) : undefined
          }
        />
      ) : null}

      <TaskHistorySection
        activeTaskId={activeTask?.id ?? ""}
        tasks={tasks}
        onSelectTask={setActiveTaskId}
      />
    </section>
  );
}

function CampaignDiscoverySummary({ campaign }: { campaign: Campaign }) {
  return (
    <div className="lead-campaign-card surface-panel">
      <div className="lead-campaign-header">
        <div>
          <span className="section-kicker">已确认获客任务</span>
          <h3>{campaign.name}</h3>
          <p>任务 ID：{campaign.id}</p>
        </div>
        <span className="status-badge status-badge--confirmed">已确认</span>
      </div>

      <dl className="lead-summary-list">
        <div>
          <dt>目标国家/地区</dt>
          <dd>
            {formatOptional(campaign.target_country)}
            {campaign.target_region ? ` / ${campaign.target_region}` : ""}
          </dd>
        </div>
        <div>
          <dt>目标行业</dt>
          <dd>{formatOptional(campaign.target_industry)}</dd>
        </div>
        <div>
          <dt>目标角色</dt>
          <dd>{formatOptional(campaign.target_role)}</dd>
        </div>
        <div>
          <dt>线索上限</dt>
          <dd>{campaign.lead_limit} 条</dd>
        </div>
      </dl>

      <div className="lead-product-snapshot">
        <span>关联产品配置</span>
        <strong>{campaign.product_card_snapshot?.name ?? "已确认产品卡片"}</strong>
        <p>
          {campaign.product_card_snapshot?.description ??
            "线索发现会使用确认时锁定的产品卡片快照。"}
        </p>
      </div>
    </div>
  );
}

function TaskStatusPanel({ task }: { task: TaskRun | null }) {
  if (!task) {
    return (
      <section className="lead-status-card surface-panel">
        <div>
          <span className="section-kicker">当前任务</span>
          <h3>尚未开始线索发现</h3>
          <p>点击“开始发现线索”后，这里会显示后端返回的任务状态。</p>
        </div>
      </section>
    );
  }

  return (
    <section className="lead-status-card surface-panel">
      <div className="lead-status-card__header">
        <div>
          <span className="section-kicker">当前任务</span>
          <h3>{taskStatusLabels[task.status]}</h3>
          <p className="task-id">任务 ID：{task.id}</p>
        </div>
        <TaskBadge status={task.status} />
      </div>

      <div className="lead-status-grid">
        <div>
          <span>任务类型</span>
          <strong>线索发现</strong>
        </div>
        <div>
          <span>执行渠道</span>
          <strong>{task.provider_name}</strong>
        </div>
        <div>
          <span>创建时间</span>
          <strong>{formatDate(task.created_at)}</strong>
        </div>
        <div>
          <span>完成时间</span>
          <strong>{formatDate(task.finished_at)}</strong>
        </div>
      </div>

      <div className="task-progress" aria-label={`任务进度 ${task.progress}%`}>
        <span style={{ width: `${task.progress}%` }} />
      </div>

      <div className="task-query">
        <span>搜索关键词</span>
        <p>{task.search_query || "后端未返回搜索关键词"}</p>
      </div>

      {task.status === "failed" ? (
        <div className="lead-error-card">
          <strong>线索发现任务失败</strong>
          <span>{task.error_message ?? "任务执行失败，但后端未返回详细原因。"}</span>
        </div>
      ) : null}
    </section>
  );
}

function LeadResultsSection({
  filteredLeads,
  isLoading,
  leads,
  onSearchTextChange,
  onSelectLead,
  onStartValidation,
  searchText,
  selectedLeadId,
  showZeroResult,
}: {
  filteredLeads: Lead[];
  isLoading: boolean;
  leads: Lead[];
  onSearchTextChange: (value: string) => void;
  onSelectLead: (leadId: string) => void;
  onStartValidation: (lead: Lead) => void;
  searchText: string;
  selectedLeadId: string;
  showZeroResult: boolean;
}) {
  return (
    <section className="lead-results surface-panel">
      <div className="lead-table-toolbar">
        <div>
          <span className="section-kicker">候选线索</span>
          <h3>发现结果（{leads.length}）</h3>
        </div>
        <label className="lead-search">
          <span>搜索候选线索</span>
          <input
            onChange={(event) => onSearchTextChange(event.target.value)}
            placeholder="搜索公司、官网、行业或关键词"
            value={searchText}
          />
        </label>
      </div>

      <div className="lead-provider-note">
        当前结果来自模拟搜索提供方，仅用于开发验证，不代表真实外部客户证据。
      </div>

      {isLoading ? (
        <StatePanel title="正在读取线索" text="正在同步后端候选线索列表。" />
      ) : null}

      {!isLoading && showZeroResult ? (
        <StatePanel
          title="线索发现已完成，但没有候选线索"
          text="后端任务已完成，当前搜索配置没有保存新的候选线索。可以调整获客任务后复制为草稿，再重新确认并启动发现。"
        />
      ) : null}

      {!isLoading && leads.length === 0 && !showZeroResult ? (
        <StatePanel
          title="尚未发现候选线索"
          text="启动线索发现任务后，候选线索会从后端接口读取并展示在这里。"
        />
      ) : null}

      {!isLoading && leads.length > 0 ? (
        <div className="table-wrap">
          <table className="campaign-table lead-table">
            <thead>
              <tr>
                <th>公司名称</th>
                <th>官网</th>
                <th>国家 / 行业</th>
                <th>来源渠道</th>
                <th>发现原因</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {filteredLeads.map((lead) => (
                <tr
                  className={lead.id === selectedLeadId ? "selected-row" : ""}
                  key={lead.id}
                >
                  <td>
                    <button
                      className="link-button table-title"
                      onClick={() => onSelectLead(lead.id)}
                      type="button"
                    >
                      {lead.company_name}
                    </button>
                    <span>{lead.normalized_name}</span>
                  </td>
                  <td>
                    <a
                      className="mini-link"
                      href={websiteHref(lead.website)}
                      rel="noreferrer"
                      target="_blank"
                    >
                      {lead.website}
                    </a>
                  </td>
                  <td>
                    <strong>{formatOptional(lead.country, "未知国家")}</strong>
                    <span>{formatOptional(lead.industry, "未知行业")}</span>
                  </td>
                  <td>
                    <strong>{lead.provider_name}</strong>
                    <span>{lead.search_query}</span>
                  </td>
                  <td>
                    <span>{lead.discovery_reason ?? "后端未返回发现原因"}</span>
                  </td>
                  <td>
                    <div className="lead-status-stack">
                      <span className="mini-status mini-status--success">已发现</span>
                      <span
                        className={`mini-status ${
                          validationStatusTone[lead.validation_status]
                        }`}
                      >
                        {validationStatusLabels[lead.validation_status]}
                      </span>
                      <span className="mini-status mini-status--neutral">
                        {reviewStatusLabels[lead.review_status]}
                      </span>
                    </div>
                  </td>
                  <td>
                    <div className="row-actions lead-row-actions">
                      <button onClick={() => onSelectLead(lead.id)} type="button">
                        查看验证
                      </button>
                      {lead.validation_status === "pending" ? (
                        <button
                          onClick={() => onStartValidation(lead)}
                          type="button"
                        >
                          开始验证
                        </button>
                      ) : null}
                      <a
                        className="source-link"
                        href={lead.source_url}
                        rel="noreferrer"
                        target="_blank"
                      >
                        打开来源
                      </a>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredLeads.length === 0 ? (
            <div className="lead-filter-empty">没有匹配当前搜索条件的候选线索。</div>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}

function LeadValidationSection({
  canStartValidation,
  intelligenceItems,
  isLoading,
  isStarting,
  lead,
  message,
  onRefresh,
  onStartValidation,
  task,
  tasks,
  validationError,
}: {
  canStartValidation: boolean;
  intelligenceItems: LeadIntelligence[];
  isLoading: boolean;
  isStarting: boolean;
  lead: Lead | null;
  message: string;
  onRefresh: () => void;
  onStartValidation: () => void;
  task: TaskRun | null;
  tasks: TaskRun[];
  validationError: string;
}) {
  if (!lead) {
    return null;
  }

  const latestIntelligence = intelligenceItems[0] ?? null;
  const hasBlockingTask = task
    ? blockingTaskStatuses.includes(task.status)
    : false;
  const actionLabel = isStarting
    ? "正在启动..."
    : task?.status === "failed" && lead.validation_status === "pending"
      ? "重新验证"
      : hasBlockingTask || lead.validation_status !== "pending"
        ? "已完成验证"
        : "开始验证";

  return (
    <section className="lead-validation surface-panel" aria-label="线索验证与网站情报">
      <div className="lead-validation-heading">
        <div>
          <span className="section-kicker">前端第五阶段</span>
          <h3>线索验证与网站情报</h3>
          <p>
            基于后端 Phase 5 接口启动线索验证，并展示事实型网站情报和验证任务状态。
          </p>
        </div>
        <button className="secondary-button" disabled={isLoading} onClick={onRefresh} type="button">
          {isLoading ? "同步中..." : "刷新验证状态"}
        </button>
      </div>

      {message ? <div className="notice notice--success">{message}</div> : null}
      {validationError ? (
        <div className="notice notice--error">
          <strong>线索验证未完成</strong>
          <span>{validationError}</span>
        </div>
      ) : null}

      <div className="lead-validation-layout">
        <article className="validation-lead-card">
          <div className="lead-campaign-header">
            <div>
              <span className="section-kicker">当前线索</span>
              <h4>{lead.company_name}</h4>
              <p>{lead.description ?? "后端未返回线索描述。"}</p>
            </div>
            <span
              className={`mini-status ${
                validationStatusTone[lead.validation_status]
              }`}
            >
              {validationStatusLabels[lead.validation_status]}
            </span>
          </div>

          <dl className="validation-lead-meta">
            <div>
              <dt>官网</dt>
              <dd>
                <a className="mini-link" href={websiteHref(lead.website)} rel="noreferrer" target="_blank">
                  {lead.website}
                </a>
              </dd>
            </div>
            <div>
              <dt>国家 / 行业</dt>
              <dd>
                {formatOptional(lead.country, "未知国家")} /{" "}
                {formatOptional(lead.industry, "未知行业")}
              </dd>
            </div>
            <div>
              <dt>发现渠道</dt>
              <dd>{lead.provider_name}</dd>
            </div>
            <div>
              <dt>发现原因</dt>
              <dd>{lead.discovery_reason ?? "后端未返回发现原因。"}</dd>
            </div>
          </dl>

          <button
            className="primary-button"
            disabled={!canStartValidation}
            onClick={onStartValidation}
            type="button"
          >
            {actionLabel}
          </button>
          <p className="validation-contract-note">
            当前阶段只做验证和事实情报采集，不执行评分、人审、联系人查找或 Gmail 草稿。
          </p>
        </article>

        <ValidationTaskCard lead={lead} task={task} />
      </div>

      <LeadIntelligencePanel
        intelligence={latestIntelligence}
        isLoading={isLoading}
        lead={lead}
        task={task}
      />

      <ValidationTaskHistory tasks={tasks} />
    </section>
  );
}

function ValidationTaskCard({ lead, task }: { lead: Lead; task: TaskRun | null }) {
  if (!task) {
    return (
      <article className="validation-task-card">
        <span className="section-kicker">验证任务</span>
        <h4>尚未开始验证</h4>
        <p>
          启动验证后，这里会显示后端 `lead_validation` 任务状态和用于验证的网站地址。
        </p>
        <div className="validation-status-hero validation-status-hero--pending">
          <span />
          <strong>待验证</strong>
        </div>
      </article>
    );
  }

  return (
    <article className="validation-task-card">
      <div className="lead-status-card__header">
        <div>
          <span className="section-kicker">验证任务</span>
          <h4>{taskStatusLabels[task.status]}</h4>
          <p className="task-id">任务 ID：{task.id}</p>
        </div>
        <TaskBadge status={task.status} />
      </div>

      <div className="lead-status-grid validation-task-grid">
        <div>
          <span>任务类型</span>
          <strong>线索验证</strong>
        </div>
        <div>
          <span>执行渠道</span>
          <strong>{task.provider_name}</strong>
        </div>
        <div>
          <span>验证网站</span>
          <strong>{task.input_url ?? lead.website}</strong>
        </div>
        <div>
          <span>完成时间</span>
          <strong>{formatDate(task.finished_at)}</strong>
        </div>
      </div>

      <div className="task-progress" aria-label={`验证任务进度 ${task.progress}%`}>
        <span style={{ width: `${task.progress}%` }} />
      </div>

      {task.status === "failed" ? (
        <div className="lead-error-card">
          <strong>验证任务失败</strong>
          <span>{task.error_message ?? "任务失败，但后端未返回详细原因。"}</span>
        </div>
      ) : null}
    </article>
  );
}

function LeadIntelligencePanel({
  intelligence,
  isLoading,
  lead,
  task,
}: {
  intelligence: LeadIntelligence | null;
  isLoading: boolean;
  lead: Lead;
  task: TaskRun | null;
}) {
  if (isLoading) {
    return (
      <StatePanel
        title="正在读取网站情报"
        text="正在从后端同步该线索的验证任务和事实型网站情报。"
      />
    );
  }

  if (lead.validation_status === "pending" && !task) {
    return (
      <StatePanel
        title="尚未验证"
        text="该线索尚未开始验证。启动验证后，系统会基于后端模拟抓取结果生成事实型网站情报。"
      />
    );
  }

  if (lead.validation_status === "duplicate") {
    return (
      <ValidationOutcomePanel
        title="线索重复"
        tone="neutral"
        text="该线索与当前获客任务中的已有线索重复。当前阶段只标记重复结果，不执行合并、删除或人审判断。"
      />
    );
  }

  if (lead.validation_status === "invalid") {
    return (
      <ValidationOutcomePanel
        title="验证无效"
        tone="danger"
        text={
          intelligence?.error_message ??
          "目标网站地址不受支持或格式无效，无法形成有效网站情报。"
        }
      />
    );
  }

  if (lead.validation_status === "insufficient_content") {
    return (
      <ValidationOutcomePanel
        title="网站内容不足"
        tone="warning"
        text="后端已完成验证任务，但目标网站内容不足，暂不能形成完整有效的网站情报。"
      />
    );
  }

  if (!intelligence) {
    return (
      <StatePanel
        title="暂无网站情报"
        text="后端暂未返回该线索的网站情报记录。请刷新验证状态或查看任务错误。"
      />
    );
  }

  return (
    <section className="intelligence-panel">
      <div className="intelligence-header">
        <div>
          <span className="section-kicker">网站情报</span>
          <h4>验证有效，已形成事实型网站情报</h4>
          <p>
            来源：{" "}
            <a className="mini-link" href={intelligence.source_url} rel="noreferrer" target="_blank">
              {intelligence.source_url}
            </a>
          </p>
        </div>
        <span className="mini-status mini-status--success">
          {intelligence.content_quality === "sufficient"
            ? "内容充足"
            : intelligence.content_quality}
        </span>
      </div>

      <div className="intelligence-grid">
        <InfoBlock title="网站摘要">
          <p>{intelligence.website_summary ?? "后端未返回网站摘要。"}</p>
        </InfoBlock>
        <InfoBlock title="商业模式">
          <p>{intelligence.business_model ?? "后端未返回商业模式。"}</p>
        </InfoBlock>
        <InfoBlock title="产品与服务">
          <ValueList items={intelligence.products_or_services} />
        </InfoBlock>
        <InfoBlock title="目标客户">
          <ValueList items={intelligence.target_customers} />
        </InfoBlock>
        <InfoBlock title="痛点线索">
          <ValueList items={intelligence.pain_points} />
        </InfoBlock>
        <InfoBlock title="证据列表">
          <EvidenceList items={intelligence.evidence} />
        </InfoBlock>
      </div>
    </section>
  );
}

function ValidationOutcomePanel({
  text,
  title,
  tone,
}: {
  text: string;
  title: string;
  tone: "danger" | "neutral" | "warning";
}) {
  return (
    <section className={`validation-outcome validation-outcome--${tone}`}>
      <h4>{title}</h4>
      <p>{text}</p>
    </section>
  );
}

function InfoBlock({
  children,
  title,
}: {
  children: ReactNode;
  title: string;
}) {
  return (
    <article className="intelligence-block">
      <h5>{title}</h5>
      {children}
    </article>
  );
}

function ValueList({ items }: { items: string[] }) {
  if (items.length === 0) {
    return <p className="muted-text">后端未返回相关内容。</p>;
  }
  return (
    <ul className="intelligence-list">
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}

function EvidenceList({ items }: { items: Array<Record<string, unknown>> }) {
  if (items.length === 0) {
    return <p className="muted-text">后端未返回可展示证据。</p>;
  }

  return (
    <div className="evidence-list">
      {items.map((item, index) => {
        const sourceUrl = formatEvidenceValue(item.source_url);
        const snippet = formatEvidenceValue(item.snippet);
        return (
          <div className="evidence-item" key={`${sourceUrl}-${index}`}>
            <strong>证据 {index + 1}</strong>
            <p>{snippet}</p>
            <span>{sourceUrl}</span>
          </div>
        );
      })}
    </div>
  );
}

function ValidationTaskHistory({ tasks }: { tasks: TaskRun[] }) {
  return (
    <section className="validation-history">
      <div className="lead-table-toolbar">
        <div>
          <span className="section-kicker">验证任务历史</span>
          <h4>历史验证记录（{tasks.length}）</h4>
        </div>
      </div>

      {tasks.length === 0 ? (
        <StatePanel
          title="暂无验证任务"
          text="当前线索还没有线索验证执行记录。"
        />
      ) : (
        <div className="table-wrap">
          <table className="campaign-table validation-history-table">
            <thead>
              <tr>
                <th>任务 ID</th>
                <th>状态</th>
                <th>执行渠道</th>
                <th>验证网站</th>
                <th>创建时间</th>
                <th>完成时间</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((item) => (
                <tr key={item.id}>
                  <td>
                    <span className="table-title">{item.id}</span>
                  </td>
                  <td>
                    <TaskBadge status={item.status} />
                  </td>
                  <td>{item.provider_name}</td>
                  <td>{item.input_url ?? "未记录"}</td>
                  <td>{formatDate(item.created_at)}</td>
                  <td>{formatDate(item.finished_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function TaskHistorySection({
  activeTaskId,
  onSelectTask,
  tasks,
}: {
  activeTaskId: string;
  onSelectTask: (taskId: string) => void;
  tasks: TaskRun[];
}) {
  return (
    <section className="lead-history surface-panel">
      <div className="lead-table-toolbar">
        <div>
          <span className="section-kicker">任务历史</span>
          <h3>历史执行记录（{tasks.length}）</h3>
        </div>
      </div>

      {tasks.length === 0 ? (
        <StatePanel
          title="暂无任务历史"
          text="当前获客任务还没有线索发现执行记录。"
        />
      ) : (
        <div className="table-wrap">
          <table className="campaign-table lead-history-table">
            <thead>
              <tr>
                <th>任务 ID</th>
                <th>状态</th>
                <th>执行渠道</th>
                <th>搜索关键词</th>
                <th>创建时间</th>
                <th>完成时间</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((task) => (
                <tr
                  className={task.id === activeTaskId ? "selected-row" : ""}
                  key={task.id}
                >
                  <td>
                    <button
                      className="link-button table-title"
                      onClick={() => onSelectTask(task.id)}
                      type="button"
                    >
                      {task.id}
                    </button>
                  </td>
                  <td>
                    <TaskBadge status={task.status} />
                  </td>
                  <td>{task.provider_name}</td>
                  <td>
                    <span>{task.search_query}</span>
                  </td>
                  <td>{formatDate(task.created_at)}</td>
                  <td>{formatDate(task.finished_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function TaskBadge({ status }: { status: TaskStatus }) {
  return (
    <span className={`task-badge task-badge--${status}`}>
      {taskStatusLabels[status]}
    </span>
  );
}

function StatePanel({ text, title }: { text: string; title: string }) {
  return (
    <div className="state-panel lead-state-panel">
      <div className="state-icon" />
      <h3>{title}</h3>
      <p>{text}</p>
    </div>
  );
}
