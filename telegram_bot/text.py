standard_subscripition = (
    "*Standard Subscription*:\n"
    "- 5 dollars per month\n"
    "- Unlimited chat with the bot\n"
    "- 50,000 tokens per month (approximately 40,000 words)\n"
    "- Access to all basic features\n"
)

pro_subscription = (
    "*Pro Subscription*:\n"
    "- 10 dollars per month\n"
    "- All Standard Subscription features\n"
    "- Double the tokens: 100,000 tokens per month (approximately 80,000 words)\n"
    "- Additional 20,000 tokens per month\n"
    "- Faster response time\n"
    "- Priority access to new features and updates\n"
)

subscription_note = "*Note*: _If you exceed your monthly token limit, you won't be able to use the service until the next month. However, your subscription will remain active. If your subscription expires but you still have remaining tokens, these tokens will be retained when you resubscribe._"

subscription_text = (
    standard_subscripition + "\n" + pro_subscription + "\n" + subscription_note
)


bot_text = {
    "en": {
        "main_menu_text": (
            "*OpenAI GPT-3.5 DALL-E Bot*(Beta)\n"
            "*NOTE*: _The bot now implements the GPT-3.5 model and real chat feature like ChatGPT._\n"
            "\n"
            "👋 Hi, I am a bot that uses OpenAI GPT-3.5 and DALL-E to help you.\n"
            "\n"
            "🤔 *What can I do?*\n"
            "🤖 Chat with me\n"
            "🔎 Find answers\n"
            "📚 Write academic essays\n"
            "💻 Programming code\n"
            "👩‍💻 Write emails and letters\n"
            "🌎 Translate and chat in any language\n"
            "🖼 Generate images\n"
            "\n"
            "📚 *How to use?*\n"
            "*/chat* - _Have a conversation with me._\n"
            "\n"
            "*/ask* - _ Ask anything you want._\n"
            "\n"
            "*/images* - _Generate images with prompt._\n"
            "\n"
            "*/help* - _Find assistance for your querie._\n"
            "\n"
            "Contact: fengrongman@gmail.com\n"
        ),
        "main_menu_buttons_text": {
            "ask": "You can ask me anything.",
            "chat": "Let's chat.",
            "images": "Give me a prompt and I will generate the image. The generation process may take a while.",
            "chat_help": (
                "/chat\n"
                "   *start a chat* - _You can use the chat command and I will have a chat with you. "
            ),
            "images_help": (
                "/images\n"
                "   *generate images* - _You can use the images command then input something then generate images._\n"
            ),
            "ask_help": (
                "/ask\n"
                "   *ask me anything* - _You can use the ask command then input something then I will answer._\n"
            ),
            "help": "Instruction",
        },
        "button_text": {
            "ask": "💬Ask",
            "chat": "📢Chat",
            "images": "🎨Images",
            "help": "❓Help",
            "subscription": "🌟 Subscription(TEST)",
            "language": "🌎  Language",
        },
        "command_description_text": {
            "chat": "Have a conversation with me.",
            "ask": "Ask anything you want.",
            "images": "Generate images with prompt.",
            "help": "Find assistance for your querie.",
        },
        "token_limit_text": (
            "*Token limit*\n"
            "_Since the token of the current prompt has exceeded the limit_\n"
            "_You can reduce the length of the input or start a new conversation with /chat_"
        ),
        "choose_language_text": (
            "*Choose a language*\n"
            "You can choose a language to chat with me.\n"
        ),
    },
    "zh": {
        "main_menu_text": (
            "*OpenAI GPT-3.5 DALL-E Bot*(Beta)\n"
            "*注意*: _该机器人现在实现了 GPT-3.5 模型和 ChatGPT 类似的真实聊天功能_\n"
            "\n"
            "👋 你好,我是一个使用 OpenAI GPT-3.5 和 DALL-E 的机器人,可以帮助你。\n"
            "\n"
            "🤔 *我能做什么？*\n"
            "🤖 与我聊天\n"
            "🔎 寻找答案\n"
            "📚 写学术论文\n"
            "💻 编程代码\n"
            "👩‍💻 写电子邮件和信件\n"
            "🌎 翻译并使用任何语言聊天\n"
            "🖼 生成图像\n\n"
            "📚 *如何使用？*:\n"
            "*/chat* - 与我对话。\n"
            "\n"
            "*/ask* - 问任何你想知道的问题。\n"
            "\n"
            "*/images* - 根据你的输入生成图像。\n"
            "\n"
            "*/help* - 找到你的问题的帮助。\n"
            "\n"
            "联系方式: fengrongman@gmail.com\n"
        ),
        "main_menu_buttons_text": {
            "ask": "你可以问我任何问题。",
            "chat": "让我们聊天。",
            "images": "给我一个提示,我会生成图片。生成过程可能需要一些时间。",
            "chat_help": ("/chat\n" "   *开始聊天* - _你可以使用聊天命令,我会和你聊天。_"),
            "images_help": (
                "/images\n" "   *生成图片* - _你可以使用图片命令,然后输入一些内容,然后生成图片。_\n"
            ),
            "ask_help": (
                "/ask\n" "   *问我任何问题* - _你可以使用 ask 命令,然后输入问题,然后我会回答。_\n"
            ),
            "help": "帮助",
        },
        "button_text": {
            "ask": "💬提问",
            "chat": "📢聊天",
            "images": "🎨图片",
            "help": "❓帮助",
            "subscription": "🌟 订阅(TEST)",
            "language": "🌎  语言",
        },
        "command_description_text": {
            "chat": "开始聊天。",
            "ask": "问任何你想知道的问题。",
            "images": "根据你的输入生成图像。",
            "help": "找到你的问题的帮助。",
        },
        "token_limit_text": (
            "*令牌限制*\n" "_由于当前提示的令牌已超过限制_\n" "_您可以缩短输入的长度或使用 /chat 开始新的对话_"
        ),
        "choose_language_text": ("*选择语言*\n" "你可以选择一种语言与我聊天。\n"),
    },
    "zh-hk": {
        "main_menu_text": (
            "*OpenAI GPT-3.5 DALL-E Bot*(Beta)\n"
            "*注意*: _該機器人現在實現了 GPT-3.5 模型和 ChatGPT 類似的真實聊天功能_\n"
            "\n"
            "👋 你好,我是一個使用 OpenAI GPT-3.5 和 DALL-E 的機器人,可以幫助你。\n"
            "\n"
            "🤔 *我能做什麼？*\n"
            "🤖 與我聊天\n"
            "🔎 尋找答案\n"
            "📚 寫學術論文\n"
            "💻 編程代碼\n"
            "👩‍💻 寫電子郵件和信件\n"
            "🌎 翻譯並使用任何語言聊天\n"
            "🖼 生成圖像\n"
            "\n"
            "📚 *點樣用啊*:\n"
            "*/chat* - 與我對話。\n"
            "\n"
            "*/ask* - 問任何你想知道的問題。\n"
            "\n"
            "*/images* - 根據你的輸入生成圖像。\n"
            "\n"
            "*/help* - 找到你的問題的幫助。\n"
            "\n"
            "聯繫方式: fengrongman@gmail.com\n"
        ),
        "main_menu_buttons_text": {
            "ask": "你可以問我任何問題。",
            "chat": "讓我們聊天。",
            "images": "給我一個提示,我會生成圖片。生成過程可能需要一些時間。",
            "chat_help": ("/chat\n" "   *開始聊天* - _你可以使用聊天命令,我會和你聊天。_"),
            "images_help": (
                "/images\n" "   *生成圖片* - _你可以使用圖片命令,然後輸入一些內容,然後生成圖片。_\n"
            ),
            "ask_help": (
                "/ask\n" "   *問我任何問題* - _你可以使用 ask 命令,然後輸入問題,然後我會回答。_\n"
            ),
            "help": "幫助",
        },
        "button_text": {
            "ask": "💬提問",
            "chat": "📢聊天",
            "images": "🎨圖片",
            "help": "❓幫助",
            "subscription": "🌟 訂閱(TEST)",
            "language": "🌎  語言",
        },
        "command_description_text": {
            "chat": "開始同我傾計。",
            "ask": "有咩可以幫到你。",
            "images": "根據你的輸入整幅靚相。",
            "help": "幫緊你幫緊你",
        },
        "token_limit_text": (
            "*令牌限制*\n" "_由於當前提示的令牌已超過限制_\n" "_您可以縮短輸入的長度或使用 /chat 開始新的對話_"
        ),
        "choose_language_text": ("*選擇語言*\n" "你可以選擇一種語言與我聊天。\n"),
    },
}
