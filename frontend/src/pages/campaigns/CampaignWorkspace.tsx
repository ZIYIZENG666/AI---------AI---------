import { FormEvent, useEffect, useMemo, useState } from "react";

import {
  ApiError,
  Campaign,
  CampaignPayload,
  CampaignStatus,
  CampaignUpdatePayload,
  Company,
  ProductCard,
  archiveCampaign,
  confirmCampaign,
  createCampaign,
  deleteCampaign,
  duplicateCampaign,
  listCampaigns,
  listCompanies,
  listConfirmedProductCards,
  updateCampaign,
} from "../../api/campaigns";

type StatusFilter = "all" | CampaignStatus;
type WorkspaceView = "list" | "create" | "detail" | "edit";
type ModalAction = "confirm" | "delete" | "archive";

interface FormState {
  product_card_id: string;
  name: string;
  target_country: string;
  target_region: string;
  target_industry: string;
  target_company_type: string;
  target_role: string;
  search_keywords: string;
  qualification_criteria: string;
  outreach_angle: string;
  lead_limit: string;
}

const statusLabels: Record<CampaignStatus, string> = {
  draft: "草稿",
  confirmed: "已确认",
  archived: "已归档",
};

const statusTone: Record<CampaignStatus, string> = {
  draft: "status-badge status-badge--draft",
  confirmed: "status-badge status-badge--confirmed",
  archived: "status-badge status-badge--archived",
};

const statusFilters: Array<{ value: StatusFilter; label: string }> = [
  { value: "all", label: "全部" },
  { value: "draft", label: "草稿" },
  { value: "confirmed", label: "已确认" },
  { value: "archived", label: "已归档" },
];

const emptyFormState: FormState = {
  product_card_id: "",
  name: "",
  target_country: "",
  target_region: "",
  target_industry: "",
  target_company_type: "",
  target_role: "",
  search_keywords: "",
  qualification_criteria: "",
  outreach_angle: "",
  lead_limit: "20",
};

function toNullable(value: string) {
  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}

