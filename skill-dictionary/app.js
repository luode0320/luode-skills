(function () {
  const data = window.SKILL_DICTIONARY;
  const state = {
    query: "",
    status: "all",
    activeDomain: "all",
    selectedId: null,
  };

  const searchInput = document.getElementById("search-input");
  const statusFilters = document.getElementById("status-filters");
  const summaryCards = document.getElementById("summary-cards");
  const domainNav = document.getElementById("domain-nav");
  const skillList = document.getElementById("skill-list");
  const docList = document.getElementById("doc-list");
  const detailView = document.getElementById("detail-view");
  const resultHint = document.getElementById("result-hint");

  const statusOptions = [
    { id: "all", label: "全部状态" },
    { id: "implemented", label: "已实现" },
    { id: "planned", label: "规划中" },
    { id: "seed", label: "扩展种子" },
  ];

  const detailIndex = new Map();
  data.items.forEach((item) => detailIndex.set(item.id, { ...item, entityType: "skill" }));
  data.docs.forEach((doc) => detailIndex.set(doc.id, { ...doc, entityType: "doc" }));

  function summaryCard(label, value, copy) {
    return `
      <article class="summary-card">
        <span>${label}</span>
        <strong>${value}</strong>
        <p class="muted">${copy}</p>
      </article>
    `;
  }

  function renderSummary() {
    const summary = data.summary;
    const downloadedState = data.downloaded_seeds.entry_count
      ? `downloaded-seeds 当前有 ${data.downloaded_seeds.entry_count} 个条目`
      : "downloaded-seeds 当前为空";

    summaryCards.innerHTML = [
      summaryCard("已落地规划", `${summary.implemented_total}/${summary.planned_total}`, "按主规划落地的 skill 数量"),
      summaryCard("规划缺口", summary.planned_missing, "仍未正式建目录的规划 skill"),
      summaryCard("扩展种子", summary.seed_total, "仓库内已存在但未并入主规划"),
      summaryCard("文档 / 状态", `${summary.doc_total} / ${downloadedState}`, "根目录分析文档和种子目录状态"),
    ].join("");
  }

  function renderDomainNav() {
    domainNav.innerHTML = "";
    const allButton = document.createElement("button");
    allButton.type = "button";
    allButton.className = `domain-link ${state.activeDomain === "all" ? "is-active" : ""}`;
    allButton.innerHTML = `
      <span>
        <strong>全部域</strong>
        <small>浏览全部 skill 与文档</small>
      </span>
      <span class="chip neutral">${data.items.length}</span>
    `;
    allButton.addEventListener("click", () => {
      state.activeDomain = "all";
      render();
    });
    domainNav.appendChild(allButton);

    data.domains.forEach((domain) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `domain-link ${state.activeDomain === domain.label ? "is-active" : ""}`;
      button.innerHTML = `
        <span>
          <strong>${domain.order.toString().padStart(2, "0")} ${domain.label}</strong>
          <small>${domain.description}</small>
        </span>
        <span class="chip neutral">${domain.total_count}</span>
      `;
      button.addEventListener("click", () => {
        state.activeDomain = domain.label;
        render();
      });
      domainNav.appendChild(button);
    });
  }

  function renderStatusFilters() {
    statusFilters.innerHTML = "";
    statusOptions.forEach((option) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `status-filter ${state.status === option.id ? "is-active" : ""}`;
      button.textContent = option.label;
      button.addEventListener("click", () => {
        state.status = option.id;
        render();
      });
      statusFilters.appendChild(button);
    });
  }

  function matchesQuery(item) {
    if (!state.query) {
      return true;
    }
    const corpus = [
      item.name,
      item.title,
      item.domain_label,
      item.auto_trigger,
      item.core_responsibility,
      ...(item.sections || []),
      ...(item.references || []),
    ]
      .join(" ")
      .toLowerCase();

    return corpus.includes(state.query);
  }

  function matchesFilters(item) {
    const statusMatched = state.status === "all" || item.status === state.status;
    const domainMatched = state.activeDomain === "all" || item.domain_label === state.activeDomain;
    return statusMatched && domainMatched && matchesQuery(item);
  }

  function filterSkills() {
    return data.items.filter(matchesFilters);
  }

  function filterDocs() {
    if (state.activeDomain !== "all") {
      return [];
    }
    return data.docs.filter((doc) => {
      if (!state.query) {
        return true;
      }
      const corpus = `${doc.title} ${doc.kind} ${doc.path}`.toLowerCase();
      return corpus.includes(state.query);
    });
  }

  function renderSkillList(items) {
    const grouped = new Map();
    items.forEach((item) => {
      const key = item.domain_label;
      if (!grouped.has(key)) {
        grouped.set(key, []);
      }
      grouped.get(key).push(item);
    });

    skillList.innerHTML = "";

    if (!items.length) {
      skillList.innerHTML = `<div class="empty-state">当前筛选条件下没有匹配的 skill。</div>`;
      return;
    }

    data.domains.forEach((domain) => {
      const domainItems = grouped.get(domain.label);
      if (!domainItems || !domainItems.length) {
        return;
      }

      const block = document.createElement("section");
      block.className = "domain-block";
      block.innerHTML = `
        <div class="domain-block-head">
          <div>
            <h4>${domain.order.toString().padStart(2, "0")} ${domain.label}</h4>
            <p class="muted">${domain.description}</p>
          </div>
          <div class="domain-progress">${domainItems.length} 条命中</div>
        </div>
        <div class="item-list"></div>
      `;

      const list = block.querySelector(".item-list");
      domainItems.forEach((item) => {
        const article = document.createElement("article");
        article.className = `item-row ${state.selectedId === item.id ? "is-active" : ""}`;
        article.tabIndex = 0;
        article.innerHTML = `
          <div class="item-row-top">
            <span class="item-order">${String(item.item_order).padStart(2, "0")}</span>
            <h5>${item.name}</h5>
            <span class="chip status-${item.status}">${item.status_label}</span>
            ${item.references.length ? `<span class="chip neutral">refs ${item.references.length}</span>` : ""}
            ${item.agents.length ? `<span class="chip neutral">agents ${item.agents.length}</span>` : ""}
          </div>
          <p>${item.core_responsibility}</p>
          <div class="item-meta">
            <span class="chip neutral">${item.title}</span>
            ${item.skill_path ? `<span class="chip neutral mono">${item.skill_path}</span>` : `<span class="chip neutral">待建目录</span>`}
          </div>
        `;

        const activate = () => {
          state.selectedId = item.id;
          render();
        };
        article.addEventListener("click", activate);
        article.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            activate();
          }
        });
        list.appendChild(article);
      });

      skillList.appendChild(block);
    });
  }

  function renderDocList(docs) {
    docList.innerHTML = "";
    if (!docs.length) {
      docList.innerHTML = `<div class="empty-state">当前筛选条件下没有命中文档。</div>`;
      return;
    }

    docs.forEach((doc) => {
      const article = document.createElement("article");
      article.className = `doc-row ${state.selectedId === doc.id ? "is-active" : ""}`;
      article.tabIndex = 0;
      article.innerHTML = `
        <div class="doc-row-top">
          <h5>${doc.title}</h5>
          <span class="chip neutral">${doc.kind}</span>
          ${doc.is_plan_doc ? `<span class="chip status-implemented">主规划</span>` : ""}
        </div>
        <p>${doc.path}</p>
      `;
      const activate = () => {
        state.selectedId = doc.id;
        render();
      };
      article.addEventListener("click", activate);
      article.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activate();
        }
      });
      docList.appendChild(article);
    });
  }

  function createLinkList(items) {
    if (!items.length) {
      return `<div class="empty-state">暂无可直接打开的文件。</div>`;
    }
    return `
      <ul class="link-list">
        ${items
          .map(
            (item) =>
              `<li><a href="../${item.path}"><span>${item.label}</span><span class="mono">${item.path}</span></a></li>`,
          )
          .join("")}
      </ul>
    `;
  }

  function createBulletList(items) {
    if (!items.length) {
      return `<div class="empty-state">暂无信息。</div>`;
    }
    return `<ul class="bullet-list">${items.map((item) => `<li>${item}</li>`).join("")}</ul>`;
  }

  function renderSkillDetail(item) {
    const links = [];
    if (item.skill_path) {
      links.push({ label: "打开 SKILL.md", path: item.skill_path });
    }
    if (item.directory_path) {
      links.push({ label: "打开目录", path: item.directory_path });
    }
    item.references.forEach((path) => links.push({ label: "打开参考文件", path }));
    item.agents.forEach((path) => links.push({ label: "打开 agent 文件", path }));

    detailView.innerHTML = `
      <section class="detail-head">
        <div class="item-row-top">
          <span class="chip neutral">${item.domain_label}</span>
          <span class="chip status-${item.status}">${item.status_label}</span>
          ${item.has_license ? `<span class="chip neutral">LICENSE</span>` : ""}
        </div>
        <h3>${item.title}</h3>
        <p class="detail-copy">${item.name}</p>
      </section>
      <section class="detail-grid">
        <div class="detail-section">
          <h4>核心职责</h4>
          <p class="detail-copy">${item.core_responsibility}</p>
        </div>
        <div class="detail-section">
          <h4>自动触发 / 使用说明</h4>
          <p class="detail-copy">${item.auto_trigger}</p>
        </div>
        <div class="detail-section">
          <h4>当前建议切入点</h4>
          ${createBulletList(item.focus_points)}
        </div>
        <div class="detail-section">
          <h4>结构章节</h4>
          ${createBulletList(item.sections)}
        </div>
        <div class="detail-section">
          <h4>相关文件</h4>
          ${createLinkList(links)}
        </div>
      </section>
    `;
  }

  function renderDocDetail(doc) {
    detailView.innerHTML = `
      <section class="detail-head">
        <div class="item-row-top">
          <span class="chip neutral">项目文档</span>
          <span class="chip neutral">${doc.kind}</span>
          ${doc.is_plan_doc ? `<span class="chip status-implemented">主规划</span>` : ""}
        </div>
        <h3>${doc.title}</h3>
        <p class="detail-copy">${doc.file_name}</p>
      </section>
      <section class="detail-grid">
        <div class="detail-section">
          <h4>作用</h4>
          <p class="detail-copy">${
            doc.is_plan_doc
              ? "这是当前仓库的主规划文档，所有域顺序、缺失 skill 和后续字典分类均以它为主。"
              : "这是根目录的过程性文档，适合结合 skill 条目一起看演进背景、波次验证和遗留问题。"
          }</p>
        </div>
        <div class="detail-section">
          <h4>打开文档</h4>
          ${createLinkList([{ label: "打开 Markdown", path: doc.path }])}
        </div>
        <div class="detail-section">
          <h4>查看建议</h4>
          ${createBulletList([
            "先对照相邻 skill 的当前状态，再回看文档里对应波次或规划段落。",
            "如果准备优化某个 skill，优先记录触发信号、边界冲突和 references 是否足够。",
            "如果文档中的规划已和仓库结构不一致，先在字典中确认差异再决定更新方向。",
          ])}
        </div>
      </section>
    `;
  }

  function renderDetail(filteredSkills, filteredDocs) {
    const candidateIds = new Set([
      ...filteredSkills.map((item) => item.id),
      ...filteredDocs.map((item) => item.id),
      data.items[0]?.id,
      data.docs[0]?.id,
    ]);

    if (!state.selectedId || !candidateIds.has(state.selectedId)) {
      state.selectedId = filteredSkills[0]?.id || filteredDocs[0]?.id || data.items[0]?.id || data.docs[0]?.id || null;
    }

    if (!state.selectedId) {
      detailView.innerHTML = `<div class="empty-state">没有可展示的详情。</div>`;
      return;
    }

    const entity = detailIndex.get(state.selectedId);
    if (!entity) {
      detailView.innerHTML = `<div class="empty-state">当前选择的条目不存在。</div>`;
      return;
    }

    if (entity.entityType === "doc") {
      renderDocDetail(entity);
      return;
    }

    renderSkillDetail(entity);
  }

  function renderResultHint(skills, docs) {
    const docCopy = state.activeDomain === "all" ? `，文档 ${docs.length} 条` : "";
    resultHint.textContent = `命中 skill ${skills.length} 条${docCopy}`;
  }

  function render() {
    const filteredSkills = filterSkills();
    const filteredDocs = filterDocs();

    renderSummary();
    renderDomainNav();
    renderStatusFilters();
    renderSkillList(filteredSkills);
    renderDocList(filteredDocs);
    renderResultHint(filteredSkills, filteredDocs);
    renderDetail(filteredSkills, filteredDocs);
  }

  searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    render();
  });

  render();
})();
