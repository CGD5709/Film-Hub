from html import escape


def truncate_title(title: str, max_length: int = 24) -> str:
    """Return a shortened single-line title suitable for a compact SVG badge."""
    cleaned = " ".join((title or "").split())
    if not cleaned:
        return "Dataset"
    if len(cleaned) <= max_length:
        return cleaned
    if max_length <= 3:
        return cleaned[:max_length]
    cutoff = max_length - 3
    return f"{cleaned[:cutoff].rstrip()}..."


def format_downloads(downloads: int) -> str:
    """Format a dataset download counter with singular/plural grammar."""
    count = max(0, int(downloads))
    if count == 1:
        return "1 download"
    return f"{count} downloads"


def _estimate_text_width(text: str, padding: int = 16, min_width: int = 40) -> int:
    """Estimate pixel width for Verdana 11px badge text."""
    return max(min_width, int(len(text) * 6.5) + padding)


def _render_segmented_badge_svg(segments: list[tuple[str, str]], aria_label: str) -> str:
    """Render a flat-style multi-segment shields.io-inspired SVG badge."""
    widths = [_estimate_text_width(text) for text, _ in segments]
    total_width = sum(widths)
    safe_aria = escape(aria_label, quote=True)

    rects = []
    texts = []
    offset = 0
    for (label, color), width in zip(segments, widths):
        safe_label = escape(label, quote=True)
        center_x = offset + width / 2
        rects.append(f'<rect x="{offset}" width="{width}" height="20" fill="{color}"/>')
        texts.append(f'<text x="{center_x:.1f}" y="15" fill="#010101" fill-opacity=".3">{safe_label}</text>')
        texts.append(f'<text x="{center_x:.1f}" y="14">{safe_label}</text>')
        offset += width

    rects_markup = "".join(rects)
    texts_markup = "".join(texts)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20" ',
        f'role="img" aria-label="{safe_aria}">',
        f"<title>{safe_aria}</title>",
        '<linearGradient id="s" x2="0" y2="100%">',
        '<stop offset="0" stop-color="#bbb" stop-opacity=".1"/>',
        '<stop offset="1" stop-opacity=".1"/>',
        "</linearGradient>",
        '<clipPath id="r">',
        f'<rect width="{total_width}" height="20" rx="3" fill="#fff"/>',
        "</clipPath>",
        '<g clip-path="url(#r)">',
        rects_markup,
        f'<rect width="{total_width}" height="20" fill="url(#s)"/>',
        "</g>",
        '<g fill="#fff" text-anchor="middle" ',
        'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">',
        texts_markup,
        "</g>",
        "</svg>",
    ]
    return "".join(parts)


def render_dataset_badge_svg(title: str, doi: str, downloads: int) -> str:
    """Render an XML-valid SVG badge showing short title, DOI and downloads."""
    short_title = truncate_title(title)
    doi_label = f"DOI {doi}"
    downloads_label = format_downloads(downloads)
    aria_label = f"{short_title} | {doi_label} | {downloads_label}"
    segments = [
        (short_title, "#555"),
        (doi_label, "#007ec6"),
        (downloads_label, "#2ea44f"),
    ]
    return _render_segmented_badge_svg(segments, aria_label)


def render_not_found_badge_svg() -> str:
    """Render an XML-valid SVG badge indicating that the DOI does not exist."""
    segments = [
        ("Film-Hub", "#555"),
        ("dataset not found", "#e05d44"),
    ]
    return _render_segmented_badge_svg(segments, "Film-Hub: dataset not found")


def build_badge_snippets(title: str, dataset_url: str, badge_url: str) -> dict[str, str]:
    """Build copyable Markdown and HTML embed snippets linking to the dataset."""
    cleaned_title = " ".join((title or "").split()) or "Dataset"
    md_alt = cleaned_title.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
    html_alt = escape(cleaned_title, quote=True)
    safe_dataset_url = escape(dataset_url, quote=True)
    safe_badge_url = escape(badge_url, quote=True)

    return {
        "markdown": f"[![{md_alt}]({badge_url})]({dataset_url})",
        "html": f'<a href="{safe_dataset_url}"><img src="{safe_badge_url}" alt="{html_alt}" /></a>',
    }
