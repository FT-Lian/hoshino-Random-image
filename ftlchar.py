# -*- coding: utf-8 -*-

import time, random, os, re
from hoshino import Service

from hoshino.typing import CQEvent
from nonebot import MessageSegment

sv = Service('acgchar', bundle='acgchr', help_='''
[今日二刺螈形象|今日二次元形象|今天我是什么少女]
'''.strip())

charproperty = {'race':'种族','age':'年龄','height':'身高','haircolor':'发型','eyescolor':'瞳孔','lucky':'幸运','CUP':'CUP','occupation':'职业','characteristic':'属性','character':'性格','skill':'技能'}
listchar = []
absPath = 'C:/XCW/hoshino/hoshino/modules/ftlchar/'

@sv.on_rex('今日二刺螈形象|今日二次元形象|今天我是什么少女')
async def sendchar(bot,ev):
    templistchar = listchar
    if listchar == []:
        await cachechar()
    userQQ = str(ev["user_id"])
    if await testQQ(userQQ) == 'always':
        charway = 'old'
        sentence = await messchar(charway,userQQ)
    elif await testQQ(userQQ) == 'none':
        charway = 'new'
        sentence = await messchar(charway,userQQ)
    else:
        await bot.send(ev, 'testQQ error 1')
    await bot.send(ev, sentence)

@sv.on_prefix('添加属性')
async def addcharlist(bot,ev):
    addproperstr = ev.message.extract_plain_text().replace(' ','')
    addproperlist = re.split('：|:|，|,',addproperstr)
    if not addproperlist[0] in charproperty.values():
        await bot.send(ev, '你加啥？')
        return
    try:
        if '\n' in addproperlist[1]:
            await bot.send(ev, '请不要一次添加多个属性')
            return
    except IndexError:
        pass
    for x in charproperty:
        if addproperlist[0] == charproperty[x]:
            if x == 'age' or x == 'height':
                await bot.send(ev,'这有什么好改的？洗洗睡吧')
                return
            elif x == 'lucky' or x == 'CUP':
                await bot.send(ev,'这有什么好改的？洗洗睡吧')
                return
            else:
                pathproper = absPath + 'data/' + x + '.txt'
                with open(pathproper, 'a', encoding='utf-8') as proper:
                    charword = '\n' + addproperlist[1]
                    proper.write(charword)
                sentence = '已在' + addproperlist[0] + '中' + '加入属性：' + addproperlist[1]
                await cachechar()                
                await bot.send(ev,sentence)


@sv.on_prefix('查看属性')
async def checkcharlist(bot,ev):
    properstr = ev.message.extract_plain_text().replace(' ','')
    if not properstr in charproperty.values():
        await bot.send(ev, '你查啥？')
        return
    for x in charproperty:
        if properstr == charproperty[x]:
            if x == 'age' or x == 'height':
                await bot.send(ev,'这有什么好看的？洗洗睡吧')
                return
            elif x == 'lucky' or x == 'CUP':
                await bot.send(ev,'这有什么好看的？洗洗睡吧')
                return 
            else:
                pathproper = absPath + 'data/' + x + '.txt'
                with open(pathproper, 'r', encoding='utf-8') as temproper:
                    propertemp = 'temp'
                    sentence = ''
                    while propertemp != '':
                        propertemp = temproper.readline()
                        if propertemp == '':
                            break
                        if propertemp[-1] == '\n':
                            propertemp =propertemp[:-1]
                        if sentence == '':
                            sentence = sentence + propertemp
                        else:
                            sentence = sentence + ',' + propertemp
                    sentence = '该属性下有：' + sentence
                    await bot.send(ev,sentence)
                    return

@sv.on_prefix('删除属性')
async def delcharlist(bot,ev):
    delproperstr = ev.message.extract_plain_text().replace(' ','')
    delproperlist = re.split('：|:|，|,',delproperstr)
    if not delproperlist[0] in charproperty.values():
        await bot.send(ev, '你删啥？')
        return
    try:
        if '\n' in delproperlist[1]:
            await bot.send(ev, '请不要一次删除多个属性')
            return
    except IndexError:
        pass
    for x in charproperty:
        if delproperlist[0] == charproperty[x]:
            if x == 'age' or x == 'height':
                await bot.send(ev,'这有什么好删的？洗洗睡吧')
                return
            elif x == 'lucky' or x == 'CUP':
                await bot.send(ev,'这有什么好删的？洗洗睡吧')
                return
            else:
                pathproper = absPath + 'data/' + x + '.txt'
                perlines = (i for i in open(pathproper, 'r', encoding='utf-8') if delproperlist[1] not in i)
                newpathproper = absPath + 'data/' + x + '_new' + '.txt'
                with open(newpathproper, 'w', encoding='utf-8') as properlist:
                    properlist.writelines(perlines)
                with open(newpathproper, 'r', encoding='utf-8') as properlist:
                    retext = properlist.read()
                    if retext[-1] == '\n':
                        retext = retext[:-1]
                with open(newpathproper, 'w', encoding='utf-8') as properlist:
                    properlist.write(retext)
                bakpathproper = absPath + 'data/' + x + 'bak' + '.txt'
                os.rename(pathproper,bakpathproper)
                os.rename(newpathproper,pathproper)
                os.remove(bakpathproper)
                await cachechar()
                await bot.send(ev,'已成功删除')
                return
        
