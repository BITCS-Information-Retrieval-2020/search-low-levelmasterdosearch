### WHAT TO USE

1. We run the grobid server on 10.1.114.114 to generate xml from pdf. So there is no need for you to install grobid once again.
2. We use the file 'xmlToJson.py' to generate json from xml.


### HOW TO USE

1. import `grobid_client` from pdfClient.py
2. Initializes a pdf client. We can change grobid parameters by config
3. Pass a pdf path to the function `process_pdf` and get Corresponding json output

You can see an example in run.py

