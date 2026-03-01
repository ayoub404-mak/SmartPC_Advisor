/**
 * SmartPC Advisor - Frontend Logic
 * Handles form submission, API calls, and page navigation.
 */

const API_BASE = 'http://127.0.0.1:8000';

let chatHistory = [];

// ============ Helpers ============
function showLoading(show = true) {
  const el = document.getElementById('loading-overlay');
  el.classList.toggle('hidden', !show);
}

function showToast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 4000);
}

function showPage(pageId) {
  document.querySelectorAll('.page-content').forEach(p => p.classList.add('hidden'));
  const page = document.getElementById(`page-${pageId}`);
  if (page) page.classList.remove('hidden');

  document.querySelectorAll('.nav-tab').forEach(btn => {
    btn.classList.toggle('bg-indigo-100', btn.dataset.page === pageId);
    btn.classList.toggle('text-indigo-700', btn.dataset.page === pageId);
  });
  // Show results tab only when we have results (set in renderResults)
  const resultsTab = document.querySelector('[data-page="results"]');
  if (resultsTab && window.hasResults) resultsTab.classList.remove('hidden');
}

async function fetchAPI(endpoint, body) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// ============ Questionnaire → Results ============
document.getElementById('questionnaire-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = {
    usage: form.usage.value,
    budget: parseFloat(form.budget.value) || 0,
    multitasking: form.multitasking.checked,
    gaming: form.gaming.checked,
  };

  showLoading(true);
  try {
    const result = await fetchAPI('/recommend-specs', data);
    window.hasResults = true;
    await renderResults(result, data);
    document.querySelector('[data-page="results"]')?.classList.remove('hidden');
    showPage('results');
  } catch (err) {
    showToast(err.message || 'Failed to get recommendations');
  } finally {
    showLoading(false);
  }
});

async function renderResults(result, userNeeds) {
  const container = document.getElementById('results-container');
  const specs = result.baseline_specs || {};
  const match = result.match_score ?? 0;
  const future = result.future_proof_score ?? 0;

  // Fetch upgrade path and sustainability in parallel (using baseline assumptions)
  let upgradeHtml = '<p class="text-slate-600 text-sm">Loading...</p>';
  let sustainHtml = '<span class="text-slate-500">Loading...</span>';
  try {
    const [upgradeRes, sustainRes] = await Promise.all([
      fetchAPI('/upgrade-path', {
        ram_slots: 2,
        storage_type: specs.storage_type || 'SSD',
        has_empty_slot: true,
      }),
      fetchAPI('/sustainability', {
        battery_life_hours: specs.battery_life_hours || 8,
        power_draw_watts: specs.power_draw_watts || 65,
        thermal_design: 'standard',
      }),
    ]);
    upgradeHtml = `
      <p class="text-slate-600 text-sm mb-2">${upgradeRes.ai_explanation || upgradeRes.summary}</p>
      <ul class="text-sm text-slate-600 list-disc list-inside">${(upgradeRes.advice || []).map(a => `<li>${a}</li>`).join('')}</ul>
    `;
    const eco = sustainRes.eco_score ?? 0;
    sustainHtml = `<span class="inline-block px-3 py-1 rounded-full text-sm font-medium bg-emerald-100 text-emerald-800">Eco: ${eco}%</span>
      <p class="text-slate-600 text-sm mt-2">${sustainRes.ai_explanation || ''}</p>`;
  } catch (_) {
    upgradeHtml = '<p class="text-slate-600 text-sm">Upgrade advice unavailable. Check API.</p>';
    sustainHtml = '<span class="text-slate-500">Eco score unavailable</span>';
  }

  container.innerHTML = `
    <div class="bg-white rounded-xl shadow-md p-6">
      <h2 class="text-xl font-semibold text-slate-800 mb-4">Recommended Specs</h2>
      <div class="grid grid-cols-2 gap-3 text-sm mb-4">
        <div><span class="text-slate-500">RAM</span> ${specs.ram_gb || 8} GB</div>
        <div><span class="text-slate-500">Storage</span> ${specs.storage_gb || 256} GB ${specs.storage_type || 'SSD'}</div>
        <div><span class="text-slate-500">CPU</span> ${specs.cpu || '-'}</div>
        <div><span class="text-slate-500">GPU</span> ${specs.gpu || '-'}</div>
        <div><span class="text-slate-500">Battery</span> ${specs.battery_life_hours || '-'}h</div>
      </div>
      <div class="p-3 bg-indigo-50 rounded-lg text-slate-700 text-sm">
        ${result.ai_explanation || 'No AI explanation available.'}
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-white rounded-xl shadow-md p-6">
        <h3 class="font-semibold text-slate-800 mb-2">Match Score</h3>
        <div class="h-4 bg-slate-200 rounded-full overflow-hidden">
          <div class="h-full bg-indigo-500 rounded-full transition-all" style="width: ${match}%"></div>
        </div>
        <span class="text-sm text-slate-600">${match}%</span>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6">
        <h3 class="font-semibold text-slate-800 mb-2">Future-proof Score</h3>
        <div class="h-4 bg-slate-200 rounded-full overflow-hidden">
          <div class="h-full bg-emerald-500 rounded-full transition-all" style="width: ${future}%"></div>
        </div>
        <span class="text-sm text-slate-600">${future}%</span>
      </div>
    </div>

    <div class="bg-white rounded-xl shadow-md p-6">
      <h3 class="font-semibold text-slate-800 mb-2 flex items-center gap-2">
        <span>🔧</span> Upgrade Path Advisor
      </h3>
      ${upgradeHtml}
    </div>

    <div class="bg-white rounded-xl shadow-md p-6">
      <h3 class="font-semibold text-slate-800 mb-2">Sustainability Score</h3>
      ${sustainHtml}
    </div>
  `;
}