async def cachechar():
    global listchar
    listchar = []
    try:
        for x in charproperty:
            if x != 'age' and x != 'height' and x != 'lucky' and x !='CUP':
                pathdata = absPath + 'data/' + x + '.txt'
                with open( pathdata ,'r', encoding='utf-8') as temp:
                    locals()[x] = []
                    strcache = 'temp'
                    while strcache != '':
                        strcache = temp.readline()
                        if strcache == '':
                            break
                        if strcache[-1] == '\n':
                                strcache = strcache[:-1]
                        locals()[x].append(strcache)
                    listchar.append(locals()[x])           
        return 'success'
    except:
        return 'error'


async def testQQ(userQQ):
    try:
        pathuser = absPath + 'user/' + userQQ + '.txt'
        with open(pathuser, 'r', encoding='utf-8') as temp:
            daycheck = temp.readline()
            # 此处有意向加入一个一天限制在n个次数的代码，但懒得写
            if daycheck == time.strftime("%Y,%m,%d\n", time.localtime()):
                return 'none'
            else:
                return 'none'
    except FileNotFoundError:
        usercache = open(pathuser, 'w', encoding='utf-8')
        usercache.close()
        return 'none'
    except :
        return 'error'


async def messchar(charway,userQQ):
    sentence = ''
    tempcharlist = 0
    if charway == 'new':
        for x in charproperty:
            if x == 'age':
                sentence = sentence + charproperty[x] + '：' + str(random.choice(range(10,41))) + '\n'
            elif x == 'height':
                if sentence[:7] == '种族：拉拉菲尔':
                    height = str(random.choice(range(86,101)))
                elif sentence[:6] == '种族：鲁加族':
                    height = str(random.choice(range(213,231)))
                elif sentence[:6] == '种族：维埃拉':
                    height = str(random.choice(range(178,192)))
                else:
                    height = str(random.choice(range(135,201)))
                sentence = sentence + charproperty[x] + '：' + height + '\n'
            elif x == 'lucky':
                templu = random.choice(range(65,72))
                if templu == 71:
                    lu = 'S'
                else:
                    lu = chr(templu)
                sentence = sentence + charproperty[x] + '：' + lu + '\n'
            elif x == 'CUP':
                tempcu = random.choice(range(1,72))
                if tempcu in range(1,6):
                    charcup = '飞机场'
                elif tempcu in range(6,16):
                    charcup = 'A'
                elif tempcu in range(16,31):
                    charcup = 'B'
                elif tempcu in range(31,46):
                    charcup = 'C'
                elif tempcu in range(46,56):
                    charcup = 'D'
                elif tempcu in range(56,61):
                    charcup = 'E'
                elif tempcu in range(61,65):
                    charcup = 'F'
                elif tempcu in range(65,68):
                    charcup = 'G'
                elif tempcu in range(68,70):
                    charcup = 'H'  
                elif tempcu == 71:
                    charcup = 'I'
                sentence = sentence + charproperty[x] + '：' + charcup + '\n'
            elif sentence[:6] == '种族：史莱姆' and (x == 'haircolor' or x == 'eyecolor'):
                sentence = sentence +charproperty[x] + '：' + '蓝色\n'
                tempcharlist += 1 
            else:
                sentence = sentence + charproperty[x] + '：' + listchar[tempcharlist][random.choice(range(0,len(listchar[tempcharlist])))] + '\n'
                tempcharlist += 1
            userdatasen = time.strftime("%Y,%m,%d\n", time.localtime()) + sentence
            userpath = absPath + 'user/' + userQQ + '.txt'
            with open(userpath, 'w', encoding='utf-8') as userwrite:
                userwrite.write(userdatasen)
    if charway == 'old':
        userpath = absPath + 'user/' + userQQ + '.txt'
        sentence = '今天你已经有可用形象了哦\n'
        with open(userpath, 'r', encoding='utf-8') as userread:
            userread.readline()
            tempone = 'temp'    
            while tempone != '':
                tempone = userread.readline()
                sentence = sentence + tempone
    sentence = sentence[:-1]
    return sentence
