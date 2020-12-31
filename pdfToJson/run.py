import json
from pdfClient import grobid_client


def get_content(pdf_path):
    config_path = './config.json'
    pdfClient = grobid_client(config_path=config_path)
    jsonData = pdfClient.process_pdf(pdf_path)  # for use
    return jsonData


if __name__ == "__main__":
    pdf_path = '../paper/6.pdf'
    jsonData = get_content(pdf_path)

    title = jsonData["title"]
    authors = jsonData["authors"]
    keywords = jsonData["keywords"]
    abstract = jsonData["abstract"]
    paperContent = jsonData["paperContent"]
    references = jsonData["references"]

    with open("../paper/6.json", "w", encoding="utf-8") as fout:
        output = json.dumps(jsonData, ensure_ascii=False, indent=2, separators=(',', ': '))
        fout.write(output)
