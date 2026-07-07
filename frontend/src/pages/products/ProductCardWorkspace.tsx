import { FormEvent, useEffect, useMemo, useState } from "react";

import {
  ApiError,
  Company,
  ProductCard,
  ProductCardPayload,
  ProductCardStatus,
  ProductCardUpdatePayload,
  confirmProductCard,
  createManualProductCard,
  deleteProductCard,
  generateProductCard,
  listCompanies,
  listProductCards,
  updateProductCard,
} from "../../api/productCards";

type StatusFilter = "all" | ProductCardStatus;
type DialogState =
  | { mode: "create" }
  | { mode: "detail"; productCard: ProductCard };
type ModalAction = "confirm" | "delete";

interface FormState {
  name: string;
  description: string;
  target_customer: string;
  pain_points: string;
  value_proposition: string;
  use_cases: string;
  differentiators: string;
}

const emptyFormState: FormState = {
  name: "",
  description: "",
  target_customer: "",
  pain_points: "",
  value_proposition: "",
  use_cases: "",
  differentiators: "",
};

const statusLabels: Record<ProductCardStatus, string> = {
  draft: "待确认",
  confirmed: "已确认",
};

const statusTone: Record<ProductCardStatus, string> = {
  draft: "status-badge status-badge--draft",
  confirmed: "status-badge status-badge--confirmed",
};

const sourceLabels = {
  ai_generated: "AI 生成",
  manual: "手动创建",
};

const statusFilters: Array<{ value: StatusFilter; label: string }> = [
  { value: "all", label: "全部" },
  { value: "draft", label: "待确认" },
  { value: "confirmed", label: "已确认" },
];

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
    if (error.status === 409) {
      return "已被获客任务使用，无法删除。";
    }
    return error.code ? `${error.message}（${error.code}）` : error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "操作失败，请稍后重试。";
}

function toFormState(productCard?: ProductCard): FormState {
  if (!productCard) {
    return emptyFormState;
  }

  return {
    name: productCard.name,
    description: productCard.description,
    target_customer: productCard.target_customer,
    pain_points: joinList(productCard.pain_points),
    value_proposition: productCard.value_proposition,
    use_cases: joinList(productCard.use_cases),
    differentiators: joinList(productCard.differentiators),
  };
}

function toPayload(form: FormState) {
  return {
    name: form.name.trim(),
    description: form.description.trim(),
    target_customer: form.target_customer.trim(),
    pain_points: splitList(form.pain_points),
    value_proposition: form.value_proposition.trim(),
    use_cases: splitList(form.use_cases),
    differentiators: splitList(form.differentiators),
  };
}

function ProductCardStatusBadge({ status }: { status: ProductCardStatus }) {
  return <span className={statusTone[status]}>{statusLabels[status]}</span>;
}

