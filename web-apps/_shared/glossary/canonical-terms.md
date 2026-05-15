# Canonical translation glossary — metricsAI

Authoritative `EN → ES` (and later `EN → JA`) for terms that appear in chapter web apps and the project website. Subagents producing translations MUST use these exact equivalents — do not invent alternatives.

When a term is missing, add a row to this file before translating, and note the rationale. Cross-chapter consistency is enforced by treating this file as the single source of truth.

## How to use this file

- **For translators (humans or LLM subagents):** look up every term in your source string here first. If it's listed, use the exact ES (and later JA) equivalent. Do not paraphrase.
- **When extending to a new language:** add a column for the new language code (`JA`, `FR`, `DE`, …) and fill in every row before producing translations. Then run `python3 scripts/i18n_check.py` to catch any string-file entries still missing the new language.
- **When discovering a term not yet listed:** add the row, document the choice in `Notes`, then translate.

---

## 1. Site chrome (navbar + UI shared across all 19 pages)

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| About | Acerca de | 概要 | Site nav |
| Notebooks | Cuadernos | ノートブック | Site nav (was "Python Notebooks") |
| Tutors | Tutores | チューター | Site nav (was "AI Tutors") |
| Web Apps | Aplicaciones Web | ウェブアプリ | Site nav |
| Books | Libros | 書籍 | Site nav |
| Videos | Videos | 動画 | Site nav |
| Podcasts | Podcasts | ポッドキャスト | Site nav (loanword) |
| Authors | Autores | 著者 | Site nav |
| More Resources | Más recursos | その他のリソース | Site nav |
| Content based on | Contenido basado en | コンテンツの基礎： | Cameron credit, navbar |
| Learn More | Saber más | 詳細を見る | Cameron credit CTA |

## 2. UI / chrome strings (cross-chapter)

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| Try this | Pruébalo | 試してみよう | Callout heading |
| What you can do here | Qué puedes hacer aquí | ここでできること | Howto callout heading |
| Take-away: | Para recordar: | ポイント： | Lead-in to chapter takeaway |
| Read: | Lectura: | 読み物： | Lead-in to a "read" callout |
| Key insight | Idea clave | 重要なポイント | Callout label |
| Trade-off | Compromiso | トレードオフ | |
| ↺ Reset | ↺ Reiniciar | ↺ リセット | Button |
| Show | Mostrar | 表示 | Toggle label |
| On / Off | Activado / Desactivado | オン / オフ | |
| Variable | Variable | 変数 | |
| View | Vista | 表示 | Toggle group label |
| Resimulate | Resimular | 再シミュレーション | Button |
| Density | Densidad | 密度 | Axis label |
| Dark | Oscuro | ダーク | Theme toggle (now in navbar) |
| Light | Claro | ライト | Theme toggle (now in navbar) |
| Code Summary | Resumen de código | コード要約 | Section heading |
| Copy code | Copiar código | コードをコピー | Button |
| Copied! | ¡Copiado! | コピーしました！ | Button confirmation state |
| Open empty Colab notebook | Abrir un cuaderno Colab vacío | 空のColabノートブックを開く | Link |
| Paste into your Stata do-file editor | Pega esto en tu editor do-file de Stata | Stataのdoファイルエディタに貼り付けてください | Code-tab note |
| Paste into your R console or RStudio | Pega esto en tu consola R o RStudio | RコンソールまたはRStudioに貼り付けてください | Code-tab note |
| ↑ Back to top | ↑ Volver arriba | ↑ トップへ戻る | Footer |
| Chapter NN of 18 · Interactive Dashboard | Capítulo NN de 18 · Tablero interactivo | 第NN章 / 全18章 · インタラクティブ・ダッシュボード | Header badge |

