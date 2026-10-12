/* Translations for the static laptop illustration; no motion or feature controls. */
(function () {
    'use strict';
    const root = document.querySelector('.learning-showcase');
    if (!root) return;
    window.__rerender_workspace = function () {
        root.querySelectorAll('[data-workspace-alt]').forEach(function (el) {
            el.alt = t(el.dataset.workspaceAlt);
        });
    };
    window.__rerender_workspace();
})();
