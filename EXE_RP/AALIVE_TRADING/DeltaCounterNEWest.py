import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
#########################################
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#######################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
####################
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, TicksUtile, RP_Snapshot
import glob, csv, subprocess, datetime, shutil, time, os.path
from datetime import datetime
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
##date = '20151104'
##today = date
#############################
symbol_list = symdict.keys()
symbol_list =['ES']
########################################
def sum_array(array,mode):
    c=0
    suma =0
    while c < len(array):
        suma+=int(array[c])
        c+=1
        if mode == 'toponly':
            suma = int(array[0])
        else:
            pass
    return suma
#######
def sum_2arrays_weighted(array,array2,mode):
    c=0
    suma =0
    while c < len(array):
        suma+=float(array[c])*1#float(array2[c])
        c+=1
        if mode == 'toponly':
            suma = int(array[0])
        else:
            pass
    return suma/c
#############
def prepare_empty_array(fnums):
    c=0
    arrayout = []
    while c < fnums:
        arrayout.append(0)
        c+=1
    return arrayout
###########################
def checkDOMticks(sym,fnums):
    filein = DataDown +today+'.'+sym+ '.RTMktDepth.csv'
    buylineprice = prepare_empty_array(fnums)
    buylinesize = prepare_empty_array(fnums)
    selllineprice = prepare_empty_array(fnums)
    selllinesize =  prepare_empty_array(fnums)
    prevtotdiff = 0
    for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),1500):
##        print line
        
        position = int(line[1].replace('position=','').replace('>','').replace(' ',''))
        size = float(line[5].replace('size=','').replace('>','').replace(' ',''))
        operation = line[2].replace('operation=','').replace('>','').replace(' ','')
        price = float(line[4].replace('price=','').replace('>','').replace(' ',''))
        time = line[6].replace(' ','')
        zflag = 'clean'
        if price == 0 or size == 0:
##            print 'zeros'
            zflag = 'haszeros'
        if 'side=1' in str(line):
            buylineprice[position] = price
            buylinesize[position] = size
            buylinesizewtd = buylineprice[position] * buylinesize[position]
        else:
            selllineprice[position] = price
            selllinesize[position] = size
    ##        return buylineprice, buylinesize,selllineprice,selllinesize,timenow
    sizeweightedbid = sum_2arrays_weighted(buylineprice,buylinesize,'bla')
    sizeweightedsell = sum_2arrays_weighted(selllineprice,selllinesize,'bla')
    totalbuy = float(sum_array(buylinesize,'all'))
    totalsell = float(sum_array(selllinesize,'all') )    
    totdiff = totalbuy - totalsell
    totalratio = totalbuy/totalsell
    topbuy = float(sum_array(buylinesize,'toponly'))
    topsell = float(sum_array(selllinesize,'toponly'))     
    topdiff = topbuy - topsell
    if totdiff == 0:
        totdiff = 1
    if totalbuy > 0:
        totdiffperc = 100 * (round(float(totdiff/(totalsell +totalbuy)),3))
    else:
        totdiffperc  = 0.0
        ############
    if topdiff == 0:
        topdiff = 1
    if topbuy > 0:
        topdiffperc = 100 * (round(float(topdiff/(topsell +topbuy)),3))
    else:
        topdiffperc  = 0.0
##        print totdiffperc, totdiff, totalbuy
    difftoprev = totdiff - prevtotdiff
    prevtotdiff = totdiff
    buytopprice = buylineprice[0]
    selltopprice = selllineprice[0]
##    print 'SELL', selllinesize, totalsell, totdiff
    showflag = 'no'
    if abs(totalratio) > 1.20 or totalratio < .95 :
        showflag = 'show'
    if abs(difftoprev) > 2000000:
        showflag ='show'
    if  abs(topdiffperc)> 20000 :
        showflag = 'show'
    if showflag == 'show' :
##            print buytopprice,'BUY', buylinesize, totalbuy, totdiff, totalsell, selllinesize, 'SELL',selltopprice,time,difftoprev,str(totdiffperc)
##        print 'tot',totalbuy,'x',totalsell, totdiff, str(totdiffperc),'%', difftoprev
        print 'topBOOK>>',topbuy,'x',topsell, 'Topbuy ratio =',round(topbuy/(topsell+1),2), 'Totalbook Ratio >>>',round(totalratio,2)
