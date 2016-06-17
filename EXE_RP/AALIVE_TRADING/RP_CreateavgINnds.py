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
global recentlimit, time_format,today,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time
from datetime import datetime
import ctypes 
date = today
now = datetime.strftime(datetime.now(),spaceYtime_format)
#######################
cpfname = EXE + 'signalcontroller.txt'
symbol_list = symbol_list2
print symbol_list
##symbol_list = ['EUR.USD']
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday':#  and b != '5 secs':
##    if modedict[b] == 'daily'  and b != '5 secs':
        barlist.append(b)
##print barlist
##################
prevsigid = ''
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
def read_varlist(cpfname): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(cpfname)
    lista =[]
    for line in paramlines:    
        varstring = line[0]
        lista.append(varstring)
    return lista
#########################3
def check_for_CP_change(fname): ##read timestamp from the control panel file
##    from datetime import datetime
    fstring = '%a %b %d %H:%M:%S %Y'
    now_epoch = time.time() 
    filetime = time.ctime(os.path.getmtime(fname))
    filetime_ep = int(time.mktime(time.strptime(filetime, fstring)))
    diff = now_epoch - filetime_ep
    return diff
#########################3
def read_vars(varstringin,cpfname): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(cpfname)
    for line in paramlines:
##        print line
        varstring = line[0]
        if len(line) > 1 and varstring == varstringin:
            varvalue =line[1]
    return varvalue
########################
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
############################
import winsound, sys
def beep(sound):
    pass
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
###############
def look_for_dupe_sig(livesigid,livesigtime,delay):
    showflag = 'show'
    livesigepoch = TicksUtile.time_to_epoch(livesigtime)
    if os.path.isfile(sigarea + today +'.recentsigs.csv'): 
        tradedsigs= rpu_rp.CsvToLines(sigarea + today +'.recentsigs.csv')
        showflag = 'show'     
        for lin in tradedsigs:
##            print lin
            if len(lin) > 3:
##                print lin
                sigid = lin[9]
                sigtime = lin[3]              
##                print sigid,sigtime,livesigid,livesigtime
                sigtimeepoch = TicksUtile.time_to_epoch(sigtime)
                timediff = livesigepoch - sigtimeepoch
                if sigid == livesigid and timediff < delay:
                    showflag = 'supress'
    return showflag
#################################
def show_spots(sym,date,limit):
    curprice = float(TicksUtile.recenttick(sym,'recent'))
    spotfile = libarea + 'spotlines.' + sym+ '.csv'
    spotlines= rpu_rp.CsvToLines(spotfile)
    print limit, ' is limit'
    for l in spotlines:
        spotp = float(l[0])
        distance = abs(spotp-curprice)
        if (spotp-curprice) > 0:
            underover = 'under'
        else:
            underover = 'over'
        if distance < limit:
##            print curprice-spotp,spotp,curprice,sym,'spot prices',limit
            if underover == 'under':
                print 'ready to SELL at ',spotp, 'how manypasses?',curprice,sym,distance
            else:
                print 'ready TO BUY at ',spotp, 'how manypasses?',curprice,sym,distance
#####################
def show_bar8_range(start,end,sym,date):
    print 'this is the bar8 range of lines',start,end
    after5lines = RP_Snapshot.show_bar_range(sym,'5mins',start,end,date)
    linecount =0
    trigger = 'inactive'
    for line in after5lines:
        bartime = line[1]
        linecount +=1
##        print line
        if linecount ==1:
            starthi = line[3]
            startlo = line[4]
            print '>>>> BAR 8 HILO = <<<<<', starthi, startlo, bartime
            pass
        curbarhi = line[3]
        curbarlo = line[4]
        if curbarhi < startlo and trigger != 'active':
            print 'going down',line
            trigger = 'active'
        elif curbarlo > starthi and trigger != 'active':
            print 'going up',line
            trigger = 'active'
        else:
            pass
    print '======================'
