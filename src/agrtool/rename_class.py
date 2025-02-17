# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:05:17 2023

@author: marianne.bezaire
"""
import sys
import re

def main():
    if len(sys.argv) > 2:
        file = sys.argv[-1] # "submission/Circle.java" # sys.argv[-1] # "submission/Circle.java" # 
        realclass =  sys.argv[-2] # "Square" # sys.argv[-2]

        rename(file, realclass)

def rename(file, realclass):
    patt = re.compile("public[\s ]+class[\s ]+([a-zA-Z0-9]+)")

    with open(file,"r") as f:
        content = f.read() #lines()
        
        temp = re.findall(patt, content)
        
        classname = temp[0]
        
        newcontent = re.sub("public[\s ]+class[\s ]+" + classname, "public class " + realclass, content)
        newcontent = re.sub("(^[\s\t ]*)public[\s ]+" + classname + "[\s ]*\(", r"\1public " + realclass + "(", newcontent, flags=re.M)
        newcontent = re.sub("([\s\t =]+)new[\s ]+" + classname + "[\s ]*\(", r"\1new " + realclass + "(", newcontent, flags=re.M)
        newcontent = re.sub("(^[\s\t ]*)" + classname + "([ \s\t=;]+)", r"\1" + realclass + r"\2", newcontent, flags=re.M)
        
    #    print(newcontent)
    with open("/".join(file.split("/")[:-1]) + "/" + realclass + ".java", "w") as f: #file.replace(classname, realclass),"w") as f:
        f.write(newcontent)
        
        
if __name__ == "__main__":
    main()            