## 3. Chapter titles

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| Analysis of Economic Data | Análisis de datos económicos | 経済データの分析 | ch01 |
| Univariate Data Summary | Resumen de datos univariados | 一変量データの要約 | ch02 |
| The Sample Mean | La media muestral | 標本平均 | ch03 |
| Statistical Inference for the Mean | Inferencia estadística para la media | 平均に関する統計的推測 | ch04 |
| Bivariate Data Summary | Resumen de datos bivariados | 二変量データの要約 | ch05 |
| The Least Squares Estimator | El estimador de mínimos cuadrados | 最小二乗推定量 | ch06 |
| Statistical Inference for Bivariate Regression | Inferencia estadística para regresión bivariada | 二変量回帰の統計的推測 | ch07 |
| Case Studies for Bivariate Regression | Estudios de caso para regresión bivariada | 二変量回帰のケーススタディ | ch08 |
| Models with Natural Logarithms | Modelos con logaritmos naturales | 自然対数を用いたモデル | ch09 |
| Data Summary for Multiple Regression | Resumen de datos para regresión múltiple | 重回帰のためのデータ要約 | ch10 |
| Statistical Inference for Multiple Regression | Inferencia estadística para regresión múltiple | 重回帰の統計的推測 | ch11 |
| Additional Topics in Multiple Regression | Temas adicionales en regresión múltiple | 重回帰の追加トピック | ch12 |
| Case Studies for Multiple Regression | Estudios de caso para regresión múltiple | 重回帰のケーススタディ | ch13 |
| Regression with Indicator Variables | Regresión con variables indicadoras | ダミー変数を用いた回帰 | ch14 |
| Regression with Transformed Variables | Regresión con variables transformadas | 変数変換を用いた回帰 | ch15 |
| Model and Data Verification | Verificación del modelo y los datos | モデルとデータの検証 | ch16 |
| Panel Data, Time Series, and Causality | Datos de panel, series de tiempo y causalidad | パネルデータ、時系列、因果性 | ch17 |

## 4. Descriptive statistics

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| mean | media | 平均 | |
| median | mediana | 中央値 | |
| standard deviation | desviación estándar | 標準偏差 | abbrev: DE |
| variance | varianza | 分散 | |
| skewness | asimetría | 歪度 | |
| kurtosis | curtosis | 尖度 | |
| quartile / Q1 / Q3 | cuartil / Q1 / Q3 | 四分位数 / Q1 / Q3 | |
| IQR | RIC | IQR（四分位範囲） | rango intercuartílico |
| min / max | mín / máx | 最小値 / 最大値 | |
| sample size (n) | tamaño de muestra (n) | 標本サイズ (n) | |
| coefficient of variation (CV) | coeficiente de variación (CV) | 変動係数 (CV) | abbrev kept |
| z-score | puntaje z | z値 | |
| trimmed mean | media recortada | トリム平均 | |
| CAGR | TCAC | CAGR（年平均成長率） | tasa de crecimiento anual compuesto |
| MSE | ECM | MSE（平均二乗誤差） | error cuadrático medio |
| RMSE | RECM | RMSE（平均二乗誤差平方根） | raíz del error cuadrático medio |
| sample | muestra | 標本 | |
| distribution | distribución | 分布 | |
| symmetric | simétrica | 対称的 | |
| approximately symmetric | aproximadamente simétrica | ほぼ対称的 | |
| moderately skewed | moderadamente sesgada | 中程度に歪んでいる | |
| highly skewed | altamente sesgada | 強く歪んでいる | |
| right-skewed | sesgada a la derecha | 右に歪んでいる | |

