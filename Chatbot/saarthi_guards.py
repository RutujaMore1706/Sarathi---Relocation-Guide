from guardrails import Guard
from guardrails.hub import ToxicLanguage
from guardrails.errors import ValidationError
from guardrails.hub import RestrictToTopic
from guardrails.hub import UnusualPrompt
from guardrails.hub import BanList

# Setup Guard
topic_guard = Guard().use(
    RestrictToTopic(
        valid_topics=["apartments", "boston", "apartment hunt", "food", "tourist","rent", "hobbies", "music"],
        invalid_topics=["politics", "nuclear weapons", "Any political leader", "finance"],
        disable_classifier=True,
        disable_llm=False,
        on_fail="exception"
    )
)

guard = Guard().use(
    ToxicLanguage(threshold=0.7, validation_method="sentence", on_fail="exception"
))


# Setup Guard
ban_guard = Guard().use(
    BanList(banned_words=['trump','politics', 'jailbreak', 'system prompt', 'messi', 'weapons', 'drugs'])
)

unusual_guard = Guard().use(UnusualPrompt, on="sentence", on_fail="exception")