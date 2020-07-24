

class Malt:
    hwe=0
    eff=0
    kg=0
    vol=0


    def __init__(self, kg, hwe, eff, vol):
        self.kg=kg
        self.hwe=hwe
        self.eff=eff
        self.vol=vol

    def calculate_og(self):
        og=round((self.kg*self.hwe*self.eff/self.vol), 2)
        return og


if __name__ == "__main__":
    ## pale ale 310
    ## crystal e blonde 280
    ## dark e roaster 250
    ## dry 350
    VOL=23
    EFF=0.7
    YEAST_ATT=0.75
    
    PALE_KG=5.5
    CRYSTAL_KG=1.5
    DARK_KG=0
    DRY_KG=0

    pale=Malt(PALE_KG,310,EFF,VOL)
    crystal=Malt(CRYSTAL_KG,280,EFF,VOL)
    dark=Malt(DARK_KG,250,EFF,VOL)
    dry=Malt(DRY_KG,350,EFF,VOL)

    pale_og=pale.calculate_og()
    crystal_og=crystal.calculate_og()
    dark_og=dark.calculate_og()
    dry_og=dry.calculate_og()

    print("MALT \t\tKG \tOG%")
    print("Pale ale \t"+str(pale.kg)+" Kg \t"+str(pale_og))
    print("Crystal \t"+str(crystal.kg)+" Kg \t"+str(crystal_og))
    print("Dark \t\t"+str(dark.kg)+" Kg \t"+str(dark_og))
    print("Dry Extr \t"+str(dry.kg)+" Kg \t"+str(dry_og))

    og=int(round((1000+pale_og+crystal_og+dark_og+dry_og)))
    fg=int(round((og-1000)*(1-YEAST_ATT)+1000))
    abv=round((og-fg)/7.5,1)

    print("Estimated OG: \t"+str(og))
    print("Estimated FG: \t"+str(fg))
    print("Estimated ABV: \t"+str(abv))