## 5. Regression & inference

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| regression | regresión | 回帰 | |
| linear regression | regresión lineal | 線形回帰 | |
| bivariate regression | regresión bivariada | 二変量回帰 | |
| multiple regression | regresión múltiple | 重回帰 | |
| OLS / ordinary least squares | MCO / mínimos cuadrados ordinarios | OLS（最小二乗法） | |
| 2SLS / two-stage least squares | MC2E / mínimos cuadrados en dos etapas | 2SLS（二段階最小二乗法） | |
| BLUE | MELI | BLUE（最良線形不偏推定量） | mejor estimador lineal insesgado |
| slope | pendiente | 傾き | |
| intercept | intercepto | 切片 | |
| residuals | residuos | 残差 | |
| fitted values | valores ajustados | 当てはめ値 | |
| prediction | predicción | 予測 | |
| predictor / x-variable | predictor / variable predictora | 説明変数 / x変数 | |
| response / y-variable | variable de respuesta | 被説明変数 / y変数 | |
| R-squared | R² | R² | |
| adjusted R-squared | R² ajustado | 自由度調整済みR² | |
| standard error | error estándar | 標準誤差 | abbrev: EE |
| t-statistic | estadístico t | t統計量 | |
| p-value | valor p | p値 | |
| F-statistic | estadístico F | F統計量 | |
| coefficient | coeficiente | 係数 | |
| coefficient estimate | estimación del coeficiente | 係数推定値 | |
| explained variation (ESS) | variación explicada (SCE) | 説明された変動 (ESS) | |
| residual variation (RSS) | variación residual (SCR) | 残差変動 (RSS) | |
| total variation (TSS) | variación total (SCT) | 全変動 (TSS) | |
| sum of squared residuals | suma de cuadrados residuales | 残差平方和 | |
| association | asociación | 関連 | |
| causation | causalidad | 因果関係 | |
| omitted variables | variables omitidas | 欠落変数 | |
| omitted variable bias | sesgo por variables omitidas | 欠落変数バイアス | abbrev: SVO |
| outliers | valores atípicos | 外れ値 | |
| extrapolating / extrapolation | extrapolando / extrapolación | 外挿 | |
| marginal effect | efecto marginal | 限界効果 | abbrev: EM |
| partial effect | efecto parcial | 偏効果 | |
| ceteris paribus | ceteris paribus | ceteris paribus（他の条件を一定として） | Latin loanword, kept |
| controlling for | controlando por | 〜をコントロールして | |
| holding constant | manteniendo constante | 〜を一定に保って | |
| unbiased | insesgado | 不偏 | |
| efficient | eficiente | 有効 | |
| Gauss-Markov | Gauss-Markov | Gauss-Markov | proper noun, kept |
| confidence interval | intervalo de confianza | 信頼区間 | abbrev: IC |
| prediction interval | intervalo de predicción | 予測区間 | abbrev: IP |
| hypothesis test | prueba de hipótesis | 仮説検定 | |
| null hypothesis | hipótesis nula | 帰無仮説 | |
| alternative hypothesis | hipótesis alternativa | 対立仮説 | |
| significance level | nivel de significancia | 有意水準 | |
| critical value | valor crítico | 臨界値 | abbrev: t-crít |
| margin of error | margen de error | 誤差の幅 | |
| two-tailed test | prueba de dos colas | 両側検定 | |
| one-tailed test | prueba de una cola | 片側検定 | |
| reject | rechazar | 棄却する | |
| fail to reject | no rechazar | 棄却しない | |
| sampling distribution | distribución muestral | 標本分布 | |
| central limit theorem | teorema del límite central | 中心極限定理 | |
| degrees of freedom | grados de libertad | 自由度 | abbrev: gl |
| tail area | área de cola | 裾の面積 | |
| rejection region | región de rechazo | 棄却域 | |
| sample proportion (p̂) | proporción muestral (p̂) | 標本比率 (p̂) | |

## 6. Heteroscedasticity, robustness, time-series

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| heteroscedasticity / heteroskedasticity | heterocedasticidad | 不均一分散 | NOT "heteroscedasticidad" with s; modern Spanish drops the s |
| heteroscedastic / heteroskedastic | heterocedástico | 不均一分散の | |
| homoscedasticity / homoskedasticity | homocedasticidad | 均一分散 | |
| homoscedastic / homoskedastic | homocedástico | 均一分散の | |
| robust standard error (HC1) | error estándar robusto (HC1) | ロバスト標準誤差 (HC1) | abbrev: EE robusto HC1 |
| HAC standard error | error estándar HAC | HAC標準誤差 | "Newey-West" kept as proper noun |
| autocorrelation | autocorrelación | 自己相関 | |
| autocorrelation function | función de autocorrelación | 自己相関関数（ACF） | abbrev: FAC (NOT ACF) |
| serial correlation | correlación serial | 系列相関 | |
| moving average | media móvil | 移動平均 | |

## 7. Multivariate / regression diagnostics

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| multicollinearity | multicolinealidad | 多重共線性 | |
| variance inflation factor (VIF) | factor de inflación de la varianza (FIV) | 分散拡大要因 (VIF) | |
| correlation matrix | matriz de correlación | 相関行列 | |
| pairwise correlation | correlación por pares | ペアワイズ相関 | |
| scatter plot matrix | matriz de diagramas de dispersión | 散布図行列 | |
| Cook's distance | distancia de Cook | Cook距離 | |
| DFFITS / DFBETAS | DFFITS / DFBETAS | DFFITS / DFBETAS | proper-noun acronyms, kept |
| standardized residuals | residuos estandarizados | 標準化残差 | |
| studentized residuals | residuos estudentizados | スチューデント化残差 | |
| Q-Q plot / normal Q-Q plot | gráfico Q-Q / gráfico Q-Q normal | Q-Qプロット / 正規Q-Qプロット | |
| residual plot | gráfico de residuos | 残差プロット | |
| Breusch-Pagan test | prueba de Breusch-Pagan | Breusch-Pagan検定 | proper-noun, kept |
| White test | prueba de White | White検定 | |
| Durbin-Watson test | prueba de Durbin-Watson | Durbin-Watson検定 | |
| model misspecification | especificación incorrecta del modelo | モデルの定式化の誤り | |
| functional form | forma funcional | 関数形 | |

