from appJar import gui
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path


def split_pages(input_file, page_range, out_file):
    output = PdfFileWriter()
    input_pdf = PdfFileReader(open(input_file, "rb"))
    output_file = open(out_file, "wb")

    page_ranges = (x.split("-") for x in page_range.split(","))
    range_list = [i for r in page_ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    for p in range_list:
        try:
            output.addPage(input_pdf.getPage(p - 1))
        except IndexError:
            app.infoBox("Info", "Range exceeded number of pages in input.\nFile will still be saved.")
            break
    output.write(output_file)
    if (app.questionBox("File Save", "Output PDF saved. Do you want to quit?")):
        app.stop()


def validate_inputs(input_file, output_dir, range, file_name):
    errors = False
    error_msgs = []

    if Path(input_file).suffix.upper() != ".PDF":
        errors = True
        error_msgs.append("Please select a PDF input file")

    if len(range) < 1:
        errors = True
        error_msgs.append("Please enter a valid page range")

    if not (Path(output_dir)).exists():
        errors = True
        error_msgs.append("Please Select a valid output directory")

    if len(file_name) < 1:
        errors = True
        error_msgs.append("Please enter a file name")
    return (errors, error_msgs)


def press(button):
    if button == "Process":
        src_file = app.getEntry("Input_File")
        dest_dir = app.getEntry("Output_Directory")
        page_range = app.getEntry("Page_Ranges")
        out_file = app.getEntry("Output_name")
        errors, error_msg = validate_inputs(src_file, dest_dir, page_range, out_file)
        if errors:
            app.errorBox("Error", "\n".join(error_msg), parent=None)
        else:
            split_pages(src_file, page_range, Path(dest_dir, out_file))
    else:
        app.stop()


app = gui("PDF Splitter", useTtk=True)
app.setTtkTheme("vista")
app.setSize(500, 200)


app.addLabel("Choose Source PDF File")
app.addFileEntry("Input_File")

app.addLabel("Select Output Directory")
app.addDirectoryEntry("Output_Directory")

app.addLabel("Output file name")
app.addEntry("Output_name")

app.addLabel("Page Ranges: 1,3,4-10")
app.addEntry("Page_Ranges")


app.addButtons(["Process", "Quit"], press)


app.go()
