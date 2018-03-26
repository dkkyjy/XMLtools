from pprint import pprint
from collections import Counter
from xml.etree import ElementTree as ET
from xml.dom import minidom


def prettify(elem):
    rough_string = ET.tostring(elem)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="")


class NewModel(object):
    def SaveModel(self, filename):
        tree = ET.ElementTree(self.root)
        tree.write(filename)

    def __init__(self):
        self.root = ET.Element('source_library', title='source_library')

    def AddSrcEle(self, srcName, srcEle):
        source = self.root.find('./source[@name="%s"]' % srcName)
        source.extend(srcEle)

    def AddSpectialEle(self, srcName, spectialEle):
        spectrum = self.root.find('./source[@name="%s"]/spectrum' % srcName)
        spectrum.extend(spectialEle)

    def AddSpatialEle(self, srcName, spatialEle):
        spatialModel = self.root.find('./source[@name="%s"]/spatialModel' % srcName)
        spatialModel.extend(spatialEle)

    def AddPointSource(self, srcName, SpectralType=None, SpectralPars=None, skycrd_C=None):
        source = ET.Element('source', name=srcName, type='PointSource')

        if SpectralType:
            spectrum = ET.SubElement(source, 'spectrum', type=SpectralType)
        if SpectralPars:
            for parName, parDict in SpectralPars.items():
                free = str(parDict['free'])
                scale = str(parDict['scale'])
                value = str(parDict['value'])
                parmin = str(parDict['min'])
                parmax = str(parDict['max'])
                ET.SubElement(spectrum, 'parameter', free=free, max=parmax, min=parmin, name=parName, scale=scale, value=value)

        if SpectralType:
            spatialModel = ET.SubElement(source, 'spatialModel', type='SkyDirFunction')
        if skycrd_C:
            ra = str(skycrd_C[0])
            dec = str(skycrd_C[1])
            ET.SubElement(spatialModel, 'parameter', free='0', max='360.', min='-360.', name='RA', scale='1.0', value=ra)
            ET.SubElement(spatialModel, 'parameter', free='0', max='90.', min='-90.', name='DEC', scale='1.0', value=dec)

        try:
            source = ET.fromstring(prettify(source))
        except:
            pass
        self.root.append(source)

    def AddDiffuseSource(self, srcName, SpectralType=None, SpectralPars=None, SpatialType=None, SpatialFile=None, SpatialPar=None):
        source = ET.Element('source', name=srcName, type='DiffuseSource')

        if SpectralType:
            spectrum = ET.SubElement(source, 'spectrum', type=SpectralType)
        if SpectralPars:
            for parName, parDict in SpectralPars.items():
                free = str(parDict['free'])
                scale = str(parDict['scale'])
                value = str(parDict['value'])
                parmin = str(parDict['min'])
                parmax = str(parDict['max'])
                ET.SubElement(spectrum, 'parameter', free=free, max=parmax, min=parmin, name=parName, scale=scale, value=value)

        if SpatialFile and SpatialType:
            spatialModel = ET.SubElement(source, 'spatialModel', file=SpatialFile, type=SpatialType)
        if SpatialPar:
            name = SpatialPar['name']
            free = str(SpatialPar['free'])
            scale = str(SpatialPar['scale'])
            value = str(SpatialPar['value'])
            parmin = str(SpatialPar['min'])
            parmax = str(SpatialPar['max'])
            ET.SubElement(spatialModel, 'parameter', free=free, max=parmax, min=parmin, name=name, scale=scale, value=value)

        try:
            source = ET.fromstring(prettify(source))
        except:
            pass
        self.root.append(source)


