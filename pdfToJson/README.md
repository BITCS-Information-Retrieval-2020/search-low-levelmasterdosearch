### WHAT TO USE

1. We run the grobid server on 10.1.114.114 to generate xml from pdf. So there is no need for you to install grobid once again.
2. We use the file 'xmlToJson.py' to generate json from xml.


### HOW TO USE

1. import `grobid_client` from pdfClient.py
2. Initializes a pdf client. We can change grobid parameters by config
3. Pass a pdf path to the function `process_pdf` and get Corresponding json output

You can see an example in run.py

### DATA FORMAT

```json
{
    "title": "title of a paper",
 	"authors": [
        {
            "firstName": "firstName of an author",
            "lastName": "lastName of an author "
        }
    ],
    "keywords":["keyword1","keyword2"],
    "abstract": "abstract of a paper",
    "paperContent":{
        "text": "all content of a paper (This is also a concatenation of subtexts)",
        "subtitles": ["Introduction", "Model"],
        "subtexts": ["section1Content", "section2Content"]
    },
    "references":[
        {
            "refTitle": "title of a reference paper",
            "refAuthors": [
                {
                    "firstName": "firstName of an author",
                    "lastName": "lastName of an author "
                }
            ],
            "refYear": "publised year of a reference paper",
            "refPublisher": "publised journal of a reference paper"
        }
    ]
}
```

