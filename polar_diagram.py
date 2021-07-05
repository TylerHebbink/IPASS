import json


def write_polartable():
    """
            deze functie maakt een json file aan met daarin voor de windsnelheden 6 t/m 20 de snelhijd die de boot heeft
            voor elke graad ten opzichten van de wind. de functie heeft een json file nodig met daarin het polare
            diagram van de boot uitgeschreven

            """
    y = {}
    with open("PolarDiagram.json", "r") as read_file:
        diagram = json.load(read_file)

    with open("PolarTable.json", "w") as table:

        for x in range(15):

            objects = {}
            kts = x + 6
            if kts in (6, 8, 10, 12, 14, 16, 20):
                minimum = float(diagram["laagste_course"][str(kts)]["course"])
                maximum = float(diagram["hoogste_course"][str(kts)]["course"])
                for course in range(180):
                    if course > minimum or course < maximum:
                        speed = 0
                        objects[str(course)] = str(speed)
                    elif maximum <= course < 52:
                        s0 = float(diagram["hoogste_course"][str(kts)]["speed"])
                        s1 = float(diagram["52"][str(kts)])
                        deltas = s1 - s0
                        marge = deltas/(52 - maximum)
                        deltac = course - maximum

                        speed = round(s0 + (marge*deltac), 2)
                    elif 52 <= course < 60:
                        speed = calculate_snelheid(52, 60, course, kts)
                    elif 60 <= course < 75:
                        speed = calculate_snelheid(60, 75, course, kts)
                    elif 75 <= course < 90:
                        speed = calculate_snelheid(75, 90, course, kts)
                    elif 90 <= course < 110:
                        speed = calculate_snelheid(90, 110, course, kts)
                    elif 110 <= course < 120:
                        speed = calculate_snelheid(110, 120, course, kts)
                    elif 120 <= course < 135:
                        speed = calculate_snelheid(120, 135, course, kts)
                    elif 135 <= course < 150:
                        speed = calculate_snelheid(135, 150, course, kts)
                    elif 150 <= course < minimum:
                        s0 = float(diagram["150"][str(kts)])
                        s1 = float(diagram["laagste_course"][str(kts)]["speed"])

                        deltas = s1 - s0
                        marge = deltas/(minimum - 150)
                        deltac = course - 150

                        speed = round(s0 + (marge*deltac), 2)

                    objects[str(course)] = str(speed)
                y[kts] = objects
        for x in range(14):
            objects = {}
            kts = x + 6
            if kts not in (6, 8, 10, 12, 14, 16, 20):
                for course in range(180):
                    if kts == 7:
                        s0 = float(y[6][str(course)])
                        s1 = float(y[8][str(course)])
                        speed = round((s0 + s1) / 2,2)
                        objects[str(course)] = str(speed)

                    elif kts == 9:
                        s0 = float(y[8][str(course)])
                        s1 = float(y[10][str(course)])
                        speed = round((s0 + s1) / 2, 2)
                        objects[str(course)] = str(speed)

                    elif kts == 11:
                        s0 = float(y[10][str(course)])
                        s1 = float(y[12][str(course)])
                        speed = round((s0 + s1) / 2, 2)
                        objects[str(course)] = str(speed)

                    elif kts == 13:
                        s0 = float(y[12][str(course)])
                        s1 = float(y[14][str(course)])
                        speed = round((s0 + s1) / 2, 2)
                        objects[str(course)] = str(speed)

                    elif kts == 15:
                        s0 = float(y[14][str(course)])
                        s1 = float(y[16][str(course)])
                        speed = round((s0 + s1) / 2, 2)
                        objects[str(course)] = str(speed)

                    elif kts == 17:
                        s0 = float(y[16][str(course)])
                        s1 = float(y[20][str(course)])
                        delta = s1-s0
                        speed = round(s0 + (delta/4), 2)
                        objects[str(course)] = str(speed)

                    elif kts == 18:
                        s0 = float(y[16][str(course)])
                        s1 = float(y[20][str(course)])
                        speed = round((s0 + s1) / 2, 2)
                        objects[str(course)] = str(speed)

                    elif kts == 19:
                        s0 = float(y[16][str(course)])
                        s1 = float(y[20][str(course)])
                        delta = s1 - s0
                        speed = round(s0 + ((delta / 4)*3), 2)
                        objects[str(course)] = str(speed)
                y[kts] = objects
        json.dump(y, table, indent=4)
    table.close()


def calculate_snelheid(c1, c2, course, kts):
    """
            deze functie berekent de snelheid van de boot bij graden die niet in het polar diagram staan door gemiddelden
            wel gegeven graden te nemen.

            Parameters:
                c1 (int): course 1, dichtbij zijnde gegeven koers uit het polar diagram, onder de gezochte koers
                c2 (int): course 2, dichtbij zijnde gegeven koers uit het polar diagram, boven de gezochte koers
                course (int): de windsnelheid in knopen, de windsnelheid waar je de bootsnelheid van wilt berekene
                kts (int): de windsnelhijd in knopen
            Returns:
                de snelheid die bij een koers en windsnelhijd hoort. (float) afgerond op 2 decimalen
            """
    with open("PolarDiagram.json", "r") as read_file:
        diagram = json.load(read_file)
    s0 = float(diagram[str(c1)][str(kts)])
    s1 = float(diagram[str(c2)][str(kts)])
    deltas = s1 - s0
    marge = deltas / (c2 - c1)
    deltac = course - c1

    return round(s0 + marge * deltac, 2)


def check_polar_Table():
    """
            deze functie checkt of het polar tabel bestaat, en zo niet creeert de functie dit.

            """
    try:
        with open("PolarTable.json", "r") as table:
            table.close()
    except FileNotFoundError:
        write_polartable()


def safe_file(file):
    with open("PolarDiagram.json", "w") as outfile:
        json.dump(file, outfile, indent=4)
        outfile.close()
