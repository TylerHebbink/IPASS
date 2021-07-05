import calculations as cal
import polar_diagram as pd
import time as t


def test1(list_co,counter):
    """
       deze functie geeft elke keer een andere boot locatie mee om te laten zien dat het programma steeds een nieuwe
       koers berekent gebaseerd op de huidige boot locatie.

       Parameters:
           list_co (list): een lijst met coordinaten
           counter (int): een counter

       Returns:
           boot_co (list): boot coordinate, de test coordinaten van de boot
       """
    try:
        boot_co = list_co[counter]
        return boot_co
    except IndexError:
        print("end test")


def run_main(kts,TWA,list_co, coordinate_wp):
    """
        de funtie main is een loop die zich elke 10 seconden herhaald en alles bij elkaar brengt.

        Parameters:
            kts (int): de windkracht, in knopen
            TWA (int): de windrichting
            list_co (list): een lijst met coordinaten
            coordinate_wp (int): de coordinaten van het waypoint

        Returns:
            boot_co (list): boot coordinate, de test coordinaten van de boot
        """
    counter = 0
    main = 1
    while main == 1:
        pd.check_polar_Table()
        coordinate_boat = test1(list_co, counter)
        WPA = cal.direct_course(coordinate_boat,coordinate_wp)
        print(cal.optimal_vmc(WPA, TWA, kts))
        t.sleep(10)
        counter = counter + 1




def test_loop(windspeed,wind_richting,coordinate_boats,coordinate_wp):
    run_main(windspeed,wind_richting,coordinate_boats,coordinate_wp)

