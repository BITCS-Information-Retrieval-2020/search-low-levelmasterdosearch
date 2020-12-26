import json
from pdfClient import grobid_client


if __name__ == "__main__":
    pdf_path = '/home/xjw/pdfToJson/hw/example.pdf'
    config_path = './config.json'
    pdfClient = grobid_client(config_path=config_path)
    jsonData = pdfClient.process_pdf(pdf_path) #for use

    with open('example.json','w',encoding='utf8') as f:
        json.dump(jsonData,f)