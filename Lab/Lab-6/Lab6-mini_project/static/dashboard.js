/**
 * Modern Dashboard — อุบัติเหตุทางถนน 2568
 */
const charts = {};
let tableRows = [];
let tableTotal = 0;
let pageOffset = 0;

const COLORS = {
    primary: '#5D87FF',
    palette: ['#5D87FF', '#49BEFF', '#13DEB9', '#FFAE1F', '#FA896B', '#539BFF', '#8B5CF6', '#ECF2FF'],
};

const chartBase = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { labels: { font: { family: 'Plus Jakarta Sans', size: 11 }, boxWidth: 12 } },
    },
};

function qs(id) { return document.getElementById(id); }

function filterParams() {
    const p = new URLSearchParams();
    const map = {
        'f-province': 'province',
        'f-region': 'region',
        'f-severity': 'severity',
        'f-vehicle': 'vehicle',
        'f-road': 'road_type',
        'f-time': 'time_slot',
        'f-month': 'month',
    };
    for (const [elId, key] of Object.entries(map)) {
        const v = qs(elId)?.value;
        if (v) p.set(key, v);
    }
    const plimit = qs('f-province-limit')?.value;
    if (plimit) p.set('province_limit', plimit);
    const q = qs('globalSearch')?.value?.trim();
    if (q) p.set('q', q);
    return p;
}

async function api(path, extra = {}) {
    const p = filterParams();
    for (const [k, v] of Object.entries(extra)) p.set(k, v);
    const url = p.toString() ? `${path}?${p}` : path;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`API ${path} failed`);
    return res.json();
}

function destroyChart(id) {
    if (charts[id]) {
        charts[id].destroy();
        delete charts[id];
    }
}

function severityBadge(s) {
    const map = {
        'เสียชีวิต': 'badge-danger',
        'บาดเจ็บสาหัส': 'badge-warning',
        'บาดเจ็บปานกลาง': 'badge-warning',
        'บาดเจ็บเล็กน้อย': 'badge-success',
        'ไม่บาดเจ็บ': 'badge-info',
    };
    const cls = map[s] || 'badge-info';
    return `<span class="badge ${cls}">${s || '—'}</span>`;
}

function fillSelect(id, items, allLabel = 'ทั้งหมด') {
    const el = qs(id);
    if (!el) return;
    const cur = el.value;
    el.innerHTML = `<option value="">${allLabel}</option>`;
    items.forEach(v => {
        const o = document.createElement('option');
        o.value = typeof v === 'object' ? v.value : v;
        o.textContent = typeof v === 'object' ? v.label : v;
        el.appendChild(o);
    });
    if ([...el.options].some(o => o.value === cur)) el.value = cur;
}

async function loadMeta() {
    const meta = await api('/api/meta');
    fillSelect('f-province', meta.provinces);
    fillSelect('f-region', meta.regions);
    fillSelect('f-severity', meta.severities);
    fillSelect('f-vehicle', meta.vehicles);
    fillSelect('f-road', meta.road_types);
    fillSelect('f-time', meta.time_slots);
    fillSelect('f-month', meta.months, 'ทั้งปี');
}

function updateChips() {
    const chips = qs('activeChips');
    const labels = {
        province: 'จังหวัด', region: 'ภูมิภาค', severity: 'ความรุนแรง',
        vehicle: 'ยานพาหนะ', road_type: 'ถนน', time_slot: 'ช่วงเวลา', month: 'เดือน',
    };
    const p = filterParams();
    const parts = [];
    for (const [k, label] of Object.entries(labels)) {
        if (p.get(k)) parts.push(`${label}: ${p.get(k)}`);
    }
    if (p.get('q')) parts.push(`ค้นหา: ${p.get('q')}`);
    chips.innerHTML = parts.length
        ? parts.map(t => `<span class="chip">${t}</span>`).join('')
        : '<span class="chip">ไม่มีตัวกรอง — ข้อมูลทั้งหมด</span>';
    qs('filterStatus').textContent = parts.length ? `กรอง ${parts.length} เงื่อนไข` : 'แสดงข้อมูลทั้งหมด';
}

