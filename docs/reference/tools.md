# Research tools / Исследовательские инструменты

This catalog lists all **147** tools registered by the published Research r152 package. Each name links to its registration in the exact published source commit. Purposes summarize the registered schema and its required inputs; a registered tool is a contract, not proof that a provider, workflow, research result or depth profile is qualified.

Каталог содержит все **147** инструментов опубликованного пакета Research r152. Название ведёт к регистрации в точном опубликованном коммите. Назначение кратко передаёт схему и обязательные входы; наличие инструмента не подтверждает квалификацию поставщика, процесса, научного результата или профиля глубины.

Source / Источник: [`plugin.py`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py), [`plugin.yaml`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.yaml); commit `9077d24d5e7b6dda5db7902bac2a927503791db6`; Research archive SHA-256 `22656292a9a8987afcd0fbf085e525814a6477f9b4a29fa21055b578da3677cb`. The local installed `plugin.py` and `plugin.yaml` were checked byte-for-byte against that archive.

## Planning and execution / Планирование и исполнение

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_compare_periods`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1453) | Compare numeric observations across two periods without causal inference. | Сравнить числовые наблюдения двух периодов без вывода о причинности. |
| [`research_build_report`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1460) | Build a provisional report from supplied sources and claims. | Собрать предварительный отчёт из переданных источников и тезисов. |
| [`research_contract_create`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1467) | Create a versioned research run contract from a draft and policy. | Создать версионированный контракт исследования из черновика и правил. |
| [`research_contract_propose_revision`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1474) | Assess a proposed run-contract revision and its dependencies. | Проверить предлагаемую редакцию контракта и зависимости. |
| [`research_budget_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1481) | Assess available units against the run contract and budget policy. | Сверить доступные единицы с контрактом и бюджетными правилами. |
| [`research_beta_mode_plan_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1488) | Build a bounded, mode-specific beta execution plan. | Построить ограниченный план испытательного режима. |
| [`research_plan_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1495) | Build an ordered plan from a run reference and work packets. | Построить порядок работы из ссылки на запуск и пакетов. |
| [`research_work_execution_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1502) | Assess a typed work-execution control payload. | Проверить типизированный контроль исполнения работы. |
| [`research_route_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1509) | Assess a capability route for a specified project, run and packet. | Проверить маршрут возможности для проекта, запуска и пакета. |

## Search, coverage and source acquisition / Поиск, охват и получение источников

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_search_ledger_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1516) | Assess search ledger entries against coverage cells. | Сверить записи поиска с ячейками охвата. |
| [`research_search_execution_trace_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1523) | Compare planned search dispatch with observed external calls. | Сверить запланированный поиск с фактическими внешними вызовами. |
| [`research_search_coverage_details_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1530) | Assess language cells, sources and coverage metrics. | Проверить языковые ячейки, источники и показатели охвата. |
| [`research_coverage_status_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1537) | Assess a versioned coverage frame and denominator. | Проверить версию рамки охвата и знаменатель. |
| [`research_corpus_materialize`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1544) | Materialize a corpus record from a frame and source receipts. | Сформировать запись корпуса из рамки и квитанций источников. |
| [`research_acquisition_integrity_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1551) | Assess source acquisition and original-asset integrity. | Проверить получение источника и целостность оригинала. |
| [`research_source_select`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1558) | Assess one candidate source against a requirement and quality data. | Оценить источник-кандидат по требованию и показателям качества. |
| [`research_fragment_verify`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1565) | Verify a source fragment with an independent locator readback. | Сверить фрагмент источника с независимым чтением по адресу. |
| [`research_claim_evaluate`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1572) | Evaluate a claim and its links to known evidence fragments. | Оценить тезис и связи с известными фрагментами доказательств. |
| [`research_claim_verification_graph_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1579) | Assess claim dependencies and invalidation after reference changes. | Проверить зависимости тезисов и утрату силы при изменении ссылок. |
| [`research_numeric_reproduction_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1586) | Assess a calculation supporting a numeric claim. | Проверить расчёт, поддерживающий числовой тезис. |
| [`research_challenge_evaluate`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1593) | Assess a challenge to a claim under an evidence profile. | Оценить оспаривание тезиса с учётом доказательной области. |
| [`research_synthesis_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1600) | Assess synthesis of claims and challenge records. | Проверить синтез тезисов и записей оспаривания. |
| [`research_evidence_standard_create`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1607) | Create a versioned standard for claim evidence. | Создать версионированный стандарт доказательств для тезисов. |
| [`research_evidence_standard_propose_revision`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1614) | Assess a proposed revision of an evidence standard. | Проверить предлагаемую редакцию доказательного стандарта. |
| [`research_evidence_exception_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1621) | Assess an exception when required evidence is unavailable. | Оценить исключение при недоступном обязательном доказательстве. |
| [`research_claim_card_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1628) | Assess a structured claim card and its subject type. | Проверить карточку тезиса и тип предмета утверждения. |
| [`research_negative_knowledge_classify`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1635) | Classify a negative search result without equating absence with evidence. | Классифицировать отрицательный поиск без подмены отсутствия доказательством. |
| [`research_search_coverage_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1642) | Assess search waves, cells and retained entries. | Проверить волны поиска, ячейки и сохранённые записи. |
| [`research_source_pool_audit`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1649) | Audit candidate-source density and replacement families. | Проверить плотность пула источников и заменяющие семейства. |

