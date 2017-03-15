#!/usr/bin/python
import os, time, datetime
import sys
import logging
import json
from logging.handlers import SysLogHandler
from logging.handlers import TimedRotatingFileHandler


data = {}
items = []
itemstimer = ['tmrenforceDirectoryCount','tmrstartSharkStreams','tmrsharkStreams','tmrsaveMetadata','tmrdeletePointer','tmrgetMetadata']

for arg in sys.argv:
        if arg.find('=') >0 :
                strArg=arg.split('=')
                data[strArg[0]]=strArg[1]

loadDataResult=data['infile']+".tmp"

#### application error handler
loggerapp = logging.getLogger('swifttps')
handlerapp = TimedRotatingFileHandler('./logs/application.log', when="h", interval=1, backupCount=5)
loggerapp.addHandler(handlerapp)

def sendLogApp(msg) :
    loggerapp.error(msg)

def funcExecuteCommand(cmd) :
        result=commands.getstatusoutput(cmd)
        return result[1]

def fileLineRead(fileName):
        f=open(fileName)
        fw=open(fileName+".bak","w")
        while 1:
                line = f.readline()
                if not line:
                        break
                fw.write(line.split(' ')[0]+ ' ' + line.split(' ')[1] + ' ' +str(dataRead(line.split(' ')))+' dummy\n')
        f.close()
        fw.close()

def dataRead(data):
        startDate = datetime.datetime.now() - datetime.timedelta(minutes=1)
        startPoint=long(data[2])

        filename=data[0]+ "/" +startDate.strftime("%Y%m") +"/" +startDate.strftime("%d") +"/" +data[1] +"-"+startDate.strftime("%Y%m%d%H")
        print filename
        if not os.path.exists(filename):
                return startPoint
        else:
                f1=open(filename)

        f2=open(loadDataResult,'a+')
        lineno = 0

        for line in f1:
                lineno += 1
                if lineno > startPoint:
                        f2.write(line)
        endPoint=lineno
        print endPoint

        f1.seek(1)
        if startPoint > endPoint:
                startPoint=0
                for line in f1:
                        f2.write(line)


        lines = endPoint-startPoint
        #print lines
        #print startPoint

        f1.close()
        f2.close()
        return endPoint

def fileProcess(fileName):
        startDate = datetime.datetime.now() - datetime.timedelta(minutes=1)
        f=open(fileName)

        while 1:
                tmpdata={}
                line = f.readline()
                if not line:
                        break

                try :
                        if line.find('latency') <0 :
                                continue
                        strLine = line.split(']',1)[1].split(':',1)[1]
                        d = json.loads(strLine)

                        tmpdata['strUri'] = d.get('req').get('url')
                        tmpdata['strCode'] = str(d.get('res').get('statusCode'))
                        tmpdata['strByte'] =  str(d.get('bytesTransferred'))
                        tmpdata['strByteRecv'] = d.get('bytesTransferred')
                        tmpdata['strResptime'] = str(d.get('latency'))
                        tmpdata['strMethod'] = d.get('req').get('method')
                        tmpdata['strTenant'] = d.get('req').get('caller').get('login')
                        if tmpdata.get('strTenant') == 'None' :
                                tmpdata['strTenant'] = 'poseidon'
                        commonval='Tenant='+ tmpdata.get('strTenant') + ' Method=' + tmpdata.get('strMethod') + ' Code=' + tmpdata.get('strCode')

                        # error handling
                        if d.get('err') :
                                if data.get(commonval+' err') :
                                        data[commonval+' err'] += 1
                                else:
                                        data[commonval+' err'] = 1
                                continue

                        tmpdata['tmrenforceDirectoryCount'] = d.get('req').get('timers').get('enforceDirectoryCount')
                        tmpdata['tmrstartSharkStreams'] = d.get('req').get('timers').get('startSharkStreams')
                        tmpdata['tmrsharkStreams'] = d.get('req').get('timers').get('sharkStreams')
                        if tmpdata.get('strMethod') == 'GET' :
                                tmpdata['tmrsharkStreams'] = d.get('req').get('timers').get('streamFromSharks')
                        tmpdata['tmrsaveMetadata'] = d.get('req').get('timers').get('saveMetadata')
                        tmpdata['tmrdeletePointer'] = d.get('req').get('timers').get('deletePointer')
                        tmpdata['tmrgetMetadata'] = d.get('req').get('timers').get('getMetadata')

                except :
                        sendLogApp(line)
                        pass

                try :

                        if tmpdata.get('strByte') == 'None' :
                                tmpdata['strByte']=0

                        if data.get(commonval + ' Bytes') :
                                data[commonval + ' Bytes'] += long(tmpdata.get('strByte'))
                        else :
                                data[commonval + ' Bytes'] = long(tmpdata.get('strByte'))

                        if data.get(commonval + ' Resptime') :
                                data[commonval + ' Resptime'] += float(tmpdata.get('strResptime'))
                        else :
                                data[commonval + ' Resptime'] = float(tmpdata.get('strResptime'))

                        for itemtimer in itemstimer :
                                if data.get(commonval + ' '+ itemtimer) and tmpdata.get(itemtimer) :
                                        data[commonval + ' ' + itemtimer] += float(tmpdata.get(itemtimer))
                                elif tmpdata.get(itemtimer) :
                                        data[commonval + ' ' +itemtimer] = float(tmpdata.get(itemtimer))

                        if data.get(commonval) :
                                data[commonval] += 1
                        else :
                                data[commonval] = 1
                                items.append(commonval)
                                data[commonval + ' Resp_5'] = 0
                                data[commonval + ' Resp1'] = 0
                                data[commonval + ' Resp2'] = 0
                                data[commonval + ' Resp2o'] = 0

                                data[commonval + ' Size1'] = 0
                                data[commonval + ' Size2'] = 0
                                data[commonval + ' Size3'] = 0
                                data[commonval + ' Size4'] = 0
                                data[commonval + ' Size5'] = 0

                        if float(tmpdata.get('strResptime')) <= 330 :
                                data[commonval + ' Resp_5'] += 1
                        elif float(tmpdata.get('strResptime')) <= 1000 :
                                data[commonval + ' Resp1'] += 1
