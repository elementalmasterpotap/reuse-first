"""
REUSE FIRST — паттерны детекции.

SKIP_PATTERNS, CREATE_VERBS, OBJECT_NOUNS, STANDALONE_TRIGGERS,
TECH_KEYWORDS, DOMAIN_PHRASES.
"""

# ══════════════════════════════════════════════════════════════════════════
# SKIP — ЕДИНСТВЕННЫЕ случаи когда НЕ триггерить
# Жёсткий whitelist. Всё остальное = потенциальный триггер.
# ══════════════════════════════════════════════════════════════════════════
SKIP_PATTERNS = [
    # ── Точечные фиксы ─────────────────────────────────────────────────
    r"^(исправь|фикс|почини|поправь|пофикс|пофиксь|фиксни|залатай)\s",
    r"^(fix|repair|patch|hotfix|bugfix)\s",
    r"(исправ|фикс|почин|поправ)\s.{0,15}(баг|ошибк|опечатк|тест|lint|типизаци)",

    # ── Read-only / вопросы / исследование ─────────────────────────────
    r"^(объясни|расскажи|покажи|найди|перечисли|опиши|прочитай|проверь|глянь|посмотри|выведи|распечатай)\s",
    r"^(explain|show|find|list|describe|read|check|look|print|display|inspect|examine|debug|trace)\s",
    r"^\s*\?",
    r"^(как\s+работает|что\s+такое|что\s+это|зачем\s+нужн|почему|в\s+чём\s+разниц|чем\s+отличается)\s",
    r"^(what\s+(is|are|does)|how\s+does|why\s+does|where\s+is|when\s+did|who)\s",

    # ── Стилевые мелочи (без создания нового) ──────────────────────────
    r"^(измени|поменяй|замени|смени|переключи)\s.{0,30}(цвет|шрифт|отступ|размер|текст|строк[уи]|слово|название|иконк|заголовок|подпись|placeholder|label|title)",
    r"^(change|swap|replace|toggle|switch)\s.{0,30}(color|font|padding|margin|size|text|string|word|name|icon|title|label|placeholder)",

    # ── Удаление / очистка ─────────────────────────────────────────────
    r"^(удали|убери|вырежи|снеси|очисти|почисти|зачисти|вычисти|сотри)\s",
    r"^(delete|remove|drop|clean|purge|wipe|clear|erase|trim)\s",

    # ── Короткие ответы / подтверждения / продолжения ──────────────────
    r"^(yes|no|ok|да|нет|ок|ага|угу|норм|збс|го|погнали|давай|лан|ладно|хорош|принято|все|всё|ну|ясно|понял|круто|класс|топ|огонь|пушка|заебись|хуйня|пиздец|блять|ёп|дальше|продолжай|continue|next|done|good|great|nice|cool|fine|sure|yep|nope|nah)\s*$",
    r"^[yn1-9]\s*$",

    # ── Слеш-команды ───────────────────────────────────────────────────
    r"^/",

    # ── Workflow (деплой, коммит, патчнот, бэкап) ──────────────────────
    r"^(деплой|задеплой|закоммит|коммит|запуш|пуш|синхронизируй|синк|бэкап|забэкапь)\b",
    r"^(deploy|commit|push|sync|backup)\b",
    r"\b(патчнот|patchnote|changelog|release\s*note)\b",
    r"^(compact|сожми|сжать|clear|reset)\b",

    # ── Мелкие обновления ──────────────────────────────────────────────
    r"^(обнови|апдейт|upgrade|bump|update)\s.{0,40}$",

    # ── Файловые операции ──────────────────────────────────────────────
    r"^(перенеси|скопируй|переименуй|move|copy|rename|mv|cp)\s",

    # ── Процессы ───────────────────────────────────────────────────────
    r"^(запусти|останови|перезапусти|run|start|stop|restart|kill|abort)\s",

    # ── Ревью / аудит ──────────────────────────────────────────────────
    r"^(review|ревью|разбор|аудит|audit|analyze|проанализируй)\b",

    # ── Форматирование / линтинг ───────────────────────────────────────
    r"^(отформатируй|format|lint|prettier|eslint|black|isort)\b",

    # ── Навигация / структура ──────────────────────────────────────────
    r"^(открой|open|cd|перейди|зайди)\s",
    r"^(покажи\s+структур|tree|ls|dir)\b",
]

