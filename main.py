import sys, csv
from lxml import etree



class Converter:

    def __init__(self, arg):    #конструктор класса
        self.file = ''
        self.format = ''
        if len(arg) != 3:
            print('''
            Недостаточно аргументов (и фактов)
            ''')
        else:
            self.file = arg[1]
            self.format = arg[2]
            #self.__start()

    def __convert_to_xml(self):

        with open(self.file, encoding='utf-8') as prs:
            data = csv.DictReader(prs, delimiter='\t')
            root = etree.Element('body')
            for each in data:
                if not each['#sentno'].startswith('#meta'):
                    if each['#wordno'] == '1' and each['#nvar'] == '1': sentence = etree.SubElement(root, 'se')
                    if each['#nvar'] == '1': word = etree.SubElement(sentence, 'word')
                    if each['#word'] != ' ':
                        a = etree.SubElement(sentence, 'ana')
                        a.set('lex', each['#lem'])
                        a.set('morph', each['#flex'])
                        a.set('gr', ','.join((each['#lex'], each['#gram'])))
                        if each['#nvar'] == each['#nvars']:
                            a.tail = each['#word']
                            word.tail = each['#punctr']
        with open(self.file[:-4]+'_c.xml', 'w', encoding='utf-8') as xml:
            xml.write(etree.tostring(root, pretty_print=True, encoding='utf-8').decode())


    def __convert_to_prs(self):

        with open(self.file, encoding='utf-8') as xml:
            xmltree = etree.fromstring(xml.read())
            s_num = len(list(xmltree.iter('se')))
            sentno = 0
            rows = []

            for each_sentence in xmltree.iter('se'):
                wordno = 0
                sentno += 1
                #lemmas = []

                for each_word in each_sentence.iter('w'):
                    wordno += 1
                    nvars = 0
                    nvar = 0
                    lemmas = []
                    lang = ''
                    punctl = ''
                    trans_ru = ''
                    indexword = "\t"
                    # punctuation_right check

                    if each_word.tail != None:
                        punctuation_right = each_word.tail.strip()
                    else:
                        punctuation_right = ''

                    # SENT_POS CHECK
                    if wordno == 1:
                        sent_pos = 'bos'
                    elif wordno == s_num:
                        sent_pos == 'eos'
                    else:
                        sent_pos == ''

                    word = each_word.xpath("string()").strip().replace('\t', '')
                    #print(word)
                    # CAP checker
                    if word[0].isupper():
                        cap = 'cap'
                    else:
                        cap = ''

                    # LEMMAS CHECKER 
                    for ana in each_word.iter('ana'):
                        nvars += 1
                        lemma = ana.get('lex')
                        if lemma not in lemmas:
                            lemmas.append(lemma)
                            #print(lemmas)

                    nlems = len(lemmas)

                    # GRAMMA
                    for ana in each_word.iter('ana'):
                        nvar += 1
                        gr = ana.get('gr')

                        if ',' in gr:
                            lex, gram = gr.split(',', 1)
                        else:
                            lex = gr
                            gram = ''

                        try:
                            lem = ana.get('lex').strip()
                        except:
                            lem = ''
                        try:
                            trans = ana.get('trans').strip()
                        except:
                            trans = ''
                        try:
                            flex = ana.get('morph').strip()
                        except:
                            flex = ''

                        data_hash = { '#sentno': sentno, '#wordno': wordno, '#lang': lang, '#graph': cap, '#word':  word, '#indexword': indexword, '#nvars': nvars, '#nlems': nlems, '#nvar': nvar, '#lem': lem, '#trans': trans, '#trans_ru': trans_ru, '#lex': lex, '#gram': gram, '#flex': flex, '#punctl': punctl, '#punctr': punctuation_right, '#sent_pos': sent_pos }
                        rows.append(data_hash)
                        data_hash = None
                        #print(word)


        with open(self.file[:-4]+'_c.prs', 'w', encoding='utf-8') as prs:
            fieldnames = ['#sentno','#wordno','#lang','#graph','#word','#indexword','#nvars','#nlems','#nvar','#lem','#trans','#trans_ru','#lex','#gram','#flex','#punctl','#punctr','#sent_pos']
            writer = csv.DictWriter(prs, fieldnames, delimiter = '\t')
            writer.writeheader()
            writer.writerows(rows)

    def start(self):
        self.__checker()

    def __checker(self):
        if self.file != '' and self.format != '':
            if self.format == 'prs':
                if self.file.endswith('.xml'):
                    self.__convert_to_prs()
                else:
                    print('xml file PLS')
            elif self.format == 'xml':
                if self.file.endswith('.prs'):
                    self.__convert_to_xml()
                else:
                    print('prs file PLS')
            else:
                print('''
                Ничего :с
                ''')



def main(argv):

    conv = Converter(argv)
    conv.start()
    #print(conv)


main(sys.argv)
