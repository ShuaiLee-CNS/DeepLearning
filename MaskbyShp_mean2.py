# -*- coding: cp936 -*-

#scrip
#ʹ��shp���������ü�դ�����ݲ�ͳ�ƾ�ֵ
print"ʹ��shp���������ü�դ�����ݲ�ͳ�ƽ����ֵ"

###########�޸Ĳ���###########

ras_file = r"H:\FCave\FC\geotiff"   #���ü���ԭʼդ�����ݴ洢�ļ���·��
suffix = 'tif'  #���ü���ԭʼդ�����ݺ�׺
bvalue= -9999   #���ü���ԭʼդ�����ݱ���ֵ

shp_file = r"E:\�й��߽�\������ԭ54���������վ���ϱ߽�"   #�ü�����shpģ�����ݴ洢�ļ���·��

ras_file_cut = r"H:\FCave\FC\smbasin\basin"   #�ü���դ�����ݽ���洢�ļ���·��
txtname=r"H:\FCave\FC\smbasin\stats"     #���ͳ���ı�·��

#############################


#���㲿��
import arcpy
arcpy.env.workspace=shp_file
shps=arcpy.ListFeatureClasses()
arcpy.env.workspace=ras_file
ras=arcpy.ListRasters('*',suffix)
print "����"+str(len(ras))+"��դ������"
#
print "Processing......"
for sh in shps:
    shtmp=sh.encode('cp936')
    shpfile=shp_file+"\\"+shtmp
    print "����"+str(len(shps))+"��shp���ݣ����ڴ����"+str(shps.index(sh)+1)+"����"+shtmp
    result=[]
    for rs in ras:
        rstmp=rs.encode('cp936')
        outname=ras_file_cut+"\\"+rstmp[0:len(rstmp)-4]+shtmp[0:len(shtmp)-len(suffix)]+".tif"
        #arcpy.Clip_management(rstmp,"#",outname,shpfile,"#","ClippingGeometry")
        arcpy.Clip_management(rstmp,"#",outname,shpfile,str(bvalue),"ClippingGeometry") #������Чֵ
        stats=arcpy.GetRasterProperties_management(outname,"MEAN")
        result.append(rstmp+'   '+str(stats)+"\n")
        arcpy.Delete_management(outname,"")
        print rstmp+"   OK!"

    file(txtname+"\\"+shtmp[0:len(shtmp)-4]+".txt",'w').writelines(result)

print "Finish!"
