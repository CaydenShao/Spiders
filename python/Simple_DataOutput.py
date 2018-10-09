# coding:utf-8
import codecs

class DataOutput(object):
    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)
    
    def output_html(self):
        fout = codecs.open('baike.html', 'w', encoding = 'utf-8')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<tb>%s</tb>" % data['url'])
            fout.write("<tb>%s</tb>" % data['title'])
            fout.write("<tb>%s</tb>" % data['summary'])
            fout.write("</tr>")
            self.datas.remove(data)
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()