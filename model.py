# -'''- coding: utf-8 -'''-

"""
    AnonymousWatcher
    Copyright (C) 2019, 2023  Relius Wang

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import xml.etree.cElementTree as ET
import re
import presentation

__regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def emailValid(email: str):
    return re.fullmatch(__regex, email)


def genenrateXML(emailstr: str, phonenum=""):
    root = ET.Element("Data")
    if (emailValid(emailstr)):
        ET.SubElement(root, "Email").text = emailstr
    else:
        print("Invalid Email")
        #ET.SubElement(root, "Cellphone").text = phonenum
    tree = ET.ElementTree(root)
    tree.write("evolto.xml", encoding="UTF-8", xml_declaration=True)


def parseXML() -> dict:
    tree = ET.parse("evolto.xml")
    root = tree.getroot()
    __datadict = dict()
    for child in root:
        __datadict[child.tag] = child.text

    return __datadict


def updateXML(emailstr="", phonenum=""):
    tree = ET.parse("evolto.xml")
    root = tree.getroot()

    if(emailstr != "" and emailValid(emailstr)):
        elt = root.find("Email")
        elt.text = emailstr
    # if(phonenum != ""):
    #     elt = root.find("Cellphone")
    #     elt.text = phonenum

    tree.write("evolto.xml", encoding="UTF-8", xml_declaration=True)


def deleteXML():
    tree = ET.parse("evolto.xml")
    root = tree.getroot()
    elt = root.find("Email")
    elt.text = ""
    #elt = root.find("Cellphone")
    #elt.text = ""
    tree.write("evolto.xml", encoding="UTF-8", xml_declaration=True)

def readXML() -> dict:
    tree = ET.parse("Alpha.xml")
    root = tree.getroot()
    __datadict = dict()
    for child in root:
        __datadict[child.tag] = child.text

    return __datadict



if __name__ == "__main__":
    genenrateXML("aa@gmail.com")
    print(parseXML())
    updateXML("s@gmail.com")
    print(parseXML())
    print(readXML())