## 8. Models with logs, transformations, interactions

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| natural logarithm (ln) | logaritmo natural (ln) | 自然対数 (ln) | |
| log transformation | transformación logarítmica | 対数変換 | |
| log scale | escala log | 対数スケール | |
| log-transformed | transformada con log | 対数変換された | |
| log-log model | modelo log-log | log-logモデル | |
| log-linear model | modelo log-lineal | log-linearモデル | |
| linear-log model | modelo lineal-log | linear-logモデル | |
| level-level model | modelo nivel-nivel | level-levelモデル | |
| elasticity | elasticidad | 弾力性 | |
| semi-elasticity | semielasticidad | 準弾力性 | |
| percent change | cambio porcentual | 変化率 | |
| approximate | aproximado | 近似 | |
| quadratic term | término cuadrático | 二乗項 | |
| polynomial | polinomio | 多項式 | |
| turning point | punto de inflexión | 転換点 | |
| nonlinear effect | efecto no lineal | 非線形効果 | |
| interaction term | término de interacción | 交互作用項 | |
| interaction effect | efecto de interacción | 交互作用効果 | |
| smearing factor | factor de smearing | smearing係数 | "smearing" kept (no canonical Spanish term); (jp: TBD) |
| naive prediction | predicción ingenua | 単純予測 | |
| retransformation bias | sesgo de retransformación | 逆変換バイアス | |
| standardized coefficients | coeficientes estandarizados | 標準化係数 | |

## 9. Indicator / categorical variables

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| indicator variable | variable indicadora | 指示変数 | |
| dummy variable | variable ficticia (dummy) | ダミー変数 | |
| binary variable | variable binaria | 二値変数 | |
| categorical variable | variable categórica | カテゴリ変数 | |
| base / reference category | categoría base / categoría de referencia | 基準カテゴリ / 参照カテゴリ | |
| slope dummy | dummy de pendiente | 傾きダミー | |
| intercept dummy | dummy de intercepto | 切片ダミー | |
| group mean | media del grupo | グループ平均 | |
| ANOVA | ANOVA | ANOVA（分散分析） | análisis de varianza |
| F-test | prueba F | F検定 | |
| joint test / joint significance | prueba conjunta / significancia conjunta | 同時検定 / 同時有意性 | |
| restricted / unrestricted model | modelo restringido / no restringido | 制約付きモデル / 制約なしモデル | |

## 10. Panel data, causal inference, IV

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| panel data | datos de panel | パネルデータ | |
| time series | serie de tiempo | 時系列 | |
| cross-sectional data | datos de corte transversal | 横断面データ | |
| longitudinal data | datos longitudinales | 縦断データ | |
| pooled OLS | MCO agrupada | プールドOLS | |
| fixed effects | efectos fijos | 固定効果 | |
| random effects | efectos aleatorios | 変量効果 | |
| individual effect | efecto individual | 個別効果 | |
| time effect | efecto temporal | 時間効果 | |
| within estimator | estimador intra-grupos (within) | グループ内推定量（within） | |
| between estimator | estimador entre-grupos (between) | グループ間推定量（between） | |
| first difference | primera diferencia | 一階差分 | |
| differences-in-differences (DiD) | diferencias en diferencias (DiD) | 差の差分法（DiD） | |
| treatment / control group | grupo de tratamiento / grupo de control | 処置群 / 対照群 | |
| pre-treatment / post-treatment | pre-tratamiento / post-tratamiento | 処置前 / 処置後 | |
| counterfactual | contrafactual | 反実仮想 | |
| causal inference | inferencia causal | 因果推論 | |
| causal effect | efecto causal | 因果効果 | |
| natural experiment | experimento natural | 自然実験 | |
| randomized experiment | experimento aleatorizado | 無作為化実験 | |
| RCT (randomized controlled trial) | ECA (ensayo controlado aleatorizado) | RCT（ランダム化比較試験） | |
| instrumental variable (IV) | variable instrumental (VI) | 操作変数（IV） | NOT "IV" in Spanish text — use VI |
| endogeneity / exogeneity | endogeneidad / exogeneidad | 内生性 / 外生性 | |
| trend | tendencia | トレンド | |
| seasonality | estacionalidad | 季節性 | |
| stationary | estacionario | 定常的 | |
| lag | rezago | ラグ | |

