import time
from pathlib import Path


from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    VlmPipelineOptions,
    granite_vision_vlm_conversion_options,
    smoldocling_vlm_conversion_options,
    smoldocling_vlm_mlx_conversion_options,
)
from docling.datamodel.settings import settings
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline

from docling_core.types.doc import DocItemLabel, ImageRefMode
from docling_core.types.doc.document import DEFAULT_EXPORT_LABELS


def read_resume(sources:list[str]):
    ## Use experimental VlmPipeline
    pipeline_options = VlmPipelineOptions()
    # If force_backend_text = True, text from backend will be used instead of generated text
    pipeline_options.force_backend_text = True
    ## Pick a VLM model. Fast Apple Silicon friendly implementation for SmolDocling-256M via MLX
    pipeline_options.vlm_options = smoldocling_vlm_conversion_options
    #pipeline_options.vlm_options = granite_vision_vlm_conversion_options


    ## Set up pipeline for PDF or image inputs
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline,
                pipeline_options=pipeline_options,
            ),
            InputFormat.IMAGE: PdfFormatOption(
                pipeline_cls=VlmPipeline,
                pipeline_options=pipeline_options,
            ),
        }
    )
    out_path = Path("scratch")
    out_path.mkdir(parents=True, exist_ok=True)
    for source in sources:
        start_time = time.time()
        print("================================================")
        print("Processing... {}".format(source))
        print("================================================")
        print("")
        res = converter.convert(source)
        print("")
        print(res.document.export_to_markdown())
        res.document.save_as_html(
            filename=Path("{}/{}.html".format(out_path, res.input.file.stem)),
            image_mode=ImageRefMode.REFERENCED,
            labels=[*DEFAULT_EXPORT_LABELS, DocItemLabel.FOOTNOTE],
        )
        res.document.save_as_markdown(
            out_path / f"{res.input.file.stem}.md",
            image_mode=ImageRefMode.PLACEHOLDER,
        )
        pg_num = res.document.num_pages()
        print("")
        inference_time = time.time() - start_time
        print(
            f"Total document prediction time: {inference_time:.2f} seconds, pages: {pg_num}"
        )