async function loadKpis() {
    const d = await api('/api/summary');
    qs('kpi-accidents').textContent = (d.total_accidents || 0).toLocaleString();
    qs('kpi-deaths').textContent = (d.total_deaths || 0).toLocaleString();
    qs('kpi-injured').textContent = (d.total_injured || 0).toLocaleString();
    qs('kpi-avg').textContent = d.avg_injured_per_accident ?? '—';
    qs('kpi-fatal').textContent = (d.fatal_cases || 0).toLocaleString();
    qs('kpi-fatal-rate').textContent = `อัตราเสียชีวิต ${d.fatal_rate_pct || 0}%`;
    qs('kpi-provinces').textContent = (d.province_count || 0).toLocaleString();
}

async function loadCharts() {
    const [provinces, regions, monthly, severity, vehicles, roads, times] = await Promise.all([
        api('/api/by-province'),
        api('/api/by-region'),
        api('/api/monthly'),
        api('/api/severity'),
        api('/api/vehicle-type', { limit: 10 }),
        api('/api/by-road-type'),
        api('/api/by-time-slot'),
    ]);

    const months = ['', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];

    destroyChart('chartProvince');
    charts.chartProvince = new Chart(qs('chartProvince'), {
        type: 'bar',
        data: {
            labels: provinces.map(r => r['จังหวัด']),
            datasets: [
                { label: 'อุบัติเหตุ', data: provinces.map(r => r['จำนวนครั้ง']), backgroundColor: COLORS.primary, borderRadius: 6 },
                { label: 'เสียชีวิต', data: provinces.map(r => r['ผู้เสียชีวิต']), backgroundColor: COLORS.palette[4], borderRadius: 6 },
            ],
        },
        options: { ...chartBase, indexAxis: 'y', scales: { x: { beginAtZero: true } } },
    });

    destroyChart('chartRegion');
    charts.chartRegion = new Chart(qs('chartRegion'), {
        type: 'doughnut',
        data: {
            labels: regions.map(r => r['ภูมิภาค']),
            datasets: [{ data: regions.map(r => r['จำนวนครั้ง']), backgroundColor: COLORS.palette }],
        },
        options: { ...chartBase, plugins: { ...chartBase.plugins, legend: { position: 'bottom' } } },
    });

    destroyChart('chartMonthly');
    charts.chartMonthly = new Chart(qs('chartMonthly'), {
        type: 'line',
        data: {
            labels: monthly.map(r => months[r['เดือน']] || r['เดือน']),
            datasets: [
                { label: 'อุบัติเหตุ', data: monthly.map(r => r['จำนวนครั้ง']), borderColor: COLORS.primary, backgroundColor: 'rgba(93,135,255,0.1)', fill: true, tension: 0.35 },
                { label: 'เสียชีวิต', data: monthly.map(r => r['ผู้เสียชีวิต']), borderColor: COLORS.palette[4], tension: 0.35 },
                { label: 'บาดเจ็บ', data: monthly.map(r => r['ผู้บาดเจ็บ']), borderColor: COLORS.palette[2], tension: 0.35, hidden: true },
            ],
        },
        options: { ...chartBase, scales: { y: { beginAtZero: true } } },
    });

    destroyChart('chartSeverity');
    charts.chartSeverity = new Chart(qs('chartSeverity'), {
        type: 'polarArea',
        data: {
            labels: severity.map(r => r['ความรุนแรง']),
            datasets: [{ data: severity.map(r => r['จำนวน']), backgroundColor: COLORS.palette.map(c => c + '99') }],
        },
        options: chartBase,
    });

    destroyChart('chartVehicle');
    charts.chartVehicle = new Chart(qs('chartVehicle'), {
        type: 'pie',
        data: {
            labels: vehicles.map(r => r['ยานพาหนะ']),
            datasets: [{ data: vehicles.map(r => r['จำนวน']), backgroundColor: COLORS.palette }],
        },
        options: { ...chartBase, plugins: { ...chartBase.plugins, legend: { position: 'right' } } },
    });

    destroyChart('chartRoad');
    charts.chartRoad = new Chart(qs('chartRoad'), {
        type: 'bar',
        data: {
            labels: roads.map(r => r['ประเภทถนน'] || '—'),
            datasets: [{ label: 'จำนวน', data: roads.map(r => r['จำนวน']), backgroundColor: COLORS.palette[1], borderRadius: 6 }],
        },
        options: { ...chartBase, scales: { y: { beginAtZero: true } } },
    });

    destroyChart('chartTime');
    charts.chartTime = new Chart(qs('chartTime'), {
        type: 'bar',
        data: {
            labels: times.map(r => r['ช่วงเวลา'] || '—'),
            datasets: [{ data: times.map(r => r['จำนวน']), backgroundColor: COLORS.palette[2], borderRadius: 8 }],
        },
        options: { ...chartBase, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
    });
}

async function loadTable() {
    const limit = parseInt(qs('pageSize').value, 10) || 50;
    const data = await api('/api/accidents', { limit, offset: pageOffset });
    tableRows = data.rows;
    tableTotal = data.total;

    const tbody = qs('tableBody');
    if (!tableRows.length) {
        tbody.innerHTML = '<tr><td colspan="12" class="loading-overlay">ไม่พบข้อมูล</td></tr>';
    } else {
        tbody.innerHTML = tableRows.map(r => `
            <tr>
                <td><code>${r.accident_id}</code></td>
                <td>${r['วันที่เกิดเหตุ'] || '—'}</td>
                <td>${r['เวลาเกิดเหตุ'] || '—'}</td>
                <td><strong>${r['จังหวัด'] || '—'}</strong></td>
                <td>${r['อำเภอ'] || '—'}</td>
                <td>${r['ภูมิภาค'] || '—'}</td>
                <td>${r['ประเภทถนน'] || '—'}</td>
                <td>${r['ยานพาหนะหลัก'] || '—'}</td>
                <td>${severityBadge(r['ความรุนแรง'])}</td>
                <td>${r['ช่วงเวลา'] || '—'}</td>
                <td>${r['จำนวนผู้เสียชีวิต'] ?? 0}</td>
                <td>${r['จำนวนผู้บาดเจ็บรวม'] ?? 0}</td>
            </tr>
        `).join('');
    }

    const from = tableTotal ? pageOffset + 1 : 0;
    const to = Math.min(pageOffset + limit, tableTotal);
    qs('tableInfo').textContent = `แสดง ${from.toLocaleString()}–${to.toLocaleString()} จาก ${tableTotal.toLocaleString()} แถว`;
    qs('btnPrev').disabled = pageOffset <= 0;
    qs('btnNext').disabled = pageOffset + limit >= tableTotal;
}

async function refreshAll() {
    updateChips();
    await Promise.all([loadKpis(), loadCharts(), loadTable()]);
}

function resetFilters() {
    ['f-province', 'f-region', 'f-severity', 'f-vehicle', 'f-road', 'f-time', 'f-month'].forEach(id => {
        const el = qs(id);
        if (el) el.value = '';
    });
    qs('globalSearch').value = '';
    pageOffset = 0;
}

function exportCSV() {
    if (!tableRows.length) return;
    const headers = Object.keys(tableRows[0]);
    const lines = [
        headers.join(','),
        ...tableRows.map(r => headers.map(h => `"${String(r[h] ?? '').replace(/"/g, '""')}"`).join(',')),
    ];
    const blob = new Blob(['\uFEFF' + lines.join('\n')], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `accidents_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
}

function setupNav() {
    document.querySelectorAll('.nav-link[data-scroll]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            const id = link.getAttribute('data-scroll');
            document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
}

let searchTimer;
function bindEvents() {
    qs('btnApply').addEventListener('click', () => { pageOffset = 0; refreshAll(); });
    qs('btnReset').addEventListener('click', () => { resetFilters(); refreshAll(); });
    qs('btnRefresh').addEventListener('click', refreshAll);
    qs('btnExport').addEventListener('click', exportCSV);
    qs('pageSize').addEventListener('change', () => { pageOffset = 0; loadTable(); });
    qs('btnPrev').addEventListener('click', () => {
        pageOffset = Math.max(0, pageOffset - parseInt(qs('pageSize').value, 10));
        loadTable();
    });
    qs('btnNext').addEventListener('click', () => {
        pageOffset += parseInt(qs('pageSize').value, 10);
        loadTable();
    });
    qs('f-province-limit').addEventListener('change', loadCharts);
    qs('globalSearch').addEventListener('input', () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => { pageOffset = 0; loadTable(); updateChips(); }, 400);
    });
}

window.addEventListener('DOMContentLoaded', async () => {
    setupNav();
    bindEvents();
    try {
        await loadMeta();
        await refreshAll();
    } catch (err) {
        console.error(err);
        qs('tableBody').innerHTML = `<tr><td colspan="12" class="loading-overlay">เกิดข้อผิดพลาด: ${err.message}</td></tr>`;
    }
});