class LoadModel(NewModel):
    def __init__(self, filename):
        self.basename = filename.split('.xml')[0]
        self.filename = filename
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

        self.ParsNumDict = dict(Counter(self.SrcList))
        self.SrcList = list(self.ParsNumDict.keys())
        self.FreeNumDict = dict(Counter(self.FreeSrcList))
        self.FreeSrcList = list(self.FreeNumDict.keys())

    def GetSrcInfo(self, srcName):
        source = self.root.find('./source[@name="%s"]' % srcName)
        pprint(source.tag)
        pprint(source.attrib)

    def GetSrcEle(self, srcName):
        source = self.root.find('./source[@name="%s"]' % srcName)
        return source

    def GetSrcDir(self, srcName):
        source = self.root.find('./source[@name="%s"]' % srcName)
        if source.attrib['type'] == 'PointSource':
            ra = source.find('spatialModel/parameter[@name="RA"]')
            dec = source.find('spatialModel/parameter[@name="DEC"]')
            ra = float(ra.attrib['value'])
            dec = float(dec.attrib['value'])
        if source.attrib['type'] == 'DiffuseSource':
            ra = float(source.attrib['RA'])
            dec = float(source.attrib['DEC'])
        return (ra, dec)
        
    def GetSpectralType(self, srcName):
        spectrum = self.root.find('./source[@name="%s"]/spectrum' % srcName)
        pprint(spectrum.tag)
        pprint(spectrum.attrib)

    def GetSpectralEle(self, srcName):
        spectrum = self.root.find('./source[@name="%s"]/spectrum' % srcName)
        return spectrum

    def GetSpatialType(self, srcName):
        spatialModel = self.root.find('./source[@name="%s"]/spatialModel' % srcName)
        pprint(spatialModel.tag)
        pprint(spatialModel.attrib)

    def GetSpatialEle(self, srcName):
        spatialModel = self.root.find('./source[@name="%s"]/spatialModel' % srcName)
        return spatialModel

    def GetParInfo(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        pprint(parameter.tag)
        pprint(parameter.attrib)

    def GetParEle(self, srcName, parName):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        return parameter

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
        outfile = self.basename + '_SetScaledValue_{}_{}_{}.xml'.format(srcName, parName, value)
        self.SaveModel(outfile)

    def SetParScale(self, srcName, parName, scale):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        parameter.set('scale', str(scale))
        outfile = self.basename + '_SetParScale_{}_{}_{}.xml'.format(srcName, parName, scale)
        self.SaveModel(outfile)

    def SetParFree(self, srcName, parName, free):
        parameter = self.root.find('./source[@name="%s"]/spectrum/parameter[@name="%s"]' % (srcName, parName))
        parameter.set('free', str(free))
        outfile = self.basename + '_SetFree_{}_{}_{}.xml'.format(srcName, parName, free)
        self.SaveModel(outfile)

    def DelSource(self, srcName):
        source = self.root.find('./source[@name="%s"]' % srcName)
        self.root.remove(source)
        outfile = self.basename + '_DelSource_{}.xml'.format(srcName)
        self.SaveModel(outfile)


if __name__ == '__main__':
    filename = 'myModel.xml'
    mymodel = NewModel(filename)

    SpectralType = 'PowerLaw'
    SpectralPars = {'Prefactor': {'free':1, 'max':1000, 'min':0.001, 'scale':1e-9, 'value':1},
                        'Index': {'free':1, 'max':5, 'min':1, 'scale':-1, 'value':2},
                        'Scale': {'free':0, 'max':2000, 'min':30, 'scale':1, 'value':100}}
    skycrd_C = (83.45, 21.72)
    mymodel.AddPointSource('myPowerLaw_source', SpectralType, SpectralPars, skycrd_C)

    SpatialType = 'SpatialMap'
    SpatialFile = 'SpatialMap_source.fits'
    SpatialPar = {'name': "Normalization", 'free':1, 'min':0.001, 'max':1000, 'scale':1, 'value':100}
    mymodel.AddDiffuseSource('myDiffuse_source', SpectralType, SpectralPars, SpatialType, SpatialFile, SpatialPar)


    filename = 'XMLmodel.xml'
    model = LoadModel(filename)
    model.AddPointSource('myPowerLaw_source', SpectralType, SpectralPars, skycrd_C)

    pprint(model.SrcList)
    pprint(model.FixSrcList)
    pprint(model.FreeSrcList)
    pprint(model.ParList)
    pprint(model.FixParList)
    pprint(model.FreeParList)
    pprint(model.ParsNumDict)
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

    model.DelSource('myPowerLaw_source')
