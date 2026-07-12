from pathlib import Path


def test_sidebar_selectbox_selected_value_uses_dark_text() -> None:
    styles = Path("src/reality_glitch/ui/styles.py").read_text(encoding="utf-8")

    assert 'div[data-baseweb="select"] > div *' in styles
    assert 'color: #082f3b !important;' in styles
    assert '-webkit-text-fill-color: #082f3b !important;' in styles


def test_form_inputs_use_navy_text() -> None:
    styles = Path("src/reality_glitch/ui/styles.py").read_text(encoding="utf-8")

    assert "input," in styles
    assert "color: navy !important;" in styles
    assert "-webkit-text-fill-color: navy !important;" in styles
    assert '[role="combobox"]' in styles


def test_mask_overlay_ui_is_present() -> None:
    app = Path("app.py").read_text(encoding="utf-8")
    assert "render_mask_overlay_preview" in app
    assert "mask_overlay_opacity" in app
    assert "mask_overlay_grid" in app
