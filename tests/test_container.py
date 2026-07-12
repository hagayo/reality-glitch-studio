from __future__ import annotations

from reality_glitch.container import build_container


def test_container_builds_complete_application_graph() -> None:
    container = build_container()

    assert container.registry.list_definitions()
    assert container.presets.list_all()
    assert container.pipeline is not None
    assert container.animation is not None
    assert container.exporter is not None
    assert container.image_service is not None


def test_each_container_build_has_independent_services() -> None:
    first = build_container()
    second = build_container()

    assert first is not second
    assert first.registry is not second.registry
    assert first.pipeline is not second.pipeline


def test_container_exposes_preset_blender() -> None:
    container = build_container()
    assert container.preset_blender is not None
