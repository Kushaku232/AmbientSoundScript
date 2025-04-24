import os 
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def SortFilesAlphaNumeric(folderName):
    for root, dirs, files in os.walk(os.path.abspath(folderName)):
        #print(dirs)
        i=1
        for folder in sorted_alphanumeric(dirs):
            foldval=re.findall(r'^\D*(\d+)', folder)[0]
            if (not int(foldval)==i):

                fixedFolderName=folder.replace(foldval,str(i),1)
                print(fixedFolderName)
                os.rename(os.path.join(root, folder),os.path.join(root, fixedFolderName),)
            i=i+1
if __name__ == "__main__":
    SortFilesAlphaNumeric("Ambience Playlists")