import unittest
import xml2json
import optparse
import json
import os

xmlstring = ""
options = None

class SimplisticTest(unittest.TestCase):

    def setUp(self):
        global xmlstring, options
        filename = os.path.join(os.path.dirname(__file__), 'xml_ns2.xml')
        xmlstring = open(filename).read()
        options = optparse.Values({"pretty": False})

    def test_default_namespace_attribute(self):
        strip_ns = 0
        json_string = xml2json.xml2json(xmlstring,options,strip_ns)
        # check string
        self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)
        self.assertTrue(json_string.find("{http://www.w3.org/TR/html4/}tr") != -1)
        self.assertTrue(json_string.find("@class") != -1)

        # check the simple name is not exist
        json_data = json.loads(json_string)
        self.assertFalse("table" in json_data["root"])

    def test_strip_namespace(self):
        strip_ns = 1
        json_string = xml2json.xml2json(xmlstring,options,strip_ns)
        json_data = json.loads(json_string)

        # namespace is stripped
        self.assertFalse(json_string.find("{http://www.w3.org/TR/html4/}table") != -1)

        # TODO , attribute shall be kept
        #self.assertTrue(json_string.find("@class") != -1)

        #print json_data["root"]["table"]
        #print json_data["root"]["table"][0]["tr"]
        self.assertTrue("table" in json_data["root"])
        self.assertEqual(json_data["root"]["table"][0]["tr"]["td"] , ["Apples", "Bananas"])

    # def test_internal_to_elem(self):
    #     dic = {'id':'15','name':'Vasya','is_clone':True}
    #     f = xml2json.internal_to_elem(dic)
    #     self.assertTrue(f is not None)

    def test_json2xml(self):
        u_dic = "{}"
        string_dic = "{'#text':'Good day!','#tail':'Good bay!'}"
        js_big = {'students': [{'name': 'Sula'}, {'name': 'Bekzat'}], 'surname': 'Khabirov', 'name': 'Roman'}
        js = {'name':'Roman'}
        js_err = "{'name':'Roman','surname':'Khabirov'}"
        js2 = {'@sdsfd':'Roman'}
        js3 = {'#text':'Good day!','#tail':'Good bay!'}
        # res_big_false = xml2json.json2xml(js_big)
        res_big_true = xml2json.json2xml({'root': js_big})
        res = xml2json.json2xml(js)
        res2 = xml2json.json2xml({'@root':js2})
        res3 = xml2json.json2xml({'root':js3})
        res4 = xml2json.json2xml({'root':js3})
        # res_dic = xml2json.json2xml("{'root':"+string_dic+"}")

        res_u = xml2json.json2xml(u_dic)
        
        # print res_big_true
        # print str(res)
        # print f(js) == 'AD'
        # self.assertFalse(res_big_false == '<name>Roman</name><surname>Khabirov</surname><students><name>Sula</name><name>Bekzat</name></students>')
        self.assertTrue(res == '<name>Roman</name>')
        self.assertFalse(res2 == '<name>Roman</name>')
        self.assertFalse(res3 == '<name>Roman</name>')
        self.assertFalse(res4 == '<name>Roman</name>')
        # self.assertFalse(res_dic == '<name>Roman</name>')
        self.assertFalse(res_u == '<></>') 
        res_err = xml2json.json2xml(js_err)
        self.assertFalse(res_err == 'ValidationError!') 

        self.assertTrue(res_big_true == '<root><students><name>Sula</name></students><students><name>Bekzat</name></students><surname>Khabirov</surname><name>Roman</name></root>')

    def test_main(self):
        self.assertFalse(xml2json.main() == None)

    def test_xml2json(self):
        class Bla():
            pretty = True
        bl = Bla()
        xml_big = '<root><students><name>Sula</name></students><students><name>Bekzat</name></students><surname>Khabirov</surname><name>Roman</name></root>'
        xml = '<name>Roman</name>'
        # res_big_false = xml2json.json2xml(js_big)
        res_big_true = xml2json.xml2json(xml_big,bl)
        res = xml2json.xml2json(xml,bl)
        # print res_big_true
        # print str(res)
        # print f(js) == 'AD'
        # self.assertFalse(res_big_false == '<name>Roman</name><surname>Khabirov</surname><students><name>Sula</name><name>Bekzat</name></students>')
        self.assertFalse(res == "{'name':'Roman'}")
        self.assertFalse(res_big_true == "{'students': [{'name': 'Sula'}, {'name': 'Bekzat'}], 'surname': 'Khabirov', 'name': 'Roman'}")

    def test_json2elem(self):
        js = {}
        # js['name'] = 'Roma'
        # res = xml2json.json2elem(js)
        # self.assertFalse(res == "{'name':'Roman'}")



if __name__ == '__main__':
    unittest.main()
