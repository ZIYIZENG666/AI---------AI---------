import { useEffect, useMemo, useState } from "react";

import { ApiError, Campaign } from "../../api/campaigns";
import {
  Lead,
  TaskRun,
  TaskStatus,
  getTask,
  listCampaignLeads,
  listLeadDiscoveryTasks,
  startLeadDiscovery,
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
  valid: "后续阶段",
  invalid: "后续阶段",
  duplicate: "后续阶段",
  insufficient_content: "后续阶段",
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

function upsertTask(tasks: TaskRun[], task: TaskRun) {
  const existingIndex = tasks.findIndex((item) => item.id === task.id);
  if (existingIndex === -1) {
    return [task, ...tasks];
  }

  return tasks.map((item) => (item.id === task.id ? task : item));
}

function isTerminalTask(status: TaskStatus) {
  return status === "completed" || status === "failed" || status === "cancelled";
}

export default function LeadDiscoveryPanel({ campaign }: { campaign: Campaign }) {
  const [tasks, setTasks] = useState<TaskRun[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [activeTaskId, setActiveTaskId] = useState("");
  const [searchText, setSearchText] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const activeTask = useMemo(
    () => tasks.find((task) => task.id === activeTaskId) ?? tasks[0] ?? null,
    [activeTaskId, tasks],
  );

  const blockingTask = useMemo(
    () => tasks.find((task) => blockingTaskStatuses.includes(task.status)) ?? null,
    [tasks],
  );

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

  useEffect(() => {
    setTasks([]);
    setLeads([]);
    setActiveTaskId("");
    setSearchText("");
    setMessage("");
    void refreshDiscoveryData();
  }, [campaign.id]);

  useEffect(() => {
    if (!activeTask || isTerminalTask(activeTask.status)) {
      return;
    }

    const timer = window.setInterval(() => {
      void refreshTask(activeTask.id);
    }, 2500);

    return () => window.clearInterval(timer);
  }, [activeTask?.id, activeTask?.status]);

  const canStartDiscovery = !blockingTask && !isStarting;
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
        showZeroResult={showZeroResult}
        onSearchTextChange={setSearchText}
      />

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
  searchText,
  showZeroResult,
}: {
  filteredLeads: Lead[];
  isLoading: boolean;
  leads: Lead[];
  onSearchTextChange: (value: string) => void;
  searchText: string;
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
                <tr key={lead.id}>
                  <td>
                    <strong>{lead.company_name}</strong>
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
                      <span className="mini-status mini-status--warning">
                        {validationStatusLabels[lead.validation_status]}
                      </span>
                      <span className="mini-status mini-status--neutral">
                        {reviewStatusLabels[lead.review_status]}
                      </span>
                    </div>
                  </td>
                  <td>
                    <a
                      className="source-link"
                      href={lead.source_url}
                      rel="noreferrer"
                      target="_blank"
                    >
                      打开来源
                    </a>
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
