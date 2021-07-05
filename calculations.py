import math as m
import json
import polar_diagram as pd


def absolute_waarde(getal):
    """
       deze functie geeft de absolute waarde van een getal terug

       Parameters:
           getal (int):

       Returns:
           absolute waarde van getal
       """
    if getal < 0:
        return getal*-1
    else:
        return getal



def direct_course(boot_c,waypoint):
    """
       deze functie berekent de directecourse van de locatie van de boot naar het waypoint

       Parameters:
           boot_c (float): de coordinaat van de boot
           waypoint (float): de coodinaat van het waypoint

       Returns:
           course (int): de directe course van je loctie tot het waypoint
       """
    deltab = waypoint[0] - boot_c[0]
    deltal = waypoint[1] - boot_c[1]
    if deltal == 0:
        if deltab > 0:
            course = 0
        elif deltab < 0:
            course = 180
    elif deltab == 0:
        if deltal > 0:
            course = 90
        elif deltal < 0:
            course = 270
    elif deltab == 0 and deltal == 0:
        main = 0
    else:
        course = m.degrees(m.atan(absolute_waarde(deltab)/absolute_waarde(deltal)))
        if deltal > 0 < deltab:
            course = 90 - course
        elif deltal > 0 > deltab:
            course = course + 90
        elif deltal < 0 > deltab:
            course = 180 + (90 - course)
        elif deltab < 0 < deltal:
            course = course + 270
    return round(course)



def boat_wind_angle(TWA, course):
    """
           deze functie berekent de hoek vvan de wind op de koers van de boot

           Parameters:
               TWA (int): true wind angle, of wel de windrichting in grade. een getal van 0 tot 360
               course (int): de richting waar de boot in vaart in graden. een getal van 0 tot 360

           Returns:
               bwa (int): boat wind angle, de hoek van de wind ten opzichte van hoe de bood vaart in graden. een getal van 0 tot 180
           """
    bwa = absolute_waarde(course - TWA)
    if bwa >180:
        if course > 180:
            bwa = TWA + absolute_waarde(360-course)
        elif TWA > 180:
            bwa = course + absolute_waarde(360-TWA)
    elif bwa == 180:
        bwa = 0
    return bwa


def waypoint_course_dif(c, WPA):
    """
           deze functie berektent het verschil tussen de directe koers en een optionele koers

           Parameters:
               c (int): optionele koers van de boot in graden. een getal van 0 tot 360
               WPA (int): WayPoint Angle, de directe koers van de loctie van de boot tot het waypoint in grade.
                          een getalvan 0 tot 360.

           Returns:
               wcd (int): waypoint course difrence, de hoek tussen de optionele koers en de waypoint angle.
                          een getal van 0 tot 180
           """
    wcd = absolute_waarde(c - WPA)
    if wcd >180:
        if c > 180:
            wcd = WPA + absolute_waarde(360-c)
        elif WPA > 180:
            wcd = c + absolute_waarde(360-WPA)
    return wcd


def Course_speed(bwa, kts):
    """
           deze functie haalt de bijbehoornde snelheid van de boot uit het polar tabel

           Parameters:
               bwa (int): boat wind angle, de hoek van de wind ten opzichte van hoe de bood vaart in graden. een getal
               van 0 tot 180
               kts (int): de windsnelheid in knopen

           Returns:
               de snelheid van de boot, bepaald vanuit het polar tabel
           """
    with open('PolarTable.json') as f:
        data = json.load(f)
    return float(data[str(kts)][str(bwa)])


def optimal_vmc(WPA, TWA, kts):
    """
           deze functie berekent de optimale VMG

           Parameters:
               WPA (int): WayPoint Angle, de directe koers van de loctie van de boot tot het waypoint in grade.
                          een getalvan 0 tot 360.
               TWA (int): true wind angle, of wel de windrichting in grade. een getal van 0 tot 360
               kts (int): de windsnelheid in knopen

           Returns:
               oc (int): optimal course, de optimale koers die de boot kan varen richting het waypoint.
           """
    oVMC = 0
    oc = 0
    for i in range(180):
        c = WPA + i - 90
        if c < 0:
            c = 360 + c
        bwa = boat_wind_angle(TWA, c)
        cs = Course_speed(bwa, kts)
        wcd = waypoint_course_dif(c, WPA)
        VMC = absolute_waarde(cs * m.cos(m.radians(wcd)))
        if VMC > oVMC:
            oc = c
            oVMC = VMC
    return oc

