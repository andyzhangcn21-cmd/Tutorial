import xml.sax

class BookHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.current_element = ""
        self.title = ""
        self.author = ""
        self.year = ""

    def startElement(self, tag, attributes):
        self.current_element = tag

    def endElement(self, tag):
        if tag == "book":
            print(f"Title: {self.title}, Author: {self.author}, Year: {self.year}")
            self.title = ""
            self.author = ""
            self.year = ""
        self.current_element = ""

    def characters(self, content):
        if self.current_element == "title":
            self.title = content
        elif self.current_element == "author":
            self.author = content
        elif self.current_element == "year":
            self.year = content

if __name__ == "__main__":
    parser = xml.sax.make_parser()
    handler = BookHandler()
    parser.setContentHandler(handler)
    parser.parse("13_api.xml")
