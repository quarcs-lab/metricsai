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
| About | Acerca de | — | Site nav |
| Notebooks | Cuadernos | — | Site nav (was "Python Notebooks") |
| Tutors | Tutores | — | Site nav (was "AI Tutors") |
| Web Apps | Aplicaciones Web | — | Site nav |
| Books | Libros | — | Site nav |
| Videos | Videos | — | Site nav |
| Podcasts | Podcasts | — | Site nav (loanword) |
| Authors | Autores | — | Site nav |
| More Resources | Más recursos | — | Site nav |
| Content based on | Contenido basado en | — | Cameron credit, navbar |
| Learn More | Saber más | — | Cameron credit CTA |

## 2. UI / chrome strings (cross-chapter)

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| Try this | Pruébalo | — | Callout heading |
| What you can do here | Qué puedes hacer aquí | — | Howto callout heading |
| Take-away: | Para recordar: | — | Lead-in to chapter takeaway |
| Read: | Lectura: | — | Lead-in to a "read" callout |
| Key insight | Idea clave | — | Callout label |
| Trade-off | Compromiso | — | |
| ↺ Reset | ↺ Reiniciar | — | Button |
| Show | Mostrar | — | Toggle label |
| On / Off | Activado / Desactivado | — | |
| Variable | Variable | — | |
| View | Vista | — | Toggle group label |
| Resimulate | Resimular | — | Button |
| Density | Densidad | — | Axis label |
| Dark | Oscuro | — | Theme toggle (now in navbar) |
| Light | Claro | — | Theme toggle (now in navbar) |
| Code Summary | Resumen de código | — | Section heading |
| Copy code | Copiar código | — | Button |
| Copied! | ¡Copiado! | — | Button confirmation state |
| Open empty Colab notebook | Abrir un cuaderno Colab vacío | — | Link |
| Paste into your Stata do-file editor | Pega esto en tu editor do-file de Stata | — | Code-tab note |
| Paste into your R console or RStudio | Pega esto en tu consola R o RStudio | — | Code-tab note |
| ↑ Back to top | ↑ Volver arriba | — | Footer |
| Chapter NN of 18 · Interactive Dashboard | Capítulo NN de 18 · Tablero interactivo | — | Header badge |

## 3. Chapter titles

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| Analysis of Economic Data | Análisis de datos económicos | — | ch01 |
| Univariate Data Summary | Resumen de datos univariados | — | ch02 |
| The Sample Mean | La media muestral | — | ch03 |
| Statistical Inference for the Mean | Inferencia estadística para la media | — | ch04 |
| Bivariate Data Summary | Resumen de datos bivariados | — | ch05 |
| The Least Squares Estimator | El estimador de mínimos cuadrados | — | ch06 |
| Statistical Inference for Bivariate Regression | Inferencia estadística para regresión bivariada | — | ch07 |
| Case Studies for Bivariate Regression | Estudios de caso para regresión bivariada | — | ch08 |
| Models with Natural Logarithms | Modelos con logaritmos naturales | — | ch09 |
| Data Summary for Multiple Regression | Resumen de datos para regresión múltiple | — | ch10 |
| Statistical Inference for Multiple Regression | Inferencia estadística para regresión múltiple | — | ch11 |
| Additional Topics in Multiple Regression | Temas adicionales en regresión múltiple | — | ch12 |
| Case Studies for Multiple Regression | Estudios de caso para regresión múltiple | — | ch13 |
| Regression with Indicator Variables | Regresión con variables indicadoras | — | ch14 |
| Regression with Transformed Variables | Regresión con variables transformadas | — | ch15 |
| Model and Data Verification | Verificación del modelo y los datos | — | ch16 |
| Panel Data, Time Series, and Causality | Datos de panel, series de tiempo y causalidad | — | ch17 |

## 4. Descriptive statistics

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| mean | media | — | |
| median | mediana | — | |
| standard deviation | desviación estándar | — | abbrev: DE |
| variance | varianza | — | |
| skewness | asimetría | — | |
| kurtosis | curtosis | — | |
| quartile / Q1 / Q3 | cuartil / Q1 / Q3 | — | |
| IQR | RIC | — | rango intercuartílico |
| min / max | mín / máx | — | |
| sample size (n) | tamaño de muestra (n) | — | |
| coefficient of variation (CV) | coeficiente de variación (CV) | — | abbrev kept |
| z-score | puntaje z | — | |
| trimmed mean | media recortada | — | |
| CAGR | TCAC | — | tasa de crecimiento anual compuesto |
| MSE | ECM | — | error cuadrático medio |
| RMSE | RECM | — | raíz del error cuadrático medio |
| sample | muestra | — | |
| distribution | distribución | — | |
| symmetric | simétrica | — | |
| approximately symmetric | aproximadamente simétrica | — | |
| moderately skewed | moderadamente sesgada | — | |
| highly skewed | altamente sesgada | — | |
| right-skewed | sesgada a la derecha | — | |

