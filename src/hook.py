#!/usr/bin/env python3
"""
REUSE FIRST v1.0 — ультимативный UserPromptSubmit хук для Claude Code.

Максимально агрессивный детектор задач где нужно сначала искать готовое.
Философия: лучше 10 ложных срабатываний чем 1 пропуск.

6 триггерных комбинаций. 400+ паттернов. RU + EN.

Hook: UserPromptSubmit
Output: {"injectedSystemPrompt": "..."} на stdout
"""
import json
import re
import sys


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
    # доп. глаголы
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
    # extra verbs
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
    r'\bподскажи\s+\w+',  # "подскажи" + любое слово = вероятно просит совет

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


def where_to_search(text):
    """Ультимативный детектор: ГДЕ искать + конкретные поисковые запросы."""
    sources = {"GitHub"}
    queries = []  # конкретные поисковые запросы

    # ── Package registries by language ─────────────────────────────────
    REGISTRY_CHECKS = [
        # JavaScript / TypeScript ecosystem
        (r'\b(npm|node|js|ts|react|vue|svelte|next|express|typescript|javascript|bun|deno|angular|astro|remix|solid|qwik|nuxt|gatsby|vite|webpack|rollup|esbuild)\b',
         "npmjs.com", "npm search '[task]'"),
        # Python ecosystem
        (r'\b(pip|python|django|flask|fastapi|pandas|pytorch|poetry|uv|celery|scrapy|sqlalchemy|pydantic|httpx|aiohttp|beautifulsoup|lxml)\b',
         "PyPI (pypi.org)", "pip search / pypi.org/search/?q=[task]"),
        # Rust
        (r'\b(cargo|rust|actix|axum|tokio|serde|warp|hyper)\b',
         "crates.io", "crates.io/search?q=[task]"),
        # C# / .NET
        (r'\b(nuget|c#|csharp|dotnet|\.net|maui|avalonia|wpf|winforms|blazor|asp\.net)\b',
         "NuGet (nuget.org)", "nuget.org/packages?q=[task]"),
        # Go
        (r'\b(go|golang|gin|echo|fiber|gorilla|chi|cobra)\b',
         "pkg.go.dev", "pkg.go.dev/search?q=[task]"),
        # Ruby
        (r'\b(gem|ruby|rails|sinatra|sidekiq|rspec)\b',
         "RubyGems", "rubygems.org/search?query=[task]"),
        # PHP
        (r'\b(composer|php|laravel|symfony|wordpress|drupal|yii)\b',
         "Packagist", "packagist.org/search/?q=[task]"),
        # Java / Kotlin
        (r'\b(maven|gradle|java|kotlin|spring|quarkus|micronaut|ktor)\b',
         "Maven Central", "search.maven.org/search?q=[task]"),
        # Swift
        (r'\b(swift|swiftui|cocoapods|spm|vapor|alamofire)\b',
         "Swift Package Index", "swiftpackageindex.com/search?q=[task]"),
        # Dart / Flutter
        (r'\b(dart|flutter|pub\.dev)\b',
         "pub.dev", "pub.dev/packages?q=[task]"),
        # Elixir
        (r'\b(elixir|phoenix|hex\.pm|ecto)\b',
         "hex.pm", "hex.pm/packages?search=[task]"),
    ]

    # ── Specialized platforms ──────────────────────────────────────────
    PLATFORM_CHECKS = [
        # Docker / containers
        (r'\b(docker|k8s|kubernetes|podman|container|helm|compose)\b',
         "Docker Hub", "hub.docker.com/search?q=[task]"),
        # CI/CD
        (r'\b(ci|cd|action|workflow|pipeline|github\s+action|gitlab\s+ci|jenkins)\b',
         "GitHub Actions Marketplace", "github.com/marketplace?type=actions&query=[task]"),
        # Claude Code
        (r'\b(claude|claude.?code|mcp|claude.?plugin|anthropic)\b',
         "claude-code-plugins marketplace", "search claude-code-plugins for '[task]'"),
        # VS Code
        (r'\b(vscode|vs\s*code|visual\s*studio\s*code)\b',
         "VS Code Marketplace", "marketplace.visualstudio.com/search?term=[task]"),
        # JetBrains
        (r'\b(jetbrains|intellij|pycharm|webstorm|goland|rider)\b',
         "JetBrains Marketplace", "plugins.jetbrains.com/search?search=[task]"),
        # Browser extensions
        (r'\b(chrome|firefox|browser\s+extension|расширение\s+браузер|addon)\b',
         "Chrome Web Store / Firefox Add-ons", None),
        # WordPress
        (r'\b(wordpress|wp\s+plugin|wp\s+theme)\b',
         "WordPress Plugin Directory", "wordpress.org/plugins/search/[task]"),
        # Terraform
        (r'\b(terraform|tf\s+module|infrastructure.?as.?code)\b',
         "Terraform Registry", "registry.terraform.io/search/modules?q=[task]"),
        # Ansible
        (r'\b(ansible|playbook|galaxy)\b',
         "Ansible Galaxy", "galaxy.ansible.com/search?keywords=[task]"),
    ]

    # ── Creative / visual ──────────────────────────────────────────────
    CREATIVE_CHECKS = [
        (r'\b(эффект|анимаци|canvas|css\s+effect|animation|transition|parallax|hover\s+effect|scroll\s+effect|typing\s+effect|particle|ripple|glow|gradient|морфинг|морф)\b',
         "CodePen", "codepen.io/search/pens?q=[task]"),
        (r'\b(shader|hlsl|glsl|шейдер|webgl|raymarching|sdf|noise)\b',
         "ShaderToy", "shadertoy.com/results?query=[task]"),
        (r'\b(three\.?js|3d|webgl|babylon|aframe)\b',
         "three.js examples + GitHub", "threejs.org/examples/ + github search"),
        (r'\b(d3|chart|graph|visualization|визуализаци|диаграмм|график)\b',
         "Observable / D3 Gallery", "observablehq.com/search?query=[task]"),
        (r'\b(icon|иконк|svg|sprite|emoji|pictogram)\b',
         "Iconify / Lucide / Heroicons", "icones.js.org/search?q=[task]"),
        (r'\b(font|шрифт|typography|типографик)\b',
         "Google Fonts / Fontsource", "fonts.google.com / fontsource.org"),
        (r'\b(color|цвет|палитр|gradient|градиент|oklch|hsl)\b',
         "Coolors / Color Hunt / OKLCH", "coolors.co / colorhunt.co"),
        (r'\b(illustration|иллюстраци|vector|вектор|svg\s+art)\b',
         "unDraw / Storyset / Humaaans", "undraw.co/search"),
        (r'\b(звук|sound|audio|sfx|music|notification\s+sound)\b',
         "Freesound / Mixkit", "freesound.org/search/?q=[task]"),
        (r'\b(lottie|motion|micro.?interaction|micro.?animation)\b',
         "LottieFiles", "lottiefiles.com/search?q=[task]"),
    ]

    # ── Templates / starters ───────────────────────────────────────────
    TEMPLATE_CHECKS = [
        (r'\b(template|шаблон|boilerplate|starter|scaffold|skeleton|каркас|archetype)\b',
         "GitHub Templates + Awesome lists", "github.com/topics/[task]-template"),
        (r'\b(landing|лендинг|homepage|промо.?страниц)\b',
         "HTML5 UP / Tailwind Templates", "html5up.net + tailwindui.com"),
        (r'\b(admin|dashboard|дашборд|панель\s+управлени|backoffice)\b',
         "AdminLTE / Tremor / Refine", "github.com/topics/admin-dashboard"),
        (r'\b(email\s+template|письм[оа]\s+шаблон|newsletter)\b',
         "MJML / React Email / Maizzle", "github.com/topics/email-template"),
    ]

    # ── Knowledge / docs / best practices ──────────────────────────────
    KNOWLEDGE_CHECKS = [
        (r'\b(best\s+practice|лучш\w+\s+практик|паттерн|pattern|архитектур|design\s+pattern)\b',
         "Awesome lists + Refactoring.Guru", "github.com/topics/awesome + refactoring.guru"),
        (r'\b(туториал|tutorial|guide|гайд|how.?to|руководств)\b',
         "Dev.to / FreeCodeCamp / MDN", "dev.to/search?q=[task]"),
        (r'\b(cheatsheet|шпаргалк|справочник|reference)\b',
         "devhints.io / tldr-pages", "devhints.io/[task]"),
        (r'\b(курс|course|learn|обучени|изучить)\b',
         "FreeCodeCamp / Exercism / Egghead", "freecodecamp.org + exercism.org"),
    ]

    # ── API / integration ──────────────────────────────────────────────
    API_CHECKS = [
        (r'\b(telegram|телеграм|тг\s*бот|tg\s*bot)\b',
         "Telegram Bot API examples + PTB", "github.com/python-telegram-bot/python-telegram-bot/tree/master/examples"),
        (r'\b(discord)\b',
         "discord.js guide + discord.py", "discordjs.guide + discordpy.readthedocs.io"),
        (r'\b(slack)\b',
         "Slack Bolt SDK", "github.com/slackapi/bolt-python"),
        (r'\b(stripe|платёж|оплат|payment)\b',
         "Stripe docs + examples", "stripe.com/docs + github.com/stripe-samples"),
        (r'\b(firebase|supabase|pocketbase|appwrite)\b',
         "Official docs + community tools", "[platform].com/docs + awesome-[platform]"),
        (r'\b(openai|gpt|llm|langchain|llamaindex|anthropic)\b',
         "LangChain Hub + Awesome LLM", "smith.langchain.com/hub + github.com/topics/awesome-llm"),
        (r'\b(oauth|auth|sso|jwt|авторизаци|аутентификаци)\b',
         "Auth.js / Lucia / Passport.js / Official SDK", "authjs.dev + lucia-auth.com"),
        (r'\b(s3|cloudflare|aws|gcp|azure)\b',
         "Official SDK + Terraform modules", "registry.terraform.io + official docs"),
        (r'\b(webhook|вебхук)\b',
         "Svix / Hookdeck / ngrok", "github.com/topics/webhook"),
        (r'\b(email|smtp|почт[аеу]|рассылк)\b',
         "Nodemailer / Resend / React Email", "github.com/topics/email + resend.com"),
        (r'\b(sms|push\s*notification|пуш)\b',
         "Twilio / OneSignal / Firebase FCM", "twilio.com/docs + onesignal.com"),
        (r'\b(pdf|генераци\w+\s+pdf|pdf\s+generat)\b',
         "Puppeteer PDF / WeasyPrint / jsPDF", "github.com/topics/pdf-generation"),
        (r'\b(excel|xlsx|csv|spreadsheet|таблиц\w+\s+файл)\b',
         "SheetJS / OpenPyXL / Pandas", "github.com/topics/excel"),
        (r'\b(qr|qr.?code|штрих.?код|barcode)\b',
         "QRCode.js / python-qrcode / zxing", "github.com/topics/qrcode"),
        (r'\b(map|карт[ау]|geolocation|геолокаци|leaflet|mapbox)\b',
         "Leaflet / MapLibre / Deck.gl", "leafletjs.com + github.com/topics/maps"),
        (r'\b(calendar|календар|date.?picker|datepicker)\b',
         "FullCalendar / react-datepicker", "github.com/topics/calendar"),
        (r'\b(markdown|md\s+editor|wysiwyg|rich.?text|редактор\s+текст)\b',
         "TipTap / Lexical / Milkdown / Toast UI", "github.com/topics/rich-text-editor"),
        (r'\b(file\s+upload|загрузк\w+\s+файл|drag.?drop\s+upload|uploader)\b',
         "Filepond / Uppy / Dropzone", "github.com/topics/file-upload"),
        (r'\b(image\s+crop|обрезк\w+\s+фото|resize|ресайз|compress\w*\s+image)\b',
         "Sharp / Cropper.js / Squoosh", "github.com/topics/image-processing"),
        (r'\b(video\s+player|видео.?плеер|streaming|стриминг)\b',
         "Video.js / Plyr / hls.js", "github.com/topics/video-player"),
        (r'\b(chat|чат|real.?time\s+messag|мессенджер)\b',
         "Stream Chat / Socket.io / Ably", "getstream.io + socket.io"),
        (r'\b(search|поиск|full.?text|полнотекстов|autocomplete|автозаполнени)\b',
         "MeiliSearch / Typesense / Fuse.js / Algolia", "github.com/topics/search-engine"),
        (r'\b(i18n|l10n|локализаци|перевод|internationalization|translate)\b',
         "i18next / FormatJS / Paraglide", "github.com/topics/i18n"),
        (r'\b(form\s+valid|валидаци\w+\s+форм|zod|yup|ajv|joi)\b',
         "Zod / Yup / Valibot / AJV", "github.com/topics/validation"),
        (r'\b(state\s+manag|стейт|zustand|redux|pinia|jotai|recoil)\b',
         "Zustand / Pinia / Jotai / XState", "github.com/topics/state-management"),
        (r'\b(toast|notification\s+ui|snackbar|уведомлени\w+\s+ui)\b',
         "Sonner / React Hot Toast / Notistack", "github.com/topics/toast"),
        (r'\b(table|data.?grid|data.?table|таблиц\w+\s+компонент)\b',
         "TanStack Table / AG Grid / Tabulator", "github.com/topics/data-table"),
        (r'\b(carousel|карусел|swiper|slider|слайдер)\b',
         "Swiper / Embla / Keen-Slider / Splide", "github.com/topics/carousel"),
        (r'\b(modal|модальн|dialog|диалог\w+\s+окн)\b',
         "Headless UI / Radix Dialog / SweetAlert2", "github.com/topics/modal"),
    ]

    all_checks = (
        REGISTRY_CHECKS + PLATFORM_CHECKS + CREATIVE_CHECKS
        + TEMPLATE_CHECKS + KNOWLEDGE_CHECKS + API_CHECKS
    )

    for pattern, source, query in all_checks:
        if re.search(pattern, text, re.I):
            sources.add(source)
            if query:
                queries.append(query)

    return " · ".join(sorted(sources)), queries


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = (
        data.get("user_message")
        or data.get("user_prompt")
        or data.get("prompt")
        or ""
    ).strip()

    if not prompt or len(prompt) < 15:
        return

    prompt_lower = prompt.lower()

    # ── SKIP check ─────────────────────────────────────────────────────
    for skip in SKIP_PATTERNS:
        if re.search(skip, prompt_lower, re.IGNORECASE):
            return

    # ── Signal detection ───────────────────────────────────────────────
    has_create_verb = bool(
        re.search(CREATE_VERBS_RU, prompt_lower, re.I)
        or re.search(CREATE_VERBS_EN, prompt_lower, re.I)
    )
    has_object_noun = bool(
        re.search(OBJECT_NOUNS_RU, prompt_lower, re.I)
        or re.search(OBJECT_NOUNS_EN, prompt_lower, re.I)
    )
    has_standalone = any(
        re.search(p, prompt_lower, re.I) for p in STANDALONE_TRIGGERS
    )
    has_tech = bool(re.search(TECH_KEYWORDS, prompt_lower, re.I))
    has_domain = any(
        re.search(p, prompt_lower, re.I) for p in DOMAIN_PHRASES
    )

    # ── TRIGGER LOGIC (6 комбинаций) ───────────────────────────────────
    reasons = []
    if has_create_verb and has_object_noun:  reasons.append("verb+noun")
    if has_standalone:                       reasons.append("standalone")
    if has_create_verb and has_tech:         reasons.append("verb+tech")
    if has_tech and has_object_noun:         reasons.append("tech+noun")
    if has_domain:                           reasons.append("domain")
    if has_create_verb and len(prompt) > 60: reasons.append("verb+long")

    if not reasons:
        return

    # ── Output ─────────────────────────────────────────────────────────
    where_sources, where_queries = where_to_search(prompt_lower)
    reason_str = "+".join(reasons)

    print(
        f"\n\U0001f50d [REUSE_FIRST] \u0418\u0449\u0438 \u0433\u043e\u0442\u043e\u0432\u043e\u0435 \u2192 {where_sources}\n",
        file=sys.stderr,
    )

    # Build deep search queries block
    q_block = ""
    if where_queries:
        q_lines = " | ".join(where_queries[:6])
        q_block = f" Конкретные источники: {q_lines}."

    hint = (
        f"[REUSE_FIRST] ({reason_str}) "
        f"СТОП! Перед написанием ЛЮБОГО кода — ОБЯЗАТЕЛЬНЫЙ 3-этапный поиск готовых реализаций.\n"
        f"\n"
        f"## ЭТАП 1 — Прямой поиск готового (БЛОКЕР)\n"
        f"Выполни 2-3 WebSearch запроса:\n"
        f"  - \"[суть задачи] github stars:>50\"\n"
        f"  - \"[суть задачи] npm package\" / \"pip install [задача]\"\n"
        f"  - \"awesome [тема]\" / \"[задача] library 2025\"\n"
        f"Где искать: {where_sources}.{q_block}\n"
        f"\n"
        f"## ЭТАП 2 — Оценка найденного\n"
        f"  \u2705 100+ stars, активный, MIT/Apache \u2192 ИСПОЛЬЗОВАТЬ. Не писать своё. [УЛЬТИМАТИВНЫЙ ПРИОРИТЕТ]\n"
        f"  \u26a0\ufe0f 20-100 stars, покрывает 50%+ \u2192 Взять как базу, адаптировать.\n"
        f"  \u274c Ничего подходящего \u2192 перейти к Этапу 3.\n"
        f"\n"
        f"## ЭТАП 3 — Референсы и best practices (если готового нет)\n"
        f"  - \"[задача] best practices 2025\"\n"
        f"  - \"[задача] tutorial\" / \"how to [задача]\"\n"
        f"  - \"[задача] example code\" / \"[задача] implementation guide\"\n"
        f"  Писать на основе найденных референсов, НЕ из памяти.\n"
        f"\n"
        f"## ОТЧЁТ (обязательно в начале ответа)\n"
        f"\U0001f50d Поиск: [что искал]\n"
        f"  \u251c\u2500 \u2705 Найдено: [название] (\u2b50 N, ссылка) \u2192 использую\n"
        f"  \u251c\u2500 \u26a0\ufe0f Частичное: [название] \u2192 беру как базу\n"
        f"  \u2514\u2500 \u274c Не найдено \u2192 пишу с нуля, референсы: [ссылки]\n"
        f"\n"
        f"ГОТОВОЕ РЕШЕНИЕ = УЛЬТИМАТИВНЫЙ ПРИОРИТЕТ. НЕ НАЧИНАЙ писать код пока не выполнил все 3 этапа."
    )
    print(json.dumps({"injectedSystemPrompt": hint}, ensure_ascii=False))


if __name__ == "__main__":
    main()
