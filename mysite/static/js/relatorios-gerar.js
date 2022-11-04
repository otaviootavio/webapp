window.jsPDF = window.jspdf.jsPDF;

// Convert HTML content to PDF
function Convert_HTML_To_PDF() {
    var doc = new jsPDF();

    // Source HTMLElement or a string containing HTML.
    var elementHTML = document.querySelector("#contentToPrint");

    doc.html(elementHTML, {
        callback: function(doc) {
            // Save the PDF
            doc.save("document-html.pdf");
        },
        margin: [10, 10, 10, 10],
        autoPaging: 'text',
        x: 0,
        y: 0,
        width: 190, //target width in the PDF document
        windowWidth: 675 //window width in CSS pixels
    });
}