import os
import sys

import hop
import malt


class Recipe:
    water_temp=20

    filepath=0
    status="on"
    ## VARS got from recipe file
    sys_vol=0
    sys_eff=0
    ##mash features
    mash_single_step_time=0
    mash_single_step_temp=0
    mash_fitasi_time=0
    mash_fitasi_temp=0
    mash_proteinrest_time=0
    mash_proteinrest_temp=0
    mash_betamilasi_time=0
    mash_betamilasi_temp=0
    mash_alphamilasi_time=0
    mash_alphamilasi_temp=0
    mashout_time=0
    mashout_temp=0
    mash_pause=0
    sparge_temp=0
    sparge_time=0
    sparge_pause=0
    boil_time=0
    boil_temp=0
    yatt=0
    ## classi Hop
    ##hop_bitter=0
    ## hop_taste=0
    ##hop_flav=0
    hops=[]
    hop_num=0
    ## classi Malt
    malt_dry=0
    malt_liquid=0
    malt_pils=0
    malt_pale=0
    malt_wheat=0
    ##
    malt_crystal=0
    malt_maris_otter=0
    malt_vienna=0
    malt_munich=0
    malt_biscuit=0
    malt_rye=0
    malt_special_b=0
    malt_cara_vienna=0
    malt_cara_munich=0
    malt_cara_pils=0
    ##
    malt_black=0
    malt_chocolate=0
    malt_roasted_barley=0
    ##
    flaked_barley=0
    flaked_wheat=0
    flaked_oat=0
    flaked_corn=0
    flaked_rice=0
    ##
    white_sugar=0
    brown_sugar=0
    honey=0


    ##estimated values based on the recipe
    og=0
    fg=0
    abv=0
    ibu=0
    style=0
    brew_time="0"

    def __init__(self, filepath):
        if len(sys.argv)==2:
            self.filepath=sys.argv[1]
        else:
            self.filepath=filepath

    def parseRecipe(self):
        print("Opening file: "+self.filepath)
        file=open(self.filepath, 'r')

        for l in file:
            ##excluding comments
            if "#" not in l:
                sub=l.split(":")
                if sub[0]=="system_final_volume":
                    self.sys_vol=float(sub[1])
                elif sub[0]=="system_efficiency":
                    self.sys_eff=float(sub[1])
                elif sub[0]=="dry_extract":
                    self.malt_dry=malt.Malt(float(sub[1]), 350, self.sys_eff, self.sys_vol)
                elif sub[0]=="liquid_extract":
                    self.malt_liquid=malt.Malt(float(sub[1]), 290, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_pilsner":
                    self.malt_pils=malt.Malt(float(sub[1]), 310, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_pale_ale":
                    self.malt_pale=malt.Malt(float(sub[1]), 300, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_wheat":
                    self.malt_wheat=malt.Malt(float(sub[1]), 320, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_crystal":
                    self.malt_crystal=malt.Malt(float(sub[1]), 270, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_maris_otter":
                    self.malt_maris_otter=malt.Malt(float(sub[1]), 310, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_vienna":
                    self.malt_vienna=malt.Malt(float(sub[1]), 300, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_munich":
                    self.malt_munich=malt.Malt(float(sub[1]), 300, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_biscuit":
                    self.malt_biscuit=malt.Malt(float(sub[1]), 300, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_rye":
                    self.malt_rye=malt.Malt(float(sub[1]), 310, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_special_b":
                    self.malt_special_b=malt.Malt(float(sub[1]), 270, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_cara_pils":
                    self.malt_cara_pils=malt.Malt(float(sub[1]), 280, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_cara_vienna":
                    self.malt_cara_vienna=malt.Malt(float(sub[1]), 280, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_cara_munich":
                    self.malt_cara_munich=malt.Malt(float(sub[1]), 280, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_acid":
                    self.malt_acid=malt.Malt(float(sub[1]), 290, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_chocolate":
                    self.malt_chocolate=malt.Malt(float(sub[1]), 250, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_black":
                    self.malt_black=malt.Malt(float(sub[1]), 250, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_roasted_barley":
                    self.malt_roasted_barley=malt.Malt(float(sub[1]), 250, self.sys_eff, self.sys_vol)
                elif sub[0]=="flaked_barley":
                    self.flaked_barley=malt.Malt(float(sub[1]), 280, self.sys_eff, self.sys_vol)
                elif sub[0]=="flaked_wheat":
                    self.flaked_wheat=malt.Malt(float(sub[1]), 290, self.sys_eff, self.sys_vol)
                elif sub[0]=="flaked_oat":
                    self.flaked_oat=malt.Malt(float(sub[1]), 280, self.sys_eff, self.sys_vol)
                elif sub[0]=="flaked_corn":
                    self.flaked_corn=malt.Malt(float(sub[1]), 330, self.sys_eff, self.sys_vol)
                elif sub[0]=="flaked_rice":
                    self.flaked_rice=malt.Malt(float(sub[1]), 320, self.sys_eff, self.sys_vol)
                elif sub[0]=="white_sugar":
                    self.white_sugar=malt.Malt(float(sub[1]), 360, self.sys_eff, self.sys_vol)
                elif sub[0]=="brown_sugar":
                    self.brown_sugar=malt.Malt(float(sub[1]), 350, self.sys_eff, self.sys_vol)
                elif sub[0]=="honey":
                    self.honey=malt.Malt(float(sub[1]), 270, self.sys_eff, self.sys_vol)
                elif sub[0]=="hop":
                    self.hops.append(hop.Hop(sub[1],float(sub[3]), float(sub[2]), float(sub[4]), self.sys_vol, float(sub[5])))
                    self.hop_num=self.hop_num+1
                ##elif sub[0]=="hop_taste":
                ##    self.hop_taste=hop.Hop(float(sub[3]), float(sub[2]), float(sub[1]), self.sys_vol, float(sub[4]))
                ##elif sub[0]=="hop_flavour":
                ##    self.hop_flav=hop.Hop(float(sub[3]), float(sub[2]), float(sub[1]), self.sys_vol, float(sub[4]))
                elif sub[0]=="yeast_att":
                  self.yatt=float(sub[1])
                elif sub[0]=="brew":
                    if sub[1]=="mash":
                        if sub[2]=="single_step":
                            self.mash_single_step_time=float(sub[4])
                            self.mash_single_step_temp=float(sub[3])
                        elif sub[2]=="fitasi":
                            self.mash_fitasi_time=float(sub[4])
                            self.mash_fitasi_temp=float(sub[3])
                        elif sub[2]=="proteinrest":
                            self.mash_proteinrest_time=float(sub[4])
                            self.mash_proteinrest_temp=float(sub[3])
                        elif sub[2]=="betamilasi":
                            self.mash_betamilasi_time=float(sub[4])
                            self.mash_betamilasi_temp=float(sub[3])
                        elif sub[2]=="alphamilasi":
                            self.mash_alphamilasi_time=float(sub[4])
                            self.mash_alphamilasi_temp=float(sub[3])
                        elif sub[2]=="mashout":
                            self.mashout_time=float(sub[4])
                            self.mashout_temp=float(sub[3])
                        elif sub[2]=="pause":
                            self.mash_pause=float(sub[3])
                    elif sub[1]=="sparge":
                        if sub[2]=="pause":
                            self.sparge_pause=float(sub[3])
                        else:
                           self.sparge_time=float(sub[3])
                           self.sparge_temp=float(sub[2])
                    elif sub[1]=="boil":
                        self.boil_time=float(sub[3])
                        self.boil_temp=float(sub[2])

        self.__estimated_og()
        self.__estimated_fg()
        self.__estimated_abv()
        self.__estimated_ibu()
        self.__estimated_style()
        self.__estimated_time()


    def __estimated_time(self):
        result=0
        if self.mash_single_step_time == 0:
            result=result+((self.mash_fitasi_temp-self.water_temp)*40)
            result=result+(self.mash_fitasi_time*60)
            result=result+((self.mash_proteinrest_temp-self.mash_fitasi_temp)*40)
            result=result+(self.mash_proteinrest_time*60)
            result=result+((self.mash_betamilasi_temp-self.mash_proteinrest_temp)*40)
            result=result+(self.mash_betamilasi_time*60)
            result=result+((self.mash_alphamilasi_temp-self.mash_betamilasi_temp)*40)
            result=result+(self.mash_alphamilasi_time*60)
            result=result+((self.mashout_temp-self.mash_single_step_temp)*70)
        else:
            result=result+((self.mash_single_step_temp-self.water_temp)*40)
            result=result+(self.mash_single_step_time*60)
            result=result+((self.mashout_temp-sel.mash_single_step_temp)*70)
        result=result+(self.mashout_time*60)
        result=result+(self.mash_pause*60)
        result=result+(self.sparge_temp-self.water_temp)*30
        result=result+(self.sparge_time*60)
        result=result+(self.sparge_pause*60)
        result=result+((self.boil_temp-self.mash_single_step_temp)*70)
        result=result+(self.boil_temp*60)
        hour=result%3600
        minute=(result-hour*3600)%60
        second=(result-(hour*3600+minute*60)
        self.brew_time="%02d:%02d:%02d" % (hour,minute,second)
        print("%02d:%02d:%02d" % (hour,minute,second))
    ##def __estimated_og(self):
    def __estimated_og(self):
        self.og+=1000
        if self.malt_crystal:
            self.og+=self.malt_crystal.calculate_og()
        if self.malt_pale:
            self.og+=self.malt_pale.calculate_og()
        if self.malt_black:
            self.og+=self.malt_black.calculate_og()
        if self.malt_dry:
            self.og+=self.malt_dry.calculate_og()

    def __estimated_fg(self):
        self.fg=int(round((self.og-1000)*(1-self.yatt)+1000))

    def __estimated_abv(self):
        self.abv=round((self.og-self.fg)/7.5, 1)

    def __estimated_ibu(self):
	for i in self.hops:
            self.ibu+=i.calculate_ibu()

    def __estimated_style(self):
        styles=(("Porter",30,50),("Stout",30,70),("APA",30,45),("EnglishIPA",40,60),("ImperialIPA",60,150),("Belgian",20,40))
        style_str=""
        for l in styles:
            if self.ibu >= int(l[1]) and self.ibu <= int(l[2]):
                if l[0]=="Porter" or l[0]=="Stout":
                   if str(self.malt_chocolate.kg)=="0.0" and str(self.malt_black.kg)=="0.0" and str(self.malt_roasted_barley.kg)=="0.0":
                      continue
                   else:
                      style_str += str(l[0]) + ","
##		if l[0]=="Porter" or l[0]=="Stout":
##		    if self.malt_chocolate.kg !=0.0 or self.malt_black.kg != 0.0 or self.malt_roasted_barley != 0.0:
##                	style_str += str(l[0]) + ","
		else:
                   if str(self.malt_chocolate.kg)=="0.0" and str(self.malt_black.kg)=="0.0" and str(self.malt_roasted_barley.kg)=="0.0":
                        style_str += str(l[0]) + ","
        self.style=style_str[:-1]


    def print_recipe(self):
	print("***********************")
	print( "\tRECIPE")
	print( "***********************")
	print( "MALT \t\tKg")
	print( "***********************")
	if self.malt_pils.kg != 0.0: print "PILS \t"+str(self.malt_pils.kg)
	if self.malt_pale.kg != 0.0: print "PALE ALE \t"+str(self.malt_pale.kg)
	if self.malt_wheat.kg != 0.0: print "WHEAT  \t"+str(self.malt_wheat.kg)
	if self.malt_dry.kg != 0.0: print "DRY_EXT \t"+str(self.malt_dry.kg)
	if self.malt_liquid.kg != 0.0: print "LIQ_EXT \t"+str(self.malt_liquid.kg)
	if self.malt_crystal.kg != 0.0: print "CRYSTAL \t"+str(self.malt_crystal.kg)
	if self.malt_maris_otter.kg != 0.0: print "MARIS \t"+str(self.malt_maris_otter.kg)
	if self.malt_vienna.kg != 0.0: print "VIENNA \t"+str(self.malt_vienna.kg)
	if self.malt_munich.kg != 0.0: print "MUNICH \t"+str(self.malt_munich.kg)
	if self.malt_biscuit.kg != 0.0: print "BISCUIT \t"+str(self.malt_biscuit.kg)
	if self.malt_rye.kg != 0.0: print "RYE \t"+str(self.malt_rye.kg)
	if self.malt_special_b.kg != 0.0: print "SPECIALB \t"+str(self.malt_special_b.kg)
	if self.malt_acid.kg != 0.0: print "ACID \t"+str(self.malt_acid.kg)
	if self.malt_cara_pils.kg != 0.0: print "CARAPILS \t"+str(self.malt_cara_pils.kg)
	if self.malt_cara_vienna.kg != 0.0: print "CARAVIENNA \t"+str(self.malt_cara_vienna.kg)
	if self.malt_cara_munich.kg != 0.0: print "CARAMUNICH \t"+str(self.malt_cara_munich.kg)
	if self.malt_chocolate.kg != 0.0: print "CHOCOLATE \t"+str(self.malt_chocolate.kg)
	if self.malt_black.kg != 0.0: print "BLACK \t"+str(self.malt_black.kg)
	if self.malt_roasted_barley.kg != 0.0: print "ROASTED \t"+str(self.malt_roasted_barley.kg)
	if self.flaked_barley.kg != 0.0: print "FLK_BAR \t"+str(self.flaked_barley.kg)
	if self.flaked_wheat.kg != 0.0: print "FLK_WHE \t"+str(self.flaked_wheat.kg)
	if self.flaked_oat.kg != 0.0: print "FLK_OAT \t"+str(self.flaked_oat.kg)
	if self.flaked_corn.kg != 0.0: print "FLK_COR \t"+str(self.flaked_corn.kg)
	if self.flaked_rice.kg != 0.0: print "FLK_RIC \t"+str(self.flaked_rice.kg)
	if self.white_sugar.kg != 0.0: print "WHT_SUG \t"+str(self.white_sugar.kg)
	if self.brown_sugar.kg != 0.0: print "BRO_SUG \t"+str(self.brown_sugar.kg)
	if self.honey.kg != 0.0: print "HONEY \t"+str(self.honey.kg)
	print("******************************************")
	print("HOP \tgr \tkind \ttime \taa")
	print("******************************************")
	for i in self.hops:
           if i.weight != 0: print i.name+" \t"+str(i.weight)+" \t"+str(i.kind)+" \t"+str(i.boil_time)+" \t"+str(i.aa)
	print("******************************************")
	print("BREW PROCESS")
	print("******************************************")
	if self.mash_single_step_time != 0:
           print("MASH \tSINGLE STEP \t"+str(self.mash_single_step_time)+" min @ "+str(self.mash_single_step_temp)+" C" )
	else:
           print("MASH \tFITASI \t\t"+str(self.mash_fitasi_time)+" min @ "+str(self.mash_fitasi_temp)+" C" )
           print("MASH \tPROTEINREST \t"+str(self.mash_proteinrest_time)+" min @ "+str(self.mash_proteinrest_temp)+" C" )
           print("MASH \tBETA-AMI \t"+str(self.mash_betamilasi_time)+" min @ "+str(self.mash_betamilasi_temp)+" C" )
           print("MASH \tALFA-AMI \t"+str(self.mash_alphamilasi_time)+" min @ "+str(self.mash_alphamilasi_temp)+" C" )
	print("MASH OUT \t\t"+str(self.mashout_time)+" min @ "+str(self.mashout_temp)+" C" )
	print("MASH PAUSE \t\t"+str(self.mash_pause)+" min" )
	print("SPARGE \t\t\t"+str(self.sparge_time)+" min @ "+str(self.sparge_temp)+" C")
	print("SPARGE PAUSE \t\t"+str(self.sparge_pause)+" min" )
	print("BOIL \t\t\t"+str(self.boil_time)+" min @ "+str(self.boil_temp)+" C")
	print("******************************************")
	print("******************************************")
	print("Estimated Result @ sys_eff="+str(self.sys_eff)+":")
        print("\tOG: \t"+str(self.og))
        print("\tFG: \t"+str(self.fg))
        print("\tABV: \t"+str(self.abv)+" %")
        print("\tIBU: \t"+str(int(round(self.ibu))))
        print("\tStyle: \t"+str(self.style))
	print("")
	print("Overall time: "+self.brew_time)

if __name__=="__main__":
    rec=Recipe("recipe.txt")
    rec.parseRecipe()

    rec.print_recipe()

    ##print "\tOG: \t"+str(rec.og)
    ##print "\tFG: \t"+str(rec.fg)
    ##print "\tABV: \t"+str(rec.abv)+" %"
    ##print "\tIBU: \t"+str(int(round(rec.ibu)))
    ##print "\tStyle: \t"+str(rec.style)

