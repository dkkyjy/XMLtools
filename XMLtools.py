from pprint import pprint
from collections import Counter
import xml.etree.ElementTree as ET

class XMLmodel(object):
    def __init__(self, filename):
        self.filename = filename.split('.xml')[0]
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()

        self.SrcList = []
        self.FixSrcList = []
        self.FreeSrcList = []

        self.ParList = []
        self.FixParList = []
        self.FreeParList = []

        for source in self.root:
            srcName = source.get('name')
            self.FixSrcList.append(srcName)
            for parameter in source.findall('.//spectrum/parameter'):
                self.SrcList.append(srcName)
                parName = parameter.get('name')
                self.ParList.append(srcName + '__' + parName)
                if parameter.get('free') == '0':
                    self.FixParList.append(srcName + '__' + parName)
                if parameter.get('free') == '1':
                    self.FreeParList.append(srcName + '__' + parName)
                    self.FreeSrcList.append(srcName)
                    try:
                        self.FixSrcList.remove(srcName)
                    except:
                        pass

        self.NumDict = dict(Counter(self.SrcList))
        self.SrcList = list(self.NumDict.keys())
        self.FreeNumDict = dict(Counter(self.FreeSrcList))
        self.FreeSrcList = list(self.FreeNumDict.keys())

    def GetSrcInfo(self, srcName):
        source = self.root.find('./source[@name="%s"]' % srcName)
        pprint(source.tag)
        pprint(source.attrib)

    def GetSpectralType(self, srcName):
        spectrum = self.root.find('./source[@name="%s"]/spectrum' % srcName)
        pprint(spectrum.tag)
        pprint(spectrum.attrib)

    def GetSpatialType(self, srcName):
        spatialModel = self.root.find('./source[@name="%s"]/spatialModel' % srcName)
        pprint(spatialModel.tag)
        pprint(spatialModel.attrib)

    def GetParInfo(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        pprint(parameter.tag)
        pprint(parameter.attrib)

    def GetParFree(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        kwd = parameter.attrib
        return kwd['free']

    def GetParScale(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        kwd = parameter.attrib
        return kwd['scale']

    def GetParValue(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        kwd = parameter.attrib
        value = float(kwd['value']) * float(kwd['scale'])
        try:
            error = float(kwd['error']) * float(kwd['scale'])
        except:
            error = None
        return value, error

    def GetParScaledValue(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        kwd = parameter.attrib
        return kwd['value']

    def SetParScaledValue(self, srcName, parName, value):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        parameter.set('value', str(value))
        outfile = self.filename + '_SetScaledValue_{}_{}_{}.xml'.format(srcName, parName, value)
        self.tree.write(outfile)
        return self.__init__(outfile)

    def SetParScale(self, srcName, parName, scale):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        parameter.set('scale', str(scale))
        outfile = self.filename + '_SetParScale_{}_{}_{}.xml'.format(srcName, parName, scale)
        self.tree.write(outfile)
        return self.__init__(outfile)

    def SetParFree(self, srcName, parName, free):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        parameter.set('free', str(free))
        outfile = self.filename + '_SetFree_{}_{}_{}.xml'.format(srcName, parName, free)
        self.tree.write(outfile)
        return self.__init__(outfile)


if __name__ == '__main__':
    modelfile = 'XMLmodel.xml'
    model = XMLmodel(modelfile)

    pprint(model.SrcList)
    pprint(model.FixSrcList)
    pprint(model.FreeSrcList)
    pprint(model.ParList)
    pprint(model.FixParList)
    pprint(model.FreeParList)
    pprint(model.NumDict)
    pprint(model.FreeNumDict)

    srcName = 'PowerLaw_source'
    model.GetSrcInfo(srcName)
    model.GetSpectralType(srcName)
    model.GetSpatialType(srcName)

    parName = 'Prefactor'
    model.GetParInfo(srcName, parName)
    print(model.GetParFree(srcName, parName))
    print(model.GetParScale(srcName, parName))
    print(model.GetParValue(srcName, parName))
    print(model.GetParScaledValue(srcName, parName))

    model.SetParScaledValue(srcName, parName, 1)
    model.SetParScale(srcName, parName, 1e-10)
    model.SetParFree(srcName, parName, 0)
