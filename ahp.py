# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:38:48 2019

@author: atidem
"""

"""
Bu proje Atakan Demir(2016280050) ve Kaan Karavar(2016280022) tarafından yapılmıştır.
Bu program anaconda framework içindeki spyder editörü kullanılarak hazırlandı.
Kütüphaneler komut satırına (cmd) pip install kütüphane adı yazılarak indirilebilir.
Kullanılan kütüphaneler kullandığımız framework ile default olarak gelmektedir.

"""
import pandas as pd
import numpy as np

text = open("Dagdeviren.prj","r") ### HESAPLAMAK İSTEDİĞİNİZ DOSYA ADINI YAZINIZ.. // open file from text
txt = text.read()
txt = txt.replace(';',' ')
lst = pd.DataFrame(data=txt.split("\n"))
productCount = int(lst.iloc[0,0]) #Ürün Sayımız  // count of product
products = list(lst.iloc[1:productCount+1,0]) #Ürün isimlerimiz // name of products
ahp = [] # prj dosyasının bize gelişi bu  
result = [] # en son elde edilecek sonuclar

#Dosyayı işlemler için dataframe haline çeviriyoruz  //  convert to dataframe from file
for i in range(productCount+1,len(lst.iloc[:,0])):
    ahp.append(lst.iloc[i,0].split())
ahp=pd.DataFrame(data=ahp)

#Elimizdeki verilerin satır toplamlarını bulup geri döndürüyoruz.  // return row sum
def rowSum(matrix):
    matrix = pd.DataFrame(data=matrix)
    rowSum = []
    for i in range(len(matrix.iloc[:,1])):
        l = 0.0
        m = 0.0
        u = 0.0
        for j in range(len(matrix.iloc[1,:])):         
            if((j+1) % 3 == 0):
                u = u + float(matrix.iloc[i,j])
            elif((j+1) % 3 == 1):
                l = l + float(matrix.iloc[i,j])
            elif((j+1) % 3  == 2):
                m = m + float(matrix.iloc[i,j])
        rowSum.append([l,m,u])  
    return(rowSum)

#Verilerin isimleri bir listenin içine yazıp döndürüyoruz.  // get name of criteria
def getNode(matrix):
    liste = []    
    for i in range(len(matrix.iloc[:,1])):
        if(matrix.iloc[i,0].isalpha()):
            print(matrix.iloc[i,0])
            liste.append([matrix.iloc[i,0],matrix.iloc[i,1]])    
    
    return liste

#Her bir matris için S değerini hesaplıyoruz.    //  s value calculate
def sVaules(rowSum = []):
    s = []
    for i in range(len(rowSum)):
        x = 0
        z = 0
        q = 0
        for j in range(len(rowSum)):
            if(i != j):
                x = x + rowSum[j][2]
                z = z + rowSum[j][0]
            q = q + rowSum[j][1]
        l = float(rowSum[i][0]) / (float(rowSum[i][0])+ x )
        u = float(rowSum[i][2]) / (float(rowSum[i][2])+ z )
        m = float(rowSum[i][1]) / q
        s.append([l,m,u])
    
    return s 

#Elde ettiğimiz s'ler ve satır toplamlarını kullanarak ilgili ağırlıkları buluyoruz.  // find weight with s values
def weightFirst(sValues = []):
    w= []
    V = []
    tmp = []
    for i in range(len(sValues)):
        for j in range(len(sValues)):
            if(i != j):
                if(sValues[i][1] >= sValues[j][1]):
                    tmp.append(1)
                elif(sValues[i][2] >= sValues[j][0]):
                    tmp.append((sValues[i][2]-(sValues[j][0]))/((sValues[i][2]-sValues[i][1])+(sValues[j][1]-(sValues[j][0]))))
                else:
                    tmp.append(0)
        V.append(tmp.copy())
        tmp.clear()
    
    for i in range(len(V)):
        w.append(min(V[i]))
        
    summ = sum(w)
    for i in range(len(w)):
        w[i] = w[i] / summ
    return w  

# Dallanan matris içinden gidilebilecek yolları buluyoruz ama hepsi   // find all path 
# istediğimiz yol en uca (yaprağa kadar giden) gittiğinde o yol için ilgili değerlerle hesaplanıyor.  // calculate value top to leaf 
# dataframe de node lar yanındaki sayılar azaltılarak sadece ilgili alt noda ait ağırlık değeri kullanılarak hesaplandı.  
def allOfRoad(liste,i):
    if(i<len(nodeList)):
        nodeList[i][1] = int(nodeList[i][1])
        if(len(liste)!= 0):
            liste[-1][1] = liste[-1][1] - 1
        if(int(nodeList[i][1])!=0):
            nodeList[i][1] =  int(nodeList[i][1])
            liste.append(nodeList[i])            
            allOfRoad(liste,i+1)
        elif(int(nodeList[i][1])==0):
            liste.append(nodeList[i]) 
            calcRows(liste)
            liste.pop()
            if(i<(len(nodeList)-1) and int(nodeList[i+1][1]) != 0):                
                liste.pop()
            allOfRoad(liste,i+1)
            
        else:
            liste.pop()
            allOfRoad(liste,i+1) 

#Bulduğumuz her bir yolun değerini hesaplıyoruz  // calculate all path
def calcRows(liste):
    mult = 1
    for i in range(len(liste)-1):
        mult = mult * weights[liste[i][0]][liste[i][1]]   
    result.append(mult*np.array(weights[liste[-1][0]]))  
        
#Bulduğum tüm nodeların ağırlıklarını hesaplıyoruz. // calculate weigths all node    
def weightCalcAllNodes():
    weights = {}
    for i in range(len(ahp.iloc[:,0])-1):
        if(ahp.iloc[i,0].isalpha()):
            if(int(ahp.iloc[i,1])==0):
                a = ahp.iloc[i+1:i+1+productCount,:productCount*3]
                tmp = weightFirst(sVaules(rowSum(a)))
                tmp.reverse()
                weights[ahp.iloc[i,0]] = tmp            
            else:
                y = int(ahp.iloc[i,1])
                a = ahp.iloc[i+1:i+1+y,:y*3]
                tmp = weightFirst(sVaules(rowSum(a)))
                tmp.reverse()
                weights[ahp.iloc[i,0]] = tmp
                
    return weights
            
#En sonunda tüm sonuçlarını ilgili sütunlarını toplayıp, sonucu döndüyoruz.     // find final result   
def sonuc(result):
    result = np.array(result)   
    return np.sum(result, axis=0)
                       
weights = weightCalcAllNodes()
nodeList = getNode(ahp)
liste=[]
allOfRoad(liste,0)
products.reverse()
result = pd.DataFrame(data = sonuc(result),index = products)


print(ahp.iloc[6,0].isalpha())
print("ağırlıklar ters halinde yazılmıştır.")
print(weights)
print(result)
