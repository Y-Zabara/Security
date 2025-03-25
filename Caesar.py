# ------------ КЛАСИЧНИЙ шифроалгоритм з кодом Цезаря англомовного транскрипту

import time

# ------------ Функція шифрування / дешифрування кодом Цезаря англомовного транскрипту
def CryptDcrypt (message, key, mode):

    '''

    шифр Цезаря - класичний шифр заміни літерала вхідного тексту на літерал із словника з позицією ключа

    :param message: текст що підлягає перетворенню -  шифрування / дешифрування
    :param key: ключ шифрування
    :param mode: напрям перетворення - шифрування / дешифрування вхідного тексту
    :return: перетворений текст - шифрування / дешифрування

    '''


    symbols='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !&.'

    global outtranslated
    translated=''
    for symbol in message:
        if symbol in symbols:
            symbolindex = symbols.find(symbol)
            if mode=='encrypt':
                translatedindex=symbolindex+key
            elif mode == 'decrypt':                           # Альтернатива
                 translatedindex = symbolindex - key
            if translatedindex >=len(symbols):                # Контроль загортання
                 translatedindex=translatedindex-len(symbols)
            elif translatedindex <0:                           # Альтернатива
                translatedindex = translatedindex + len(symbols)
            translated=translated+symbols[translatedindex]
        else:
            translated = translated + symbol
    print("--------------------------------------------------------------")
    print(mode,'=',translated)

    return translated


# ----- Дослідження стійкості криптоалгоритму Цезаря методом перебору ключа ----
def HacCrypt (message):
    '''

    Злам шифру методом перебору ключа ("грубої сили") - алфавіт має бути відомий

    :param message: текст що підлягає зламу
    :return: нічого

    '''


    symbols='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !&.'

    for key in range(len(symbols)):
        translated = ''
        for symbol in message:
            if symbol in symbols:
                symbolindex = symbols.find(symbol)
                translatedindex = symbolindex - key
                if translatedindex <0:
                    translatedindex = translatedindex + len(symbols)
                translated = translated + symbols[translatedindex]
            else:
                translated = translated + symbol
        print('key=', key, ' ', translated)

    return


if __name__ == '__main__':

    key = 13


    imputFilename = 'test_file.txt'
    ouputFilename = 'crypt_test_file.txt'
    fileObj = open(imputFilename)
    content = fileObj.read()
    fileObj.close()

    print("--------------------------------------------------------------")
    print('input =', content)

    #  ----------------- Шифрування - криптографія ----------------------
    StartTime = time.time()
    outtranslated= CryptDcrypt(content, key, 'encrypt')  # Кодування
    CryptDcrypt (outtranslated, key, 'decrypt')          # Декодування
    totalTime = (time.time() - StartTime)
    print('totalTime =', totalTime, 's')

    outputfileObj = open(ouputFilename, 'w')
    outputfileObj.write(outtranslated)  # Запис інформації у файл
    outputfileObj.close()

    # ----- Дослідження стійкості алгоритму через злам - криптологія -----
    print ('-------------- Злам шифру методом перебору ("грубої сили") -----------------')
    StartTime=time.time()
    HacCrypt (outtranslated)
    totalTime = (time.time()-StartTime)
    print('totalTime =', totalTime, 's')