## Architecture, quality and decisions / Архитектура, качество и решения

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_udr_architecture_select`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1656) | Select a research architecture from scope, corpus scale and risk. | Выбрать архитектуру исследования по области, масштабу корпуса и риску. |
| [`research_udr_plan_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1663) | Assess packets, loops and gates in an architecture plan. | Проверить пакеты, циклы и шлюзы архитектурного плана. |
| [`research_quality_dashboard_project`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1670) | Project quality indicators from registries without manual override. | Построить показатели качества из реестров без ручной подмены. |
| [`research_decision_envelope_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1677) | Assess the strength and bounds of a recommendation. | Проверить силу и границы рекомендации. |
| [`research_delta_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1684) | Assess material change between baseline and current revision. | Оценить существенное изменение между базовой и текущей редакцией. |
| [`research_incident_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1691) | Assess an incident against dated sources and claims. | Оценить инцидент по датированным источникам и тезисам. |
| [`research_independent_support_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1698) | Assess whether claimed support comes from independent origins. | Проверить независимость происхождения опоры тезиса. |
| [`research_engagement_level_select`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1705) | Select research depth from supplied material and synthesis need. | Выбрать уровень исследования по материалам и потребности в синтезе. |
| [`research_engagement_level_propose_revision`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1712) | Assess a proposed change to an engagement level. | Проверить изменение уровня исследования. |

## Documents and representations / Документы и представления

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_parsing_result_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1719) | Assess a parse result against original and parsed content hashes. | Сверить результат разбора с хешами оригинала и производного текста. |
| [`research_parse_intake_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1726) | Assess document intake metadata and file type declarations. | Проверить сведения приёма документа и заявленный тип файла. |
| [`research_parse_runs_record`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1733) | Record parser runs bound to one original artifact. | Зарегистрировать запуски разбора для одного оригинала. |
| [`research_unicode_representations_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1740) | Build exact and display text representations with confusable checks. | Построить точное и отображаемое представления текста с проверкой похожих знаков. |
| [`research_document_graph_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1747) | Build a page- and element-linked document graph. | Построить граф документа с привязкой к страницам и элементам. |
| [`research_document_graph_verify`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1754) | Assess a document graph against quality observations. | Проверить граф документа по наблюдениям качества. |

## Search methods and instruments / Поисковые методы и инструменты

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_query_ast_compile`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1761) | Compile a structured query for a declared compiler. | Преобразовать структурированный запрос для заданного компилятора. |
| [`research_search_strategy_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1768) | Assess a versioned search strategy and material scope. | Проверить версию поисковой стратегии и область материала. |
| [`research_search_environment_record`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1775) | Record the execution environment of a search query. | Зафиксировать среду исполнения поискового запроса. |
| [`research_search_stop_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1782) | Assess search stopping from coverage, yield and residual estimates. | Оценить остановку поиска по охвату, отдаче и остатку. |
| [`research_screening_stop_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1789) | Assess a proposed screening stop against decisions and rule. | Проверить остановку отбора по решениям и правилу. |
| [`research_instrument_portfolio_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1796) | Build a portfolio of candidate research instruments. | Сформировать набор исследовательских инструментов-кандидатов. |
| [`research_instrument_strategy_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1803) | Build a strategy from a versioned instrument portfolio. | Построить стратегию из версионированного набора инструментов. |
| [`research_tool_query_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1810) | Build a tool-specific query from a strategy item. | Составить запрос к инструменту по элементу стратегии. |
| [`research_instrument_strategy_propose_revision`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1817) | Assess a proposed instrument-strategy revision. | Проверить предлагаемую редакцию стратегии инструментов. |