# ══════════════════════════════════════════════════════════════════════════
# CREATE VERBS — глаголы создания (RU + EN)
# Любой из них + объект/технология = ТРИГГЕР
# ══════════════════════════════════════════════════════════════════════════
CREATE_VERBS_RU = (
    r'\b(созда[йюь]|сделай|напиши|разработай|реализуй|построй|сгенерируй'
    r'|прикрути|внедри|подключи|интегрируй|имплементируй'
    r'|добавь|настрой|сконфигурируй|организуй|собери|оформи'
    r'|автоматизируй|заверни|оберни|спроектируй|придумай'
    r'|накидай|набросай|склепай|запили|захуярь|забацай|наваяй'
    r'|подними|разверни|подготовь|выстрой|скомпонуй'
    r'|замути|сооруди|сваргань|соедини|склей|сцепи|свяжи|переделай'
    r'|перепиши|портируй|мигрируй|конвертируй|трансформируй'
    r'|оптимизируй|ускорь|улучши|прокачай|докрути|допили|доделай'
    r'|расширь|дополни|встрой|вмонтируй|вкорячь|вкрути|воткни)\b'
)

CREATE_VERBS_EN = (
    r'\b(create|build|make|write|implement|develop|design|generate'
    r'|set\s?up|add|configure|integrate|wire\s?up|compose'
    r'|automate|wrap|scaffold|bootstrap|spin\s?up|craft'
    r'|architect|engineer|assemble|construct|establish|produce'
    r'|port|migrate|convert|transform|refactor|rewrite'
    r'|optimize|improve|enhance|extend|expand|augment'
    r'|embed|mount|hook\s?up|plug\s?in|connect|link'
    r'|provision|orchestrate|containerize|dockerize'
    r'|prototype|mock\s?up|wireframe|sketch|draft)\b'
)

