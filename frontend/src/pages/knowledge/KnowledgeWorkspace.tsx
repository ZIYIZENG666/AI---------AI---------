import { FormEvent, ReactNode, useEffect, useMemo, useState } from "react";

import {
  ApiError,
  Company,
  CompanyPayload,
  CompanySource,
  KnowledgeItem,
  KnowledgeStatus,
  SourcePayload,
  SourceType,
  confirmKnowledge,
  createCompany,
  createKnowledgeDraft,
  createSource,
  listCompanies,
  listKnowledge,
  listSources,
  rejectKnowledge,
  updateCompany,
} from "../../api/knowledgeBase";

type WorkspaceTab = "company" | "sources" | "knowledge";
type KnowledgeFilter = "all" | KnowledgeStatus;
type DrawerState =
  | { type: "company"; mode: "create" | "edit" }
  | { type: "source" };
type ModalState =
  | { type: "sourceDetail"; source: CompanySource }
  | { type: "knowledgeDetail"; knowledge: KnowledgeItem }
  | { type: "confirmKnowledge"; knowledge: KnowledgeItem }
  | { type: "rejectKnowledge"; knowledge: KnowledgeItem };

interface CompanyFormState {
  name: string;
  website: string;
  industry: string;
  description: string;
  target_market: string;
  value_proposition: string;
}

interface SourceFormState {
  source_type: SourceType;
  title: string;
  url: string;
  raw_content: string;
}

const emptyCompanyForm: CompanyFormState = {
  name: "",
  website: "",
  industry: "",
  description: "",
  target_market: "",
  value_proposition: "",
};

const emptySourceForm: SourceFormState = {
  source_type: "text",
  title: "",
  url: "",
  raw_content: "",
};

const workspaceTabs: Array<{ value: WorkspaceTab; label: string }> = [
  { value: "company", label: "公司概况" },
  { value: "sources", label: "资料来源" },
  { value: "knowledge", label: "知识审核" },
];

const knowledgeFilters: Array<{ value: KnowledgeFilter; label: string }> = [
  { value: "all", label: "全部" },
  { value: "draft", label: "草稿" },
  { value: "confirmed", label: "已确认" },
  { value: "rejected", label: "已拒绝" },
];

const sourceTypeLabels: Record<SourceType, string> = {
  text: "文本资料",
  url: "网页链接",
};

const knowledgeStatusLabels: Record<KnowledgeStatus, string> = {
  draft: "草稿",
  confirmed: "已确认",
  rejected: "已拒绝",
};

const knowledgeStatusTone: Record<KnowledgeStatus, string> = {
  draft: "status-badge status-badge--draft",
  confirmed: "status-badge status-badge--confirmed",
  rejected: "status-badge status-badge--archived",
};

function toNullable(value: string) {
  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}

function toCompanyForm(company?: Company): CompanyFormState {
  if (!company) {
    return emptyCompanyForm;
  }

  return {
    name: company.name,
    website: company.website ?? "",
    industry: company.industry ?? "",
    description: company.description ?? "",
    target_market: company.target_market ?? "",
    value_proposition: company.value_proposition ?? "",
  };
}

