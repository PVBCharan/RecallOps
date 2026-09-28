/* ═══════════════════════════════════════════════════════════════════
   RecallOps — Client-side JavaScript
   ═══════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    initFlashMessages();
    initFileUpload();
    initTabs();
    initDomainSelector();
    initLoadingStates();
});

/* ── Flash messages auto-dismiss ──────────────────────────────────── */
function initFlashMessages() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach((flash, i) => {
        setTimeout(() => {
            flash.style.animation = 'flashOut 0.3s ease forwards';
            setTimeout(() => flash.remove(), 300);
        }, 4000 + i * 500);
    });
}

/* ── File upload handling ─────────────────────────────────────────── */
function initFileUpload() {
    const area = document.getElementById('file-upload-area');
    const input = document.getElementById('evidence-files');
    const list = document.getElementById('file-list');

    if (!area || !input) return;

    // Click to select
    area.addEventListener('click', () => input.click());

    // Drag and drop
    area.addEventListener('dragover', (e) => {
        e.preventDefault();
        area.classList.add('dragover');
    });
    area.addEventListener('dragleave', () => {
        area.classList.remove('dragover');
    });
    area.addEventListener('drop', (e) => {
        e.preventDefault();
        area.classList.remove('dragover');
        input.files = e.dataTransfer.files;
        updateFileList();
    });

    // File selection
    input.addEventListener('change', updateFileList);

    function updateFileList() {
        if (!list) return;
        list.innerHTML = '';
        const files = input.files;
        if (!files.length) return;

        for (const file of files) {
            const item = document.createElement('div');
            item.className = 'file-item';
            const icon = getFileIcon(file.name);
            const size = formatFileSize(file.size);
            item.innerHTML = `
                <span class="file-icon">${icon}</span>
                <span class="file-name">${file.name}</span>
                <span class="file-size">${size}</span>
            `;
            list.appendChild(item);
        }
    }
}

function getFileIcon(name) {
    const ext = name.split('.').pop().toLowerCase();
    const icons = {
        csv: '📊', jpg: '🖼️', jpeg: '🖼️', png: '🖼️',
        gif: '🖼️', bmp: '🖼️', webp: '🖼️',
        mp4: '🎬', avi: '🎬', mov: '🎬', mkv: '🎬', webm: '🎬',
    };
    return icons[ext] || '📎';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

/* ── Tab navigation ───────────────────────────────────────────────── */
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const group = tab.closest('.tabs');
            const container = group ? group.parentElement : document;

            // Deactivate all tabs in this group
            group.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Show corresponding content
            const target = tab.dataset.tab;
            container.querySelectorAll('.tab-content').forEach(c => {
                c.classList.toggle('active', c.id === target);
            });
        });
    });
}

/* ── Domain selector on new case form ─────────────────────────────── */
function initDomainSelector() {
    const select = document.getElementById('domain-select');
    const exampleBtn = document.getElementById('load-example-btn');
    if (!select) return;

    select.addEventListener('change', () => {
        updateDomainLabels(select.value);
    });

    if (exampleBtn) {
        exampleBtn.addEventListener('click', loadExample);
    }
}

function updateDomainLabels(domain) {
    // Update field labels based on domain config (from data attributes)
    const container = document.getElementById('case-form');
    if (!container) return;
    const labels = container.dataset;
    // This is handled server-side via template; placeholder for future AJAX
}

function loadExample() {
    const select = document.getElementById('domain-select');
    if (!select) return;
    const domain = select.value;

    // Fetch example from API
    fetch(`/api/domains`)
        .then(r => r.json())
        .then(domains => {
            const config = domains[domain];
            if (!config || !config.example) return;
            const ex = config.example;

            const title = document.getElementById('case-title');
            const desc = document.getElementById('case-description');
            const symptoms = document.getElementById('case-symptoms');
            const action = document.getElementById('case-action');
            const outcome = document.getElementById('case-outcome');

            if (title) title.value = ex.title || '';
            if (desc) desc.value = ex.description || '';
            if (symptoms) symptoms.value = ex.symptoms || '';
            if (action) action.value = ex.action_taken || '';
            if (outcome) outcome.value = ex.outcome || '';

            // Visual feedback
            const btn = document.getElementById('load-example-btn');
            if (btn) {
                const orig = btn.textContent;
                btn.textContent = '✓ Loaded!';
                btn.classList.add('btn-success');
                setTimeout(() => {
                    btn.textContent = orig;
                    btn.classList.remove('btn-success');
                }, 1500);
            }
        })
        .catch(() => {});
}

/* ── Loading states for form submission ───────────────────────────── */
function initLoadingStates() {
    const forms = document.querySelectorAll('form[data-loading]');
    forms.forEach(form => {
        form.addEventListener('submit', () => {
            const overlay = document.getElementById('loading-overlay');
            const msg = form.dataset.loading || 'Processing...';
            if (overlay) {
                overlay.querySelector('p').textContent = msg;
                overlay.classList.add('active');
            }

            // Disable submit buttons
            form.querySelectorAll('button[type="submit"], .btn-primary').forEach(btn => {
                btn.disabled = true;
                btn.style.opacity = '0.6';
            });
        });
    });
}

/* ── Flash out animation ──────────────────────────────────────────── */
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes flashOut {
        from { opacity: 1; transform: translateX(0); }
        to   { opacity: 0; transform: translateX(20px); }
    }
`;
document.head.appendChild(styleSheet);