# ══════════════════════════════════════════════════════════════════════════
# OBJECT NOUNS — что создаётся (УЛЬТИМАТИВНЫЙ список)
# ══════════════════════════════════════════════════════════════════════════
OBJECT_NOUNS_RU = (
    # ── Софт / код ─────────────────────────────────────────────────────
    r'\b(систем[уа]|утилит[уа]|инструмент|тул|скрипт|програм[уа]'
    r'|бот[а]?|сервис|приложени[ея]|апп|софт'
    r'|библиотек[уа]|модуль|пакет|плагин|расширени[ея]|аддон'
    r'|хук[и]?|интеграци[юя]|автоматизаци[юя]'

    # ── Обработка данных ───────────────────────────────────────────────
    r'|парсер|конвертер|генератор|валидатор|транслятор'
    r'|фильтр|сортировщик|агрегатор|трансформер'
    r'|импортёр|экспортёр|загрузчик|лоадер|даунлоадер'
    r'|скрейпер|краулер|сборщик|паук|спайдер'

    # ── Мониторинг / логи / алерты ─────────────────────────────────────
    r'|мониторинг|логгер|логирован\w*|трекер|профайлер'
    r'|дашборд|панел[ьи]|консол[ьи]|терминал'
    r'|нотификаци\w*|уведомлени\w*|алерт\w*|оповещени\w*'

    # ── UI / UX / визуал ───────────────────────────────────────────────
    r'|виджет|компонент|элемент|блок|секци[юя]'
    r'|форм[уа]|галере[юя]|слайдер|карусел[ьи]|табл?иц[уа]'
    r'|модальн\w*|попап|тултип|дропдаун|меню|навигаци\w*'
    r'|анимаци[юя]|эффект|шейдер|частиц\w*|переход\w*|transition'
    r'|лейаут|layout|сетк[уа]|grid|тем[уа]'

    # ── API / протоколы ────────────────────────────────────────────────
    r'|API|SDK|CLI|GUI|UI|UX|TUI'
    r'|endpoint|роут|маршрут|контроллер|хендлер|обработчик'
    r'|webhook|вебхук|колбек|callback'

    # ── Веб ────────────────────────────────────────────────────────────
    r'|сайт|страниц[уа]|лендинг|портал|витрин[уа]'
    r'|блог|форум|вики|CMS|магазин|маркетплейс'

    # ── Инфраструктура ─────────────────────────────────────────────────
    r'|базу?\s*данных|хранилищ[еа]|кеш|кэш|очеред[ьи]'
    r'|сервер|бэкенд|фронтенд|микросервис|демон|воркер'
    r'|пайплайн|конвейер|цепочк[уа]|поток|процесс'
    r'|контейнер|кластер|нод[уа]|инстанс'

    # ── Обёртки / прослойки ────────────────────────────────────────────
    r'|обёртк[уа]|враппер|прокси|мидлвар\w*|middleware'
    r'|адаптер|мост|bridge|фасад|декоратор|шлюз|gateway'

    # ── Безопасность / авторизация ─────────────────────────────────────
    r'|авторизаци[юя]|аутентификаци[юя]|auth\w*'
    r'|токен\w*|сесси[юя]|permission|роль|RBAC'

    # ── Тестирование ───────────────────────────────────────────────────
    r'|тест\w*|фикстур\w*|мок\w*|стаб\w*'

    # ── DevOps / CI/CD ─────────────────────────────────────────────────
    r'|деплой\w*|ci.?cd|workflow|action'
    r'|бэкап\w*|миграци\w*|синхронизаци\w*'
    r'|установщик|инсталлятор|визард|мастер|installer'

    # ── Коммуникации ───────────────────────────────────────────────────
    r'|чат|мессенджер|рассылк\w*|newsletter|email.?sender'

    # ── Аналитика / отчёты ─────────────────────────────────────────────
    r'|отчёт\w*|репорт\w*|статистик\w*|аналитик\w*|метрик\w*'

    # ── Шаблоны / генерация ────────────────────────────────────────────
    r'|шаблон|темплейт|стартер|заготовк\w*|болванк\w*|каркас'

    # ── Менеджмент / оркестрация ───────────────────────────────────────
    r'|конфиг\w*|настройк\w*|менеджер|оркестратор'
    r'|планировщик|шедулер|крон|cron|диспетчер'

    # ── Просмотр / редактирование ──────────────────────────────────────
    r'|редактор|вьюер|превьювер|рендерер|плеер|проигрыватель'

    # ── AI / ML ────────────────────────────────────────────────────────
    r'|модел[ьи]|нейросет[ьи]|классификатор|детектор|предиктор'
    r'|эмбеддинг\w*|векторн\w*|RAG|чат.?бот|ассистент|агент)\b'
)

