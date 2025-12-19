import xml.dom.minidom

def parse_xml_dom(file_path):
    dom_tree = xml.dom.minidom.parse(file_path)
    root = dom_tree.documentElement

    books = root.getElementsByTagName("book")
    for book in books:
        title = book.getElementsByTagName("title")[0].childNodes[0].data
        author = book.getElementsByTagName("author")[0].childNodes[0].data
        year = book.getElementsByTagName("year")[0].childNodes[0].data
        print(f"Title: {title}, Author: {author}, Year: {year}")

if __name__ == "__main__":
    parse_xml_dom("13_api.xml")
