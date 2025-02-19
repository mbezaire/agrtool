# -*- coding: utf-8 -*-
"""
Correct class name errors.

Given an expected class name, rename the submitted file
if its name does not match. Also rename any usages of the
class name inside the file.
"""
import sys
import re

def main():
    if len(sys.argv) > 2:
        file = sys.argv[-1]
        realclass =  sys.argv[-2]

        rename(file, realclass)

def rename(file, realclass):
    """Renames a Java class and all usages within the class file

    Given a desired filename, this function uses regex to find
    all usages of the class (declaration, instantiation) and
    the class header. It renames all of them to the realclass
    argument and then saves the updated file with the realclass
    file name.

    Args:
        file (str): name/path of the file to rename/fix naming
        realclass (str): desired name of the class
    """


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