OBJECT_NOUNS_EN = (
    # ── Software / code ────────────────────────────────────────────────
    r'\b(system|utility|tool|script|program|app|application|software'
    r'|bot|service|library|module|package|plugin|extension|addon'
    r'|hook|integration|automation'

    # ── Data processing ────────────────────────────────────────────────
    r'|parser|converter|generator|validator|translator'
    r'|filter|sorter|aggregator|transformer|processor'
    r'|importer|exporter|loader|downloader'
    r'|scraper|crawler|spider|collector|fetcher'

    # ── Monitoring / logging / alerts ──────────────────────────────────
    r'|monitor|logger|tracker|profiler|debugger'
    r'|dashboard|panel|console|terminal'
    r'|notification|alert|webhook'

    # ── UI / UX / visual ───────────────────────────────────────────────
    r'|widget|component|element|block|section'
    r'|form|gallery|slider|carousel|table|grid'
    r'|modal|popup|tooltip|dropdown|menu|navbar|nav|sidebar'
    r'|animation|effect|shader|particle|transition'
    r'|layout|theme|skin'

    # ── API / protocols ────────────────────────────────────────────────
    r'|API|SDK|CLI|GUI|TUI'
    r'|endpoint|route|controller|handler|resolver'
    r'|webhook|callback|listener|subscriber|observer'

    # ── Web ────────────────────────────────────────────────────────────
    r'|site|website|page|landing|portal|storefront'
    r'|blog|forum|wiki|CMS|shop|marketplace'

    # ── Infrastructure ─────────────────────────────────────────────────
    r'|database|storage|cache|queue|worker|daemon|server'
    r'|backend|frontend|microservice|pipeline|workflow'
    r'|container|cluster|node|instance|pod'

    # ── Wrappers / layers ──────────────────────────────────────────────
    r'|wrapper|proxy|middleware|layer|adapter|bridge'
    r'|facade|decorator|gateway|interceptor'

    # ── Auth / security ────────────────────────────────────────────────
    r'|auth\w*|login|signup|register|session|permission|role|RBAC'
    r'|token|oauth|jwt|sso|passport'

    # ── Testing ────────────────────────────────────────────────────────
    r'|test\w*|fixture|mock|stub|spy|harness|benchmark'

    # ── DevOps / CI/CD ─────────────────────────────────────────────────
    r'|deploy\w*|ci.?cd|docker\w*|k8s|terraform|ansible'
    r'|backup|migration|sync\w*|installer|wizard|setup'

    # ── Communication ──────────────────────────────────────────────────
    r'|chat|messenger|mailer|newsletter|notifier'

    # ── Analytics / reports ────────────────────────────────────────────
    r'|report|statistic|analytics|metric|insight'

    # ── Templates / generation ─────────────────────────────────────────
    r'|template|starter|boilerplate|scaffold|skeleton|archetype'

    # ── Management / orchestration ─────────────────────────────────────
    r'|config\w*|manager|orchestrator|scheduler|cron|dispatcher'

    # ── Viewing / editing ──────────────────────────────────────────────
    r'|editor|viewer|previewer|renderer|player'

    # ── AI / ML ────────────────────────────────────────────────────────
    r'|model|neural\s*net|classifier|detector|predictor'
    r'|embedding|vector\w*|RAG|chatbot|assistant|agent)\b'
)

# ══════════════════════════════════════════════════════════════════════════
# STANDALONE TRIGGERS — триггерят БЕЗ комбинации
# ══════════════════════════════════════════════════════════════════════════
STANDALONE_TRIGGERS = [
    # ── "С нуля" ───────────────────────────────────────────────────────
    r'\b(с\s+нуля|от\s+нуля|from\s+scratch|ground\s+up)\b',
    r'\b(новый\s+проект|new\s+project|init\s+project|стартуем)\b',

    # ── "Нужен / хочу" ────────────────────────────────────────────────
    r'\b(нужен|нужна|нужно)\s+\w+',
    r'\b(хочу|хотелось\s+бы)\s+(чтобы|сделать|получить|иметь|видеть)',
    r'\b(need|want|looking\s+for|searching\s+for)\s+',
    r'\b(I\s+need|we\s+need|I\s+want)\s+',

    # ── "Как сделать" ─────────────────────────────────────────────────
    r'\b(how\s+to\s+(build|create|make|implement|set\s*up|develop|write|design))\b',
    r'\b(как\s+(сделать|создать|написать|реализовать|построить|настроить|организовать|автоматизировать))\b',

    # ── "Лучший способ" ───────────────────────────────────────────────
    r'\b(best\s+(way|approach|practice|method|solution)\s+to)\b',
    r'\b(лучший\s+способ|оптимальн\w+\s+(подход|способ|решени)|правильн\w+\s+способ)\b',
    r'\b(рекомендуемый\s+(подход|способ)|recommended\s+approach)\b',

    # ── "Аналог / альтернатива" ───────────────────────────────────────
    r'\b(аналог|альтернатив[уа]|замен[уа]\s+(для|вместо)|вместо\s+\w+\s+использовать)\b',
    r'\b(alternative\s+to|analog\s+of|replacement\s+for|instead\s+of)\b',
    r'\b(есть\s+что.?то\s+(типа|вроде|похож)|is\s+there\s+(something|anything)\s+like)\b',

    # ── "Можно ли / есть ли" ──────────────────────────────────────────
    r'\b(можно\s+ли|есть\s+ли|существует\s+ли)\b.{5,}',
    r'\b(is\s+there|does\s+.*\s+exist|are\s+there\s+any)\b',

    # ── Прямые запросы на поиск ────────────────────────────────────────
    r'\b(подскажи|посоветуй|порекомендуй)\s+\w*\s*(готов|библиотек|пакет|инструмент|утилит|решени|способ|фреймворк|тул)',
    r'\b(suggest|recommend|advise)\s+.{0,10}(library|package|tool|framework|solution|approach)',
    r'\bподскажи\s+\w+',

    # ── Паттерны задач ─────────────────────────────────────────────────
    r'\b(автоматически|автоматический|автоматическ\w+)\s+\w+',
    r'\b(periodic|scheduled|recurring|automated|automatic)\s+\w+',
]

