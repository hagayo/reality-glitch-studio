from pathlib import Path


def test_preset_loader_does_not_write_to_rendered_widget_key() -> None:
    app_source = Path('app.py').read_text(encoding='utf-8')
    function_source = app_source.split('def load_preset', 1)[1].split(
        'def queue_preset', 1
    )[0]

    assert 'preset_selector =' not in function_source
    assert 'pending_preset' in app_source


def test_sidebar_styles_define_readable_effect_control_contrast() -> None:
    style_source = Path(
        'src/reality_glitch/ui/styles.py'
    ).read_text(encoding='utf-8')

    assert 'Sidebar widget contrast' in style_source
    assert '[data-testid="stSidebar"] details > summary' in style_source
    assert '[role="listbox"]' in style_source
