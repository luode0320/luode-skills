(function () {
  const data = window.SKILL_DICTIONARY;
  const nf = new Intl.NumberFormat("zh-CN");
  const domains = [...data.domains].sort((a, b) => a.order - b.order);
  const skills = data.items;
  const skillMap = new Map(skills.map((item) => [item.id, item]));
  const defaultDomain = domains.find((item) => item.label === "总控层")?.label || domains[0]?.label || "";
  const state = {
    query: "",
    domain: defaultDomain,
    skillId: skills[0]?.id || null,
  };

  const els = {
    searchInput: document.getElementById("search-input"),
    resultHint: document.getElementById("result-hint"),
    domainTabs: document.getElementById("domain-tabs"),
    skillHint: document.getElementById("skill-hint"),
    skillStrip: document.getElementById("skill-strip"),
    detailPanel: document.getElementById("detail-panel"),
  };

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function hrefOf(path) {
    return `./${String(path).split("/").map(encodeURIComponent).join("/")}`;
  }

  function empty(message) {
    return `<div class="empty-state">${escapeHtml(message)}</div>`;
  }

  function matchSkill(item) {
    if (item.domain_label !== state.domain) {
      return false;
    }

    if (!state.query) {
      return true;
    }

    const corpus = [
      item.name,
      item.title,
      item.domain_label,
      item.auto_trigger,
      item.core_responsibility,
      item.skill_path,
      ...(item.sections || []),
      ...(item.references || []),
      ...(item.agents || []),
    ]
      .join(" ")
      .toLowerCase();

    return corpus.includes(state.query);
  }

  function filteredSkills() {
    return skills.filter(matchSkill);
  }

  function ensureSelection(items) {
    if (!items.some((item) => item.id === state.skillId)) {
      state.skillId = items[0]?.id || skills[0]?.id || null;
    }
  }

  function renderDomainTabs(items) {
    const countInDomain = (domainLabel) =>
      items.filter((item) => item.domain_label === domainLabel).length;

    els.domainTabs.innerHTML = domains
      .map(
        (domain) => `
          <button
            type="button"
            class="domain-tab ${state.domain === domain.label ? "is-active" : ""}"
            data-action="set-domain"
            data-domain="${escapeHtml(domain.label)}"
          >
            <span>${String(domain.order).padStart(2, "0")} ${escapeHtml(domain.label)}</span>
            <strong>${nf.format(countInDomain(domain.label))}</strong>
          </button>
        `,
      )
      .join("");
  }

  function renderSkillStrip(items) {
    els.skillHint.textContent = `${state.domain}，命中 ${nf.format(items.length)} 条`;

    if (!items.length) {
      els.skillStrip.innerHTML = empty("当前条件下没有匹配的 skill。");
      return;
    }

    els.skillStrip.innerHTML = items
      .map(
        (item) => `
          <button
            type="button"
            class="skill-chip ${state.skillId === item.id ? "is-active" : ""}"
            data-action="select-skill"
            data-skill-id="${escapeHtml(item.id)}"
          >
            <span>${escapeHtml(item.name)}</span>
            <small>${String(item.domain_order).padStart(2, "0")}-${String(item.item_order).padStart(2, "0")}</small>
          </button>
        `,
      )
      .join("");
  }

  function renderDetail() {
    const item = skillMap.get(state.skillId);
    if (!item) {
      els.detailPanel.innerHTML = empty("当前没有可展示的规则说明。");
      return;
    }

    const relatedFiles = [
      ...(item.skill_path ? [{ label: "SKILL.md", path: item.skill_path }] : []),
      ...(item.directory_path ? [{ label: "目录", path: item.directory_path }] : []),
      ...item.references.map((path, index) => ({ label: `Reference ${index + 1}`, path })),
      ...item.agents.map((path, index) => ({ label: `Agent ${index + 1}`, path })),
    ];

    els.detailPanel.innerHTML = `
      <div class="detail-head">
        <div class="detail-tags">
          <span class="tag">${escapeHtml(item.domain_label)}</span>
          <span class="tag">${escapeHtml(item.status_label)}</span>
        </div>
        <h2>${escapeHtml(item.title)}</h2>
        <p class="detail-name">${escapeHtml(item.name)}</p>
      </div>

      <section class="detail-block">
        <h3>何时使用</h3>
        <p>${escapeHtml(item.auto_trigger)}</p>
      </section>

      <section class="detail-block">
        <h3>核心职责</h3>
        <p>${escapeHtml(item.core_responsibility)}</p>
      </section>

      <section class="detail-block">
        <h3>结构章节</h3>
        <div class="plain-list">
          ${(item.sections || []).map((section) => `<div>${escapeHtml(section)}</div>`).join("") || "<div>暂无</div>"}
        </div>
      </section>

      <section class="detail-block">
        <h3>优化时优先看</h3>
        <div class="plain-list">
          ${(item.focus_points || []).map((point) => `<div>${escapeHtml(point)}</div>`).join("") || "<div>暂无</div>"}
        </div>
      </section>

      <section class="detail-block">
        <h3>相关文件</h3>
        <div class="file-list">
          ${
            relatedFiles.length
              ? relatedFiles
                  .map(
                    (file) => `
                      <a href="${hrefOf(file.path)}" target="_blank" rel="noreferrer">
                        <span>${escapeHtml(file.label)}</span>
                        <small>${escapeHtml(file.path)}</small>
                      </a>
                    `,
                  )
                  .join("")
              : "<div class='empty-inline'>暂无文件</div>"
          }
        </div>
      </section>
    `;
  }

  function render() {
    const items = filteredSkills();
    ensureSelection(items);
    renderDomainTabs(items);
    renderSkillStrip(items);
    renderDetail();
    els.resultHint.textContent = `${state.domain} 当前显示 ${nf.format(items.length)} 条`;
  }

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-action]");
    if (!trigger) {
      return;
    }

    const action = trigger.dataset.action;
    if (action === "set-domain") {
      state.domain = trigger.dataset.domain;
      render();
      return;
    }

    if (action === "select-skill") {
      state.skillId = trigger.dataset.skillId;
      render();
    }
  });

  els.searchInput.addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    render();
  });

  render();
})();
