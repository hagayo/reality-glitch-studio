from dataclasses import dataclass

from reality_glitch.effects import (
    CenterBulgeEffect,
    CenterPinchEffect,
    CircularRippleEffect,
    DoubleExposureEffect,
    GlitchEffect,
    GrayscaleEffect,
    KaleidoscopeEffect,
    LocalTwirlEffect,
    MirrorEffect,
    MosaicEffect,
    PaletteTransplantEffect,
    PixelSortEffect,
    PortalEffect,
    RetroCrtEffect,
    RgbSplitEffect,
    SwirlEffect,
    WaveEffect,
)
from reality_glitch.infrastructure import (
    InMemoryEffectRegistry,
    InMemoryPresetRepository,
)
from reality_glitch.services import (
    GifAnimationService,
    ImagePipelineService,
    PillowImageExporter,
    PillowImageService,
)


@dataclass(frozen=True, slots=True)
class ApplicationContainer:
    registry: InMemoryEffectRegistry
    presets: InMemoryPresetRepository
    image_service: PillowImageService
    pipeline: ImagePipelineService
    animation: GifAnimationService
    exporter: PillowImageExporter


def build_container() -> ApplicationContainer:
    registry = InMemoryEffectRegistry(
        (
            WaveEffect(),
            GlitchEffect(),
            GrayscaleEffect(),
            RgbSplitEffect(),
            MirrorEffect(),
            PortalEffect(),
            PixelSortEffect(),
            KaleidoscopeEffect(),
            CircularRippleEffect(),
            MosaicEffect(),
            SwirlEffect(),
            RetroCrtEffect(),
            CenterBulgeEffect(),
            CenterPinchEffect(),
            LocalTwirlEffect(),
            DoubleExposureEffect(),
            PaletteTransplantEffect(),
        )
    )
    image_service = PillowImageService(max_size=1200)
    pipeline = ImagePipelineService(registry, image_service)
    return ApplicationContainer(
        registry=registry,
        presets=InMemoryPresetRepository(),
        image_service=image_service,
        pipeline=pipeline,
        animation=GifAnimationService(registry, pipeline),
        exporter=PillowImageExporter(),
    )
