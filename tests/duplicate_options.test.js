// Regression test for issue #63: loading the spell data more than once
// (switching between editions 5.5 and 5.0) must not duplicate the
// "Clase" and "Escuela" filter options.
// Runs with plain Node.js (no dependencies): node tests/duplicate_options.test.js
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

class FakeSelect {
  constructor() { this.options = []; this.value = ""; }
  addEventListener() {}
  appendChild(opt) { this.options.push(opt); return opt; }
  get length() { return this.options.length; }
  set length(n) { this.options.length = n; }
}

function fakeElement() {
  return { value: '', innerHTML: '', textContent: '', style: {}, disabled: false,
    classList: { add() {}, remove() {} }, addEventListener() {}, appendChild() {},
    querySelectorAll() { return []; }, replaceChildren() {} };
}

const selects = { classFilter: new FakeSelect(), schoolFilter: new FakeSelect() };
selects.classFilter.appendChild({ value: '', textContent: 'Todas' });
selects.schoolFilter.appendChild({ value: '', textContent: 'Todas' });

const elements = new Map();
const document = {
  getElementById(id) {
    if (!elements.has(id)) elements.set(id, selects[id] || fakeElement());
    return elements.get(id);
  },
  querySelector(sel) {
    if (sel === 'input[name="edition"]:checked') return { value: '5.5' };
    return null;
  },
  querySelectorAll() { return []; },
  createElement(tag) { return { tagName: tag, value: '', textContent: '' }; },
  addEventListener() {},
};

const spells = [
  { nombre: 'Bola de fuego', nivel: 3, clases: ['Mago', 'Hechicero'], escuela: 'Evocación' },
  { nombre: 'Curar heridas', nivel: 1, clases: ['Clérigo', 'Bardo'], escuela: 'Evocación' },
  { nombre: 'Escudo', nivel: 1, clases: ['Mago'], escuela: 'Abjuración' },
];

const context = {
  document,
  console,
  window: { addEventListener() {} },
  parseInt,
  fetch(url) {
    const body = String(url).endsWith('VERSION') ? '1' : null;
    return Promise.resolve({
      text: () => Promise.resolve(body || '1'),
      json: () => Promise.resolve(JSON.parse(JSON.stringify(spells))),
    });
  },
};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'app.js'), 'utf8'), context);

const flush = () => new Promise(resolve => setTimeout(resolve, 10));

(async () => {
  await flush();              // first load (DOMContentLoaded)
  await context.loadData();   // simulate switching editions again
  await flush();
  await context.loadData();   // and once more
  await flush();

  const expectedClasses = 5;  // Bola/Curar/Escudo: Mago, Hechicero, Clérigo, Bardo + "Todas"
  const expectedSchools = 3;  // Evocación, Abjuración + "Todas"
  const got = selects.classFilter.options.length;
  const gotSchools = selects.schoolFilter.options.length;
  if (got !== expectedClasses) {
    throw new Error(`expected ${expectedClasses} class options after loading twice, got ${got}`);
  }
  if (gotSchools !== expectedSchools) {
    throw new Error(`expected ${expectedSchools} school options after loading twice, got ${gotSchools}`);
  }
  console.log('OK: class and school options are not duplicated');
})().catch(err => { console.error(err.message); process.exit(1); });
