from bs4 import BeautifulSoup
from bs4.element import NavigableString
import json
import string

class XmlToJson(object):
    def init(self, tei):
        self.soup = BeautifulSoup(tei, 'xml')
        self.title = ""
        self.authors = []
        # self.year = ""
        # self.publisher = ""
        self.keywords = []
        self.abstract = ""
        self.subtitles = []
        self.subtexts = []
        self.references = []
        self.data = None

    def dealHeader(self):
        s_header = self.soup.find(name='teiHeader')

        # title
        self.title = s_header.find_all(name='title', level='a', type='main')[0].text.strip().lower()
        if(self.title == ''):
            return None

        # keywords
        keywords = s_header.find(name='keywords').find_all(name='term')
        for keyword in keywords:
            self.keywords.append(keyword.text.strip())
        
        # abstract
        self.abstract = s_header.find(name='abstract').text.strip()
        
        # authors
        authors = s_header.find_all(name='author')
        for author in authors:
            fname = author.find('forename')
            if (fname):
                firstName = fname.text.strip()
                name = firstName
            else:
                firstName = ""
                name = ""

            sname = author.find('surname')
            if (sname):
                lastName = sname.text.strip()
                name += " " + lastName
            else:
                lastName = ""

            if (firstName != "" or lastName != ""):
                self.authors.append({'firstName': firstName, 'lastName': lastName})

            """
            if (name != ""):
                self.authors.append(name)
            """

    def _getText(self, tag, ptext):
        text = ""
        if(ptext != ""):
            text = ptext
        else:
            text = ""
        
        for child in tag.children:
            if (isinstance(child, NavigableString)):
                if (child == '\n'):
                    continue
                if (child[0] in string.punctuation):
                    text = text.strip() + child.strip()
                else:
                    text = text.strip() + " " + child.strip()
            else:
                if(child.name == 'formula'):
                    continue
                elif(child.name == 'ref'): #type=bibr/table/figure
                    continue
                else:
                    #text += " " + child.text
                    child_text = child.text
                    if (child_text[0] in string.punctuation):
                        text = text.strip() + child_text.strip()
                    else:
                        text = text.strip() + " " + child_text.strip()
        
        return text.strip()

    def dealBody(self):
        s_body = self.soup.find(name='body')
        divs = s_body.find_all('div')
        key0 = {}.keys()
        cnt = 3
        whitespace = ['\n',' ']

        for i, div in enumerate(divs):
            if ('xmlns' not in div.attrs.keys()):
                continue

            dhead = div.find('head')
            dtitle = ""

            if (dhead):
                if (key0 != {}.keys()):
                    if (dhead.attrs.keys() == key0):
                        pass
                    else:
                        flag = False

                        for div_nextchild in divs[i + 1:i + cnt + 1]:
                            div_nextchild_head = div_nextchild.find('head')
                            if (div_nextchild_head):
                                if (div_nextchild_head.attrs.keys() == key0):
                                    flag = True
                                    break
                        if (flag):
                            # append the text to precious p
                            _dtext = []
                            _ptext = ""
                            for child in div.children:
                                if (isinstance(child, NavigableString) and child in whitespace):
                                    continue
                                if child.name == 'head':
                                    continue
                                if(child.name == 'formula'):
                                    continue
                                elif(child.name == 'ref'):
                                    continue
                                else:
                                    #p
                                    _dtext.append(self._getText(child,_ptext))
                                    _ptext = ""
                            
                            self.subtexts[-1] += _dtext
                            continue

                        else:
                            break

                elif (dhead.attrs.keys() != {}.keys()):
                    key0 = dhead.attrs.keys()

                if ('n' in dhead.attrs.keys()):
                    dtitle += dhead.attrs['n']
                if (dtitle != ""):
                    dtitle += " "
                dtitle += dhead.text
            else:
                continue

            if ('appendix' in dtitle.lower()):
                continue

            if ('reference' in dtitle.lower()):
                continue

            dtext = []
            ptext = ""
            for child in div.children:
                if (isinstance(child, NavigableString) and child in whitespace):
                    continue
                if child.name == 'head':
                    continue
                if(child.name == 'formula'):
                    continue
                elif(child.name == 'ref'):
                    continue
                else:
                    #p
                    dtext.append(self._getText(child,ptext))
                    ptext = ""

            self.subtitles.append(dtitle)
            self.subtexts.append(dtext)

    def dealBack(self):
        s_back = self.soup.find(name='back')
        # ref
        ref_div = s_back.find('div', attrs={'type': 'references'})
        refs = ref_div.find_all('biblStruct')

        for ref in refs:
            refItem = {}

            """
            rid = ""
            if("xml:id" in ref.attrs.keys()):
                rid = ref.attrs['xml:id']
            refItem['id'] = rid
            """

            rt = ref.find('title', attrs={'level': 'a'})
            if (rt):
                refTitle = rt.text
            else:
                continue

            refItem['refTitle'] = refTitle

            ref_authors = ref.find_all('author')
            refAuthors = []

            for rauthor in ref_authors:
                fname = rauthor.find('forename')
                if (fname):
                    firstName = fname.text.strip()
                    name = firstName
                else:
                    firstName = ""
                    name = ""

                sname = rauthor.find('surname')
                if (sname):
                    lastName = sname.text.strip()
                    name += " " + lastName
                else:
                    lastName = ""

                if (firstName != "" or lastName != ""):
                    refAuthors.append({'firstName': firstName, 'lastName': lastName})

            refItem['refAuthors'] = refAuthors
            ry = ref.find('date', attrs={'type': 'published'})
            if(ry):
                refItem['refYear'] = ry.attrs['when'].strip()
            else:
                refItem['refYear'] = ""

            rj = ref.find('title', attrs={'level': 'j'})
            if (rj):
                refItem['refPublisher'] = rj.text.strip()
            else:
                refItem['refPublisher'] = ""

            self.references.append(refItem)

    def run(self, tei):
        self.init(tei)
        self.dealHeader()
        self.dealBody()
        self.dealBack()

        textall = ""
        for subtext in self.subtexts:
            for text in subtext:
                textall += text
        paperContent = {
            'text': textall,
            'subtitles': self.subtitles,
            'subtexts': self.subtexts
        }

        self.data = {
            'title': self.title,
            'authors': self.authors,
            'keywords': self.keywords,
            'abstract': self.abstract,
            'paperContent': paperContent,
            'references': self.references,
        }

        return self.data

if __name__ == '__main__':
    xml_path = "3.xml"
    with open(xml_path,'r',encoding='utf-8') as f:
        tei = f.read()
    
    tool = XmlToJson()
    data = tool.run(tei)

    json_path = "3.json"
    with open(json_path,'w') as f:
        json.dump(data,f)