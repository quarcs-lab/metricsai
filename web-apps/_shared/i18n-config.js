/* metricsAI shared i18n config — single source of truth for the language list.
 * Add a new language by:
 *   1. Pushing its code onto `languages` (e.g. "ja").
 *   2. Adding its `<lang>: "..."` field to every entry in web-apps/_shared/strings/*.js.
 *   3. Running `python3 scripts/i18n_check.py` to verify parity.
 * No HTML or runtime code needs to change.
 */
window.I18N_CONFIG = {
  languages:   ["en", "es"],
  defaultLang: "en",
  storageKey:  "language"
};