## 5. Regression & inference

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| regression | regresión | — | |
| linear regression | regresión lineal | — | |
| bivariate regression | regresión bivariada | — | |
| multiple regression | regresión múltiple | — | |
| OLS / ordinary least squares | MCO / mínimos cuadrados ordinarios | — | |
| 2SLS / two-stage least squares | MC2E / mínimos cuadrados en dos etapas | — | |
| BLUE | MELI | — | mejor estimador lineal insesgado |
| slope | pendiente | — | |
| intercept | intercepto | — | |
| residuals | residuos | — | |
| fitted values | valores ajustados | — | |
| prediction | predicción | — | |
| predictor / x-variable | predictor / variable predictora | — | |
| response / y-variable | variable de respuesta | — | |
| R-squared | R² | — | |
| adjusted R-squared | R² ajustado | — | |
| standard error | error estándar | — | abbrev: EE |
| t-statistic | estadístico t | — | |
| p-value | valor p | — | |
| F-statistic | estadístico F | — | |
| coefficient | coeficiente | — | |
| coefficient estimate | estimación del coeficiente | — | |
| explained variation (ESS) | variación explicada (SCE) | — | |
| residual variation (RSS) | variación residual (SCR) | — | |
| total variation (TSS) | variación total (SCT) | — | |
| sum of squared residuals | suma de cuadrados residuales | — | |
| association | asociación | — | |
| causation | causalidad | — | |
| omitted variables | variables omitidas | — | |
| omitted variable bias | sesgo por variables omitidas | — | abbrev: SVO |
| outliers | valores atípicos | — | |
| extrapolating / extrapolation | extrapolando / extrapolación | — | |
| marginal effect | efecto marginal | — | abbrev: EM |
| partial effect | efecto parcial | — | |
| ceteris paribus | ceteris paribus | — | Latin loanword, kept |
| controlling for | controlando por | — | |
| holding constant | manteniendo constante | — | |
| unbiased | insesgado | — | |
| efficient | eficiente | — | |
| Gauss-Markov | Gauss-Markov | — | proper noun, kept |
| confidence interval | intervalo de confianza | — | abbrev: IC |
| prediction interval | intervalo de predicción | — | abbrev: IP |
| hypothesis test | prueba de hipótesis | — | |
| null hypothesis | hipótesis nula | — | |
| alternative hypothesis | hipótesis alternativa | — | |
| significance level | nivel de significancia | — | |
| critical value | valor crítico | — | abbrev: t-crít |
| margin of error | margen de error | — | |
| two-tailed test | prueba de dos colas | — | |
| one-tailed test | prueba de una cola | — | |
| reject | rechazar | — | |
| fail to reject | no rechazar | — | |
| sampling distribution | distribución muestral | — | |
| central limit theorem | teorema del límite central | — | |
| degrees of freedom | grados de libertad | — | abbrev: gl |
| tail area | área de cola | — | |
| rejection region | región de rechazo | — | |
| sample proportion (p̂) | proporción muestral (p̂) | — | |

## 6. Heteroscedasticity, robustness, time-series

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| heteroscedasticity / heteroskedasticity | heterocedasticidad | — | NOT "heteroscedasticidad" with s; modern Spanish drops the s |
| heteroscedastic / heteroskedastic | heterocedástico | — | |
| homoscedasticity / homoskedasticity | homocedasticidad | — | |
| homoscedastic / homoskedastic | homocedástico | — | |
| robust standard error (HC1) | error estándar robusto (HC1) | — | abbrev: EE robusto HC1 |
| HAC standard error | error estándar HAC | — | "Newey-West" kept as proper noun |
| autocorrelation | autocorrelación | — | |
| autocorrelation function | función de autocorrelación | — | abbrev: FAC (NOT ACF) |
| serial correlation | correlación serial | — | |
| moving average | media móvil | — | |

## 7. Multivariate / regression diagnostics

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| multicollinearity | multicolinealidad | — | |
| variance inflation factor (VIF) | factor de inflación de la varianza (FIV) | — | |
| correlation matrix | matriz de correlación | — | |
| pairwise correlation | correlación por pares | — | |
| scatter plot matrix | matriz de diagramas de dispersión | — | |
| Cook's distance | distancia de Cook | — | |
| DFFITS / DFBETAS | DFFITS / DFBETAS | — | proper-noun acronyms, kept |
| standardized residuals | residuos estandarizados | — | |
| studentized residuals | residuos estudentizados | — | |
| Q-Q plot / normal Q-Q plot | gráfico Q-Q / gráfico Q-Q normal | — | |
| residual plot | gráfico de residuos | — | |
| Breusch-Pagan test | prueba de Breusch-Pagan | — | proper-noun, kept |
| White test | prueba de White | — | |
| Durbin-Watson test | prueba de Durbin-Watson | — | |
| model misspecification | especificación incorrecta del modelo | — | |
| functional form | forma funcional | — | |

