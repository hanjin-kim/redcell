"""CJK leakage scrubber — final pass before writing markdown output.

Qwen (and other multilingual models) occasionally emit Chinese / Japanese
ideographs inside Korean text — typically Chinese tokens that share
semantics with the intended Korean word ("与此同时" instead of "동시에",
"现金" instead of "현금", etc.). The upstream prompts in
``redcell/sim/`` ask for Korean explicitly but the model still leaks.

This module runs a paragraph-level scrub: any paragraph that contains
non-Hangul CJK characters is sent back to the LLM with a strict
"Korean only, preserve formatting" instruction. Paragraphs without
leakage are passed through unchanged so cost stays minimal.

Detection regex: ``[一-鿿]`` — the CJK Unified Ideographs basic
block. This includes Korean Hanja, but modern Korean business writing
uses Hangul almost exclusively, so any Hanja in a redcell brief is
almost certainly a model leak.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Callable

logger = logging.getLogger(__name__)

# CJK Unified Ideographs basic block — catches both simplified Chinese
# and traditional Hanja. Hangul is in U+AC00-U+D7A3 and not matched here.
CJK_RE = re.compile(r"[一-鿿]")


def has_cjk(text: str) -> bool:
    return bool(CJK_RE.search(text))


def _scrub_paragraph(snippet: str, llm: Any) -> str:
    """Send one CJK-tainted paragraph to the LLM for rewrite.

    Returns the rewritten text. If the LLM's reply still contains CJK
    characters, logs a warning and returns the LLM reply anyway — partial
    cleanup is better than no cleanup. If the LLM call itself fails, the
    exception propagates so the caller (and the user) knows the scrub
    didn't run.
    """
    prompt = (
        "다음 한국어 문서 단편(snippet)에 중국어/일본어 한자가 섞여있다. "
        "이를 자연스러운 한국어로 바꿔라.\n"
        "- 마크다운 포맷 (헤더, 표, 볼드, 인용 등) 은 그대로 유지\n"
        "- 영어 고유명사 / 숫자 / 코드 / URL 은 손대지 말 것\n"
        "- 한국어 한자(漢字) 표기도 모두 한글로 풀어 쓸 것\n"
        "- 의미가 불분명한 단발 한자는 문맥상 가장 자연스러운 한국어로 추정해 대체\n"
        "- 추가 설명·주석 없이 *수정된 텍스트만* 그대로 출력\n\n"
        "원문:\n"
        f"{snippet}"
    )
    result = llm.complete(
        system="당신은 한국어 텍스트 교정기. 한국어(한글)로만 답한다. "
               "중국어·일본어·한자 절대 사용 금지.",
        user=prompt,
        temperature=0.0,
        max_tokens=max(800, len(snippet) // 2 + 400),
    )
    if has_cjk(result):
        logger.warning(
            "CJK scrub: paragraph still has %d CJK chars after rewrite",
            len(CJK_RE.findall(result)),
        )
    return result


def scrub_cjk_leakage(
    text: str,
    llm: Any,
    *,
    log: Callable[[str], None] = lambda _msg: None,
) -> str:
    """Paragraph-level CJK scrub. Returns the scrubbed text.

    If ``text`` has no CJK, returns it unchanged (no LLM calls). Otherwise,
    splits on blank lines, scrubs only the dirty paragraphs, reassembles.
    Logs a one-line summary via ``log``.
    """
    if not has_cjk(text):
        return text

    paragraphs = text.split("\n\n")
    n_dirty = 0
    n_total = len(paragraphs)
    out: list[str] = []
    for para in paragraphs:
        if has_cjk(para):
            n_dirty += 1
            out.append(_scrub_paragraph(para, llm))
        else:
            out.append(para)
    scrubbed = "\n\n".join(out)
    residual = len(CJK_RE.findall(scrubbed))
    log(
        f"[redcell] CJK scrub: {n_dirty}/{n_total} paragraphs rewritten, "
        f"{residual} CJK chars remaining"
    )
    return scrubbed
