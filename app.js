'use strict';

let spells = [];
let filtered = [];
let currentPage = 1;
let currentSortKey = null;
let currentSortDir = 0;

const searchInput = document.getElementById('search');
const levelFilter = document.getElementById('levelFilter');
const classFilter = document.getElementById('classFilter');
const schoolFilter = document.getElementById('schoolFilter');
const pageSizeSelect = document.getElementById('pageSize');
const rangeUnitSelect = document.getElementById('rangeUnit');
const tableBody = document.getElementById('table-body');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
const pageInfo = document.getElementById('page-info');
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modal-title');
const modalMaterials = document.getElementById('modal-materials');
const modalDescription = document.getElementById('modal-description');
const modalClose = document.getElementById('modal-close');

function getSelectedEdition() {
  const el = document.querySelector('input[name="edition"]:checked');
  return el ? el.value : '5.5';
}

function getSpellDataPath() {
  const ed = getSelectedEdition();
  return ed === '5.0' ? 'spells_ed5_0.json' : 'spells_ed5_5.json';
}

function normalize(str) {
  return str.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
}

function applySort(arr) {
  if (!currentSortKey || currentSortDir === 0) return arr;
  return arr.slice().sort((a, b) => {
    let valA = a[currentSortKey];
    let valB = b[currentSortKey];
    if (currentSortKey === 'nivel') {
      return (valA - valB) * currentSortDir;
    }
    if (Array.isArray(valA)) valA = valA.join(', ');
    if (Array.isArray(valB)) valB = valB.join(', ');
    return valA.localeCompare(valB, 'es', { sensitivity: 'base' }) * currentSortDir;
  });
}

function updateSortIndicators() {
  document.querySelectorAll('th.sortable').forEach(th => {
    th.classList.remove('sorted-asc', 'sorted-desc');
    const key = th.getAttribute('data-key');
    if (key === currentSortKey) {
      if (currentSortDir === 1) th.classList.add('sorted-asc');
      else if (currentSortDir === -1) th.classList.add('sorted-desc');
    }
  });
}

function formatByUnit(field) {
  if (Array.isArray(field)) {
    if (rangeUnitSelect.value === 'pies') return field[0];
    if (rangeUnitSelect.value === 'metros') return field[1];
  }
  return field;
}