## 8. Models with logs, transformations, interactions

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| natural logarithm (ln) | logaritmo natural (ln) | — | |
| log transformation | transformación logarítmica | — | |
| log scale | escala log | — | |
| log-transformed | transformada con log | — | |
| log-log model | modelo log-log | — | |
| log-linear model | modelo log-lineal | — | |
| linear-log model | modelo lineal-log | — | |
| level-level model | modelo nivel-nivel | — | |
| elasticity | elasticidad | — | |
| semi-elasticity | semielasticidad | — | |
| percent change | cambio porcentual | — | |
| approximate | aproximado | — | |
| quadratic term | término cuadrático | — | |
| polynomial | polinomio | — | |
| turning point | punto de inflexión | — | |
| nonlinear effect | efecto no lineal | — | |
| interaction term | término de interacción | — | |
| interaction effect | efecto de interacción | — | |
| smearing factor | factor de smearing | — | "smearing" kept (no canonical Spanish term) |
| naive prediction | predicción ingenua | — | |
| retransformation bias | sesgo de retransformación | — | |
| standardized coefficients | coeficientes estandarizados | — | |

## 9. Indicator / categorical variables

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| indicator variable | variable indicadora | — | |
| dummy variable | variable ficticia (dummy) | — | |
| binary variable | variable binaria | — | |
| categorical variable | variable categórica | — | |
| base / reference category | categoría base / categoría de referencia | — | |
| slope dummy | dummy de pendiente | — | |
| intercept dummy | dummy de intercepto | — | |
| group mean | media del grupo | — | |
| ANOVA | ANOVA | — | análisis de varianza |
| F-test | prueba F | — | |
| joint test / joint significance | prueba conjunta / significancia conjunta | — | |
| restricted / unrestricted model | modelo restringido / no restringido | — | |

## 10. Panel data, causal inference, IV

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| panel data | datos de panel | — | |
| time series | serie de tiempo | — | |
| cross-sectional data | datos de corte transversal | — | |
| longitudinal data | datos longitudinales | — | |
| pooled OLS | MCO agrupada | — | |
| fixed effects | efectos fijos | — | |
| random effects | efectos aleatorios | — | |
| individual effect | efecto individual | — | |
| time effect | efecto temporal | — | |
| within estimator | estimador intra-grupos (within) | — | |
| between estimator | estimador entre-grupos (between) | — | |
| first difference | primera diferencia | — | |
| differences-in-differences (DiD) | diferencias en diferencias (DiD) | — | |
| treatment / control group | grupo de tratamiento / grupo de control | — | |
| pre-treatment / post-treatment | pre-tratamiento / post-tratamiento | — | |
| counterfactual | contrafactual | — | |
| causal inference | inferencia causal | — | |
| causal effect | efecto causal | — | |
| natural experiment | experimento natural | — | |
| randomized experiment | experimento aleatorizado | — | |
| RCT (randomized controlled trial) | ECA (ensayo controlado aleatorizado) | — | |
| instrumental variable (IV) | variable instrumental (VI) | — | NOT "IV" in Spanish text — use VI |
| endogeneity / exogeneity | endogeneidad / exogeneidad | — | |
| trend | tendencia | — | |
| seasonality | estacionalidad | — | |
| stationary | estacionario | — | |
| lag | rezago | — | |

## 11. Charting / visualization

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| scatter plot | diagrama de dispersión | — | |
| box plot | diagrama de caja | — | |
| histogram | histograma | — | |
| bin / bin width | bin / ancho del bin | — | "bin" kept (technical loanword) |
| KDE / kernel density estimate | KDE / estimación de densidad kernel | — | |
| Gaussian kernel | núcleo Gaussiano | — | |
| whiskers | bigotes | — | |
| LOWESS bandwidth | ancho de banda LOWESS | — | |
| kernel smoothing | suavizado por núcleo | — | |
| seasonally adjusted | ajustada estacionalmente | — | |
| recession shading | sombreado de recesiones | — | |
| SE bands | bandas EE | — | |

## 12. Correlation

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| correlation | correlación | — | |
| correlation coefficient | coeficiente de correlación | — | |
| covariance | covarianza | — | |
| positive / negative correlation | correlación positiva / negativa | — | |
| linear / nonlinear relationship | relación lineal / no lineal | — | |

## 13. House-data variables (used in ch01, ch07, ch10, ch11)

| EN | ES | JA | Notes |
| --- | --- | --- | --- |
| Sale price ($) | Precio de venta ($) | — | |
| Size (sq ft) | Tamaño (pies²) | — | "pies²" preferred over "ft²" |
| House size (sq ft) | Tamaño de la casa (pies²) | — | |
| Bedrooms | Dormitorios | — | |
| Bathrooms | Baños | — | |
| Lot size | Tamaño del lote | — | |
| Age (years) | Antigüedad (años) | — | |
| Month sold | Mes de venta | — | |