// ============ Risk Check ============
document.getElementById('risk-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = {
    battery_health_percent: parseFloat(form.battery_health.value) || 0,
    ssd_health_percent: parseFloat(form.ssd_health.value) || 0,
    cycle_count: parseInt(form.cycle_count.value) || 0,
    temperature_celsius: form.temperature.value ? parseFloat(form.temperature.value) : null,
  };

  showLoading(true);
  try {
    const result = await fetchAPI('/risk-check', data);
    const el = document.getElementById('risk-result');
    const risk = result.risk_score ?? 0;
    const badgeClass = risk < 30 ? 'bg-emerald-100 text-emerald-800' : risk < 60 ? 'bg-amber-100 text-amber-800' : 'bg-red-100 text-red-800';
    el.innerHTML = `
      <div class="p-4 rounded-lg border border-slate-200">
        <h3 class="font-semibold text-slate-800 mb-2">Risk Score</h3>
        <span class="inline-block px-4 py-2 rounded-full text-lg font-bold ${badgeClass}">${risk}%</span>
        <p class="mt-3 text-slate-600 text-sm">${result.ai_explanation || ''}</p>
      </div>
    `;
    el.classList.remove('hidden');
  } catch (err) {
    showToast(err.message || 'Risk check failed');
  } finally {
    showLoading(false);
  }
});

// ============ Budget Stretch ============
document.getElementById('budget-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = { budget: parseFloat(form.budget.value) || 0 };

  showLoading(true);
  try {
    const result = await fetchAPI('/budget-stretch', data);
    const el = document.getElementById('budget-result');
    el.innerHTML = `
      <div class="p-4 rounded-lg border border-slate-200 bg-indigo-50">
        <h3 class="font-semibold text-slate-800 mb-2">Trade-off Suggestions</h3>
        <p class="text-slate-700">${result.trade_offs || result.ai_explanation || 'No suggestions.'}</p>
      </div>
    `;
    el.classList.remove('hidden');
  } catch (err) {
    showToast(err.message || 'Budget stretch failed');
  } finally {
    showLoading(false);
  }
});

// ============ Judge Mode Demo ============
document.getElementById('judge-demo-btn')?.addEventListener('click', async () => {
  const output = document.getElementById('judge-output');
  output.classList.remove('hidden');
  output.innerHTML = '<p class="text-slate-600">Running demo...</p>';
  showLoading(true);

  const steps = [];

  try {
    // 1. Questionnaire
    const needs = { usage: 'student', budget: 700, multitasking: true, gaming: false };
    const rec = await fetchAPI('/recommend-specs', needs);
    steps.push(`<strong>1. Recommendation</strong>: ${rec.ai_explanation}`);
    steps.push(`Specs: ${rec.baseline_specs?.ram_gb}GB RAM, ${rec.baseline_specs?.storage_gb}GB ${rec.baseline_specs?.storage_type}`);

    // 2. Compare
    const laptops = [
      { name: 'Laptop A', specs: { ram_gb: 8, storage_gb: 256, storage_type: 'SSD', gpu: 'Integrated' } },
      { name: 'Laptop B', specs: { ram_gb: 16, storage_gb: 512, storage_type: 'SSD', gpu: 'Integrated' } },
    ];
    const comp = await fetchAPI('/compare-laptops', laptops);
    steps.push(`<strong>2. Comparison</strong>: ${comp.comparison}`);

    // 3. Risk check
    const health = { battery_health_percent: 78, ssd_health_percent: 92, cycle_count: 250 };
    const risk = await fetchAPI('/risk-check', health);
    steps.push(`<strong>3. Risk Check</strong>: Risk ${risk.risk_score}% - ${risk.ai_explanation}`);

    output.innerHTML = steps.map(s => `<div class="p-3 bg-slate-50 rounded-lg text-sm">${s}</div>`).join('');
  } catch (err) {
    output.innerHTML = `<div class="p-3 bg-red-50 text-red-700 rounded-lg">Error: ${err.message}</div>`;
  } finally {
    showLoading(false);
  }
});

// ============ AI Chat Logic ============
document.getElementById('chat-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const input = form.message;
  const message = input.value.trim();
  if (!message) return;

  const container = document.getElementById('chat-messages');

  // Add user message to UI
  renderChatMessage('user', message);
  input.value = '';

  showLoading(true);
  try {
    const result = await fetchAPI('/chat', {
      history: chatHistory,
      message: message
    });

    // Update history and UI
    chatHistory = [...chatHistory, ...result.history_update];
    renderChatMessage('assistant', result.response);
  } catch (err) {
    showToast(err.message || 'Chat failed');
  } finally {
    showLoading(false);
  }
});

function renderChatMessage(role, content) {
  const container = document.getElementById('chat-messages');
  const div = document.createElement('div');

  const isUser = role === 'user';
  div.className = `message-bubble ${role} p-3 max-w-[80%] text-sm rounded-2xl shadow-sm animate-fade-in`;

  if (isUser) {
    div.classList.add('bg-indigo-600', 'text-white', 'ml-auto', 'rounded-tr-none');
  } else {
    div.classList.add('bg-white', 'border', 'border-slate-200', 'text-slate-700', 'rounded-tl-none');
  }

  div.textContent = content;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

// ============ Navigation ============
document.querySelectorAll('.nav-tab').forEach(btn => {
  btn.addEventListener('click', () => showPage(btn.dataset.page));
});