function AppIcon({
  name,
}: {
  name: "plus" | "tasks" | "box" | "gear" | "home" | "card";
}) {
  const icons = {
    plus: <path d="M12 5v14M5 12h14" />,
    tasks: <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" />,
    box: <path d="m21 8-9-5-9 5 9 5 9-5ZM3 8v8l9 5 9-5V8M12 13v8" />,
    gear: (
      <path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM4 12h2M18 12h2M12 4v2M12 18v2M6.4 6.4l1.4 1.4M16.2 16.2l1.4 1.4M17.6 6.4l-1.4 1.4M7.8 16.2l-1.4 1.4" />
    ),
    home: <path d="m4 10 8-6 8 6v9a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1v-9Z" />,
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

export default function ProductCardWorkspace() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState("");
  const [productCards, setProductCards] = useState<ProductCard[]>([]);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [dialog, setDialog] = useState<DialogState | null>(null);
  const [modal, setModal] = useState<{
    type: ModalAction;
    productCard: ProductCard;
  } | null>(null);
  const [isBootLoading, setIsBootLoading] = useState(true);
  const [isDataLoading, setIsDataLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");

  const selectedCompany = companies.find((item) => item.id === selectedCompanyId);

  const visibleProductCards = useMemo(() => {
    if (statusFilter === "all") {
      return productCards;
    }
    return productCards.filter((item) => item.status === statusFilter);
  }, [productCards, statusFilter]);

  const counts = useMemo(
    () => ({
      all: productCards.length,
      draft: productCards.filter((item) => item.status === "draft").length,
      confirmed: productCards.filter((item) => item.status === "confirmed").length,
    }),
    [productCards],
  );

  async function refreshCompanyData(companyId = selectedCompanyId) {
    if (!companyId) {
      return;
    }

    setIsDataLoading(true);
    setError("");
    try {
      const result = await listProductCards(companyId);
      setProductCards(result.items);
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
        setSelectedCompanyId(companyResult.items[0]?.id ?? "");
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
    setDialog(null);
    setModal(null);
    if (selectedCompanyId) {
      void refreshCompanyData(selectedCompanyId);
    } else {
      setProductCards([]);
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

  async function handleCreate(payload: Omit<ProductCardPayload, "company_id">) {
    if (!selectedCompanyId) {
      setError("请先选择公司资料。");
      return;
    }

    await runAction(async () => {
      const created = await createManualProductCard({
        company_id: selectedCompanyId,
        ...payload,
      });
      await refreshCompanyData(selectedCompanyId);
      setDialog({ mode: "detail", productCard: created });
      showToast("产品卡片已保存为待确认。");
    });
  }

  async function handleGenerateFromKnowledge() {
    if (!selectedCompanyId) {
      setError("请先选择公司资料。");
      return;
    }

    await runAction(async () => {
      const created = await generateProductCard(selectedCompanyId);
      await refreshCompanyData(selectedCompanyId);
      setDialog({ mode: "detail", productCard: created });
      showToast("已根据已确认知识生成待确认产品卡片。");
    });
  }

  async function handleUpdate(
    productCard: ProductCard,
    payload: ProductCardUpdatePayload,
  ) {
    await runAction(async () => {
      const updated = await updateProductCard(productCard.id, payload);
      await refreshCompanyData(productCard.company_id);
      setDialog({ mode: "detail", productCard: updated });
      showToast("产品卡片信息已保存。");
    });
  }

  async function handleModalConfirm() {
    if (!modal) {
      return;
    }

    const { productCard, type } = modal;
    await runAction(async () => {
      if (type === "confirm") {
        const confirmed = await confirmProductCard(productCard.id);
        await refreshCompanyData(productCard.company_id);
        setDialog({ mode: "detail", productCard: confirmed });
        showToast("产品卡片已确认。");
      }

      if (type === "delete") {
        await deleteProductCard(productCard.id);
        await refreshCompanyData(productCard.company_id);
        setDialog(null);
        showToast("产品卡片已删除。");
      }

      setModal(null);
    });
  }

  return (
    <div className="campaign-app product-card-app">
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
          <a href="#products" className="active">
            <AppIcon name="card" />
            产品卡片
          </a>
          <a href="#campaigns">
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
          onClick={() => setDialog({ mode: "create" })}
          type="button"
        >
          <AppIcon name="plus" />
          手动添加产品
        </button>
      </aside>

      <main className="workspace">
        <header className="workspace-header">
          <div>
            <p className="workspace-kicker">前端阶段二</p>
            <h1>产品卡片管理</h1>
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
              disabled={!selectedCompanyId || isSubmitting}
              onClick={() => void handleGenerateFromKnowledge()}
              type="button"
            >
              从已确认知识生成
            </button>
            <button
              className="primary-button"
              disabled={!selectedCompanyId}
              onClick={() => setDialog({ mode: "create" })}
              type="button"
            >
              <AppIcon name="plus" />
              手动添加产品
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
          <StatePanel title="正在加载产品卡片" text="正在读取公司资料和产品卡片。" />
        ) : null}

        {!isBootLoading && companies.length === 0 ? (
          <StatePanel
            title="暂无公司资料"
            text="请先在公司资料阶段创建公司，再进入产品卡片管理。"
          />
        ) : null}

        {!isBootLoading && selectedCompany ? (
          <>
            <ProductCardSummary
              company={selectedCompany}
              counts={counts}
              isLoading={isDataLoading}
            />

            <section className="surface-panel">
              <div className="panel-toolbar">
                <div className="segmented-control" aria-label="产品卡片状态筛选">
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

              <ProductCardTable
                isLoading={isDataLoading}
                onConfirm={(productCard) =>
                  setModal({ type: "confirm", productCard })
                }
                onDelete={(productCard) =>
                  setModal({ type: "delete", productCard })
                }
                onView={(productCard) =>
                  setDialog({ mode: "detail", productCard })
                }
                productCards={visibleProductCards}
              />
            </section>
          </>
        ) : null}
      </main>

      {dialog ? (
        <ProductCardDialog
          dialog={dialog}
          isSubmitting={isSubmitting}
          onCancel={() => setDialog(null)}
          onConfirm={(productCard) => setModal({ type: "confirm", productCard })}
          onDelete={(productCard) => setModal({ type: "delete", productCard })}
          onCreate={(payload) => void handleCreate(payload)}
          onUpdate={(productCard, payload) =>
            void handleUpdate(productCard, payload)
          }
        />
      ) : null}

      {modal ? (
        <ProductCardActionModal
          isSubmitting={isSubmitting}
          modal={modal}
          onCancel={() => setModal(null)}
          onConfirm={() => void handleModalConfirm()}
        />
      ) : null}
    </div>
  );
}

function ProductCardSummary({
  company,
  counts,
  isLoading,
}: {
  company: Company;
  counts: Record<StatusFilter, number>;
  isLoading: boolean;
}) {
  return (
    <section className="summary-grid product-summary-grid">
      <article className="summary-card summary-card--wide">
        <span>当前公司</span>
        <strong>{company.name}</strong>
        <p>{company.target_market ?? "尚未填写目标市场"}</p>
      </article>
      <article className="summary-card">
        <span>全部产品卡片</span>
        <strong>{isLoading ? "..." : counts.all}</strong>
        <p>包含待确认和已确认</p>
      </article>
      <article className="summary-card">
        <span>待确认</span>
        <strong>{isLoading ? "..." : counts.draft}</strong>
        <p>可编辑、确认或删除</p>
      </article>
      <article className="summary-card">
        <span>已确认</span>
        <strong>{isLoading ? "..." : counts.confirmed}</strong>
        <p>可用于后续获客任务</p>
      </article>
    </section>
  );
}

function ProductCardTable({
  isLoading,
  onConfirm,
  onDelete,
  onView,
  productCards,
}: {
  isLoading: boolean;
  onConfirm: (productCard: ProductCard) => void;
  onDelete: (productCard: ProductCard) => void;
  onView: (productCard: ProductCard) => void;
  productCards: ProductCard[];
}) {
  if (isLoading) {
    return <StatePanel title="正在读取产品卡片" text="正在同步当前公司的产品卡片。" />;
  }

  if (productCards.length === 0) {
    return (
      <StatePanel
        title="暂无产品卡片"
        text="可以手动添加产品，或从已确认知识生成待确认产品卡片。"
      />
    );
  }

  return (
    <div className="table-wrap">
      <table className="campaign-table product-card-table">
        <thead>
          <tr>
            <th>产品卡片 / 来源</th>
            <th>目标客户</th>
            <th>核心价值</th>
            <th>痛点数量</th>
            <th>状态</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {productCards.map((productCard) => (
            <tr key={productCard.id}>
              <td>
                <button
                  className="link-button table-title"
                  onClick={() => onView(productCard)}
                  type="button"
                >
                  {productCard.name}
                </button>
                <span>{sourceLabels[productCard.source_type]}</span>
              </td>
              <td>{productCard.target_customer}</td>
              <td>{productCard.value_proposition}</td>
              <td className="numeric-cell">{productCard.pain_points.length}</td>
              <td>
                <ProductCardStatusBadge status={productCard.status} />
              </td>
              <td>{formatDate(productCard.updated_at)}</td>
              <td>
                <ProductCardActions
                  onConfirm={onConfirm}
                  onDelete={onDelete}
                  onView={onView}
                  productCard={productCard}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ProductCardActions({
  onConfirm,
  onDelete,
  onView,
  productCard,
}: {
  onConfirm: (productCard: ProductCard) => void;
  onDelete: (productCard: ProductCard) => void;
  onView: (productCard: ProductCard) => void;
  productCard: ProductCard;
}) {
  return (
    <div className="row-actions">
      <button onClick={() => onView(productCard)} type="button">
        查看详情
      </button>
      <button onClick={() => onView(productCard)} type="button">
        编辑
      </button>
      {productCard.status === "draft" ? (
        <button onClick={() => onConfirm(productCard)} type="button">
          确认产品卡片
        </button>
      ) : null}
      <button
        className="danger-action"
        onClick={() => onDelete(productCard)}
        type="button"
      >
        删除
      </button>
    </div>
  );
}

function ProductCardDialog({
  dialog,
  isSubmitting,
  onCancel,
  onConfirm,
  onCreate,
  onDelete,
  onUpdate,
}: {
  dialog: DialogState;
  isSubmitting: boolean;
  onCancel: () => void;
  onConfirm: (productCard: ProductCard) => void;
  onCreate: (payload: Omit<ProductCardPayload, "company_id">) => void;
  onDelete: (productCard: ProductCard) => void;
  onUpdate: (productCard: ProductCard, payload: ProductCardUpdatePayload) => void;
}) {
  const productCard = dialog.mode === "detail" ? dialog.productCard : undefined;
  const [form, setForm] = useState<FormState>(() => toFormState(productCard));
  const [formError, setFormError] = useState("");

  const savedForm = useMemo(() => toFormState(productCard), [productCard]);
  const isCreate = dialog.mode === "create";
  const isDirty =
    isCreate || JSON.stringify(form) !== JSON.stringify(savedForm);

  function updateField(field: keyof FormState, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function validateForm() {
    const payload = toPayload(form);
    if (!payload.name) {
      return "请填写产品名称。";
    }
    if (!payload.description) {
      return "请填写产品描述。";
    }
    if (!payload.target_customer) {
      return "请填写目标客户。";
    }
    if (!payload.value_proposition) {
      return "请填写核心价值主张。";
    }
    return "";
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const validationError = validateForm();
    if (validationError) {
      setFormError(validationError);
      return;
    }

    setFormError("");
    const payload = toPayload(form);
    if (isCreate) {
      onCreate(payload);
      return;
    }

    if (productCard && isDirty) {
      onUpdate(productCard, payload);
    }
  }

  function handleDiscardChanges() {
    setForm(savedForm);
    setFormError("");
  }

  return (
    <div className="modal-backdrop product-dialog-backdrop" role="presentation">
      <form
        aria-labelledby="product-card-dialog-title"
        aria-modal="true"
        className="modal-card product-dialog"
        onSubmit={handleSubmit}
        role="dialog"
      >
        <div className="product-dialog-header">
          <div>
            <span>{isCreate ? "手动添加产品" : "产品卡片详情"}</span>
            <h2 id="product-card-dialog-title">
              {isCreate ? "手动添加产品" : productCard?.name}
            </h2>
          </div>
          <div className="detail-actions">
            {productCard ? (
              <ProductCardStatusBadge status={productCard.status} />
            ) : null}
            {productCard?.status === "draft" ? (
              <button
                className="primary-button"
                disabled={isSubmitting}
                onClick={() => onConfirm(productCard)}
                type="button"
              >
                确认产品卡片
              </button>
            ) : null}
            {productCard ? (
              <button
                className="danger-button"
                disabled={isSubmitting}
                onClick={() => onDelete(productCard)}
                type="button"
              >
                删除
              </button>
            ) : null}
            <button
              className="ghost-button"
              disabled={isSubmitting}
              onClick={onCancel}
              type="button"
            >
              关闭
            </button>
          </div>
        </div>

        {formError ? <div className="notice notice--error">{formError}</div> : null}

        <div className="product-dialog-grid">
          <section className="form-section">
            <h3>基本信息</h3>
            <label>
              <span>产品名称</span>
              <input
                onChange={(event) => updateField("name", event.target.value)}
                placeholder="输入完整的产品名称"
                value={form.name}
              />
            </label>
            <label>
              <span>产品描述</span>
              <textarea
                onChange={(event) =>
                  updateField("description", event.target.value)
                }
                placeholder="简要描述产品的主要功能和定位"
                rows={4}
                value={form.description}
              />
            </label>
          </section>

          <section className="form-section">
            <h3>市场定位</h3>
            <label>
              <span>目标客户</span>
              <textarea
                onChange={(event) =>
                  updateField("target_customer", event.target.value)
                }
                placeholder="说明最适合的客户类型、行业和角色"
                rows={4}
                value={form.target_customer}
              />
            </label>
            <label>
              <span>核心价值主张</span>
              <textarea
                onChange={(event) =>
                  updateField("value_proposition", event.target.value)
                }
                placeholder="产品能为客户带来的最核心价值是什么？"
                rows={4}
                value={form.value_proposition}
              />
            </label>
          </section>

          <section className="form-section form-section--wide">
            <h3>详细特征</h3>
            <div className="field-row">
              <label>
                <span>客户痛点</span>
                <textarea
                  onChange={(event) =>
                    updateField("pain_points", event.target.value)
                  }
                  placeholder={"每行一个痛点\n例如：数据孤岛严重"}
                  rows={5}
                  value={form.pain_points}
                />
              </label>
              <label>
                <span>典型使用场景</span>
                <textarea
                  onChange={(event) =>
                    updateField("use_cases", event.target.value)
                  }
                  placeholder={"每行一个使用场景\n例如：销售线索筛选"}
                  rows={5}
                  value={form.use_cases}
                />
              </label>
            </div>
            <label>
              <span>差异化优势</span>
              <textarea
                onChange={(event) =>
                  updateField("differentiators", event.target.value)
                }
                placeholder={"每行一个差异化优势\n例如：无需部署复杂系统"}
                rows={4}
                value={form.differentiators}
              />
            </label>
          </section>

          {productCard ? (
            <aside className="info-card product-side-card">
              <h3>基本信息</h3>
              <DefinitionList
                items={[
                  ["来源类型", sourceLabels[productCard.source_type]],
                  ["当前状态", statusLabels[productCard.status]],
                  ["创建时间", formatDate(productCard.created_at)],
                  ["最后更新", formatDate(productCard.updated_at)],
                ]}
              />
              <div className="divider" />
              <p>
                保存修改只更新产品卡片字段，不会改变状态。确认产品卡片是独立动作。
              </p>
              {productCard.status === "confirmed" ? (
                <p>已确认产品卡片如果已被获客任务使用，无法删除。</p>
              ) : null}
            </aside>
          ) : null}
        </div>

        <div className="modal-actions product-dialog-actions">
          {isCreate ? (
            <>
              <button
                className="secondary-button"
                disabled={isSubmitting}
                onClick={onCancel}
                type="button"
              >
                取消
              </button>
              <button
                className="primary-button"
                disabled={isSubmitting}
                type="submit"
              >
                {isSubmitting ? "保存中..." : "手动添加产品"}
              </button>
            </>
          ) : (
            <>
              {isDirty ? (
                <>
                  <button
                    className="secondary-button"
                    disabled={isSubmitting}
                    onClick={handleDiscardChanges}
                    type="button"
                  >
                    取消
                  </button>
                  <button
                    className="primary-button"
                    disabled={isSubmitting}
                    type="submit"
                  >
                    {isSubmitting ? "保存中..." : "保存修改"}
                  </button>
                </>
              ) : (
                <span className="readonly-note">没有未保存修改</span>
              )}
            </>
          )}
        </div>
      </form>
    </div>
  );
}

function ProductCardActionModal({
  isSubmitting,
  modal,
  onCancel,
  onConfirm,
}: {
  isSubmitting: boolean;
  modal: { type: ModalAction; productCard: ProductCard };
  onCancel: () => void;
  onConfirm: () => void;
}) {
  const copy = {
    confirm: {
      title: "确认产品卡片",
      text: "确认后，该产品卡片可用于后续获客任务。保存修改和确认产品卡片是两个独立动作。",
      action: "确认产品卡片",
      tone: "primary-button",
    },
    delete: {
      title: "删除产品卡片",
      text:
        modal.productCard.status === "confirmed"
          ? "删除后不可恢复。已确认产品卡片如果已被获客任务使用，无法删除。"
          : "删除后不可恢复。待确认产品卡片会被直接删除。",
      action: "删除",
      tone: "danger-button",
    },
  }[modal.type];

  return (
    <div className="modal-backdrop" role="presentation">
      <div
        aria-labelledby="product-card-action-modal-title"
        aria-modal="true"
        className="modal-card"
        role="dialog"
      >
        <h2 id="product-card-action-modal-title">{copy.title}</h2>
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

function StatePanel({ text, title }: { text: string; title: string }) {
  return (
    <div className="state-panel">
      <div className="state-icon" />
      <h3>{title}</h3>
      <p>{text}</p>
    </div>
  );
}
