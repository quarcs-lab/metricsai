/* metricsAI shared i18n runtime — defines:
 *   window.I18N                  — { strings: { "key": { en: "...", es: "..." }, ... } }
 *   window.I18N_REGISTER(table)  — called by every web-apps/_shared/strings/*.js to merge entries
 *   window.t(key, vars)          — returns the translated string for the active language;
 *                                  interpolates {name} placeholders if `vars` is given
 *   window.applyLanguage(lang)   — sets the active language, persists to localStorage,
 *                                  swaps every [data-i18n] element, refreshes the toggle
 *                                  label, and re-fires every window.__rerender_* function
 *                                  (so Plotly charts and dynamic callouts re-paint)
 *   window.toggleLanguage()      — cycles through I18N_CONFIG.languages
 *
 * Boot:
 *   - Reads localStorage["language"] synchronously so window.__lang is set BEFORE any
 *     widget IIFE runs and renders with the correct language on first paint.
 *   - On DOMContentLoaded, runs applyLanguage() to swap [data-i18n] elements and re-fire
 *     widget renderers (DOM must exist for both).
 */

(function () {
  if (!window.I18N_CONFIG) {
    console.error("[i18n-runtime] window.I18N_CONFIG is missing — load i18n-config.js first.");
    return;
  }

  window.I18N = { strings: {} };

  window.I18N_REGISTER = function (table) {
    for (const key in table) {
      window.I18N.strings[key] = table[key];
    }
  };

  window.t = function (key, vars) {
    const cfg = window.I18N_CONFIG;
    const lang = window.__lang || cfg.defaultLang;
    const entry = window.I18N.strings[key];
    let s;
    if (entry) {
      s = entry[lang];
      if (s === undefined) s = entry[cfg.defaultLang];
    }
    if (s === undefined) return key;
    if (vars) {
      for (const k in vars) s = s.split("{" + k + "}").join(String(vars[k]));
    }
    return s;
  };

  window.applyLanguage = function (lang) {
    const cfg = window.I18N_CONFIG;
    if (cfg.languages.indexOf(lang) === -1) lang = cfg.defaultLang;
    window.__lang = lang;
    try { localStorage.setItem(cfg.storageKey, lang); } catch (e) {}
    document.documentElement.lang = lang;
    const els = document.querySelectorAll("[data-i18n]");
    for (let i = 0; i < els.length; i++) {
      const key = els[i].getAttribute("data-i18n");
      els[i].innerHTML = window.t(key);
    }
    const lbl = document.getElementById("siteLanguageLabel");
    if (lbl) lbl.textContent = lang.toUpperCase();
    for (const k in window) {
      if (k.indexOf("__rerender_") === 0 && typeof window[k] === "function") {
        try { window[k](); } catch (e) {}
      }
    }
  };

  window.toggleLanguage = function () {
    const cfg = window.I18N_CONFIG;
    const cur = window.__lang || cfg.defaultLang;
    const i = cfg.languages.indexOf(cur);
    const next = cfg.languages[(i + 1) % cfg.languages.length];
    window.applyLanguage(next);
  };

  // Synchronous boot: set window.__lang before any chapter widget IIFE renders,
  // so first paint of dynamic content uses the persisted language.
  try {
    const stored = localStorage.getItem(window.I18N_CONFIG.storageKey);
    if (stored && window.I18N_CONFIG.languages.indexOf(stored) !== -1) {
      window.__lang = stored;
    }
  } catch (e) {}

  // After DOM is parsed, swap [data-i18n] elements and re-fire registered renderers.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      window.applyLanguage(window.__lang || window.I18N_CONFIG.defaultLang);
    });
  } else {
    window.applyLanguage(window.__lang || window.I18N_CONFIG.defaultLang);
  }
})();
