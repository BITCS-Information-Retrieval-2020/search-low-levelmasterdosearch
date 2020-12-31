import sys
import os
import io
import json
import argparse
import time
import concurrent.futures
from client import ApiClient
import ntpath
import requests
from xmlToJson import XmlToJson
import pickle


class grobid_client(ApiClient):

    def __init__(self, config_path='./config.json'):
        self.config = None
        self._load_config(config_path)
        self.xmlToJson = XmlToJson()
        # self.errorPdfs = []

    def _load_config(self, path='./config.json'):
        """
        Load the json configuration
        """
        config_json = open(path).read()
        self.config = json.loads(config_json)

        # test if the server is up and running...
        the_url = 'http://' + self.config['grobid_server']
        if len(self.config['grobid_port']) > 0:
            the_url += ":" + self.config['grobid_port']
        the_url += "/api/isalive"
        r = requests.get(the_url)
        status = r.status_code

        if status != 200:
            print('GROBID server does not appear up and running ' + str(status))
        else:
            print("GROBID server is up and running")

    def process_pdf(self, pdf_path, service='processFulltextDocument'):

        print(pdf_path)
        files = {
            'input': (
                pdf_path,
                open(pdf_path, 'rb'),
                'application/pdf',
                {'Expires': '0'}
            )
        }

        the_url = 'http://' + self.config['grobid_server']
        if len(self.config['grobid_port']) > 0:
            the_url += ":" + self.config['grobid_port']
        the_url += "/api/" + service

        # set the GROBID parameters
        the_data = {}
        """
        if generateIDs:
            the_data['generateIDs'] = '1'
        if consolidate_header:
            the_data['consolidateHeader'] = '1'
        if consolidate_citations:
            the_data['consolidateCitations'] = '1'
        if teiCoordinates:
            the_data['teiCoordinates'] = self.config['coordinates']
        """

        # generate xml from pdf by grobid
        res, status = self.post(
            url=the_url,
            files=files,
            data=the_data,
            headers={'Accept': 'text/plain'}
        )

        if status == 503:
            time.sleep(self.config['sleep_time'])
            return self.process_pdf(pdf_path)
        elif status != 200:
            print('Processing failed with error ' + str(status))
        else:
            # generate JSON file from xml
            try:
                jsonData = self.xmlToJson.run(res.text)
                if(jsonData is None):
                    # self.errorPdfs.append(pdf_path)
                    print("Generating resulting JSON file %s failed" % pdf_path)
                return jsonData
            except Exception as e:
                # self.errorPdfs.append(pdf_path)
                print("Generating resulting JSON file %s failed" % pdf_path)
                print("Error is %s" % e)
