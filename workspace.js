/* Native CSS 3D scene with manual, accessible feature tabs. */
(function () {
    'use strict';
    const root = document.querySelector('.learning-workspace');
    if (!root) return;
    I18N_REGISTER({
        'workspace.eyebrow': { en:'One connected learning experience', es:'Una experiencia de aprendizaje integrada', ja:'一つにつながる学習体験' },
        'workspace.pause': { en:'Pause motion', es:'Pausar animación', ja:'動きを停止' },
        'workspace.resume': { en:'Resume motion', es:'Reanudar animación', ja:'動きを再開' },
        'workspace.reduced': { en:'Motion reduced', es:'Movimiento reducido', ja:'動きを抑制中' },
        'workspace.model': { en:'First stage · AJR (2001)', es:'Primera etapa · AJR (2001)', ja:'第一段階 · AJR (2001)' },
        'workspace.open': { en:'Open in Colab', es:'Abrir en Colab', ja:'Colabで開く' },
        'workspace.menus': { en:'File &nbsp; Edit &nbsp; View &nbsp; Insert &nbsp; Runtime &nbsp; Tools', es:'Archivo &nbsp; Editar &nbsp; Ver &nbsp; Insertar &nbsp; Entorno &nbsp; Herramientas', ja:'ファイル &nbsp; 編集 &nbsp; 表示 &nbsp; 挿入 &nbsp; ランタイム &nbsp; ツール' },
        'workspace.code': { en:'Code', es:'Código', ja:'コード' },
        'workspace.text': { en:'Text', es:'Texto', ja:'テキスト' },
        'workspace.executed': { en:'Executed', es:'Ejecutado', ja:'実行済み' },
        'workspace.ai': { en:'AI-assisted interpretation', es:'Interpretación asistida por IA', ja:'AIによる解釈支援' },
        'workspace.aiCaption': { en:'Explain the code. Connect the concepts.', es:'Explica el código. Conecta los conceptos.', ja:'コードを理解し、概念をつなげる。' },
        'workspace.preview': { en:'AJR (2001) · 64 countries', es:'AJR (2001) · 64 países', ja:'AJR (2001) · 64か国' },
        'workspace.features': { en:'Learning features', es:'Funciones de aprendizaje', ja:'学習機能' },
        'workspace.scene': { en:'A portrait book beside a Colab-style notebook with executed AJR instrumental-variables code and its real first-stage plot', es:'Un libro junto a un cuaderno estilo Colab con código de variables instrumentales AJR ejecutado y su gráfico real de primera etapa', ja:'書籍とColab形式のノートブック。AJRの操作変数推定コードと実際に生成した第一段階の図。' }
    });
    const tabs = Array.from(root.querySelectorAll('[role="tab"]'));
    const panels = Array.from(root.querySelectorAll('[role="tabpanel"]'));
    const scene = root.querySelector('.workspace-scene');
    const button = document.getElementById('workspace-motion');
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    let paused = false;

    function select(index, focus) {
        tabs.forEach((tab, i) => {
            tab.setAttribute('aria-selected', String(i === index));
            tab.tabIndex = i === index ? 0 : -1;
            panels[i].hidden = i !== index;
        });
        root.dataset.feature = String(index + 1);
        if (focus) tabs[index].focus();
    }
    tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => select(index, false));
        tab.addEventListener('keydown', event => {
            let next;
            if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
            if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index + tabs.length - 1) % tabs.length;
            if (event.key === 'Home') next = 0;
            if (event.key === 'End') next = tabs.length - 1;
            if (next !== undefined) { event.preventDefault(); select(next, true); }
        });
    });
    root.classList.add('workspace-enhanced');
    select(0, false);

    function resetDepth() {
        scene.style.setProperty('--scene-x', '0deg');
        scene.style.setProperty('--scene-y', '0deg');
    }
    function renderMotion() {
        const stopped = paused || motion.matches;
        root.classList.toggle('workspace-paused', stopped);
        button.disabled = motion.matches;
        button.setAttribute('aria-pressed', String(stopped));
        const label = button.querySelector('span');
        label.dataset.i18n = motion.matches ? 'workspace.reduced' : paused ? 'workspace.resume' : 'workspace.pause';
        label.textContent = t(label.dataset.i18n);
        button.querySelector('i').className = stopped ? 'fa-solid fa-play' : 'fa-solid fa-pause';
        if (stopped) resetDepth();
    }
    button.addEventListener('click', () => { paused = !paused; renderMotion(); });
    motion.addEventListener('change', renderMotion);
    scene.addEventListener('pointermove', event => {
        if (paused || motion.matches || event.pointerType !== 'mouse') return;
        const rect = scene.getBoundingClientRect();
        scene.style.setProperty('--scene-y', ((event.clientX - rect.left) / rect.width - .5) * 10 + 'deg');
        scene.style.setProperty('--scene-x', -((event.clientY - rect.top) / rect.height - .5) * 6 + 'deg');
    });
    scene.addEventListener('pointerleave', resetDepth);
    new IntersectionObserver(entries => root.classList.toggle('workspace-offscreen', !entries[0].isIntersecting)).observe(scene);
    window.__rerender_workspace = function () {
        scene.setAttribute('aria-label', t('workspace.scene'));
        root.querySelector('[role="tablist"]').setAttribute('aria-label', t('workspace.features'));
        renderMotion();
    };
    window.__rerender_workspace();
})();