## Framing, context and oversight / Постановка, контекст и контроль

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_brief_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1824) | Build a structured brief from the original question and premises. | Составить структурированное задание из вопроса и предпосылок. |
| [`research_contextualization_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1831) | Build domain, audience and locale context for a task. | Сформировать предметный, адресный и языковой контекст задачи. |
| [`research_context_package_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1838) | Build a scoped context package for a project and role. | Сформировать ограниченный пакет контекста для проекта и роли. |
| [`research_debrief_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1845) | Compare planned and completed work in a debrief. | Сверить запланированную и выполненную работу при разборе итогов. |
| [`research_decomposition_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1852) | Assess decomposition nodes against the brief and engagement level. | Проверить декомпозицию по заданию и уровню исследования. |
| [`research_construct_operationalize`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1859) | Operationalize a defined construct for measurement. | Операционализировать определённое понятие для измерения. |
| [`research_construct_propose_revision`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1866) | Assess a proposed revision of a construct definition. | Проверить редакцию определения понятия. |
| [`research_assurance_profile_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1873) | Assess an assurance profile from risk and evidence level. | Проверить профиль обоснованности по риску и уровню доказательств. |
| [`research_basic_loop_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1880) | Assess bounded stages and iteration in a research loop. | Проверить ограниченные этапы и итерации исследовательского цикла. |
| [`research_oversight_transitions_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1887) | Assess transitions among oversight decisions. | Проверить переходы между решениями контроля. |

## Roles, collaboration and modality / Роли, взаимодействие и модальности

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_role_profile_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1894) | Assess a declared research role profile. | Проверить заявленный профиль исследовательской роли. |
| [`research_role_independence_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1901) | Assess independence among declared roles. | Проверить независимость заявленных ролей. |
| [`research_consilium_plan_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1908) | Assess a multi-role consultation plan and isolated inputs. | Проверить план совещания ролей и раздельность входов. |
| [`research_consilium_result_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1915) | Assess consultation rounds, positions and limits. | Проверить раунды, позиции и ограничения совещания. |
| [`research_topology_select`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1922) | Select a work topology from branch count and coupling. | Выбрать схему работы по числу и связанности ветвей. |
| [`research_modality_plan_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1929) | Assess which input modalities a plan uses. | Проверить модальности входных данных плана. |

## Knowledge, narrative and provenance / Знание, изложение и происхождение

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_fact_map_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1936) | Build a fact map tied to an authority revision. | Построить карту фактов, связанную с редакцией авторитетного состояния. |
| [`research_root_cause_map_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1943) | Build a root-cause map from nodes and edges. | Построить карту причин по узлам и связям. |
| [`research_knowledge_projections_reconcile`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1950) | Reconcile projections after authority-reference changes. | Сверить проекции знаний после изменения авторитетных ссылок. |
| [`research_narrative_plan_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1957) | Assess a narrative plan for audience and decision context. | Проверить план изложения с учётом аудитории и решения. |
| [`research_attribution_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1964) | Assess claim, citation, generation and verification attribution. | Проверить происхождение тезиса, цитаты, генерации и сверки. |
| [`research_source_influence_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1971) | Assess how source origins affect conclusions under leave-outs. | Оценить влияние происхождения источников на выводы при исключениях. |
| [`research_narrative_diff_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1978) | Assess changes between narrative stages. | Проверить изменения между этапами изложения. |
| [`research_provenance_export_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1985) | Assess a provenance-graph export and round trip. | Проверить экспорт графа происхождения и обратное чтение. |
| [`research_replay_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1992) | Assess execution replay against a manifest. | Проверить повтор исполнения по манифесту. |
| [`research_living_review_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L1999) | Assess a living-review update against policy and baseline. | Проверить обновление продолжаемого обзора по правилам и базе. |

## Depth qualification and recovery / Квалификация глубины и восстановление

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_deep_qualification_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2006) | Assess a scoped Deep/Ultra suite, runs and cross-checks. | Проверить ограниченный набор Deep/Ultra, запуски и перекрёстные проверки. |
| [`research_obligation_preservation_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2013) | Assess whether obligations survive a checkpoint transition. | Проверить сохранение обязательств после контрольной точки. |
| [`research_multiagent_independence_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2020) | Assess shared error channels and consensus among roles. | Проверить общие каналы ошибок и согласие ролей. |
| [`research_resilience_recovery_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2027) | Assess recovery after provider failure, drift or restart. | Проверить восстановление после отказа поставщика, дрейфа или перезапуска. |