function renderTable() {
  let data = filtered;
  data = applySort(data);
  const pageSize = parseInt(pageSizeSelect.value, 10);
  const start = (currentPage - 1) * pageSize;
  const end = start + pageSize;
  const pageItems = data.slice(start, end);

  tableBody.innerHTML = '';
  pageItems.forEach(spell => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${spell.nombre}</td>
      <td>${spell.clases.join(', ')}</td>
      <td>${spell.escuela}</td>
      <td>${spell.nivel}</td>
      <td>${spell.tiempo_de_lanzamiento}</td>
      <td>${spell.ritual ? 'Sí' : 'No'}</td>
      <td>${formatByUnit(spell.alcance)}</td>
      <td>${spell.visible ? 'Sí' : 'No'}</td>
      <td>${spell.componentes.join(', ')}</td>
      <td>${spell.concentracion ? 'Sí' : 'No'}</td>
      <td>${spell.duracion}</td>
      <td>${spell.tirada_de_salvacion || '--'}</td>
      <td>${spell.requiere_ataque ? 'Sí' : 'No'}</td>
    `;
    tr.addEventListener('click', () => {
      modalTitle.textContent = spell.nombre;
      modalMaterials.textContent = spell.materiales || 'Ninguno';
      modalDescription.innerHTML = formatByUnit(spell.descripcion);
      modal.style.display = 'block';
    });
    tableBody.appendChild(tr);
  });

  const totalPages = Math.ceil(data.length / pageSize) || 1;
  pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
  prevBtn.disabled = currentPage === 1;
  nextBtn.disabled = currentPage === totalPages;

  updateSortIndicators();
}

function updateFilter() {
  const nameQuery = normalize(searchInput.value);
  let result = spells.filter(spell => normalize(spell.nombre).includes(nameQuery));
  if (levelFilter.value) result = result.filter(spell => spell.nivel.toString() === levelFilter.value);
  if (classFilter.value) result = result.filter(spell => spell.clases.includes(classFilter.value));
  if (schoolFilter.value) result = result.filter(spell => spell.escuela === schoolFilter.value);
  filtered = result;
  currentPage = 1;
  renderTable();
}

searchInput.addEventListener('input', updateFilter);
levelFilter.addEventListener('change', updateFilter);
classFilter.addEventListener('change', updateFilter);
schoolFilter.addEventListener('change', updateFilter);
rangeUnitSelect.addEventListener('change', renderTable);
pageSizeSelect.addEventListener('change', () => { currentPage = 1; renderTable(); });
prevBtn.addEventListener('click', () => { if (currentPage > 1) { currentPage--; renderTable(); } });
nextBtn.addEventListener('click', () => { const totalPages = Math.ceil(filtered.length / parseInt(pageSizeSelect.value, 10)) || 1; if (currentPage < totalPages) { currentPage++; renderTable(); } });

modalClose.addEventListener('click', () => { modal.style.display = 'none'; });
window.addEventListener('click', e => { if (e.target === modal) modal.style.display = 'none'; });

async function loadData() {
  const filePath = getSpellDataPath();
  try {
    fetch(filePath)
      .then(response => response.json())
      .then(data => {
        spells = data;
        spells.sort((a, b) => a.nombre.localeCompare(b.nombre, 'es', { sensitivity: 'base' }));
        const classesSet = new Set();
        const schoolsSet = new Set();
        spells.forEach(s => { s.clases.forEach(c => classesSet.add(c)); schoolsSet.add(s.escuela); });
        Array.from(classesSet).sort().forEach(c => { const opt = document.createElement('option'); opt.value = c; opt.textContent = c; classFilter.appendChild(opt); });
        Array.from(schoolsSet).sort().forEach(sch => { const opt = document.createElement('option'); opt.value = sch; opt.textContent = sch; schoolFilter.appendChild(opt); });
        filtered = spells;
        renderTable();
      })
      .catch(error => {
        console.error('Error al cargar spells.json', error);
        tableBody.innerHTML = '<tr><td colspan="13">No se pudieron cargar los datos.</td></tr>';
  });

  } catch (err) {
    console.error(err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadData();
  document.querySelectorAll('th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      const key = th.getAttribute('data-key');
      if (currentSortKey !== key) { currentSortKey = key; currentSortDir = 1; }
      else { currentSortDir = currentSortDir === 1 ? -1 : currentSortDir === -1 ? 0 : 1; }
      updateFilter();
    });
  });
  document.querySelectorAll('input[name="edition"]').forEach(radio => {
    radio.addEventListener('change', () => {
      loadData(); // sin botones extra: cambia el radio y listo
    });
  });
});


fetch('./VERSION')
  .then(response => response.text())
  .then(ver_text =>{
    const version = ver_text.trim();
    document.querySelector('#app-version')?.replaceChildren(document.createTextNode(version));
  } )
  .catch(() => {});

// Reporting an issue:
const reportBtn       = document.getElementById('reportError');
const reportModal     = document.getElementById('report-modal');
const reportCloseBtn  = document.getElementById('report-modal-close');
const clearFiltersBtn = document.getElementById('clearFilters');

reportBtn.addEventListener('click', () => {
  reportModal.style.display = 'block';
});
reportCloseBtn.addEventListener('click', () => {
  reportModal.style.display = 'none';
});
window.addEventListener('click', e => {
  if (e.target === reportModal) reportModal.style.display = 'none';
});
clearFiltersBtn.addEventListener('click', () => {
  levelFilter.value = '';
  classFilter.value = '';
  schoolFilter.value = '';
  currentPage = 1;
  updateFilter();
});

// Access GitHub repository
document.getElementById('ghBtn').addEventListener('click', () => {
  window.open('https://github.com/Jtachan/DnD-5.5-Spells-ES', '_blank', 'noopener');
});