function toCompanyPayload(form: CompanyFormState): CompanyPayload {
  return {
    name: form.name.trim(),
    website: toNullable(form.website),
    industry: toNullable(form.industry),
    description: toNullable(form.description),
    target_market: toNullable(form.target_market),
    value_proposition: toNullable(form.value_proposition),
  };
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function splitTags(value: string | null) {
  return (value ?? "")
    .split(/[\n,，]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function compactText(value: string | null | undefined, fallback = "未填写") {
  const trimmed = value?.trim();
  return trimmed ? trimmed : fallback;
}

function getErrorMessage(error: unknown) {
  if (error instanceof ApiError) {
    const codeMessages: Record<string, string> = {
      company_not_found: "公司资料不存在，请刷新后重试。",
      source_not_found: "资料来源不存在，请刷新后重试。",
      knowledge_not_found: "知识条目不存在，请刷新后重试。",
      knowledge_not_draft: "该知识条目已不是草稿，无法重复处理。",
      validation_error: "请检查必填项和字段格式。",
    };

    if (error.code && codeMessages[error.code]) {
      return codeMessages[error.code];
    }

    return error.code ? `${error.message}（${error.code}）` : error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "操作失败，请稍后重试。";
}

function sourceSummary(source: CompanySource) {
  if (source.source_type === "url") {
    return source.url ?? "未填写 URL";
  }

  return compactText(source.raw_content, "未填写文本内容");
}

function sourceName(source?: CompanySource) {
  if (!source) {
    return "来源已不可用";
  }

  return `${sourceTypeLabels[source.source_type]}：${source.title}`;
}

function categoryLabel(category: string) {
  const labels: Record<string, string> = {
    source_summary: "来源摘要",
  };

  return labels[category] ?? category;
}

function KnowledgeStatusBadge({ status }: { status: KnowledgeStatus }) {
  return (
    <span className={knowledgeStatusTone[status]}>
      {knowledgeStatusLabels[status]}
    </span>
  );
}

function AppIcon({
  name,
}: {
  name:
    | "box"
    | "card"
    | "check"
    | "database"
    | "file"
    | "gear"
    | "home"
    | "link"
    | "plus"
    | "refresh"
    | "tasks";
}) {
  const icons = {
    box: <path d="m21 8-9-5-9 5 9 5 9-5ZM3 8v8l9 5 9-5V8M12 13v8" />,
    card: <path d="M4 6h16v12H4zM4 10h16M8 14h3M14 14h2" />,
    check: <path d="m5 12 4 4L19 6" />,
    database: (
      <path d="M4 6c0-2 16-2 16 0v12c0 2-16 2-16 0V6Zm0 0c0 2 16 2 16 0M4 12c0 2 16 2 16 0" />
    ),
    file: <path d="M6 3h8l4 4v14H6zM14 3v5h5M9 13h6M9 17h5" />,
    gear: (
      <path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM4 12h2M18 12h2M12 4v2M12 18v2M6.4 6.4l1.4 1.4M16.2 16.2l1.4 1.4M17.6 6.4l-1.4 1.4M7.8 16.2l-1.4 1.4" />
    ),
    home: <path d="m4 10 8-6 8 6v9a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1v-9Z" />,
    link: (
      <path d="M10 13a5 5 0 0 0 7.1 0l1.4-1.4a5 5 0 0 0-7.1-7.1L10.5 5M14 11a5 5 0 0 0-7.1 0l-1.4 1.4a5 5 0 0 0 7.1 7.1l.9-.9" />
    ),
    plus: <path d="M12 5v14M5 12h14" />,
    refresh: <path d="M20 12a8 8 0 0 1-13.7 5.7M4 12A8 8 0 0 1 17.7 6.3M18 3v4h-4M6 21v-4h4" />,
    tasks: <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" />,
  };

  return (
    <svg
      aria-hidden="true"
      className="app-icon"
      fill="none"
      viewBox="0 0 24 24"
    >
      {icons[name]}
    </svg>
  );
}

export default function KnowledgeWorkspace() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState("");
  const [sources, setSources] = useState<CompanySource[]>([]);
  const [knowledgeItems, setKnowledgeItems] = useState<KnowledgeItem[]>([]);
  const [activeTab, setActiveTab] = useState<WorkspaceTab>("company");
  const [knowledgeFilter, setKnowledgeFilter] =
    useState<KnowledgeFilter>("all");
  const [sourceSearch, setSourceSearch] = useState("");
  const [drawer, setDrawer] = useState<DrawerState | null>(null);
  const [modal, setModal] = useState<ModalState | null>(null);
  const [companyForm, setCompanyForm] =
    useState<CompanyFormState>(emptyCompanyForm);
  const [sourceForm, setSourceForm] = useState<SourceFormState>(emptySourceForm);
  const [isBootLoading, setIsBootLoading] = useState(true);
  const [isDataLoading, setIsDataLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");

  const selectedCompany = companies.find((item) => item.id === selectedCompanyId);
  const sourceById = useMemo(() => {
    return new Map(sources.map((source) => [source.id, source]));
  }, [sources]);

  const filteredSources = useMemo(() => {
    const query = sourceSearch.trim().toLowerCase();
    if (!query) {
      return sources;
    }

    return sources.filter((source) => {
      return [source.title, source.url, source.raw_content]
        .filter(Boolean)
        .some((value) => value!.toLowerCase().includes(query));
    });
  }, [sourceSearch, sources]);

  const visibleKnowledgeItems = useMemo(() => {
    if (knowledgeFilter === "all") {
      return knowledgeItems;
    }
    return knowledgeItems.filter((item) => item.status === knowledgeFilter);
  }, [knowledgeFilter, knowledgeItems]);

  const sourceCounts = useMemo(
    () => ({
      all: sources.length,
      text: sources.filter((source) => source.source_type === "text").length,
      url: sources.filter((source) => source.source_type === "url").length,
    }),
    [sources],
  );

  const knowledgeCounts = useMemo(
    () => ({
      all: knowledgeItems.length,
      draft: knowledgeItems.filter((item) => item.status === "draft").length,
      confirmed: knowledgeItems.filter((item) => item.status === "confirmed")
        .length,
      rejected: knowledgeItems.filter((item) => item.status === "rejected")
        .length,
    }),
    [knowledgeItems],
  );

  async function refreshCompanyList(preferredCompanyId?: string) {
    const result = await listCompanies();
    const nextCompanyId =
      preferredCompanyId && result.items.some((item) => item.id === preferredCompanyId)
        ? preferredCompanyId
        : result.items[0]?.id ?? "";

    setCompanies(result.items);
    setSelectedCompanyId(nextCompanyId);
    return nextCompanyId;
  }

  async function refreshPhaseData(companyId = selectedCompanyId) {
    if (!companyId) {
      setSources([]);
      setKnowledgeItems([]);
      return;
    }

    setIsDataLoading(true);
    setError("");
    try {
      const [sourceResult, knowledgeResult] = await Promise.all([
        listSources(companyId),
        listKnowledge(companyId),
      ]);
      setSources(sourceResult.items);
      setKnowledgeItems(knowledgeResult.items);
    } catch (requestError) {
      setError(getErrorMessage(requestError));
    } finally {
      setIsDataLoading(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialData() {
      setIsBootLoading(true);
      setError("");
      try {
        const result = await listCompanies();
        if (cancelled) {
          return;
        }
        setCompanies(result.items);
        setSelectedCompanyId(result.items[0]?.id ?? "");
      } catch (requestError) {
        if (!cancelled) {
          setError(getErrorMessage(requestError));
        }
      } finally {
        if (!cancelled) {
          setIsBootLoading(false);
        }
      }
    }

    void loadInitialData();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    setDrawer(null);
    setModal(null);
    setSourceSearch("");

    if (selectedCompanyId) {
      void refreshPhaseData(selectedCompanyId);
    } else {
      setSources([]);
      setKnowledgeItems([]);
    }
  }, [selectedCompanyId]);

  function showToast(message: string) {
    setToast(message);
    window.setTimeout(() => setToast(""), 3200);
  }

  async function runAction(action: () => Promise<void>) {
    setIsSubmitting(true);
    setError("");
    try {
      await action();
    } catch (requestError) {
      setError(getErrorMessage(requestError));
    } finally {
      setIsSubmitting(false);
    }
  }

  function openCompanyDrawer(mode: "create" | "edit") {
    setCompanyForm(mode === "edit" ? toCompanyForm(selectedCompany) : emptyCompanyForm);
    setDrawer({ type: "company", mode });
  }

  function openSourceDrawer() {
    setActiveTab("sources");
    setSourceForm(emptySourceForm);
    setDrawer({ type: "source" });
  }

  async function handleCompanySubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!companyForm.name.trim()) {
      setError("请填写公司名称。");
      return;
    }

    await runAction(async () => {
      const payload = toCompanyPayload(companyForm);
      const savedCompany =
        drawer?.type === "company" &&
        drawer.mode === "edit" &&
        selectedCompany
          ? await updateCompany(selectedCompany.id, payload)
          : await createCompany(payload);

      const nextCompanyId = await refreshCompanyList(savedCompany.id);
      await refreshPhaseData(nextCompanyId);
      setDrawer(null);
      showToast(
        drawer?.type === "company" && drawer.mode === "edit"
          ? "公司资料已保存。"
          : "公司资料已创建。",
      );
    });
  }

  async function handleSourceSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCompanyId) {
      setError("请先创建或选择公司资料。");
      return;
    }

    const title = sourceForm.title.trim();
    if (!title) {
      setError("请填写资料标题。");
      return;
    }

    const payload: SourcePayload = {
      source_type: sourceForm.source_type,
      title,
    };

    if (sourceForm.source_type === "text") {
      const rawContent = sourceForm.raw_content.trim();
      if (!rawContent) {
        setError("文本资料需要填写原始内容。");
        return;
      }
      payload.raw_content = rawContent;
      payload.url = null;
    } else {
      const url = sourceForm.url.trim();
      if (!url) {
        setError("网页链接需要填写 URL 地址。");
        return;
      }
      payload.url = url;
      payload.raw_content = toNullable(sourceForm.raw_content);
    }

    await runAction(async () => {
      await createSource(selectedCompanyId, payload);
      await refreshPhaseData(selectedCompanyId);
      setDrawer(null);
      showToast("资料来源已保存。");
    });
  }

  async function handleCreateKnowledgeDraft(source: CompanySource) {
    await runAction(async () => {
      await createKnowledgeDraft(source.id);
      await refreshPhaseData(source.company_id);
      setActiveTab("knowledge");
      showToast("知识草稿已生成，请在知识审核中确认或拒绝。");
    });
  }

  async function handleKnowledgeModalAction() {
    if (!modal) {
      return;
    }

    if (
      modal.type !== "confirmKnowledge" &&
      modal.type !== "rejectKnowledge"
    ) {
      return;
    }

    const knowledge = modal.knowledge;

    await runAction(async () => {
      if (modal.type === "confirmKnowledge") {
        await confirmKnowledge(knowledge.id);
        showToast("知识条目已确认。");
      }

      if (modal.type === "rejectKnowledge") {
        await rejectKnowledge(knowledge.id);
        showToast("知识草稿已拒绝。");
      }

      await refreshPhaseData(knowledge.company_id);
      setModal(null);
    });
  }

  return (
    <div className="campaign-app knowledge-app">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">AI</div>
          <div>
            <strong>AI 销售系统</strong>
            <span>智能获客工作台</span>
          </div>
        </div>

        <nav className="side-nav" aria-label="主导航">
          <a href="#knowledge" className="active">
            <AppIcon name="database" />
            知识库
          </a>
          <a href="#products">
            <AppIcon name="card" />
            产品卡片
          </a>
          <a href="#campaigns">
            <AppIcon name="tasks" />
            获客任务
          </a>
        </nav>

        <button
          className="sidebar-create-button"
          disabled={!selectedCompanyId}
          onClick={openSourceDrawer}
          type="button"
        >
          <AppIcon name="plus" />
          新增资料来源
        </button>
      </aside>

      <main className="workspace">
        <header className="workspace-header">
          <div>
            <p className="workspace-kicker">前端阶段一</p>
            <h1>公司知识库</h1>
          </div>
          <div className="header-actions">
            <label className="company-selector">
              <span>当前公司</span>
              <select
                disabled={companies.length === 0}
                onChange={(event) => setSelectedCompanyId(event.target.value)}
                value={selectedCompanyId}
              >
                {companies.length === 0 ? (
                  <option value="">暂无公司资料</option>
                ) : (
                  companies.map((company) => (
                    <option key={company.id} value={company.id}>
                      {company.name}
                    </option>
                  ))
                )}
              </select>
            </label>
            <button
              className="secondary-button"
              onClick={() =>
                selectedCompany
                  ? openCompanyDrawer("edit")
                  : openCompanyDrawer("create")
              }
              type="button"
            >
              {selectedCompany ? "编辑公司资料" : "创建公司资料"}
            </button>
            <button
              className="primary-button"
              disabled={!selectedCompanyId}
              onClick={openSourceDrawer}
              type="button"
            >
              <AppIcon name="plus" />
              新增资料来源
            </button>
          </div>
        </header>

        {toast ? <div className="toast">{toast}</div> : null}

        {error ? (
          <div className="notice notice--error">
            <strong>操作未完成</strong>
            <span>{error}</span>
            <button
              className="ghost-button"
              onClick={() => void refreshPhaseData()}
              type="button"
            >
              重试
            </button>
          </div>
        ) : null}

        {isBootLoading ? (
          <StatePanel
            title="正在加载知识库"
            text="正在读取公司资料、资料来源和知识条目。"
          />
        ) : null}

        {!isBootLoading ? (
          <>
            <PhaseTabs activeTab={activeTab} onChange={setActiveTab} />

            {selectedCompany ? (
              <KnowledgeSummary
                company={selectedCompany}
                isLoading={isDataLoading}
                knowledgeCounts={knowledgeCounts}
                sourceCounts={sourceCounts}
              />
            ) : null}

            {activeTab === "company" ? (
              <CompanyPanel
                company={selectedCompany}
                onCreate={() => openCompanyDrawer("create")}
                onEdit={() => openCompanyDrawer("edit")}
              />
            ) : null}

            {activeTab === "sources" ? (
              <SourcesPanel
                isLoading={isDataLoading}
                onCreateDraft={(source) => void handleCreateKnowledgeDraft(source)}
                onNewSource={openSourceDrawer}
                onSearch={setSourceSearch}
                onView={(source) => setModal({ type: "sourceDetail", source })}
                query={sourceSearch}
                sources={filteredSources}
              />
            ) : null}

            {activeTab === "knowledge" ? (
              <KnowledgePanel
                filter={knowledgeFilter}
                isLoading={isDataLoading}
                items={visibleKnowledgeItems}
                knowledgeCounts={knowledgeCounts}
                onConfirm={(knowledge) =>
                  setModal({ type: "confirmKnowledge", knowledge })
                }
                onFilterChange={setKnowledgeFilter}
                onReject={(knowledge) =>
                  setModal({ type: "rejectKnowledge", knowledge })
                }
                onView={(knowledge) =>
                  setModal({ type: "knowledgeDetail", knowledge })
                }
                sourceById={sourceById}
              />
            ) : null}
          </>
        ) : null}
      </main>

      {drawer?.type === "company" ? (
        <CompanyDrawer
          form={companyForm}
          isSubmitting={isSubmitting}
          mode={drawer.mode}
          onCancel={() => setDrawer(null)}
          onChange={setCompanyForm}
          onSubmit={(event) => void handleCompanySubmit(event)}
        />
      ) : null}

      {drawer?.type === "source" ? (
        <SourceDrawer
          form={sourceForm}
          isSubmitting={isSubmitting}
          onCancel={() => setDrawer(null)}
          onChange={setSourceForm}
          onSubmit={(event) => void handleSourceSubmit(event)}
        />
      ) : null}

      {modal ? (
        <KnowledgeModal
          isSubmitting={isSubmitting}
          modal={modal}
          onCancel={() => setModal(null)}
          onConfirm={() => void handleKnowledgeModalAction()}
          sourceById={sourceById}
        />
      ) : null}
    </div>
  );
}

function PhaseTabs({
  activeTab,
  onChange,
}: {
  activeTab: WorkspaceTab;
  onChange: (value: WorkspaceTab) => void;
}) {
  return (
    <section className="surface-panel phase-tabs-panel">
      <div className="segmented-control" aria-label="知识库阶段导航">
        {workspaceTabs.map((tab) => (
          <button
            className={activeTab === tab.value ? "selected" : ""}
            key={tab.value}
            onClick={() => onChange(tab.value)}
            type="button"
          >
            {tab.label}
          </button>
        ))}
      </div>
    </section>
  );
}

function KnowledgeSummary({
  company,
  isLoading,
  knowledgeCounts,
  sourceCounts,
}: {
  company: Company;
  isLoading: boolean;
  knowledgeCounts: Record<KnowledgeFilter, number>;
  sourceCounts: { all: number; text: number; url: number };
}) {
  return (
    <section className="summary-grid knowledge-summary-grid">
      <article className="summary-card summary-card--wide">
        <span>当前公司</span>
        <strong>{company.name}</strong>
        <p>{compactText(company.target_market, "尚未填写目标市场")}</p>
      </article>
      <article className="summary-card">
        <span>资料来源</span>
        <strong>{isLoading ? "..." : sourceCounts.all}</strong>
        <p>
          文本 {sourceCounts.text} 条，URL {sourceCounts.url} 条
        </p>
      </article>
      <article className="summary-card">
        <span>待审核草稿</span>
        <strong>{isLoading ? "..." : knowledgeCounts.draft}</strong>
        <p>需要人工确认或拒绝</p>
      </article>
      <article className="summary-card">
        <span>已确认知识</span>
        <strong>{isLoading ? "..." : knowledgeCounts.confirmed}</strong>
        <p>可用于后续产品卡片</p>
      </article>
    </section>
  );
}

function CompanyPanel({
  company,
  onCreate,
  onEdit,
}: {
  company?: Company;
  onCreate: () => void;
  onEdit: () => void;
}) {
  if (!company) {
    return (
      <StatePanel
        title="暂无公司资料"
        text="请先创建公司基础信息，再添加资料来源并生成知识草稿。"
      >
        <button className="primary-button" onClick={onCreate} type="button">
          <AppIcon name="plus" />
          创建公司资料
        </button>
      </StatePanel>
    );
  }

  const targetMarkets = splitTags(company.target_market);
  const valueItems = splitTags(company.value_proposition);

  return (
    <section className="company-profile-grid">
      <article className="info-card company-info-card">
        <div className="card-heading">
          <div>
            <span className="section-kicker">基础信息</span>
            <h2>公司资料</h2>
          </div>
          <button className="secondary-button" onClick={onEdit} type="button">
            编辑资料
          </button>
        </div>
        <dl className="profile-fields">
          <div>
            <dt>公司名称</dt>
            <dd>{company.name}</dd>
          </div>
          <div>
            <dt>所属行业</dt>
            <dd>{compactText(company.industry)}</dd>
          </div>
          <div>
            <dt>官方网站</dt>
            <dd>
              {company.website ? (
                <a
                  className="source-link"
                  href={company.website}
                  rel="noreferrer"
                  target="_blank"
                >
                  {company.website}
                </a>
              ) : (
                "未填写"
              )}
            </dd>
          </div>
        </dl>
      </article>

      <article className="info-card company-info-card">
        <span className="section-kicker">公司画像</span>
        <h2>业务描述</h2>
        <p>{compactText(company.description)}</p>
        <div className="divider" />
        <h3>目标市场</h3>
        {targetMarkets.length > 0 ? (
          <div className="chip-list">
            {targetMarkets.map((item) => (
              <span key={item}>{item}</span>
            ))}
          </div>
        ) : (
          <p className="muted-text">尚未填写目标市场。</p>
        )}
      </article>

      <article className="info-card company-info-card">
        <span className="section-kicker">核心价值</span>
        <h2>价值主张</h2>
        {valueItems.length > 0 ? (
          <ul className="check-list">
            {valueItems.map((item) => (
              <li key={item}>
                <AppIcon name="check" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="muted-text">尚未填写价值主张。</p>
        )}
      </article>
    </section>
  );
}

function SourcesPanel({
  isLoading,
  onCreateDraft,
  onNewSource,
  onSearch,
  onView,
  query,
  sources,
}: {
  isLoading: boolean;
  onCreateDraft: (source: CompanySource) => void;
  onNewSource: () => void;
  onSearch: (query: string) => void;
  onView: (source: CompanySource) => void;
  query: string;
  sources: CompanySource[];
}) {
  if (isLoading) {
    return (
      <StatePanel
        title="正在读取资料来源"
        text="正在同步当前公司的文本资料和 URL 记录。"
      />
    );
  }

  return (
    <section className="surface-panel">
      <div className="notice">
        <strong>当前阶段范围</strong>
        <span>仅保存文本和 URL，不会抓取、解析或读取网页内容。</span>
      </div>
      <div className="panel-toolbar">
        <label className="lead-search source-search">
          <span>搜索资料</span>
          <input
            onChange={(event) => onSearch(event.target.value)}
            placeholder="搜索资料标题、内容或 URL"
            type="search"
            value={query}
          />
        </label>
        <button className="primary-button" onClick={onNewSource} type="button">
          <AppIcon name="plus" />
          新增资料来源
        </button>
      </div>

      {sources.length === 0 ? (
        <StatePanel
          title="暂无资料来源"
          text="添加文本资料或网页链接，作为知识草稿的来源。"
        >
          <button className="primary-button" onClick={onNewSource} type="button">
            立即新增
          </button>
        </StatePanel>
      ) : (
        <div className="table-wrap">
          <table className="campaign-table phase-table">
            <thead>
              <tr>
                <th>标题</th>
                <th>来源类型</th>
                <th>内容摘要 / URL</th>
                <th>状态</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {sources.map((source) => (
                <tr key={source.id}>
                  <td>
                    <button
                      className="link-button table-title"
                      onClick={() => onView(source)}
                      type="button"
                    >
                      {source.title}
                    </button>
                  </td>
                  <td>
                    <span className="source-type-label">
                      <AppIcon name={source.source_type === "url" ? "link" : "file"} />
                      {sourceTypeLabels[source.source_type]}
                    </span>
                  </td>
                  <td className="phase-table__summary">{sourceSummary(source)}</td>
                  <td>
                    <span className="mini-status mini-status--success">已保存</span>
                  </td>
                  <td>{formatDate(source.created_at)}</td>
                  <td>
                    <div className="row-actions">
                      <button onClick={() => onView(source)} type="button">
                        查看
                      </button>
                      <button
                        onClick={() => onCreateDraft(source)}
                        type="button"
                      >
                        生成知识草稿
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function KnowledgePanel({
  filter,
  isLoading,
  items,
  knowledgeCounts,
  onConfirm,
  onFilterChange,
  onReject,
  onView,
  sourceById,
}: {
  filter: KnowledgeFilter;
  isLoading: boolean;
  items: KnowledgeItem[];
  knowledgeCounts: Record<KnowledgeFilter, number>;
  onConfirm: (knowledge: KnowledgeItem) => void;
  onFilterChange: (filter: KnowledgeFilter) => void;
  onReject: (knowledge: KnowledgeItem) => void;
  onView: (knowledge: KnowledgeItem) => void;
  sourceById: Map<string, CompanySource>;
}) {
  if (isLoading) {
    return (
      <StatePanel
        title="正在读取知识条目"
        text="正在同步草稿、已确认和已拒绝的知识记录。"
      />
    );
  }

  return (
    <section className="surface-panel">
      <div className="panel-toolbar">
        <div className="segmented-control" aria-label="知识状态筛选">
          {knowledgeFilters.map((item) => (
            <button
              className={filter === item.value ? "selected" : ""}
              key={item.value}
              onClick={() => onFilterChange(item.value)}
              type="button"
            >
              {item.label}（{knowledgeCounts[item.value]}）
            </button>
          ))}
        </div>
      </div>

      {items.length === 0 ? (
        <StatePanel
          title="暂无知识条目"
          text="请先从资料来源生成知识草稿，再在这里确认或拒绝。"
        />
      ) : (
        <div className="table-wrap">
          <table className="campaign-table phase-table knowledge-table">
            <thead>
              <tr>
                <th>标题</th>
                <th>分类</th>
                <th>内容摘要</th>
                <th>来源</th>
                <th>状态</th>
                <th>更新时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {items.map((knowledge) => {
                const source = knowledge.source_id
                  ? sourceById.get(knowledge.source_id)
                  : undefined;
                return (
                  <tr key={knowledge.id}>
                    <td>
                      <button
                        className="link-button table-title"
                        onClick={() => onView(knowledge)}
                        type="button"
                      >
                        {knowledge.title}
                      </button>
                    </td>
                    <td>{categoryLabel(knowledge.category)}</td>
                    <td className="phase-table__summary">{knowledge.content}</td>
                    <td>{sourceName(source)}</td>
                    <td>
                      <KnowledgeStatusBadge status={knowledge.status} />
                    </td>
                    <td>{formatDate(knowledge.updated_at)}</td>
                    <td>
                      <div className="row-actions">
                        <button onClick={() => onView(knowledge)} type="button">
                          查看
                        </button>
                        {knowledge.status === "draft" ? (
                          <>
                            <button
                              onClick={() => onConfirm(knowledge)}
                              type="button"
                            >
                              确认
                            </button>
                            <button
                              className="danger-action"
                              onClick={() => onReject(knowledge)}
                              type="button"
                            >
                              拒绝
                            </button>
                          </>
                        ) : null}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function CompanyDrawer({
  form,
  isSubmitting,
  mode,
  onCancel,
  onChange,
  onSubmit,
}: {
  form: CompanyFormState;
  isSubmitting: boolean;
  mode: "create" | "edit";
  onCancel: () => void;
  onChange: (form: CompanyFormState) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <DrawerFrame
      onCancel={onCancel}
      title={mode === "edit" ? "编辑公司资料" : "创建公司资料"}
    >
      <form className="drawer-form" onSubmit={onSubmit}>
        <div className="drawer-body">
          <section className="drawer-section">
            <h3>基础信息</h3>
            <label>
              <span>公司名称 *</span>
              <input
                onChange={(event) =>
                  onChange({ ...form, name: event.target.value })
                }
                required
                type="text"
                value={form.name}
              />
            </label>
            <label>
              <span>所属行业</span>
              <input
                onChange={(event) =>
                  onChange({ ...form, industry: event.target.value })
                }
                type="text"
                value={form.industry}
              />
            </label>
            <label>
              <span>官方网站</span>
              <input
                onChange={(event) =>
                  onChange({ ...form, website: event.target.value })
                }
                placeholder="https://"
                type="url"
                value={form.website}
              />
            </label>
          </section>

          <section className="drawer-section">
            <h3>公司画像</h3>
            <label>
              <span>公司描述</span>
              <textarea
                onChange={(event) =>
                  onChange({ ...form, description: event.target.value })
                }
                rows={5}
                value={form.description}
              />
            </label>
            <label>
              <span>目标市场</span>
              <textarea
                onChange={(event) =>
                  onChange({ ...form, target_market: event.target.value })
                }
                placeholder="可用逗号或换行分隔多个标签"
                rows={3}
                value={form.target_market}
              />
            </label>
            <label>
              <span>价值主张</span>
              <textarea
                onChange={(event) =>
                  onChange({ ...form, value_proposition: event.target.value })
                }
                placeholder="每行一条价值主张"
                rows={4}
                value={form.value_proposition}
              />
            </label>
          </section>
        </div>

        <div className="drawer-footer">
          <button className="secondary-button" onClick={onCancel} type="button">
            取消
          </button>
          <button className="primary-button" disabled={isSubmitting} type="submit">
            保存修改
          </button>
        </div>
      </form>
    </DrawerFrame>
  );
}

function SourceDrawer({
  form,
  isSubmitting,
  onCancel,
  onChange,
  onSubmit,
}: {
  form: SourceFormState;
  isSubmitting: boolean;
  onCancel: () => void;
  onChange: (form: SourceFormState) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <DrawerFrame onCancel={onCancel} title="新增资料来源">
      <form className="drawer-form" onSubmit={onSubmit}>
        <div className="drawer-body">
          <div className="tab-switcher">
            <button
              className={form.source_type === "text" ? "selected" : ""}
              onClick={() => onChange({ ...emptySourceForm, source_type: "text" })}
              type="button"
            >
              文本资料
            </button>
            <button
              className={form.source_type === "url" ? "selected" : ""}
              onClick={() => onChange({ ...emptySourceForm, source_type: "url" })}
              type="button"
            >
              网页链接
            </button>
          </div>

          <section className="drawer-section">
            <label>
              <span>标题 *</span>
              <input
                onChange={(event) =>
                  onChange({ ...form, title: event.target.value })
                }
                required
                type="text"
                value={form.title}
              />
            </label>

            {form.source_type === "text" ? (
              <label>
                <span>原始内容 *</span>
                <textarea
                  onChange={(event) =>
                    onChange({ ...form, raw_content: event.target.value })
                  }
                  placeholder="在此粘贴或输入文本内容"
                  required
                  rows={10}
                  value={form.raw_content}
                />
              </label>
            ) : (
              <>
                <label>
                  <span>URL 地址 *</span>
                  <input
                    onChange={(event) =>
                      onChange({ ...form, url: event.target.value })
                    }
                    placeholder="https://"
                    required
                    type="url"
                    value={form.url}
                  />
                </label>
                <label>
                  <span>备注 / 补充说明</span>
                  <textarea
                    onChange={(event) =>
                      onChange({ ...form, raw_content: event.target.value })
                    }
                    placeholder="可补充说明该链接为什么重要。当前阶段不会读取网页内容。"
                    rows={4}
                    value={form.raw_content}
                  />
                </label>
              </>
            )}

            <p className="muted-text">
              当前 Phase 1 只保存文本或 URL 记录；URL 不会被爬取、解析或自动读取。
            </p>
          </section>
        </div>

        <div className="drawer-footer">
          <button className="secondary-button" onClick={onCancel} type="button">
            取消
          </button>
          <button className="primary-button" disabled={isSubmitting} type="submit">
            保存提交
          </button>
        </div>
      </form>
    </DrawerFrame>
  );
}

function DrawerFrame({
  children,
  onCancel,
  title,
}: {
  children: ReactNode;
  onCancel: () => void;
  title: string;
}) {
  return (
    <>
      <div className="drawer-backdrop" onClick={onCancel} />
      <aside className="side-drawer" aria-modal="true" role="dialog">
        <div className="drawer-header">
          <h2>{title}</h2>
          <button className="ghost-button" onClick={onCancel} type="button">
            关闭
          </button>
        </div>
        {children}
      </aside>
    </>
  );
}

function KnowledgeModal({
  isSubmitting,
  modal,
  onCancel,
  onConfirm,
  sourceById,
}: {
  isSubmitting: boolean;
  modal: ModalState;
  onCancel: () => void;
  onConfirm: () => void;
  sourceById: Map<string, CompanySource>;
}) {
  if (modal.type === "sourceDetail") {
    return (
      <ModalFrame onCancel={onCancel} title="资料来源详情">
        <div className="detail-stack">
          <InfoLine label="标题" value={modal.source.title} />
          <InfoLine label="来源类型" value={sourceTypeLabels[modal.source.source_type]} />
          <InfoLine label="状态" value="已保存" />
          <InfoLine label="创建时间" value={formatDate(modal.source.created_at)} />
          {modal.source.source_type === "url" ? (
            <InfoLine label="URL" value={modal.source.url ?? "未填写"} />
          ) : null}
          <div>
            <span className="section-kicker">内容</span>
            <p className="modal-body-text">{sourceSummary(modal.source)}</p>
          </div>
        </div>
        <div className="modal-actions">
          <button className="primary-button" onClick={onCancel} type="button">
            关闭
          </button>
        </div>
      </ModalFrame>
    );
  }

  if (modal.type === "knowledgeDetail") {
    const source = modal.knowledge.source_id
      ? sourceById.get(modal.knowledge.source_id)
      : undefined;

    return (
      <ModalFrame onCancel={onCancel} title="知识条目详情">
        <div className="detail-stack">
          <InfoLine label="标题" value={modal.knowledge.title} />
          <InfoLine label="分类" value={categoryLabel(modal.knowledge.category)} />
          <InfoLine
            label="状态"
            value={knowledgeStatusLabels[modal.knowledge.status]}
          />
          <InfoLine label="来源" value={sourceName(source)} />
          <div>
            <span className="section-kicker">内容</span>
            <p className="modal-body-text">{modal.knowledge.content}</p>
          </div>
        </div>
        <div className="modal-actions">
          <button className="primary-button" onClick={onCancel} type="button">
            关闭
          </button>
        </div>
      </ModalFrame>
    );
  }

  const isConfirm = modal.type === "confirmKnowledge";
  const title = isConfirm ? "确认知识条目" : "拒绝知识条目";
  const description = isConfirm
    ? "确认后，该知识将作为后续产品卡片生成的可靠输入。"
    : "拒绝后，该草稿不会用于后续产品卡片生成。";

  return (
    <ModalFrame onCancel={onCancel} title={title}>
      <p>{description}</p>
      <div className="modal-actions">
        <button className="secondary-button" onClick={onCancel} type="button">
          取消
        </button>
        <button
          className={isConfirm ? "primary-button" : "danger-button"}
          disabled={isSubmitting}
          onClick={onConfirm}
          type="button"
        >
          {isConfirm ? "确认" : "拒绝"}
        </button>
      </div>
    </ModalFrame>
  );
}

function ModalFrame({
  children,
  onCancel,
  title,
}: {
  children: ReactNode;
  onCancel: () => void;
  title: string;
}) {
  return (
    <div className="modal-backdrop" role="presentation">
      <section className="modal-card" role="dialog" aria-modal="true">
        <div className="modal-card-heading">
          <h2>{title}</h2>
          <button className="ghost-button" onClick={onCancel} type="button">
            关闭
          </button>
        </div>
        {children}
      </section>
    </div>
  );
}

function InfoLine({ label, value }: { label: string; value: string }) {
  return (
    <div className="info-line">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function StatePanel({
  children,
  text,
  title,
}: {
  children?: ReactNode;
  text: string;
  title: string;
}) {
  return (
    <section className="state-panel">
      <div className="state-icon" />
      <h3>{title}</h3>
      <p>{text}</p>
      {children ? <div className="state-actions">{children}</div> : null}
    </section>
  );
}