# ══════════════════════════════════════════════════════════════════════════
# TECH KEYWORDS — технологии / фреймворки / платформы
# Если упоминается — почти 100% есть готовое решение
# ══════════════════════════════════════════════════════════════════════════
TECH_KEYWORDS = (
    # ── Messaging / social ─────────────────────────────────────────────
    r'\b(telegram|discord|slack|whatsapp|viber|signal|matrix'
    r'|twitter|mastodon|reddit|vk|vkontakte|instagram|facebook|tiktok'
    r'|twitch|youtube|linkedin'

    # ── VCS / project management ───────────────────────────────────────
    r'|github|gitlab|bitbucket|gitea|jira|linear|trello|notion|asana'

    # ── Containers / orchestration ─────────────────────────────────────
    r'|docker|kubernetes|k8s|podman|nomad|swarm'

    # ── Databases ──────────────────────────────────────────────────────
    r'|redis|postgres|postgresql|mysql|mariadb|sqlite|mongodb|dynamodb'
    r'|cassandra|couchdb|neo4j|influxdb|timescaledb|clickhouse'
    r'|elasticsearch|opensearch|meilisearch|typesense|algolia'
    r'|firebase|supabase|pocketbase|appwrite|hasura'

    # ── Payments / billing ─────────────────────────────────────────────
    r'|stripe|paypal|twilio|sendgrid|mailgun|resend|postmark'
    r'|braintree|paddle|lemon\s*squeezy|yookassa|robokassa|tinkoff'

    # ── Auth / identity ────────────────────────────────────────────────
    r'|oauth|jwt|sso|saml|openid|keycloak|auth0|clerk|lucia|supertokens'

    # ── Protocols / transport ──────────────────────────────────────────
    r'|websocket|grpc|graphql|rest\s?api|soap|mqtt|amqp|kafka|rabbitmq|nats'
    r'|protobuf|thrift|avro|json.?rpc|trpc'

    # ── AI / ML ────────────────────────────────────────────────────────
    r'|openai|anthropic|claude|gpt|llm|langchain|llamaindex|ollama'
    r'|huggingface|transformers|pytorch|tensorflow|keras|onnx'
    r'|stable.?diffusion|midjourney|whisper|deepseek|mistral|gemini'
    r'|pinecone|weaviate|qdrant|chroma|milvus'
    r'|crew.?ai|autogen|semantic.?kernel|dspy'

    # ── Frontend frameworks ────────────────────────────────────────────
    r'|react|vue|svelte|next|nuxt|angular|astro|remix|solid|qwik'
    r'|gatsby|eleventy|hugo|jekyll|vitepress|docusaurus'

    # ── Backend frameworks ─────────────────────────────────────────────
    r'|express|fastapi|django|flask|spring|rails|laravel|phoenix'
    r'|nestjs|fastify|hono|elysia|bun|deno|actix|axum|rocket|gin|echo|fiber'

    # ── Desktop / mobile ───────────────────────────────────────────────
    r'|electron|tauri|flutter|react.native|expo|ionic|capacitor'
    r'|swift|kotlin|jetpack.compose|swiftui|maui|avalonia'
    r'|winforms|wpf|uwp|tkinter|pyqt|pyside'

    # ── CSS / UI ───────────────────────────────────────────────────────
    r'|tailwind|bootstrap|material.?ui|chakra|shadcn|radix|headless.?ui'
    r'|ant.?design|prime.?vue|vuetify|quasar|mantine|daisyui'
    r'|framer.?motion|gsap|three\.?js|d3\.?js|chart\.?js|echarts'

    # ── Testing ────────────────────────────────────────────────────────
    r'|playwright|puppeteer|selenium|cypress|vitest|jest|mocha|pytest'
    r'|storybook|chromatic|testing.?library|msw|supertest'

    # ── Package managers / build ───────────────────────────────────────
    r'|npm|yarn|pnpm|pip|pipenv|poetry|uv|cargo|nuget|brew|apt|gem|composer'
    r'|webpack|vite|rollup|esbuild|turbopack|parcel|rspack|bun'

    # ── Cloud / hosting ────────────────────────────────────────────────
    r'|aws|s3|lambda|ec2|cloudflare|vercel|netlify|heroku|render'
    r'|digitalocean|linode|vultr|hetzner|fly\.io|railway|coolify'
    r'|gcp|azure|oracle.cloud'

    # ── Automation / workflow ──────────────────────────────────────────
    r'|n8n|zapier|ifttt|make\.com|temporal|prefect|airflow|dagster'

    # ── Observability ──────────────────────────────────────────────────
    r'|prometheus|grafana|sentry|datadog|newrelic|pagerduty'
    r'|opentelemetry|jaeger|zipkin|loki|seq'

    # ── Proxy / web server ─────────────────────────────────────────────
    r'|nginx|caddy|traefik|haproxy|envoy|kong|apisix'

    # ── Media processing ───────────────────────────────────────────────
    r'|ffmpeg|imagemagick|sharp|pillow|sox|audiowaveform'
    r'|puppeteer|playwright|cheerio|jsdom|beautiful.?soup|scrapy'

    # ── Data science ───────────────────────────────────────────────────
    r'|pandas|numpy|scipy|matplotlib|plotly|seaborn|bokeh'
    r'|polars|dask|spark|dbt|great.?expectations'

    # ── CMS / content ──────────────────────────────────────────────────
    r'|wordpress|strapi|sanity|contentful|directus|payload|ghost|keystone'

    # ── Claude Code specific ───────────────────────────────────────────
    r'|claude.?code|mcp|claude.?plugin)\b'
)

