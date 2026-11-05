# Render the practical guides

The `.qmd` files in this folder are the editable sources for the current PDFs.
Each file renders directly to a PDF with the same basename in this folder.
The `figs/` subfolder contains unchanged copies of the referenced training figures. Keep it with the QMD files so this worksheet project can render independently.

## VS Code

1. Install Quarto and the Quarto extension for VS Code.
2. Open either `.qmd` file and edit its content directly.
3. Use **Quarto: Render** from the Command Palette, or run the commands below in the integrated terminal.

From this folder:

```powershell
quarto render Day_01_Quick_Tutorials_Worksheet.qmd
quarto render Day_02_Top_Down_Practical_Guide.qmd
quarto render Day_03_TestStand_Practical_Guide.qmd
```

Render both guides:

```powershell
quarto render .
```

From the repository root:

```powershell
quarto render training_materials/worksheets
```

The default format is `typst`, which produces PDF using the compiler bundled with Quarto (verified with Quarto 1.9.38). A separate LaTeX installation and the old Python PDF builders are not needed.

Use `{{< pagebreak >}}` in the QMD to control page boundaries. Keep image paths relative to this folder. Save and render again after editing.

The `.md` files are retained as earlier text snapshots. The Python builders under `tools/` generate the older ReportLab editions and may overwrite those Markdown snapshots; do not use them to rebuild the current QMD/PDF editions. PDFs under `output/pdf/` are also older editions.

The nested `_quarto.yml` keeps worksheet rendering separate from the Day 1-4 slide decks in the parent folder.