## Providers and capabilities / Поставщики и возможности

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_provider_catalog_get`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2034) | Read requested provider entries from a local catalog. | Прочитать записи поставщиков из локального каталога. |
| [`research_provider_manifest_build`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2041) | Build a versioned provider-operation manifest. | Составить версионированный манифест операций поставщика. |
| [`research_provider_schema_diff`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2048) | Compare prior and current provider schemas. | Сравнить прежнюю и текущую схемы поставщика. |
| [`research_provider_operation_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2055) | Assess policy and drift state of one provider operation. | Проверить правила и дрейф одной операции поставщика. |
| [`research_provider_execution_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2062) | Assess a typed provider-execution control. | Проверить типизированный контроль исполнения поставщика. |
| [`research_provider_fallback_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2069) | Assess whether a fallback meets required properties. | Проверить соответствие резервного маршрута обязательным свойствам. |
| [`research_provider_budget_reserve`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2076) | Assess reservations against provider limits. | Сверить резервы с лимитами поставщика. |
| [`research_provider_lifecycle_reconcile`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2083) | Reconcile the state of a provider run. | Сверить состояние запуска поставщика. |
| [`research_provider_receipt_normalize`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2090) | Normalize a versioned provider receipt. | Привести квитанцию поставщика к общей форме с учётом версии. |
| [`research_provider_conformance_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2097) | Assess provider-adapter conformance evidence. | Проверить свидетельства соответствия адаптера поставщика. |
| [`research_scholarly_object_resolve`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2104) | Resolve scholarly records into a bounded object identity. | Сопоставить научные записи с ограниченной идентичностью объекта. |
| [`research_capability_gap_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2111) | Assess gaps between required and qualified capabilities. | Сверить требуемые и квалифицированные возможности. |

