from langdetect import detect
from langdetect import detect_langs
import langid
import os
from os import path
import shutil
#import sys
import chardet
#import math
from langdetect import DetectorFactory
DetectorFactory.seed = 0


def detectPDFLanguage(languageDetect):

    try:
        PathFile = os.path.join(languageDetect , 'PathFile.txt')
        print(PathFile)
        ReadPathFile = open(PathFile,'r')
        ReadingData = ReadPathFile.read()
        ReadingDataWithoutDelimeter = ReadingData.split("\n")
        source = ReadingDataWithoutDelimeter[0]
        dir = ReadingDataWithoutDelimeter[1]
        directory = ReadingDataWithoutDelimeter[2]
        logFile = ReadingDataWithoutDelimeter[3]

        source_temp = source
        print(source)

        dir_temp = dir
        print(dir)

        ReadPathFile.close()
        
        languageList = {'af':'Afrikaans', 'ar':'Arabic', 'bg':'Bulgarian', 'bn':'Bengali', 'ca':'Catalan',
                        'cs':'Czech', 'cy':'Cymraeg', 'da':'Danish', 'de':'German', 'el':'Greek', 'en':'English', 
                        'es':'Spanish', 'et':'Estonian', 'fa':'Persian', 'fi':'Finnish', 'fr':'French', 'gu':'Gujrati',
                        'he':'Hebrew', 'hi':'Hindi', 'hr':'Croatian', 'hu':'Hungarian', 'id':'Indonesian', 
                        'it':'Italian', 'ja':'Japanese', 'kn':'Kannada', 'ko':'Korean', 'lt':'Lithuanian', 'lv':'Latvian', 
                        'mk':'Macedonian', 'ml':'Malayalam', 'mr':'Marathi', 'ne':'Nepali', 'nl':'Dutch', 'no':'Norwegian', 
                        'pa':'Punjabi', 'pl':'Polish','pt':'Portuguese', 'ro':'Romanian', 
                        'ru':'Russian', 'sk':'Slovak', 'sl':'Slovenian', 'so':'Somali', 'sq':'Albanian', 'sv':'Swedish', 
                        'sw':'Swahili', 'ta':'Tamil','te':'Telugu','th':'Thai', 'tl':'Tagalog', 'tr':'Turkish', 'uk':'Ukrainian', 
                        'ur':'Urdu', 'vi':'Vietnamese','zh-cn':'Mainland China', 'zh-tw':'Taiwan',
                        'am':'Amharic', 'an':'Aragonese', 'as':'Assamese', 'az':'Azerbaijani', 'be':'Belarusian', 'br':'Breton', 
                        'bs':'Bosnian', 'dz':'Dzongkha', 'eo':'Esperanto', 'eu':'Basque', 'fo':'Faroese', 'ga':'Irish',
                        'gl':'Galician', 'ht':'Haitian', 'hy':'Armenian', 'is':'Icelandica', 'jv':'Javanese', 'ka':'Georgian', 
                        'kk':'Kazakh', 'km':'Central Khmer', 'ku':'Kurdish', 'ky':'Kyrgyz', 'la':'Latin', 'lb':'Letzeburgesch', 
                        'lo':'Lao', 'mg':'Malagasy', 'mn':'Mongolian', 'ms':'Malay', 'mt':'Maltese', 'nb':'Norwegian', 'nn':'Norwegian',
                        'oc':'Occitan', 'or':'Oriya', 'ps':'Pushto', 'qu':'Quechua', 'rw':'Kinyarwanda', 'se':'Northern Sami',
                        'si':'Sinhalese', 'sr':'Serbian', 'ug':'Uyghur', 'vo':'Volapük', 'wa':'Walloon', 'xh':'Xhosa', 'zh':'Chinese',
                        'zu':'Zulu' }
        
        log= open(logFile,"a+")
        log.write('\n')

        for filename in os.listdir(directory):
            
            source = source_temp
            dir = dir_temp
            if filename.endswith(".txt") :
                txtFile = os.path.join(directory, filename)
                print(txtFile)
                
                fileData = open(txtFile,'rb').read()
                
                encoding = chardet.detect(fileData)
                print(encoding['encoding'])
                
                fileRead = open(txtFile, 'r', encoding=encoding['encoding'])
                
                if fileRead.mode == 'r':
                    #fileRead.seek(0)
                    first_char = fileRead.read().strip()
                    #first_char = first_char.strip()
                
                    if not first_char:
                        print("file is empty")
                        log.write("File is Empty." + '\n')
                        continue
                    else:
                        #detecting Language via LangDetect
                        detectedLang = detect(first_char)
                        print(detectedLang)

                        #detecting Language via Langid
                        classifyLanguage, score = langid.classify(first_char)
                        print(classifyLanguage)

                        #detecting Language via Detect_langs
                        detectLangs = detect_langs(first_char)
                        for item in detectLangs:
                            vLangList = item.lang
                            vPerList = item.prob
                            vPerList = "{0:.2f}".format(vPerList)
                            print(vLangList)
                            print(vPerList)

                        #Comparison of the results of detect(), classify() and detect_langs() to determine the accuracy of the language.
                        if classifyLanguage == 'no' or classifyLanguage == 'is':
                            if vLangList == 'en' and detectedLang == 'en' and vPerList > '0.80':
                                classifyLanguage, score = langid.classify(first_char)
                                detectedLanguage = classifyLanguage
                            classifyLanguage, score = langid.classify(first_char)
                            detectedLanguage = classifyLanguage
                        elif classifyLanguage == 'es' and detectedLang == 'en' and vLangList == 'en' and vPerList > '0.80':
                            detectedLanguage = classifyLanguage
                        elif classifyLanguage == 'fr' and detectedLang == 'en' and vLangList == 'en' and vPerList > '0.80':
                            detectedLanguage = classifyLanguage
                        elif classifyLanguage == vLangList and classifyLanguage == detectedLang and detectedLang == vLangList:
                            detectedLanguage = classifyLanguage
                        elif classifyLanguage != vLangList or detectedLang != vLangList:
                            if vPerList > '0.80':
                                detectedLanguage = vLangList
                            else:
                                classifyLanguage, score = langid.classify(first_char)
                                detectedLanguage = classifyLanguage
                        elif classifyLanguage != vLangList and detectedLang == vLangList:
                            detectedLanguage = classifyLanguage
                        elif classifyLanguage != vLangList or detectedLang == vLangList:
                            if vPerList > '0.80':
                                detectedLanguage = vLangList
                            else:
                                classifyLanguage,score = langid.classify(first_char)
                                detectedLanguage = classifyLanguage
                        
                        print(detectedLanguage)
                        #getting the PDF filename to move to the desired language folder
                        pdfFileName = filename.replace(".txt", ".pdf")

                        print(pdfFileName)
                        source = os.path.join(source,pdfFileName)
                    
                        print(source)

                        for lang in languageList:
                            folderName = ""
                            if lang == detectedLanguage:
                                folderName = languageList[lang]
                                print(folderName)
                                dir = os.path.join(dir,folderName)
                                if not os.path.exists(dir):
                                    os.makedirs(dir)
                            
                                dir = os.path.join(dir,pdfFileName)
                                check = path.exists(dir)
                                if check != True:
                                    log.write("Moving Files : " + pdfFileName)
                                    log.write('\n')
                                    shutil.move(source, dir)
                                else:
                                    log.write("File already exists: " + pdfFileName)
                                    log.write('\n')
                                    print("file exists")
                                break
                            else:
                                continue
            else:
                continue
            
            log.write("filename : " + filename)
            log.write("  langid : " + classifyLanguage)
            log.write("  langdetect : " + detectedLang)
            log.write("  Detect Langs : " + str(detectLangs))
            log.write('\n\n')
            dir=""
            source=""
            check=""
            txtFile =""
            first_char =""
            encoding=""
            fileData=""
            detectedLanguage=""
            classifyLanguage=""
            #classifyLanguage_new=""
            folderName = ""
    
    except FileNotFoundError:
        log.write("File Not Found : " + filename)
        log.write('\n')
        print("File Not Found PathFile.txt")
    except IOError:
        log.write("Couldn't read File : " + filename)
        log.write('\n')
        print("Couldn't read File",filename)
    except UnicodeEncodeError:
        log.write("Encoding Error ")
        log.write('\n')
        print("Encoding Error")
    except UnicodeDecodeError:
        log.write("Decoding Error ")
        log.write('\n')
        print("Decoding Error")

    
#detectPDFLanguage(r'C:/Users/pavithra.balamurugan/Documents/DetectLanguage') 