#                               loggerapp.error("INFO:"+strLine)
                        elif float(tmpdata.get('strResptime')) <= 2000 :
                                data[commonval + ' Resp2'] += 1
#                               loggerapp.error("WARNING:"+strLine)
                        elif float(tmpdata.get('strResptime')) > 2000 :
                                data[commonval + ' Resp2o'] += 1
#                               loggerapp.error("ERROR:"+strLine)

                        if long(tmpdata.get('strByte')) <= 300000 :
                                data[commonval + ' Size1'] += 1
                        elif long(tmpdata.get('strByte')) <= 1000000 :
                                data[commonval + ' Size2'] += 1
                        elif long(tmpdata.get('strByte')) <= 2000000 :
                                data[commonval + ' Size3'] += 1
                        elif long(tmpdata.get('strByte')) <= 5000000 :
                                data[commonval + ' Size4'] += 1
                        elif long(tmpdata.get('strByte')) > 5000000 :
                                data[commonval + ' Size5'] += 1

                except :
                        sendLogApp(line)
                        print tmpdata
                        print line
                        print "Unexpected error:", sys.exc_info()[0]
                        pass

        f.close()

        fw=open(data['outfile']+'-'+startDate.strftime("%Y%m%d")+'-accesslog',"a+b")
        for item in items :
                fw.write("Host=" + data['host'])
                fw.write(" " +item)
                fw.write(" Count=" + str(data[item]))
                fw.write(" Bytes=" + str(data[item + ' Bytes']))
                fw.write(" Resptime=" + str(data[item + ' Resptime']) + " avg_Bytes=" + str(data[item + ' Bytes']/data[item]))
                fw.write(" avg_Resptime=" + str(data[item + ' Resptime']/data[item]/1000))
                fw.write(" Resptime_5=" + str(data[item + ' Resp_5']))
                fw.write(" Resptime1=" + str(data[item + ' Resp1']))
                fw.write(" Resptime2=" + str(data[item + ' Resp2']))
                fw.write(" Resptime2over=" + str(data[item + ' Resp2o']))
                fw.write(" TPS=" + str( float(data[item])/float(data['interval']) ) )
                fw.write(" swift=" + str(data['swift']))

                for itemtimer in itemstimer :
                        if data.get(item + ' ' + itemtimer):
                                fw.write(' ' + itemtimer + '=' + str(data[item + ' ' + itemtimer]/data[item]/1000000))
                        else :
                                fw.write(' ' + itemtimer + '=0')
                fw.write(" error=" + str(data.get(item+' err',0)))
                fw.write("\n")

                fw.write("Host=" + data['host'])
                fw.write(" " +item)
                fw.write(" Size1=" + str(data[item + ' Size1']))
                fw.write(" Size2=" + str(data[item + ' Size2']))
                fw.write(" Size3=" + str(data[item + ' Size3']))
                fw.write(" Size4=" + str(data[item + ' Size4']))
                fw.write(" Size5=" + str(data[item + ' Size5']))
                fw.write(" swift=" + str(data['swift']))
                fw.write("\n")

        fw.close()

fileLineRead(data['infile'])
os.rename (data['infile']+".bak",data['infile'])

fileProcess(loadDataResult)
os.remove (loadDataResult)
