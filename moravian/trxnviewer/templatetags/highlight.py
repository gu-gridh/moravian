import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, query):
    """
    Highlight all case-insensitive occurrences of all terms of `query` in `text` with <span class="highlight">…</span>. Escapes text to avoid breaking HTML.
    """
    if not text or not query:
        return text

    text = str(text)
    terms = [t for t in query.split() if t]
    pattern = re.compile(r"(" + "|".join(re.escape(t) for t in terms) + r")",
                         re.IGNORECASE)

    def repl(match):
        return f'<span class="highlight">{escape(match.group(0))}</span>'

    return mark_safe(pattern.sub(repl, text))