######################
def make_bars_just_5sec(startmode):
    for sym in symbol_list:
        TicksUtile.prepare_tickfilesto5secBars(today,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
#################
    #############
def make_bars_no_5sec(startmode,durmode):
    for sym in symbol_list:
        if durmode == 'alldurs':
            barlist =  barlistAll
        elif durmode == '78':
            barlist = barlist78
        else:
            barlist = barlistRecent
        for dur in barlist :
            if dur == '1min':
                basisdur = '5secs'
            else:
                basisdur  = '1min'
            TicksUtile.assemble_dur_bars(today,sym,dur,startmode,basisdur)
#################
def make_bars_just_5sec(startmode):
    for sym in symbol_list:
        TicksUtile.prepare_tickfilesto5secBars(today,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
#################
def make_states(smode,date,symbollist):
    threshold = 0.0
    if smode == 'fullist':
        indlist = fullindlist
    else:
        indlist = partindlist
    barlist = barlistRecent78
    for sym in symbollist:
        for dur in barlist :
##            print sym,dur
            rpInd.create_states_files(sym,dur,date,threshold,indlist)
#################
def run_8s(sym): 
    if sym == 'ES' and 'bla' == 'bla':
##        show_bar8_range('04:00:00','7:00:00',sym,date) #asia
        show_bar8_range('09:30:00','12:25:00',sym,date) #europe
        show_bar8_range('16:00:10','18:25:00',sym,date) #usa 
###################
def create_latest_state_array(sym):
    indlist = partindlist
    durlist = barlistRecent
    currentstates =[]
    for dur in durlist:
        for ind in indlist:
            lastbar = rpInd.ShowLastBarofInd(sym,dur,ind)
            currentstates.append(lastbar)
    return currentstates
#####################
def create_previous_state_array(sym,barnum):
    indlist = partindlist
    durlist = barlistRecent
    currentstates =[]
    last1minbar = rpInd.ShowABarofInd(sym,'1min','mcross',barnum)
    timeofbar = last1minbar[0]
    print timeofbar
    for dur in durlist:
        for ind in indlist:
            lastbar = rpInd.ShowABarofIndByTime(sym,dur,ind,timeofbar,barnum)
            currentstates.append(lastbar)
    return currentstates
#####################
##print indsMIDdict
def rule_tester(currentstates,rule,curprice):
##    print currentstates, 'arrayin' [' 2015-09-18', '17.3051', 'pos', '8.3948', 'slopeup',
##    rule = ['mcross','5mins','stringtest','neg',fnum,maxval,minval,'SELL']
    flag = 'nomatch'
    rind = rule[0]
    rdur = rule[1]
    rinddur = rind + rdur
##    print rule
    ##ROC,15mins,value,NA,1,.80%
    rtype = rule[2]
    percenttest = float(rule[5])
    rstring = rule[3]
    fnum = int(rule[4])

    rulename = rind+rdur+rtype+rstring
    midpoint = float(indsMIDdict[rinddur])
    normalslope = indsVALNORMALdict[rinddur]
    normalstring = indsSTRINGNORMALdict[rinddur]
    maxpoint = float(indsMAXdict[rinddur])
    rulerange = (maxpoint - midpoint)*2
    midvalue = maxpoint - midpoint
    trigger = percenttest * midvalue
    hitrigger = midpoint + trigger
    lotrigger = midpoint - trigger
    svalall =''
    normal = 'normal'
    for l in currentstates:
        if flag ==  'passedrule':
            pass
        else: #keep looking
            if len(l) > 0:
                sind = l[5]
                sdur = l[8]
                sindsdur = sind+sdur
##                print l
                if rtype == 'value' or rtype == 'priceCompare':
                    sval = float(l[fnum])
                else:
                    sval = l[fnum]
                svalall = svalall + str(sval)
                if '1min' in str(l):
                    stime = l[0]
                    sigprice = l[11]
                if sind == rind and sdur == rdur :
                    if rtype == 'string' and 'slope' in str(sval):
                        flag = 'BUY'
                        if rstring == 'slope' and normal == normal:
                            flag = 'SELL'
                    elif rtype == 'priceCompare':
                        print 'comparing',curprice,sval,rind
                        if sval > float(curprice) and normalstring == 'below':
                            print 'below price'
                            if normalslope == 'normal': ### akupper would have a flipped normal here..
                                flag = 'SELL'
                            else:
                                flag = 'BUY'
                        elif sval <  float(curprice)  and normalstring == 'above':
                            if normalslope == 'normal':
                                flag = 'BUY'
                            else:
                                flag = 'SELL'
                    elif rtype == 'value' :
                        if sval >  hitrigger:
                            if normal == normal:
                                flag = 'SELL'
                            else:
                                flag == 'BUY'
                        elif sval < lotrigger:
                            if normal == normal:
                                flag = 'BUY'
                            else:
                                flag == 'SELL'
                        else:
                            flag = 'nomatch'
                    else:
                        flag = 'nomatch'
    return flag,rulename,stime,sigprice,sval
##normal = slopedn sell, top20% sell, pricecompare GT is sell
##ind, dur,  midpoint value, max abs value, normal OR reverse,,,,,\
##tside [negative[lLT midpoint=BUY],normal OR reverse tside slope[slopedn = SELL],,,,,
##Stoch_CROSS5mins,0,5,slopedn,negcrossxx
##StochK,5mins,0,5,slopedn,normal
### ind,dur,typetest, testtext,fnumvalue,midval,maxval,rulerange,normalflag
##ROC,15mins,string,slopeup,4,9999
#################################################
#############################
####################
##################
def rule_testerold(currentstates,rule,curprice):
##    print currentstates, 'arrayin' [' 2015-09-18', '17.3051', 'pos', '8.3948', 'slopeup',
##    rule = ['mcross','5mins','stringtest','neg',fnum,maxval,minval,'SELL']
    flag = 'nomatch'
    rind = rule[0]
    rdur = rule[1]
    rtype = rule[2]
    rmin = float(rule[5])
    rmax = float(rule[6])
    rstring = rule[3]
    fnum = int(rule[4])
    raction= rule[7]
    rulename = rind+rdur+rtype+str(rmin)+str(rmax)+rstring+raction
    svalall =''
    for l in currentstates:
        if flag == 'nomatch':
            if len(l) > 0:
                sind = l[5]
                sdur = l[8]
                sval = l[fnum]
                svalall = svalall + sval
                if '1min' in str(l):
                    stime = l[0]
                    sigprice = l[11]
                if sind == rind and sdur == rdur :
                    if rtype == 'stringtest':
                        if sval == rstring:
                            flag = raction
                    elif rtype == 'priceCompareGT':
                        if float(sval) <  float(curprice):
                            flag = raction
                    elif rtype == 'priceCompareLT':
                        if float(sval)  >  float(curprice):
                            flag = raction
                    elif rtype == 'valtest' :
                        if float(sval) > rmin and float(sval) < rmax:
                            flag = raction
                    else:
                        flag = 'nomatch'
    return flag,rulename,stime,sigprice,sval
#######################
##rulesfile = [stochDGT20,stochD,20,'string'/'val',]
def ruleslist():
    rule1 = 'mcross on all but 1 min'
    rule2 = 'stochd under over 20 80 and sloping and crossing K'
    rule3 = 'threshold use for crosses'
    rule4 = 'if position and mcross opposite dir, close, maybe not revers'
    rule5 ='mcd 15min'
    rule6 = 'rsi'
    indlist = ['mcross','mcd','RSI','StochK','Stoch_CROSS','StochD']
###########################
def run_rulesets(sym,currentstates,sigtime,curprice):
    c=0
    rulesets =glob.glob(RulesArea +'*.rules.csv')
    results=[]
    for rulefilebig in rulesets:
        rulefiler=   rulefilebig.replace('RulesArea\\',';')
        rulefiler=   rulefilebig.replace('RulesNew\\',';')
        rulefilelen = len(rulefiler.split(';'))
        rulefile = (rulefiler.split(';'))[rulefilelen-1]
        ruleset = rpu_rp.CsvToLines(RulesArea +rulefile) # create list based on .rules.
############        print ' === ruleset ===', rulefile, sym
        c=0
        for rule in ruleset:           
            resultboth = rule_tester(currentstates,rule,curprice)
            result = resultboth[0]
            sigrealprice = resultboth[3]
            sigrealtime = resultboth[2]
            sigrulename = resultboth[1]
            sval = resultboth[4]  
            c+=1
            if c==1:
                prevresult = result
            if result == prevresult:
                fullmatch = result
                prevresult = result
            else:
                fullmatch = 'nomatch'
                prevresult = 'nomatch'
##        print 'finalresult ruleset',fullmatch,sigrulename,sigtime
        resultline=[]
        resultline.append(sym)
        resultline.append(fullmatch)
        resultline.append(rulefile)
        resultline.append(sigrealtime)
        resultline.append(sym)
        resultline.append(curprice)
        resultline.append(sigrealprice)
        resultline.append(sval)
        results.append(resultline)
    return results
    #########################
def parse_signalsNEW(rulesetoutput):
##    recentsigs = ['ES', 'SELL', 'testname', '1945.75', 'idstr', ' 2015-09-18 21:45:05']
##    [['result', 'SELL', 'stochkeasy1minSELL.rules.csv', ' 2015-09-23 08:16:05', 'CL', 46.36]]
    dur = ''
    if len(rulesetoutput) > 0:
        sigcount =0
        for sig in rulesetoutput:
            if len(sig) > 0  and sig[1] != 'nomatch':
                sig.append(now)
                print sig,'sigline'
                sigtime = sig[3]
                indvalue = 0.0 #float(sig[len(sig)-2])   <<<<<<<<<<<<<<<<<<
                sym = sig[4]
                sigtype = sig[2]
                priceinsignal = float(sig[5]) ### need to unboost the price...
                dboost = dboostdict[sym]
                newprice = priceinsignal / float(dboost)
                sig[5] = newprice
                tside =sig[1]
                dur = '0mins' # sig[8]   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                livesigid = sym+tside+dur+sigtype
                sig.append(livesigid)
                showflag = look_for_dupe_sig(livesigid,sigtime,delaydupetime)   #'notsupress'        
                sigcount+=1
                if showflag != 'supress':
                    if tside == 'SELL':
                        beep(soundarea+'sell')
                        print sig
                        beep(soundarea+sym)
                        print '==============='
                    elif tside == 'BUY':
                        beep(soundarea+'buy')
                        print sig
                        beep(soundarea+sym)
                        print '==============='
                    else:
                        print 'supressing'              
    ######                RP_Snapshot.snapshot_sym(sym,today)               
                    frsigline=[]
                    rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigs.csv', [sig]) 
                    rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigsexec.csv', [sig])   
############
####def slice_dice_dectector(sym,date,starttime,endtime,spotline,direction):
####    for bar in rangebars:
####        if direction == 'up':
####            firsttouch = if spotline is breached...5sec bar is lowhigh on spot
####            tagstatus = 'touched'
####            if tagstatus =='touched, look for next touch...withing
####            after first touch, should move back minimum 1 point...BEFORE
####            moving 2.75 handles above
####        if spotline
####        Status1tou
        ####################
btmode = 'BACKTESTxx'
if btmode == 'BACKTEST':
    loopmax = 2
else:    
    loopmax = 20000
loop = 0
delaydupetime = 200
recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = 10 #int(read_vars('CycleTime',cpfname))
print 'recent limit is now.. ', recentlimit
prevcycledelay = 2
threshold = 0.0
########################
symind = 'ES'
inddur = '15mins'
partbarlist = ['15mins','5mins','1hour']
for ind in nonlineindlist:
    for inddur in partbarlist:
        stats = rpInd.MaxMinAvgIndArray(symind,inddur,ind,1)
        print symind,inddur,ind,stats
sleep(14)    
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now
#############
##Rules EW
##Wave 3 must never be the shortest impulsive wave.
##Wave 2 can never retrace 100% of wave 1.
##Wave 4 cant overlap wave 1.
##Guidelines
##Wave 3 is generally the longest impulse wave of the 5 wave sequence.
##Wave 4 is generally a flat to sideways choppy move that tends to correct in time as opposed to price.
##Wave 2 is generally a sharp decline or a zig zag correction.
##Fibonacci Guidelines
##Wave 3 is usually a 1.618 or 2.618 extension of wave 1
##Wave 4 generally retraces between 38.2% of wave 3 if it's a 1.618 extension or 23.6% if a 2.618 extension or in between.
##Wave 5 is usually a .618 of wave 1 or equal to wave 1.
##Wave 2 will generally retrace between 50% and 78.6% of wave 1.
##So let's take those rules and guidelines to the last chart and see how many we can tick of the list.

##stochK,reverse,8020,slopenormal,####ind,pos=buy,maxboundries,slopeup=buy
##pivot,isline,8020,slopenormal
##R,isline,8020,slopenormal
##S,isline,8020,slopenormal
##
##diffvES,normal,0,slopenormal
##RSI,reverse,8020,slopenormal
##StochK,reverse,8020,slopenormal
##Stoch_CROSS,reverse,0,slopenormal
##StochD,reverse,8020,slopenormal
##mcross,normal,0,slopenormal
##ind, dur,  midpoint value, max abs value, normal OR reverse,,,,,\
##tside [negative[lLT midpoint=BUY],normal OR reverse tside slope[slopedn = SELL],,,,,
'''
Stoch_CROSS5mins,0,5,normal,normal
StochK5mins,0,5,normal,normal
ROC5mins,0,5,normal,normal
RSI5mins,0,5,normal,normal
mcd5mins,0,5,normal,normal
MACross5mins,0,5,normal,normal
klower5mins,0,5,normal,normal
'''
############