# ══════════════════════════════════════════════════════════════════════════
# DOMAIN PHRASES — фразы-индикаторы конкретных доменов
# Триггерят даже без явного глагола создания
# ══════════════════════════════════════════════════════════════════════════
DOMAIN_PHRASES = [
    # ── Веб-разработка ─────────────────────────────────────────────────
    r'\b(responsive|адаптивн\w+)\s+(layout|вёрстк|дизайн|страниц)',
    r'\b(dark\s*mode|тёмная\s*тема|light\s*mode|светлая\s*тема)\b',
    r'\b(infinite\s*scroll|бесконечн\w+\s*скролл|virtual\s*scroll|lazy\s*load)',
    r'\b(drag.?and.?drop|перетаскивани|sortable|resizable)\b',
    r'\b(real.?time|реал.?тайм|live\s+update|hot\s+reload)\b',

    # ── DevOps ─────────────────────────────────────────────────────────
    r'\b(blue.?green|canary|rolling\s+update|zero.?downtime)\b',
    r'\b(rate\s*limit|throttl|backpressure|circuit\s*breaker)\b',
    r'\b(health\s*check|readiness|liveness|graceful\s*shutdown)\b',

    # ── Данные ─────────────────────────────────────────────────────────
    r'\b(ETL|ELT|data\s*pipeline|data\s*warehouse|data\s*lake)\b',
    r'\b(CRUD|REST|GraphQL\s+schema|ORM|миграци\w+\s+базы)\b',
    r'\b(full.?text\s*search|полнотекстов\w+\s*поиск|fuzzy\s*search)\b',

    # ── AI / ML ────────────────────────────────────────────────────────
    r'\b(prompt\s*engineering|fine.?tun|RAG|embeddings|vector\s*search)\b',
    r'\b(function\s*calling|tool\s*use|agent\w*|chain.?of.?thought)\b',

    # ── Безопасность ───────────────────────────────────────────────────
    r'\b(XSS|CSRF|SQL\s*injection|sanitiz|escap|helmet|cors)\b',
    r'\b(encryption|шифрован|hashing|bcrypt|argon|PBKDF)\b',
    r'\b(2FA|MFA|TOTP|OTP|двухфакторн)\b',
]