## 11. Charting / visualization

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| scatter plot | diagrama de dispersión | 散布図 | |
| box plot | diagrama de caja | 箱ひげ図 | |
| histogram | histograma | ヒストグラム | |
| bin / bin width | bin / ancho del bin | ビン / ビン幅 | "bin" kept (technical loanword) |
| KDE / kernel density estimate | KDE / estimación de densidad kernel | KDE（カーネル密度推定） | |
| Gaussian kernel | núcleo Gaussiano | ガウシアンカーネル | |
| whiskers | bigotes | ひげ | |
| LOWESS bandwidth | ancho de banda LOWESS | LOWESSバンド幅 | |
| kernel smoothing | suavizado por núcleo | カーネル平滑化 | |
| seasonally adjusted | ajustada estacionalmente | 季節調整済み | |
| recession shading | sombreado de recesiones | リセッション陰影 | |
| SE bands | bandas EE | SEバンド | |

## 12. Correlation

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| correlation | correlación | 相関 | |
| correlation coefficient | coeficiente de correlación | 相関係数 | |
| covariance | covarianza | 共分散 | |
| positive / negative correlation | correlación positiva / negativa | 正の相関 / 負の相関 | |
| linear / nonlinear relationship | relación lineal / no lineal | 線形関係 / 非線形関係 | |

## 13. House-data variables (used in ch01, ch07, ch10, ch11)

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| Sale price ($) | Precio de venta ($) | 販売価格 ($) | |
| Size (sq ft) | Tamaño (pies²) | 面積（平方フィート） | "pies²" preferred over "ft²" |
| House size (sq ft) | Tamaño de la casa (pies²) | 住宅面積（平方フィート） | |
| Bedrooms | Dormitorios | 寝室数 | |
| Bathrooms | Baños | 浴室数 | |
| Lot size | Tamaño del lote | 敷地面積 | |
| Age (years) | Antigüedad (años) | 築年数（年） | |
| Month sold | Mes de venta | 販売月 | |

---

## 13. Phase-2 additions (promoted from ch01 pilot, 2026-05-15)

Vocabulary that surfaced during the ch01 JA pilot translation and was not yet in the canonical tables. Subagents working on chXX.js should use these forms; promote to a topical table later if it grows large.

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| confounder / confounding variable | variable de confusión | 交絡因子 | Recurs in ch01, ch07, ch08, ch10–ch17 (causal-inference framing). |
| to confound | confundir | 交絡させる | Verb form. Use です/ます when conjugating in prose. |
| proxy variable | variable proxy | 代理変数 | ch01, ch10, ch12. |
| school district | distrito escolar | 学区 | House-data context (Davis CA). |
| baseline (regression) | regresión base / referencia | 基準となる回帰 | UI label for control regressions. |
| baseline (general) | base / referencia | 基準 | Short UI label. |
| to extrapolate (verbal) | extrapolar | 外挿する | Glossary already has noun 外挿; this is the conjugating form (use 外挿になっています / 外挿します as needed). |
| boundary line | línea de frontera | 境界線 | Chart-control wording. |
| dashed boundary | frontera discontinua | 破線 | Plotly trace style. |
| eyeball line / eyeballed fit | línea a ojo | 目で見て引く線 | Pedagogical voice — "draw your own line". |
| tight sample | muestra apretada | 密な標本 | ch01, ch02, ch04, ch05. |
| dispersed sample | muestra dispersa | 散らばった標本 | Counterpart to "tight sample". |
| what-if (slope, fit) | hipotético (pendiente, ajuste) | 仮定の（傾き、当てはめ） | UI label across many widgets. |
| distance from mean | distancia respecto a la media | 平均からの距離 | R²/ANOVA framings. |
| right-skewed tail | cola sesgada a la derecha | 右に歪んだ裾 | Glossary has the verbal "highly skewed"; this is the noun-tail form. |
