import json
from pdfClient import grobid_client


def get_content(pdf_path)
    config_path = './config.json'
    pdfClient = grobid_client(config_path=config_path)
    jsonData = pdfClient.process_pdf(pdf_path) #for use
    return jsonData


if __name__ == "__main__":
    pdf_path = '/home/xjw/pdfToJson/hw/example.pdf'
    jsonData = get_content(pdf_path)

    title = jsonData["title"]
    authors = jsonData["authors"]
    keywords = jsonData["keywords"]
    abstract = jsonData["abstract"]
    paperContent = jsonData["paperContent"]
    references = jsonData["references"]