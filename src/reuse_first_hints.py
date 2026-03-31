"""
REUSE FIRST — where_to_search() с 60+ контекстными подсказками.

6 категорий: registry, platform, creative, template, knowledge, API.
Возвращает (sources_string, queries_list).
"""
import re


def where_to_search(text):
    """Ультимативный детектор: ГДЕ искать + конкретные поисковые запросы."""
    sources = {"GitHub"}
    queries = []

    # ── Package registries by language ─────────────────────────────────
    REGISTRY_CHECKS = [
        (r'\b(npm|node|js|ts|react|vue|svelte|next|express|typescript|javascript|bun|deno|angular|astro|remix|solid|qwik|nuxt|gatsby|vite|webpack|rollup|esbuild)\b',
         "npmjs.com", "npm search '[task]'"),
        (r'\b(pip|python|django|flask|fastapi|pandas|pytorch|poetry|uv|celery|scrapy|sqlalchemy|pydantic|httpx|aiohttp|beautifulsoup|lxml)\b',
         "PyPI (pypi.org)", "pip search / pypi.org/search/?q=[task]"),
        (r'\b(cargo|rust|actix|axum|tokio|serde|warp|hyper)\b',
         "crates.io", "crates.io/search?q=[task]"),
        (r'\b(nuget|c#|csharp|dotnet|\.net|maui|avalonia|wpf|winforms|blazor|asp\.net)\b',
         "NuGet (nuget.org)", "nuget.org/packages?q=[task]"),
        (r'\b(go|golang|gin|echo|fiber|gorilla|chi|cobra)\b',
         "pkg.go.dev", "pkg.go.dev/search?q=[task]"),
        (r'\b(gem|ruby|rails|sinatra|sidekiq|rspec)\b',
         "RubyGems", "rubygems.org/search?query=[task]"),
        (r'\b(composer|php|laravel|symfony|wordpress|drupal|yii)\b',
         "Packagist", "packagist.org/search/?q=[task]"),
        (r'\b(maven|gradle|java|kotlin|spring|quarkus|micronaut|ktor)\b',
         "Maven Central", "search.maven.org/search?q=[task]"),
        (r'\b(swift|swiftui|cocoapods|spm|vapor|alamofire)\b',
         "Swift Package Index", "swiftpackageindex.com/search?q=[task]"),
        (r'\b(dart|flutter|pub\.dev)\b',
         "pub.dev", "pub.dev/packages?q=[task]"),
        (r'\b(elixir|phoenix|hex\.pm|ecto)\b',
         "hex.pm", "hex.pm/packages?search=[task]"),
    ]

    # ── Specialized platforms ──────────────────────────────────────────
    PLATFORM_CHECKS = [
        (r'\b(docker|k8s|kubernetes|podman|container|helm|compose)\b',
         "Docker Hub", "hub.docker.com/search?q=[task]"),
        (r'\b(ci|cd|action|workflow|pipeline|github\s+action|gitlab\s+ci|jenkins)\b',
         "GitHub Actions Marketplace", "github.com/marketplace?type=actions&query=[task]"),
        (r'\b(claude|claude.?code|mcp|claude.?plugin|anthropic)\b',
         "claude-code-plugins marketplace", "search claude-code-plugins for '[task]'"),
        (r'\b(vscode|vs\s*code|visual\s*studio\s*code)\b',
         "VS Code Marketplace", "marketplace.visualstudio.com/search?term=[task]"),
        (r'\b(jetbrains|intellij|pycharm|webstorm|goland|rider)\b',
         "JetBrains Marketplace", "plugins.jetbrains.com/search?search=[task]"),
        (r'\b(chrome|firefox|browser\s+extension|расширение\s+браузер|addon)\b',
         "Chrome Web Store / Firefox Add-ons", None),
        (r'\b(wordpress|wp\s+plugin|wp\s+theme)\b',
         "WordPress Plugin Directory", "wordpress.org/plugins/search/[task]"),
        (r'\b(terraform|tf\s+module|infrastructure.?as.?code)\b',
         "Terraform Registry", "registry.terraform.io/search/modules?q=[task]"),
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