function splitList(value: string) {
  return value
    .split(/[\n,，]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function joinList(value: string[]) {
  return value.join("\n");
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

function getErrorMessage(error: unknown) {
  if (error instanceof ApiError) {
    return error.code ? `${error.message}（${error.code}）` : error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "操作失败，请稍后重试。";
}

function createFormState(campaign?: Campaign): FormState {
  if (!campaign) {
    return emptyFormState;
  }

  return {
    product_card_id: campaign.product_card_id,
    name: campaign.name,
    target_country: campaign.target_country ?? "",
    target_region: campaign.target_region ?? "",
    target_industry: campaign.target_industry ?? "",
    target_company_type: campaign.target_company_type ?? "",
    target_role: campaign.target_role ?? "",
    search_keywords: joinList(campaign.search_keywords),
    qualification_criteria: joinList(campaign.qualification_criteria),
    outreach_angle: campaign.outreach_angle ?? "",
    lead_limit: String(campaign.lead_limit),
  };
}

function productName(
  campaign: Campaign,
  productCards: ProductCard[],
  fallback = "已确认产品卡片",
) {
  return (
    campaign.product_card_snapshot?.name ??
    productCards.find((item) => item.id === campaign.product_card_id)?.name ??
    fallback
  );
}

function CampaignStatusBadge({ status }: { status: CampaignStatus }) {
  return <span className={statusTone[status]}>{statusLabels[status]}</span>;
}

function AppIcon({
  name,
}: {
  name: "plus" | "tasks" | "box" | "gear" | "home" | "card";
}) {
  const icons = {
    plus: (
      <path d="M12 5v14M5 12h14" />
    ),
    tasks: (
      <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" />
    ),
    box: (
      <path d="m21 8-9-5-9 5 9 5 9-5ZM3 8v8l9 5 9-5V8M12 13v8" />
    ),
    gear: (
      <path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM4 12h2M18 12h2M12 4v2M12 18v2M6.4 6.4l1.4 1.4M16.2 16.2l1.4 1.4M17.6 6.4l-1.4 1.4M7.8 16.2l-1.4 1.4" />
    ),
    home: (
      <path d="m4 10 8-6 8 6v9a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1v-9Z" />
    ),
    card: <path d="M4 6h16v12H4zM4 10h16M8 14h3M14 14h2" />,
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

export default function CampaignWorkspace() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState("");
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [productCards, setProductCards] = useState<ProductCard[]>([]);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [view, setView] = useState<WorkspaceView>("list");
  const [selectedCampaignId, setSelectedCampaignId] = useState("");
  const [modal, setModal] = useState<{
    type: ModalAction;
    campaign: Campaign;
  } | null>(null);
  const [isBootLoading, setIsBootLoading] = useState(true);
  const [isDataLoading, setIsDataLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");

  const selectedCompany = companies.find((item) => item.id === selectedCompanyId);

  const visibleCampaigns = useMemo(() => {
    if (statusFilter === "all") {
      return campaigns;
    }
    return campaigns.filter((campaign) => campaign.status === statusFilter);
  }, [campaigns, statusFilter]);

  const counts = useMemo(
    () => ({
      all: campaigns.length,
      draft: campaigns.filter((campaign) => campaign.status === "draft").length,
      confirmed: campaigns.filter((campaign) => campaign.status === "confirmed")
        .length,
      archived: campaigns.filter((campaign) => campaign.status === "archived")
        .length,
    }),
    [campaigns],
  );

  const selectedCampaign =
    campaigns.find((campaign) => campaign.id === selectedCampaignId) ??
    visibleCampaigns[0] ??
    null;

  async function refreshCompanyData(companyId = selectedCompanyId) {
    if (!companyId) {
      return;
    }

    setIsDataLoading(true);
    setError("");
    try {
      const [campaignResult, productCardResult] = await Promise.all([
        listCampaigns(companyId),
        listConfirmedProductCards(companyId),
      ]);
      setCampaigns(campaignResult.items);
      setProductCards(productCardResult.items);
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
        const companyResult = await listCompanies();
        if (cancelled) {
          return;
        }
        setCompanies(companyResult.items);
        const firstCompanyId = companyResult.items[0]?.id ?? "";
        setSelectedCompanyId(firstCompanyId);
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
    if (selectedCompanyId) {
      void refreshCompanyData(selectedCompanyId);
    } else {
      setCampaigns([]);
      setProductCards([]);
    }
  }, [selectedCompanyId]);

  function showToast(message: string) {
    setToast(message);
    window.setTimeout(() => setToast(""), 3200);
  }

  function openDetail(campaign: Campaign) {
    setSelectedCampaignId(campaign.id);
    setView("detail");
  }

  function openEdit(campaign: Campaign) {
    setSelectedCampaignId(campaign.id);
    setView("edit");
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

  async function handleCreate(payload: CampaignPayload) {
    if (!selectedCompanyId) {
      setError("请先选择公司资料。");
      return;
    }

    await runAction(async () => {
      const created = await createCampaign(selectedCompanyId, payload);
      await refreshCompanyData(selectedCompanyId);
      setSelectedCampaignId(created.id);
      setView("detail");
      showToast("草稿任务已保存。");
    });
  }

  async function handleUpdate(campaign: Campaign, payload: CampaignUpdatePayload) {
    await runAction(async () => {
      const updated = await updateCampaign(campaign.id, payload);
      await refreshCompanyData(campaign.company_id);
      setSelectedCampaignId(updated.id);
      setView("detail");
      showToast("草稿任务已更新。");
    });
  }

  async function handleDuplicate(campaign: Campaign) {
    await runAction(async () => {
      const duplicated = await duplicateCampaign(campaign.id);
      await refreshCompanyData(campaign.company_id);
      setSelectedCampaignId(duplicated.id);
      setView("detail");
      showToast("已复制为新的草稿任务，可继续编辑后再确认。");
    });
  }

  async function handleModalConfirm() {
    if (!modal) {
      return;
    }

    const { campaign, type } = modal;
    await runAction(async () => {
      if (type === "confirm") {
        const confirmed = await confirmCampaign(campaign.id);
        await refreshCompanyData(campaign.company_id);
        setSelectedCampaignId(confirmed.id);
        setView("detail");
        showToast("获客任务已确认。");
      }

      if (type === "delete") {
        await deleteCampaign(campaign.id);
        await refreshCompanyData(campaign.company_id);
        setSelectedCampaignId("");
        setView("list");
        showToast("草稿任务已删除。");
      }

      if (type === "archive") {
        const archived = await archiveCampaign(campaign.id);
        await refreshCompanyData(campaign.company_id);
        setSelectedCampaignId(archived.id);
        setView("detail");
        showToast("获客任务已归档。");
      }
      setModal(null);
    });
  }

  return (
    <div className="campaign-app">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">AI</div>
          <div>
            <strong>AI 销售系统</strong>
            <span>智能获客工作台</span>
          </div>
        </div>

        <nav className="side-nav" aria-label="主导航">
          <a href="#home">
            <AppIcon name="home" />
            首页
          </a>
          <a href="#knowledge">
            <AppIcon name="box" />
            知识库
          </a>
          <a href="#products">
            <AppIcon name="card" />
            产品卡片
          </a>
          <a href="#campaigns" className="active">
            <AppIcon name="tasks" />
            获客任务
          </a>
          <a href="#settings">
            <AppIcon name="gear" />
            系统设置
          </a>
        </nav>

        <button
          className="sidebar-create-button"
          disabled={!selectedCompanyId}
          onClick={() => setView("create")}
          type="button"
        >
          <AppIcon name="plus" />
          新建任务
        </button>
      </aside>

      <main className="workspace">
        <header className="workspace-header">
          <div>
            <p className="workspace-kicker">AI 销售知识库 + AI 客户匹配判断系统</p>
            <h1>获客任务</h1>
          </div>
          <div className="header-actions">
            <label className="company-selector">
              <span>当前公司</span>
              <select
                disabled={companies.length === 0}
                onChange={(event) => {
                  setSelectedCompanyId(event.target.value);
                  setSelectedCampaignId("");
                  setView("list");
                }}
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
              className="primary-button"
              disabled={!selectedCompanyId}
              onClick={() => setView("create")}
              type="button"
            >
              <AppIcon name="plus" />
              新建获客任务
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
              onClick={() => void refreshCompanyData()}
              type="button"
            >
              重试
            </button>
          </div>
        ) : null}

        {isBootLoading ? (
          <StatePanel title="正在加载工作台" text="正在读取公司资料和获客任务。" />
        ) : null}

        {!isBootLoading && companies.length === 0 ? (
          <StatePanel
            title="暂无公司资料"
            text="请先在公司资料阶段创建公司，再进入获客任务管理。"
          />
        ) : null}

        {!isBootLoading && selectedCompany ? (
          <>
            <CampaignSummary
              company={selectedCompany}
              counts={counts}
              isLoading={isDataLoading}
            />

            {view === "create" ? (
              <CampaignForm
                company={selectedCompany}
                isSubmitting={isSubmitting}
                mode="create"
                onCancel={() => setView("list")}
                onSubmit={(payload) => void handleCreate(payload as CampaignPayload)}
                productCards={productCards}
              />
            ) : null}

            {view === "edit" && selectedCampaign ? (
              <CampaignForm
                campaign={selectedCampaign}
                company={selectedCompany}
                isSubmitting={isSubmitting}
                mode="edit"
                onCancel={() => setView("detail")}
                onSubmit={(payload) =>
                  void handleUpdate(
                    selectedCampaign,
                    payload as CampaignUpdatePayload,
                  )
                }
                productCards={productCards}
              />
            ) : null}

            {view === "list" ? (
              <section className="surface-panel">
                <div className="panel-toolbar">
                  <div className="segmented-control" aria-label="任务状态筛选">
                    {statusFilters.map((filter) => (
                      <button
                        className={statusFilter === filter.value ? "selected" : ""}
                        key={filter.value}
                        onClick={() => setStatusFilter(filter.value)}
                        type="button"
                      >
                        {filter.label}（{counts[filter.value]}）
                      </button>
                    ))}
                  </div>
                  <button
                    className="secondary-button"
                    onClick={() => void refreshCompanyData()}
                    type="button"
                  >
                    刷新
                  </button>
                </div>

                <CampaignTable
                  campaigns={visibleCampaigns}
                  isLoading={isDataLoading}
                  onArchive={(campaign) =>
                    setModal({ type: "archive", campaign })
                  }
                  onConfirm={(campaign) =>
                    setModal({ type: "confirm", campaign })
                  }
                  onDelete={(campaign) => setModal({ type: "delete", campaign })}
                  onDuplicate={(campaign) => void handleDuplicate(campaign)}
                  onEdit={openEdit}
                  onView={openDetail}
                  productCards={productCards}
                />
              </section>
            ) : null}

            {view === "detail" && selectedCampaign ? (
              <CampaignDetail
                campaign={selectedCampaign}
                isSubmitting={isSubmitting}
                onArchive={(campaign) => setModal({ type: "archive", campaign })}
                onBack={() => setView("list")}
                onConfirm={(campaign) => setModal({ type: "confirm", campaign })}
                onDelete={(campaign) => setModal({ type: "delete", campaign })}
                onDuplicate={(campaign) => void handleDuplicate(campaign)}
                onEdit={openEdit}
                productCards={productCards}
              />
            ) : null}
          </>
        ) : null}
      </main>

      {modal ? (
        <ActionModal
          isSubmitting={isSubmitting}
          modal={modal}
          onCancel={() => setModal(null)}
          onConfirm={() => void handleModalConfirm()}
        />
      ) : null}
    </div>
  );
}

function CampaignSummary({
  company,
  counts,
  isLoading,
}: {
  company: Company;
  counts: Record<StatusFilter, number>;
  isLoading: boolean;
}) {
  return (
    <section className="summary-grid">
      <article className="summary-card summary-card--wide">
        <span>当前公司</span>
        <strong>{company.name}</strong>
        <p>{company.target_market ?? "尚未填写目标市场"}</p>
      </article>
      <article className="summary-card">
        <span>全部任务</span>
        <strong>{isLoading ? "..." : counts.all}</strong>
        <p>包含草稿、已确认和已归档</p>
      </article>
      <article className="summary-card">
        <span>可确认草稿</span>
        <strong>{isLoading ? "..." : counts.draft}</strong>
        <p>确认后锁定产品卡片快照</p>
      </article>
      <article className="summary-card">
        <span>历史归档</span>
        <strong>{isLoading ? "..." : counts.archived}</strong>
        <p>只读记录，不可恢复</p>
      </article>
    </section>
  );
}

function CampaignTable({
  campaigns,
  isLoading,
  onArchive,
  onConfirm,
  onDelete,
  onDuplicate,
  onEdit,
  onView,
  productCards,
}: {
  campaigns: Campaign[];
  isLoading: boolean;
  onArchive: (campaign: Campaign) => void;
  onConfirm: (campaign: Campaign) => void;
  onDelete: (campaign: Campaign) => void;
  onDuplicate: (campaign: Campaign) => void;
  onEdit: (campaign: Campaign) => void;
  onView: (campaign: Campaign) => void;
  productCards: ProductCard[];
}) {
  if (isLoading) {
    return <StatePanel title="正在读取任务" text="正在同步获客任务列表。" />;
  }

  if (campaigns.length === 0) {
    return (
      <StatePanel
        title="暂无获客任务"
        text="当前筛选下没有任务。您可以新建草稿任务，确认后供后续阶段使用。"
      />
    );
  }

  return (
    <div className="table-wrap">
      <table className="campaign-table">
        <thead>
          <tr>
            <th>获客任务 / 产品</th>
            <th>目标区域</th>
            <th>目标客户</th>
            <th>线索上限</th>
            <th>状态</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {campaigns.map((campaign) => (
            <tr key={campaign.id}>
              <td>
                <button
                  className="link-button table-title"
                  onClick={() => onView(campaign)}
                  type="button"
                >
                  {campaign.name}
                </button>
                <span>{productName(campaign, productCards)}</span>
              </td>
              <td>
                <strong>{campaign.target_country ?? "未填写"}</strong>
                <span>{campaign.target_region ?? "全部地区"}</span>
              </td>
              <td>
                <strong>{campaign.target_industry ?? "未填写行业"}</strong>
                <span>{campaign.target_role ?? "未填写角色"}</span>
              </td>
              <td className="numeric-cell">{campaign.lead_limit}</td>
              <td>
                <CampaignStatusBadge status={campaign.status} />
              </td>
              <td>{formatDate(campaign.updated_at)}</td>
              <td>
                <CampaignActions
                  campaign={campaign}
                  onArchive={onArchive}
                  onConfirm={onConfirm}
                  onDelete={onDelete}
                  onDuplicate={onDuplicate}
                  onEdit={onEdit}
                  onView={onView}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function CampaignActions({
  campaign,
  onArchive,
  onConfirm,
  onDelete,
  onDuplicate,
  onEdit,
  onView,
}: {
  campaign: Campaign;
  onArchive: (campaign: Campaign) => void;
  onConfirm: (campaign: Campaign) => void;
  onDelete: (campaign: Campaign) => void;
  onDuplicate: (campaign: Campaign) => void;
  onEdit: (campaign: Campaign) => void;
  onView: (campaign: Campaign) => void;
}) {
  if (campaign.status === "draft") {
    return (
      <div className="row-actions">
        <button onClick={() => onView(campaign)} type="button">
          查看详情
        </button>
        <button onClick={() => onEdit(campaign)} type="button">
          编辑
        </button>
        <button onClick={() => onConfirm(campaign)} type="button">
          确认获客任务
        </button>
        <button className="danger-action" onClick={() => onDelete(campaign)} type="button">
          删除
        </button>
      </div>
    );
  }

  if (campaign.status === "confirmed") {
    return (
      <div className="row-actions">
        <button onClick={() => onView(campaign)} type="button">
          查看详情
        </button>
        <button onClick={() => onDuplicate(campaign)} type="button">
          复制为草稿
        </button>
        <button onClick={() => onArchive(campaign)} type="button">
          归档
        </button>
      </div>
    );
  }

  return (
    <div className="row-actions">
      <button onClick={() => onView(campaign)} type="button">
        查看详情
      </button>
    </div>
  );
}

function CampaignDetail({
  campaign,
  isSubmitting,
  onArchive,
  onBack,
  onConfirm,
  onDelete,
  onDuplicate,
  onEdit,
  productCards,
}: {
  campaign: Campaign;
  isSubmitting: boolean;
  onArchive: (campaign: Campaign) => void;
  onBack: () => void;
  onConfirm: (campaign: Campaign) => void;
  onDelete: (campaign: Campaign) => void;
  onDuplicate: (campaign: Campaign) => void;
  onEdit: (campaign: Campaign) => void;
  productCards: ProductCard[];
}) {
  const snapshot = campaign.product_card_snapshot;
  const isDraft = campaign.status === "draft";
  const isConfirmed = campaign.status === "confirmed";
  const isArchived = campaign.status === "archived";

  return (
    <section className="detail-layout">
      <div className="detail-main">
        <div className="detail-header surface-panel">
          <button className="ghost-button" onClick={onBack} type="button">
            返回列表
          </button>
          <div>
            <div className="detail-title-line">
              <h2>{campaign.name}</h2>
              <CampaignStatusBadge status={campaign.status} />
            </div>
            <p>任务 ID：{campaign.id}</p>
          </div>
          <div className="detail-actions">
            {isDraft ? (
              <>
                <button className="secondary-button" onClick={() => onEdit(campaign)} type="button">
                  编辑
                </button>
                <button className="primary-button" onClick={() => onConfirm(campaign)} type="button">
                  确认获客任务
                </button>
                <button className="danger-button" onClick={() => onDelete(campaign)} type="button">
                  删除草稿
                </button>
              </>
            ) : null}
            {isConfirmed ? (
              <>
                <button
                  className="secondary-button"
                  disabled={isSubmitting}
                  onClick={() => onDuplicate(campaign)}
                  type="button"
                >
                  复制为草稿
                </button>
                <button className="secondary-button" onClick={() => onArchive(campaign)} type="button">
                  归档
                </button>
              </>
            ) : null}
            {isArchived ? (
              <span className="readonly-note">只读历史记录</span>
            ) : null}
          </div>
        </div>

        <div className="info-grid">
          <InfoCard title="目标市场">
            <DefinitionList
              items={[
                ["目标国家", campaign.target_country ?? "未填写"],
                ["目标地区", campaign.target_region ?? "全部地区"],
                ["行业", campaign.target_industry ?? "未填写"],
                ["客户类型", campaign.target_company_type ?? "未填写"],
                ["目标角色", campaign.target_role ?? "未填写"],
              ]}
            />
          </InfoCard>

          <InfoCard title="搜索与筛选参数">
            <ChipList items={campaign.search_keywords} emptyText="未填写搜索关键词" />
            <div className="divider" />
            <ChipList
              items={campaign.qualification_criteria}
              emptyText="未填写筛选条件"
            />
          </InfoCard>

          <InfoCard title="开发信角度">
            <p>{campaign.outreach_angle ?? "未填写开发信角度。"}</p>
          </InfoCard>
        </div>
      </div>

      <aside className="detail-side">
        <InfoCard title="关联产品">
          <strong className="product-title">
            {snapshot?.name ?? productName(campaign, productCards)}
          </strong>
          <p>
            {snapshot?.description ??
              productCards.find((item) => item.id === campaign.product_card_id)
                ?.description ??
              "该任务关联的产品卡片需要保持已确认状态。"}
          </p>
          <span className="mini-link">产品卡片 ID：{campaign.product_card_id}</span>
        </InfoCard>

        <InfoCard title="任务规则">
          <DefinitionList
            items={[
              ["当前状态", statusLabels[campaign.status]],
              ["线索上限", `${campaign.lead_limit} 条`],
              ["创建时间", formatDate(campaign.created_at)],
              ["更新时间", formatDate(campaign.updated_at)],
            ]}
          />
        </InfoCard>

        <InfoCard title="后续阶段提示">
          {isDraft ? (
            <p>草稿任务可以继续编辑。确认后会锁定当前产品卡片快照。</p>
          ) : null}
          {isConfirmed ? (
            <p>后续线索发现接口完成后，已确认任务才可进入下一阶段流程。</p>
          ) : null}
          {isArchived ? (
            <p>归档任务是只读历史记录，不能恢复、编辑、删除或用于新的后续流程。</p>
          ) : null}
        </InfoCard>
      </aside>
    </section>
  );
}

function CampaignForm({
  campaign,
  company,
  isSubmitting,
  mode,
  onCancel,
  onSubmit,
  productCards,
}: {
  campaign?: Campaign;
  company: Company;
  isSubmitting: boolean;
  mode: "create" | "edit";
  onCancel: () => void;
  onSubmit: (payload: CampaignPayload | CampaignUpdatePayload) => void;
  productCards: ProductCard[];
}) {
  const [form, setForm] = useState<FormState>(() => createFormState(campaign));
  const [formError, setFormError] = useState("");
  const isCreate = mode === "create";
  const selectedProduct = productCards.find(
    (item) => item.id === form.product_card_id,
  );

  function updateField(field: keyof FormState, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFormError("");

    const leadLimit = Number.parseInt(form.lead_limit, 10);
    if (!form.name.trim()) {
      setFormError("请填写任务名称。");
      return;
    }

    if (isCreate && !form.product_card_id) {
      setFormError("请选择一个已确认的产品卡片。");
      return;
    }

    if (!Number.isInteger(leadLimit) || leadLimit < 1 || leadLimit > 1000) {
      setFormError("线索上限必须在 1 到 1000 之间。");
      return;
    }

    const basePayload = {
      name: form.name.trim(),
      target_country: toNullable(form.target_country),
      target_region: toNullable(form.target_region),
      target_industry: toNullable(form.target_industry),
      target_company_type: toNullable(form.target_company_type),
      target_role: toNullable(form.target_role),
      search_keywords: splitList(form.search_keywords),
      qualification_criteria: splitList(form.qualification_criteria),
      outreach_angle: toNullable(form.outreach_angle),
      lead_limit: leadLimit,
    };

    if (isCreate) {
      onSubmit({
        ...basePayload,
        product_card_id: form.product_card_id,
      });
      return;
    }

    onSubmit(basePayload);
  }

  return (
    <form className="campaign-form" onSubmit={handleSubmit}>
      <div className="form-header surface-panel">
        <div>
          <span>{company.name}</span>
          <h2>{isCreate ? "新建获客任务" : "编辑草稿任务"}</h2>
          <p>
            {isCreate
              ? "配置获客任务条件，保存为草稿后可确认使用。"
              : "仅草稿任务可以编辑。保存修改不会改变任务状态。"}
          </p>
        </div>
        <div className="form-actions">
          <button className="secondary-button" onClick={onCancel} type="button">
            取消
          </button>
          <button
            className="primary-button"
            disabled={isSubmitting || (isCreate && productCards.length === 0)}
            type="submit"
          >
            {isSubmitting ? "保存中..." : isCreate ? "保存草稿" : "保存修改"}
          </button>
        </div>
      </div>

      {formError ? <div className="notice notice--error">{formError}</div> : null}

      {isCreate && productCards.length === 0 ? (
        <div className="notice">
          <strong>暂无可用产品卡片</strong>
          <span>获客任务只能选择已确认的产品卡片。请先完成产品卡片确认。</span>
        </div>
      ) : null}

      <div className="form-grid">
        <section className="form-section">
          <h3>基本信息</h3>
          <label>
            <span>任务名称</span>
            <input
              onChange={(event) => updateField("name", event.target.value)}
              placeholder="例如：2026 Q3 北美 SaaS 高管拓展"
              value={form.name}
            />
          </label>

          <label>
            <span>目标推广产品</span>
            <select
              disabled={!isCreate}
              onChange={(event) =>
                updateField("product_card_id", event.target.value)
              }
              value={form.product_card_id}
            >
              <option value="">请选择已确认产品卡片</option>
              {productCards.map((productCard) => (
                <option key={productCard.id} value={productCard.id}>
                  {productCard.name}（已确认）
                </option>
              ))}
            </select>
            <small>
              {isCreate
                ? "只显示当前公司下已确认的产品卡片。"
                : "编辑草稿时不修改已绑定的产品卡片。"}
            </small>
          </label>

          {selectedProduct ? (
            <div className="product-preview">
              <strong>{selectedProduct.name}</strong>
              <p>{selectedProduct.value_proposition}</p>
            </div>
          ) : null}
        </section>

        <section className="form-section">
          <h3>目标客户条件</h3>
          <div className="field-row">
            <label>
              <span>目标国家</span>
              <input
                onChange={(event) =>
                  updateField("target_country", event.target.value)
                }
                placeholder="例如：美国"
                value={form.target_country}
              />
            </label>
            <label>
              <span>目标地区</span>
              <input
                onChange={(event) =>
                  updateField("target_region", event.target.value)
                }
                placeholder="例如：加利福尼亚州、纽约州"
                value={form.target_region}
              />
            </label>
          </div>

          <div className="field-row">
            <label>
              <span>目标行业</span>
              <input
                onChange={(event) =>
                  updateField("target_industry", event.target.value)
                }
                placeholder="例如：金融科技、医疗健康"
                value={form.target_industry}
              />
            </label>
            <label>
              <span>客户类型</span>
              <input
                onChange={(event) =>
                  updateField("target_company_type", event.target.value)
                }
                placeholder="例如：企业客户、渠道商"
                value={form.target_company_type}
              />
            </label>
          </div>

          <label>
            <span>目标角色</span>
            <input
              onChange={(event) => updateField("target_role", event.target.value)}
              placeholder="例如：技术负责人、运营负责人、销售总监"
              value={form.target_role}
            />
          </label>
        </section>

        <section className="form-section form-section--wide">
          <h3>搜索与筛选参数</h3>
          <div className="field-row">
            <label>
              <span>搜索关键词</span>
              <textarea
                onChange={(event) =>
                  updateField("search_keywords", event.target.value)
                }
                placeholder={"每行一个关键词\n例如：云成本优化"}
                rows={5}
                value={form.search_keywords}
              />
            </label>
            <label>
              <span>资格判断条件</span>
              <textarea
                onChange={(event) =>
                  updateField("qualification_criteria", event.target.value)
                }
                placeholder={"每行一个条件\n例如：官网展示企业级软件产品"}
                rows={5}
                value={form.qualification_criteria}
              />
            </label>
          </div>

          <label>
            <span>开发信角度</span>
            <textarea
              onChange={(event) =>
                updateField("outreach_angle", event.target.value)
              }
              placeholder="说明后续开发信应强调的价值主张、证据和语气。"
              rows={4}
              value={form.outreach_angle}
            />
          </label>

          <label className="compact-field">
            <span>线索上限</span>
            <input
              max="1000"
              min="1"
              onChange={(event) => updateField("lead_limit", event.target.value)}
              type="number"
              value={form.lead_limit}
            />
          </label>
        </section>

        <div className="form-rule-note">
          草稿保存后仍可编辑。确认获客任务会重新校验当前产品卡片，并保存产品卡片快照。
          当前阶段仅管理获客任务配置，不展示后续阶段入口。
        </div>
      </div>
    </form>
  );
}

function InfoCard({
  children,
  title,
}: {
  children: React.ReactNode;
  title: string;
}) {
  return (
    <section className="info-card">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

function DefinitionList({ items }: { items: Array<[string, string]> }) {
  return (
    <dl className="definition-list">
      {items.map(([label, value]) => (
        <div key={label}>
          <dt>{label}</dt>
          <dd>{value}</dd>
        </div>
      ))}
    </dl>
  );
}

function ChipList({
  emptyText,
  items,
}: {
  emptyText: string;
  items: string[];
}) {
  if (items.length === 0) {
    return <p className="muted-text">{emptyText}</p>;
  }

  return (
    <div className="chip-list">
      {items.map((item) => (
        <span key={item}>{item}</span>
      ))}
    </div>
  );
}

function StatePanel({ text, title }: { text: string; title: string }) {
  return (
    <div className="state-panel">
      <div className="state-icon" />
      <h3>{title}</h3>
      <p>{text}</p>
    </div>
  );
}

function ActionModal({
  isSubmitting,
  modal,
  onCancel,
  onConfirm,
}: {
  isSubmitting: boolean;
  modal: { type: ModalAction; campaign: Campaign };
  onCancel: () => void;
  onConfirm: () => void;
}) {
  const copy = {
    confirm: {
      title: "确认获客任务",
      text: "确认后，系统会锁定当前产品卡片快照。后续不能编辑任务核心参数，如需复用请复制为草稿。",
      action: "确认",
      tone: "primary-button",
    },
    delete: {
      title: "删除草稿任务",
      text: "删除后不可恢复。只有草稿任务允许删除。",
      action: "删除",
      tone: "danger-button",
    },
    archive: {
      title: "归档获客任务",
      text: "归档后该任务会成为只读历史记录，不能恢复、编辑、删除或用于新的后续流程。",
      action: "归档",
      tone: "primary-button",
    },
  }[modal.type];

  return (
    <div className="modal-backdrop" role="presentation">
      <div
        aria-labelledby="campaign-modal-title"
        aria-modal="true"
        className="modal-card"
        role="dialog"
      >
        <h2 id="campaign-modal-title">{copy.title}</h2>
        <p>{copy.text}</p>
        <div className="modal-actions">
          <button
            className="secondary-button"
            disabled={isSubmitting}
            onClick={onCancel}
            type="button"
          >
            取消
          </button>
          <button
            className={copy.tone}
            disabled={isSubmitting}
            onClick={onConfirm}
            type="button"
          >
            {isSubmitting ? "处理中..." : copy.action}
          </button>
        </div>
      </div>
    </div>
  );
}
