import xml.etree.ElementTree as ET


class XMLmodel(object):
    def __init__(self, filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        '''
        print(self.root.tag)
        print(self.root.attrib)
        for source in self.root:
            print(source.tag)
            print(source.attrib)
        '''

        self.SrcList = []
        self.FixSrcList = []
        self.FreeSrcList = []

        self.ParList = []
        self.FixParList = []
        self.FreeParList = []

        for source in self.root:
            srcName = source.get('name')
            self.SrcList.append(srcName)
            self.FixSrcList.append(srcName)
            for parameter in source.findall('.//spectrum/parameter'):
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

    def GetSrcInfo(self, srcName):
        source = self.root.find('./source[@name="%s"]' % srcName)
        print(source.tag)
        print(source.attrib)

    def GetSpectralType(self, srcName):
        spectrum = self.root.find('./source[@name="%s"]/spectrum' % srcName)
        print(spectrum.tag)
        print(spectrum.attrib)

    def GetSpatialType(self, srcName):
        spatialModel = self.root.find('./source[@name="%s"]/spatialModel' % srcName)
        print(spatialModel.tag)
        print(spatialModel.attrib)

    def GetParInfo(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        print(parameter.tag)
        print(parameter.attrib)

    def GetParFree(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        kwd = parameter.attrib
        return kwd['free']

    def GetParValue(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        kwd = parameter.attrib
        value = float(kwd['value']) * float(kwd['scale'])
        try:
            error = float(kwd['error']) * float(kwd['scale'])
        except:
            error = 0
        return value, error

    def GetParScaledValue(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        kwd = parameter.attrib
        return kwd['value']

    def SetParScaledValue(self, srcName, parName, value):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        parameter.set('value', str(value))
        self.tree.write(self.filename)

    def SetParFree(self, srcName, parName, free):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        parameter.set('free', str(free))
        self.tree.write(self.filename)
        if free == 0 or free == '0':
            self.FixParList.append(srcName + '__' + parName)
            try:
                self.FreeParList.remove(srcName + '__' + parName)
            except:
                pass
        if free == 1 or free == '1':
            self.FreeParList.append(srcName + '__' + parName)
            try:
                self.FixParList.remove(srcName + '__' + parName)
            except:
                pass


if __name__ == '__main__':
    modelfile = 'XMLmodel.xml'
    model = XMLmodel(modelfile)

    print(model.SrcList)
    print(model.FixSrcList)
    print(model.FreeSrcList)
    print(model.ParList)
    print(model.FixParList)
    print(model.FreeParList)

    srcName = 'PowerLaw_source'
    model.GetSrcInfo(srcName)
    model.GetSpectralType(srcName)
    model.GetSpatialType(srcName)

    parName = 'Index'
    model.GetParInfo(srcName, parName)
    print(model.GetParValue(srcName, parName))

    model.SetParFree(srcName, parName, 0)
