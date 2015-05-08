import arcpy
import numpy

class masker:
	'''Provides access to functions that produces masks from remote sensing image, according to its bit structure.'''

	def __init__(self, band, *var):
		self.bandarray = band

	def getmask(self, bitpos, bitlen, value):
		'''Generates mask with given bit information.

		Parameters
			bitpos		-	Position of the specific QA bits in the value string.
			bitlen		-	Length of the specific QA bits.
			value  		-	A value indicating the desired condition.
		'''
		lenstr = ''
		for i in range(bitlen):
			lenstr += '1'
		bitlen = int(lenstr, 2)

		if type(value) == unicode:
			value = int(value, 2)

		posValue = bitlen << bitpos
		conValue = value << bitpos
		mask = (self.bandarray & posValue) == conValue

		return mask.astype(int)

inRasterLayerStr = arcpy.GetParameterAsText(0)
bitpos = int(arcpy.GetParameterAsText(1))
bitlen = int(arcpy.GetParameterAsText(2))
bitval = arcpy.GetParameterAsText(3)
outRasterFile = arcpy.GetParameterAsText(4)

inRaster = arcpy.Raster(inRasterLayerStr)
inraster = arcpy.RasterToNumPyArray(inRaster)
bitmasker = masker(inraster)
outarray = bitmasker.getmask(bitpos, bitlen, bitval)
outraster = arcpy.NumPyArrayToRaster(outarray, 
                                     arcpy.Point(inRaster.extent.XMin, inRaster.extent.YMin),
                                     inRaster,
                                     inRaster,
                                     inRaster.noDataValue)
outraster.save(outRasterFile)