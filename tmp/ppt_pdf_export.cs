using System;
using Microsoft.Office.Core;
using Microsoft.Office.Interop.PowerPoint;

public class PptPdfExporter
{
    public static void Export(string inputPath, string outputPath)
    {
        Application app = null;
        Presentation pres = null;
        try
        {
            app = new Application();
            pres = app.Presentations.Open(
                inputPath,
                MsoTriState.msoFalse,
                MsoTriState.msoFalse,
                MsoTriState.msoFalse
            );
            pres.ExportAsFixedFormat(
                outputPath,
                PpFixedFormatType.ppFixedFormatTypePDF,
                PpFixedFormatIntent.ppFixedFormatIntentPrint,
                MsoTriState.msoFalse,
                PpPrintHandoutOrder.ppPrintHandoutVerticalFirst,
                PpPrintOutputType.ppPrintOutputSlides,
                MsoTriState.msoFalse,
                null,
                PpPrintRangeType.ppPrintAll,
                "",
                true,
                true,
                false,
                true,
                false,
                Type.Missing
            );
        }
        finally
        {
            if (pres != null) pres.Close();
            if (app != null) app.Quit();
        }
    }
}
