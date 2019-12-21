'''
@Date: 2019-12-19 16:51:40
@LastEditTime : 2019-12-21 14:59:49
@LastEditors  : Please set LastEditors
@Description: In User Settings Edit
'''
import PIL.Image as Image
import os
import configparser
import time
'''
@return: 返回当前文件绝对路径
'''
class FilePath(object):
    def getPath(self):
        projectPath = os.path.realpath(__file__)
        self.path = os.path.dirname(projectPath)
        return self.path
    '''
    @description: 没有目录则创建并返回绝对路径
    @param {str} fileName 文件夹名称 
    @return: 文件夹绝对路径
    '''
    def isPath(self, fileName = "complete"):
        paperFile = os.path.join( self.path,fileName )
        if(os.path.exists( paperFile ) == False):
            os.mkdir(paperFile)
        return paperFile
'''
@description: 读取配置
@param {type} 
@return: 
'''
class ReadConfig(object):
    def __init__(self,configPath):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)
    def get_items(self, param):
        value = self.cf.items(param)
        return value
    '''
    @description: 
    @group {str} 组名 
    @name {str} 键名 
    @return: 返回键值
    '''
    def get_value(self, group, name):
        value = self.cf.get(group,name)
        return value
'''
@description: 查找图像拼接后保存
@param {type} 
@return: 
'''
class JoinImage(object):
    def __init__(self, width, height, path, imgType):
        self.width = width
        self.height = height
        self.path = path
        self.imgType = imgType
    def creatImg(self,imgRows,imgCols):
        self.to_image = Image.new('RGB', (self.height * imgCols, self.width * imgRows) ) #创建一个新图
    def findImg(self):
        self.image_names = []   #存放当前文件夹所有后缀为imgType的文件名
        for name in os.listdir(self.path):
            if(os.path.splitext(name)[1] == self.imgType):
                self.image_names.append(name)
    def join(self, imgRows, imgCols, savePath):
        self.creatImg(imgRows, imgCols)
        self.findImg()
        for y in range(1, imgRows + 1):
            for x in range(1, imgCols + 1):
                from_image = Image.open(self.path + self.image_names[imgCols * (y - 1) + x - 1]).resize(
                    ( self.height, self.width),Image.ANTIALIAS)
                self.to_image.paste(from_image, ((x - 1) * self.height, (y - 1) * self.width))
        return self.to_image.save(savePath) # 保存新图

if __name__ == "__main__":
    fPath = FilePath()
    filePath = fPath.getPath() + "\\"
    #读取config
    cnPath = os.path.join(filePath,"20170306_170809.ini")
    readConfig = ReadConfig( cnPath )
    #读取值
    imgType =  "." + readConfig.get_value("Info","fileExtention") 
    imgRows = int( readConfig.get_value("Info","Rows") )     #行
    imgCols = int( readConfig.get_value("Info","Cols") )
    imgWidth = int( readConfig.get_value("Info","CellWidth") )
    imgHeight = int ( readConfig.get_value("Info","CellHeight") )
    subBlock = readConfig.get_value("Info","SubBlock")
    #文件保存路径
    fileName = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))  
    savePath = os.path.join(fPath.isPath(),fileName + imgType)

    joinImage = JoinImage(imgWidth, imgHeight, filePath, imgType)
    joinImage.join(imgRows, imgCols, savePath)


