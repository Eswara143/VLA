// Unitree G1 Datasets — Categorized by Finger Count
// Data source: categorized_datasets.json

let allDatasets = [];
let searchQuery = '';

async function init() {
  if (window.CATEGORIZED_DATASETS && Array.isArray(window.CATEGORIZED_DATASETS) && window.CATEGORIZED_DATASETS.length > 0) {
    allDatasets = window.CATEGORIZED_DATASETS;
  } else {
    try {
      const res = await fetch('categorized_datasets.json');
      if (res.ok) {
        allDatasets = await res.json();
      }
    } catch (err) {
      console.error('Failed to load categorized_datasets.json:', err);
    }
  }

  if (!allDatasets || allDatasets.length === 0) {
    console.warn('No datasets loaded.');
    return;
  }

  renderAll();
}

function getFiltered() {
  if (!searchQuery) return allDatasets;
  return allDatasets.filter(d =>
    d.name.toLowerCase().includes(searchQuery) ||
    d.task_name.toLowerCase().includes(searchQuery) ||
    d.hand_type.toLowerCase().includes(searchQuery) ||
    d.id.toLowerCase().includes(searchQuery)
  );
}

function renderAll() {
  const filtered = getFiltered();

  const five = filtered.filter(d => d.finger_category === '5_fingers');
  const three = filtered.filter(d => d.finger_category === '3_fingers');
  const two = filtered.filter(d => d.finger_category === '2_fingers');

  renderGrid('grid-five', five, 'five');
  renderGrid('grid-three', three, 'three');
  renderGrid('grid-two', two, 'two');

  // Update counts
  setText('count-five', five.length);
  setText('count-three', three.length);
  setText('count-two', two.length);
  setText('count-total', filtered.length);
  setText('badge-total', `${allDatasets.length} DATASETS`);
  setText('badge-five', `${five.length} datasets`);
  setText('badge-three', `${three.length} datasets`);
  setText('badge-two', `${two.length} datasets`);

  // Show/hide empty sections
  toggleSection('section-five', five.length > 0);
  toggleSection('section-three', three.length > 0);
  toggleSection('section-two', two.length > 0);
}

function renderGrid(containerId, datasets, categoryKey) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (datasets.length === 0) {
    container.innerHTML = `<div class="empty-state">No datasets match your search.</div>`;
    return;
  }

  const badgeClass = categoryKey === 'five' ? 'badge-five' : categoryKey === 'three' ? 'badge-three' : 'badge-two';
  const cardClass = categoryKey === 'five' ? 'five-card' : categoryKey === 'three' ? 'three-card' : 'two-card';

  let html = '';
  datasets.forEach((d, i) => {
    const fingerLabel = d.finger_category === '5_fingers' ? '5 FINGERS' : d.finger_category === '3_fingers' ? '3 FINGERS' : '2 FINGERS';
    const delay = Math.min(i * 0.04, 0.8);

    html += `
      <div class="dataset-card ${cardClass}" style="animation-delay: ${delay}s">
        <div class="card-top-row">
          <div>
            <div class="card-task-name">${escHtml(d.task_name)}</div>
            <div class="card-hand-type">${escHtml(d.hand_type)}</div>
          </div>
          <span class="card-finger-badge ${badgeClass}">${fingerLabel}</span>
        </div>
        <div class="card-meta-row">
          <span>📥 ${d.downloads.toLocaleString()} downloads</span>
          <span>❤️ ${d.likes || 0}</span>
        </div>
        <div class="card-actions">
          <a href="${d.url}" target="_blank" rel="noopener" class="btn-card btn-open">
            Open on 🤗 HuggingFace ↗
          </a>
          <button class="btn-card btn-clone" onclick="copyClone('${escAttr(d.id)}')">
            📋 Copy Clone
          </button>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

// Search
function handleGlobalSearch(value) {
  searchQuery = value.toLowerCase().trim();
  renderAll();
}

// Scroll to category
function scrollToCategory(key) {
  const el = document.getElementById(`section-${key}`);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Copy clone command
function copyClone(repoId) {
  const cmd = `huggingface-cli download ${repoId} --repo-type dataset --local-dir ./${repoId.split('/')[1]}`;
  navigator.clipboard.writeText(cmd).then(() => showToast('Clone command copied!'));
}

// Helpers
function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function toggleSection(id, visible) {
  const el = document.getElementById(id);
  if (el) el.style.display = visible ? 'flex' : 'none';
}

function escHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function escAttr(str) {
  return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2200);
}

document.addEventListener('DOMContentLoaded', init);
