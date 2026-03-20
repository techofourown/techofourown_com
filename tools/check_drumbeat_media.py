#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "src" / "content" / "drumbeat"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SAFE_SHARE_RATIO_MIN = 1.85
SAFE_SHARE_RATIO_MAX = 1.97


@dataclass
class EntryReport:
    slug: str
    title: str
    path: Path
    frontmatter: dict
    published: bool
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    card_path: Path | None = None
    share_path: Path | None = None
    cover_path: Path | None = None
    card_ratio: float | None = None
    share_ratio: float | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Drumbeat media roles and create preview artifacts.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when hard failures are present.")
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("/tmp/drumbeat-media-report"),
        help="Directory to write preview artifacts and summary output.",
    )
    return parser.parse_args()


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = load_font(44, bold=True)
FONT_SUBTITLE = load_font(28)
FONT_LABEL = load_font(22, bold=True)
FONT_META = load_font(18)


def extract_frontmatter(path: Path) -> dict:
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"{path} is missing YAML frontmatter")
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} frontmatter did not parse to an object")
    return data


def resolve_media_path(entry_path: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return (entry_path.parent / value).resolve()


def image_ratio(path: Path) -> float:
    with Image.open(path) as image:
        width, height = image.size
    return width / height


def same_path(a: Path | None, b: Path | None) -> bool:
    return a is not None and b is not None and a.resolve() == b.resolve()


def parse_position(value: str | None) -> tuple[float, float]:
    if not value:
        return (0.5, 0.5)

    tokens = value.replace(",", " ").split()
    if not tokens:
        return (0.5, 0.5)

    def parse_token(token: str, axis: str) -> float:
        token = token.lower()
        keyword_map = {
            "left": 0.0,
            "center": 0.5,
            "right": 1.0,
            "top": 0.0,
            "bottom": 1.0,
        }
        if token in keyword_map:
            return keyword_map[token]
        match = re.fullmatch(r"(\d+(?:\.\d+)?)%", token)
        if match:
            return max(0.0, min(1.0, float(match.group(1)) / 100.0))
        if token == "middle":
            return 0.5
        if axis == "x" and token in {"start", "west"}:
            return 0.0
        if axis == "x" and token in {"end", "east"}:
            return 1.0
        return 0.5

    if len(tokens) == 1:
        only = parse_token(tokens[0], "x")
        return (only, 0.5)

    return (parse_token(tokens[0], "x"), parse_token(tokens[1], "y"))


def validate_entry(entry_path: Path) -> EntryReport:
    frontmatter = extract_frontmatter(entry_path)
    slug = entry_path.stem
    title = str(frontmatter.get("title", slug))
    published = not bool(frontmatter.get("draft", False))
    report = EntryReport(slug=slug, title=title, path=entry_path, frontmatter=frontmatter, published=published)

    if not published:
        return report

    cover_path = resolve_media_path(entry_path, frontmatter.get("coverImage"))
    card_path = resolve_media_path(entry_path, frontmatter.get("cardImage"))
    share_path = resolve_media_path(entry_path, frontmatter.get("shareImage"))
    report.cover_path = cover_path
    report.card_path = card_path
    report.share_path = share_path

    if cover_path is None:
        report.failures.append("coverImage is missing.")
    elif not cover_path.exists():
        report.failures.append(f"coverImage file not found: {frontmatter.get('coverImage')}")

    if card_path is None:
        report.failures.append("cardImage is missing.")
    elif not card_path.exists():
        report.failures.append(f"cardImage file not found: {frontmatter.get('cardImage')}")

    if share_path is None:
        report.failures.append("shareImage is missing.")
    elif not share_path.exists():
        report.failures.append(f"shareImage file not found: {frontmatter.get('shareImage')}")

    if "cardImageFit" not in frontmatter:
        report.failures.append("cardImageFit is missing.")

    card_fit = frontmatter.get("cardImageFit")
    if card_fit not in {"cover", "contain", None}:
        report.failures.append(f"cardImageFit has invalid value: {card_fit}")

    if card_path and card_path.exists():
        report.card_ratio = image_ratio(card_path)
        if card_fit == "cover":
            if report.card_ratio < 1.0 or report.card_ratio > 1.9:
                report.failures.append(
                    f"cardImage ratio {report.card_ratio:.2f} is outside the hard cover range 1.00 to 1.90."
                )
            if report.card_ratio < 1.0 and not frontmatter.get("cardImagePosition"):
                report.failures.append("portrait cover cardImage is missing cardImagePosition.")
            if report.card_ratio < 1.2 or report.card_ratio > 1.6:
                report.warnings.append(
                    f"cover cardImage ratio {report.card_ratio:.2f} is outside the preferred range 1.20 to 1.60."
                )
        elif card_fit == "contain":
            if report.card_ratio < 1.4 or report.card_ratio > 2.0:
                report.warnings.append(
                    f"contain cardImage ratio {report.card_ratio:.2f} is outside the preferred range 1.40 to 2.00."
                )

    if share_path and share_path.exists():
        report.share_ratio = image_ratio(share_path)
        if report.share_ratio < SAFE_SHARE_RATIO_MIN or report.share_ratio > SAFE_SHARE_RATIO_MAX:
            report.failures.append(
                f"shareImage ratio {report.share_ratio:.2f} is outside the allowed range "
                f"{SAFE_SHARE_RATIO_MIN:.2f} to {SAFE_SHARE_RATIO_MAX:.2f}."
            )

    if str(frontmatter.get("format")) == "text" and same_path(card_path, cover_path):
        report.warnings.append("text post is reusing coverImage as cardImage; a dedicated card asset is preferred.")

    return report


def open_rgb(path: Path) -> Image.Image:
    with Image.open(path) as image:
        return ImageOps.exif_transpose(image).convert("RGB")


def draw_placeholder(size: tuple[int, int], message: str, background: str = "#f4f7fb") -> Image.Image:
    image = Image.new("RGB", size, ImageColor.getrgb(background))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline="#cbd5e1", width=2)
    wrapped = textwrap.fill(message, width=max(12, size[0] // 16))
    draw.multiline_text((size[0] // 2, size[1] // 2), wrapped, fill="#475569", font=FONT_META, anchor="mm", align="center")
    return image


def render_card_slot(
    image_path: Path | None,
    size: tuple[int, int],
    fit: str | None,
    position: str | None,
) -> Image.Image:
    if image_path is None or not image_path.exists():
        return draw_placeholder(size, "Missing cardImage")

    if fit == "contain":
        panel = Image.new("RGB", size, ImageColor.getrgb("#eef3f8"))
        image = open_rgb(image_path)
        inner_pad = 18
        inner_size = (max(1, size[0] - inner_pad * 2), max(1, size[1] - inner_pad * 2))
        contained = ImageOps.contain(image, inner_size, Image.Resampling.LANCZOS)
        x = (size[0] - contained.width) // 2
        y = (size[1] - contained.height) // 2
        panel.paste(contained, (x, y))
    else:
        image = open_rgb(image_path)
        panel = ImageOps.fit(
            image,
            size,
            Image.Resampling.LANCZOS,
            centering=parse_position(position),
        )

    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline="#dbeafe", width=3)
    return panel


def render_share_slot(image_path: Path | None, size: tuple[int, int]) -> Image.Image:
    if image_path is None or not image_path.exists():
        return draw_placeholder(size, "Missing shareImage")

    panel = Image.new("RGB", size, ImageColor.getrgb("#f8fafc"))
    image = open_rgb(image_path)
    contained = ImageOps.contain(image, size, Image.Resampling.LANCZOS)
    x = (size[0] - contained.width) // 2
    y = (size[1] - contained.height) // 2
    panel.paste(contained, (x, y))

    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline="#cbd5e1", width=2)
    safe_x = int(size[0] * 0.06)
    safe_y = int(size[1] * 0.08)
    draw.rectangle((safe_x, safe_y, size[0] - safe_x, size[1] - safe_y), outline="#2563eb", width=3)
    return panel


def status_text(report: EntryReport) -> str:
    if report.failures:
        return "FAIL"
    if report.warnings:
        return "WARN"
    return "PASS"


def build_entry_report(report: EntryReport, output_path: Path) -> None:
    width, height = 1680, 610
    canvas = Image.new("RGB", (width, height), ImageColor.getrgb("#ffffff"))
    draw = ImageDraw.Draw(canvas)

    draw.text((40, 34), report.title, fill="#0f172a", font=FONT_TITLE)
    subtitle = f"{report.slug}  •  {status_text(report)}  •  {len(report.failures)} failure(s), {len(report.warnings)} warning(s)"
    draw.text((40, 92), subtitle, fill="#475569", font=FONT_SUBTITLE)

    slots = [
        ("Card 4:3", (40, 150), (420, 315), render_card_slot(report.card_path, (420, 315), report.frontmatter.get("cardImageFit"), report.frontmatter.get("cardImagePosition"))),
        ("Card 16:10", (500, 150), (504, 315), render_card_slot(report.card_path, (504, 315), report.frontmatter.get("cardImageFit"), report.frontmatter.get("cardImagePosition"))),
        ("Share 1200×630", (1044, 150), (600, 315), render_share_slot(report.share_path, (600, 315))),
    ]

    for label, origin, _size, panel in slots:
        draw.text((origin[0], 120), label, fill="#2563eb", font=FONT_LABEL)
        canvas.paste(panel, origin)

    details = []
    if report.card_ratio is not None:
        details.append(f"card ratio: {report.card_ratio:.2f}")
    if report.share_ratio is not None:
        details.append(f"share ratio: {report.share_ratio:.2f}")
    if report.frontmatter.get("cardImageFit"):
        details.append(f"fit: {report.frontmatter.get('cardImageFit')}")
    if report.frontmatter.get("cardImagePosition"):
        details.append(f"position: {report.frontmatter.get('cardImagePosition')}")
    draw.text((40, 500), "  •  ".join(details) if details else "No media metadata found.", fill="#475569", font=FONT_META)

    lines: list[tuple[str, str]] = []
    lines.extend(("FAIL", item) for item in report.failures)
    lines.extend(("WARN", item) for item in report.warnings)
    if not lines:
        lines.append(("PASS", "No issues found."))

    y = 530
    for kind, message in lines[:4]:
        fill = "#b91c1c" if kind == "FAIL" else "#b45309" if kind == "WARN" else "#166534"
        wrapped = textwrap.fill(message, width=100)
        draw.multiline_text((40, y), f"{kind}: {wrapped}", fill=fill, font=FONT_META, spacing=4)
        y += 28 * (wrapped.count("\n") + 1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)


def build_montage(report_paths: list[Path], output_path: Path) -> None:
    if not report_paths:
        return

    images = [Image.open(path).convert("RGB") for path in report_paths]
    try:
        width = max(image.width for image in images)
        gap = 20
        height = sum(image.height for image in images) + gap * (len(images) + 1)
        montage = Image.new("RGB", (width + 40, height), ImageColor.getrgb("#eef2f7"))
        y = gap
        for image in images:
            montage.paste(image, (20, y))
            y += image.height + gap
        output_path.parent.mkdir(parents=True, exist_ok=True)
        montage.save(output_path)
    finally:
        for image in images:
            image.close()


def write_summary(reports: list[EntryReport], summary_path: Path) -> None:
    lines = []
    failure_count = 0
    warning_count = 0

    for report in reports:
        if not report.published:
            continue
        failure_count += len(report.failures)
        warning_count += len(report.warnings)
        lines.append(f"{report.slug}: {status_text(report)}")
        if report.card_ratio is not None:
            lines.append(f"  card ratio: {report.card_ratio:.2f}")
        if report.share_ratio is not None:
            lines.append(f"  share ratio: {report.share_ratio:.2f}")
        for item in report.failures:
            lines.append(f"  FAIL: {item}")
        for item in report.warnings:
            lines.append(f"  WARN: {item}")
        if not report.failures and not report.warnings:
            lines.append("  PASS: No issues found.")
        lines.append("")

    lines.append(f"Total failures: {failure_count}")
    lines.append(f"Total warnings: {warning_count}")
    summary_path.write_text("\n".join(lines).rstrip() + "\n")


def main() -> int:
    args = parse_args()
    report_dir = args.report_dir
    if report_dir.exists():
        shutil.rmtree(report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    entries_dir = report_dir / "entries"
    entries_dir.mkdir(parents=True, exist_ok=True)

    entry_paths = sorted(CONTENT_DIR.glob("*.md"))
    reports = []
    for path in entry_paths:
        try:
            reports.append(validate_entry(path))
        except Exception as exc:
            reports.append(
                EntryReport(
                    slug=path.stem,
                    title=path.stem,
                    path=path,
                    frontmatter={},
                    published=True,
                    failures=[f"Could not validate entry: {exc}"],
                )
            )
    published_reports = [report for report in reports if report.published]

    report_paths = []
    for report in published_reports:
        output_path = entries_dir / f"{report.slug}.png"
        build_entry_report(report, output_path)
        report_paths.append(output_path)

    build_montage(report_paths, report_dir / "montage.png")
    write_summary(published_reports, report_dir / "summary.txt")

    total_failures = sum(len(report.failures) for report in published_reports)
    total_warnings = sum(len(report.warnings) for report in published_reports)

    print(f"Checked {len(published_reports)} published Drumbeat entries.")
    print(f"Failures: {total_failures}")
    print(f"Warnings: {total_warnings}")
    print(f"Report directory: {report_dir}")

    for report in published_reports:
        print(f"- {report.slug}: {status_text(report)}")
        for item in report.failures:
            print(f"  FAIL: {item}")
        for item in report.warnings:
            print(f"  WARN: {item}")

    if args.strict and total_failures > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
