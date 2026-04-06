#!/usr/bin/env python3
"""Regression checks for persona-aware suggestion filtering helpers."""

import sys

sys.path.insert(0, '.')

from app.api.routes.suggestions import (
    _extract_persona_tags_from_key,
    _infer_form_persona_tags,
    _is_persona_conflict,
    _value_conflicts_with_target_persona,
    _normalize_field_key,
)


def test_extract_persona_tags() -> None:
    lecturer_key = _normalize_field_key('Họ và tên giảng viên')
    student_key = _normalize_field_key('Mã sinh viên')

    assert 'lecturer' in _extract_persona_tags_from_key(lecturer_key)
    assert 'student' in _extract_persona_tags_from_key(student_key)


def test_infer_form_persona_tags() -> None:
    tags = _infer_form_persona_tags([
        'Mã giảng viên',
        'Họ tên giảng viên',
        'Bộ môn công tác',
        'Học vị',
    ])
    assert tags == {'lecturer'}, f'Unexpected form persona tags: {tags}'


def test_persona_conflict_detection() -> None:
    assert _is_persona_conflict({'lecturer'}, {'student'}) is True
    assert _is_persona_conflict({'lecturer'}, {'lecturer'}) is False
    assert _is_persona_conflict({'lecturer'}, set()) is False


def test_value_conflict_for_identity_field() -> None:
    target_key = _normalize_field_key('Mã giảng viên')
    assert _value_conflicts_with_target_persona('SV2023123', {'lecturer'}, target_key) is True
    assert _value_conflicts_with_target_persona('GV0123', {'lecturer'}, target_key) is False


if __name__ == '__main__':
    test_extract_persona_tags()
    test_infer_form_persona_tags()
    test_persona_conflict_detection()
    test_value_conflict_for_identity_field()
    print('Persona suggestion rule checks passed.')