##        print time,'B', buylinesize,  selllinesize, 'S',buytopprice,selltopprice
###############################
##fullarray =[]
def create_TS_array(sym,fnums):
    recentlimit = 2000000
    fullarray =[]
    filein = DataDown +today+'.'+sym+ '.RTtickData.csv'
    prevtotdiff = ask = bid =0
    prevtime =''
    string =''
    prevtradeuid=''
    time = ''
    size = ''
    tprice = 0.0
    tsize = singletrade = totdaysize= vwap =''
    totdowns = totups = 0
    tottickups=0
    nettickhits = 0
    lastsize = lastprice = bidsize = asksize =  0
    prevtick = nettickups = totHits = totLifts = 0
    tickflag = tickdir = minute = hour =  'na'
    bidsize=bidp=askp=asksize=empty = tsizenew = tpricenew= 'na'
##    aout=[tickflag,tprice,tsize,bid,ask,tickdir,nettickhits,nettickups,minute,hour,time]
    newline=[]
    newlist = [bidsize,bidp,askp,asksize,tpricenew,tsizenew,tickflag,tprice,tsize,tickdir,minute,hour,time]
    for item in newlist:
        newline.append(item)

    for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),recentlimit):
        if 'tickSize' in line[0] or 'tickPrice' in line[0]:
##            print line
            fflag = line[1].replace(' field=','')
            value = float((line[2].replace(' size=','')).replace('>','').replace(' price=',''))
            time = line[len(line)-1]
            #############
        if 'tickSize' in line[0] :
##   0 BID_SIZE tickSize() 1 BID_PRICE tickPrice() 2 ASK_PRICE tickPrice() 3 ASK_SIZE tickSize() 4 LAST_PRICE tickPrice()5 LAST_SIZE tickSize()
            size = value
            newline[int(fflag)]=value
            ##################
        if 'tickPrice' in str(line) and int(fflag) < 4:
            newline[int(fflag)]=value
##########################
        if 'tickString' in str(line) and 'tickType=48' in str(line):
            ttime = line[3]
            string = line[2].split(';')
            if len(string) > 2:
                tprice = float(string[0].replace('value=',''))
                tsize = float(string[1])
                newline[5]=tsize
                newline[7]=tprice
                newline[8]=tsize
                singletrade = string[5]
                notsure = string[5]
                totdaysize = string[3]
                vwaps  = string[4]
                if len(vwaps) > 0:
                    vwap  = round(float(string[4]),2)
                else:
                    vwap =0.0 ##            value=1984.50;1;1441796865858;207069;1982.49963539;true>
        ##            if bid == 0.0:
                tradeuid = ttime + str(tsize) + str(tprice)
                if   tradeuid != prevtradeuid:
##                    print 'adding line'
                    #bid > 0 and ask > 0 and
                    aout =[]
                    
                    if prevtick < tprice:
                        tickdir = 'uptick'
                    elif prevtick == tprice:
                        tickdir = 'flat'
                    else:
                        tickdir = 'downtick'
                    prevtick = tprice
                    if tsize > 0 and ttime != 'xxx':
                        minute = ttime[0:5]#'20:47:32.488000'
                        hour = ttime[0:4]
                 
    ##                newline=[bidsize,bidp,askp,asksize,empty,tsizenew,tickflag,tprice,tsize,bid,ask,tickdir,minute,hour,time]
                    newline[12]=ttime
                    newline[11]=hour
                    newline[10]=minute
                    newline[9]=tickdir
                    numlist = [0,1,2,3,4,5,6,7,8,9,10,11,12]
                    for n in numlist:
                        aout.append(newline[n])
                    fullarray.append(aout)  ### how many upticks in a row?
                prevtime = ttime
                prevtradeuid = tradeuid
    return fullarray
###############################
def show_by_fnum(fullarray,fnum):
    c=0
    x = len(fullarray)
    timelist =[]
    hourlist =[]
    for l in fullarray:
        timelist.append(l[fnum])
        c+=1
        if c > (x - 8):
            print l
    timelistu = rpu_rp.uniq(timelist)
    c=0
    lengtu = len(timelistu)
    for t in timelistu:
##        print t
        totalsize = 0
        HitLift = 0
        c+=1
        netdelta =0
        upticks = downticks =  HitLift =  0
        sumtagval = totsize = 0
        for l in fullarray:
            bid = l[1]
            ask = l[2]
            tsize = l[5]
            tprice = l[7]
            sumtag = l[fnum]
            if t == sumtag:
                totsize += tsize
                sumtagval +=1
                if tprice == bid:
                    quoteflag = 'HitBid'
                    HitLift = HitLift -1
                else:
                    quoteflag = 'LIFT'
##                    print bid
                    HitLift = HitLift +1
##        print HitLift
        print '%-8s %8s %8s %8s    price,vsumtagval, totsize,vHitLift' %(t,sumtagval,totsize,HitLift)     
##        if c > (lengtu - 5):
##            print t, totalsize, netdelta, upticks,downticks,neutralticks,upticksize,downticksize,neutralticksize,tprice
################        
threshold = 0.0
loopmax = 1
loop = 0
sleeptime = 9
while loop < loopmax:
    sym = 'ES'
    print '====='
    TimeAndSales = create_TS_array(sym,1)
    print '-----'