## Business and academic methods / Деловые и научные методы

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_business_design_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2118) | Assess a business research design and evidence classes. | Проверить схему делового исследования и классы доказательств. |
| [`research_business_control_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2125) | Assess a typed business control. | Проверить типизированный контроль делового исследования. |
| [`research_academic_protocol_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2132) | Assess an academic protocol and object identities. | Проверить научный протокол и идентичности объектов. |
| [`research_academic_integrity_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2139) | Assess a typed academic-integrity control. | Проверить типизированный контроль научной добросовестности. |
| [`research_meta_analysis_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2146) | Assess pooling eligibility and sensitivity requirements. | Проверить допустимость объединения результатов и чувствительность. |
| [`research_review_protocol_validate`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2153) | Validate a review protocol and amendments. | Проверить протокол обзора и поправки к нему. |
| [`research_screening_adjudicate`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2160) | Assess screening decisions and adjudication. | Проверить решения отбора и разрешение разногласий. |
| [`research_study_graph_resolve`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2167) | Resolve study-graph nodes, edges and full-text receipts. | Сопоставить узлы, связи и квитанции полного текста исследования. |
| [`research_extraction_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2174) | Assess extracted fields against schema and codebook. | Проверить извлечённые поля по схеме и кодировочной книге. |
| [`research_prisma_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2181) | Assess applicable PRISMA items and materializations. | Проверить применимые пункты PRISMA и их подтверждения. |
| [`research_prisma_flow_account`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2188) | Account for full-text dispositions in a PRISMA flow. | Учесть решения по полным текстам в схеме PRISMA. |
| [`research_risk_of_bias_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2195) | Assess recorded risk-of-bias judgments. | Проверить зарегистрированные оценки риска смещения. |
| [`research_certainty_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2202) | Assess certainty for an outcome and its domains. | Оценить определённость вывода по исходу и областям риска. |
| [`research_academic_synthesis_gate`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2209) | Assess whether academic results may enter synthesis. | Проверить допуск научных результатов к синтезу. |
| [`research_computation_replay_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2216) | Assess reproducibility of a recorded computation. | Проверить воспроизводимость сохранённого вычисления. |
| [`research_fixed_effect_compute`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2223) | Compute a declared fixed-effect summary from records. | Рассчитать заданную сводку фиксированного эффекта из записей. |

## Review, acceptance and state / Проверка, приёмка и состояние

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_review_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2230) | Assess a review against a result and requirement. | Проверить рецензию по результату и требованию. |
| [`research_acceptance_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2237) | Assess execution, claims and result acceptance. | Проверить исполнение, тезисы и приёмку результата. |
| [`research_release_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2244) | Assess a release against acceptance and required reviews. | Проверить выпуск по приёмке и обязательным рецензиям. |
| [`research_correction_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2251) | Assess a correction to a prior release. | Проверить исправление ранее выпущенного результата. |
| [`research_operation_reconcile`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2258) | Reconcile an operation by identity and idempotency key. | Сверить операцию по идентичности и ключу однократности. |
| [`research_recovery_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2265) | Assess journal and checkpoint recovery for a run. | Проверить восстановление запуска по журналу и контрольной точке. |
| [`research_invalidation_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2272) | Assess which active acceptances a changed reference invalidates. | Проверить, какие приёмки утрачивают силу после изменения ссылки. |
| [`research_object_revision_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2279) | Assess writer authority and revision of an object. | Проверить полномочия записи и редакцию объекта. |
| [`research_context_assembly_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2286) | Assess context candidates for a target project. | Проверить кандидатов контекста для целевого проекта. |
| [`research_restore_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2293) | Assess snapshot restoration and continuation. | Проверить восстановление снимка и продолжение работы. |
| [`research_bundle_import_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2300) | Assess a bundle import against manifest and target inventory. | Проверить импорт пакета по манифесту и целевому реестру. |
| [`research_legacy_migration_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2307) | Assess migration of legacy records. | Проверить перенос прежних записей. |

## Deployment and Foundation integration / Развёртывание и интеграция Foundation

| Tool | Purpose (EN) | Назначение (RU) |
| --- | --- | --- |
| [`research_deployment_candidate_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2314) | Assess an on-demand deployment candidate and dependencies. | Проверить кандидата развёртывания по режиму запуска и зависимостям. |
| [`research_profile_qualification`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2321) | Assess qualification evidence for a named profile and suite. | Проверить доказательства квалификации именованного профиля и набора. |
| [`research_depth_compare`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2328) | Compare Search, Deep and Ultra results under one task constraint. | Сравнить Search, Deep и Ultra при общих ограничениях задачи. |
| [`research_utility_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2335) | Assess result utility, time saved and verification burden. | Оценить полезность результата, экономию времени и труд проверки. |
| [`research_greenfield_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2342) | Assess isolation and scope of a new deployment target. | Проверить изоляцию и область нового экземпляра. |
| [`research_greenfield_accept`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2349) | Assess acceptance of a new instance from gate receipts. | Проверить приёмку нового экземпляра по квитанциям шлюзов. |
| [`research_foundation_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2356) | Assess Foundation contract and bridge integration. | Проверить контракт Foundation и интеграцию моста. |
| [`research_resource_admission_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2363) | Assess resources before admitting a run. | Проверить ресурсы перед допуском запуска. |
| [`research_migration_map_dry_run`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2370) | Assess a migration mapping without applying it. | Проверить схему переноса без её применения. |
| [`research_state_reconcile`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2377) | Reconcile work, issue, lease and artifact states. | Сверить состояния работы, задачи, аренды и артефакта. |
| [`research_state_semantics_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2384) | Assess a typed state-semantics control. | Проверить типизированный контроль значений состояний. |
| [`research_security_control_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2391) | Assess a typed security control. | Проверить типизированный контроль безопасности. |
| [`research_artifact_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2398) | Assess an artifact operation and file properties. | Проверить операцию с артефактом и свойства файла. |
| [`research_fragment_promote`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2405) | Assess promotion of a fragment to an evidence class. | Проверить повышение фрагмента до доказательного класса. |
| [`research_installation_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2412) | Assess installation against greenfield, Foundation and staging receipts. | Проверить установку по квитанциям нового экземпляра, Foundation и подготовки. |
| [`research_context_lifecycle_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2419) | Assess a scoped context lifecycle. | Проверить жизненный цикл ограниченного контекста. |
| [`research_circuit_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2426) | Assess route failures, retry budget and circuit state. | Проверить отказы маршрута, лимит повторов и состояние предохранителя. |
| [`research_dolt_commit_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2433) | Assess a logical Dolt commit and object references. | Проверить логическую запись Dolt и ссылки на объекты. |
| [`research_capability_model_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2440) | Assess a capability catalog, promotion and model lane. | Проверить каталог возможностей, повышение статуса и модельный маршрут. |
| [`research_provider_live_probe`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2447) | Run a bounded provider probe or classify a host-only receipt. | Выполнить ограниченную пробу поставщика или классифицировать квитанцию хоста. |
| [`research_r3_evidence_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2454) | Assess official-document, dataset and atom evidence batches. | Проверить пакеты доказательств из официального документа, набора данных и атомов. |
| [`research_context_package_assemble`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2461) | Assemble bounded context contributions for a consumer. | Собрать ограниченные вклады в контекст для получателя. |
| [`research_work_liveness_reconcile`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2468) | Reconcile observed work state with scheduled controls. | Сверить наблюдаемое состояние работы с плановыми проверками. |
| [`research_distribution_delivery_assess`](https://github.com/olegeklepikov-collab/ultra-deep-research/blob/9077d24d5e7b6dda5db7902bac2a927503791db6/plugin.py#L2475) | Assess original, sanitizer, transformation and delivery policy. | Проверить оригинал, очистку, преобразование и правила доставки. |
