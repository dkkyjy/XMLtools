import sys
from FermiST import maptools
from XMLtools import NewModel, LoadModel

def FindSource(catalog, skycrd0_C, srcReg, outfile):
    catalog = LoadModel(catalog)

    model = NewModel()
    for srcName in catalog.SrcList:
        skycrd_C = catalog.GetSrcDir(srcName)
        rad = maptools.Sep(skycrd_C, skycrd0_C)
        if rad < srcReg:
            print(rad)
            srcEle = catalog.GetSrcEle(srcName)
            if srcEle.attrib['type'] == 'PointSource':
                model.AddPointSource(srcName)
            if srcEle.attrib['type'] == 'DiffuseSource':
                spatialFile = srcEle.attrib['file']
                model.AddDiffuseSource(srcName, SpatialFile=spatialFile)
            model.AddSrcEle(srcName, srcEle)
    print(model)
    model.SaveModel(outfile)


if __name__ == '__main__':
    skycrd0_C = (float(sys.argv[1]), float(ys.argv[2]))
    srcReg = float(sys.argv[3])
    catalog = 'PointSource.xml'
    outfile = 'myModel.xml'
    FindSource(catalog, skycrd0_C, srcReg, outfile)