##    for l in TimeAndSales:
##        print l
    show_by_fnum(TimeAndSales,7) # price
    print '---'
##    show_by_fnum(TimeAndSales,9) # hour
    print '----'
##    show_by_fnum(TimeAndSales,11) #minute
##    createVolHistogram(sym,1)
    print '>>>>>'
####    checkDOMticks(sym,10)
    sleep(sleeptime)
    loop+=1
'''
another array with price gaps...then the top gap as in width between bidoffer
scenariios....
bidHitNfad...count how often
offerliftnfade
others?
trade top book bid, bid size increses...opp for sell

#################################onerow =[]
##genericTicks other types with return codes:
##100 Option Volume (currently for stocks) 29, 30
##101 Option Open Interest (currently for stocks) 27, 28
##104 Historical Volatility (currently for stocks) 23
##162 Index Future Premium 31
##165 Miscellaneous Stats 15, 16,17, 18,19, 20,21
##221 Mark Price (used in TWS P&L computations) 37
##225 Auction values (volume, price and imbalance) 34, 35,36
##########233 RTVolume - contains lasttradeprice, lastsize, lasttime, totalvolume, VWAP, single trade flag.48
##Single trade flag - True indicates filled by a single market maker; False is multiple marketmakers
##Here is an example of the RTVolume formatting for AAPL:
##RTVolume=701.28;1;1348075471534;67854;701.46918464;true
##RTVolume=701.26;3;1348075476533;67857;701.46917554;false
TickType.getField(int tickType) to
retrieve the field description. For example, a field value of 38

0 BID_SIZE tickSize()
1 BID_PRICE tickPrice()
2 ASK_PRICE tickPrice()
3 ASK_SIZE tickSize()
4 LAST_PRICE tickPrice()
5 LAST_SIZE tickSize()
6 HIGH tickPrice()
7 LOW tickPrice()
8 VOLUME tickSize()
9 CLOSE_PRICE tickPrice()
10 BID_OPTION_COMPUTATION tickOptionComputation()
See Note 1 below
11

7 LOW tickPrice()
8 VOLUME tickSize()
9 CLOSE_PRICE tickPrice()
10 BID_OPTION_COMPUTATION tickOptionComputation()
See Note 1 below
11 ASK_OPTION_COMPUTATION tickOptionComputation()
See Note 1 below
12 LAST_OPTION_COMPUTATION tickOptionComputation()
See Note 1 below
13 MODEL_OPTION_COMPUTATION tickOptionComputation()
See Note 1 below
14 OPEN_TICK tickPrice()
15 LOW_13_WEEK tickPrice()
16 HIGH_13_WEEK tickPrice()
17 LOW_26_WEEK tickPrice()
18 HIGH_26_WEEK tickPrice()
API Reference Guide 525
Chapter 9 Reference
Tick Value Description Event/Function/Method
19 LOW_52_WEEK tickPrice()
20 HIGH_52_WEEK tickPrice()
21 AVG_VOLUME tickSize()
22 OPEN_INTEREST tickSize()
23 OPTION_HISTORICAL_VOL tickGeneric()
24 OPTION_IMPLIED_VOL tickGeneric()
25 OPTION_BID_EXCH NOT USED
26 OPTION_ASK_EXCH NOT USED
27 OPTION_CALL_OPEN_INTEREST tickSize()
28 OPTION_PUT_OPEN_INTEREST tickSize()
29 OPTION_CALL_VOLUME tickSize()
30 OPTION_PUT_VOLUME tickSize()
31 INDEX_FUTURE_PREMIUM tickGeneric()
32 BID_EXCH tickString()
33 ASK_EXCH tickString()
34 AUCTION_VOLUME tickSize()
35 AUCTION_PRICE tickPrice()
36 AUCTION_IMBALANCE tickSize()
37 MARK_PRICE tickPrice()
38 BID_EFP_COMPUTATION tickEFP()
39 ASK_EFP_COMPUTATION tickEFP()
40 LAST_EFP_COMPUTATION tickEFP()
41 OPEN_EFP_COMPUTATION tickEFP()
42 HIGH_EFP_COMPUTATION tickEFP()
43 LOW_EFP_COMPUTATION tickEFP()
44 CLOSE_EFP_COMPUTATION tickEFP()
45 LAST_TIMESTAMP tickString()
46 SHORTABLE tickString()
47 FUNDAMENTAL_RATIOS tickString()
48 RT_VOLUME tickString()
49 HALTED See Note 2 below.
50 BIDYIELD tickPrice()
See Note 3 below
51 ASKYIELD tickPrice()
See Note 3 below
'''
