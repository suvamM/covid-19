# Covid-19 Regulations Checker

from z3 import *

# Define variables for entities

# ==== Aggregate variables
essential_services = Bool("essential_services")

# ==== Law Enforcement
defense = Bool("defense")
crpf = Bool("crpf")
police = Bool("police")
home_guards = Bool("home_guards")
prison_guards = Bool("prison_guards")

# ==== Services
fire_service = Bool("fire_service")
electricity_service = Bool("electricity_service")
hospital_service = Bool("hospital_service")
sanitation_service = Bool("sanitation_service")
water_service = Bool("water_service")
newspaper_service = Bool("newspaper_service")

# ==== Transportation
local_bus_public = Bool("local_bus_public")
local_bus_private = Bool("local_bus_private")
local_train = Bool("local_train")
express_train = Bool("express_train")
freight_train = Bool("freight_train")
truck = Bool("truck")
private_car = Bool("private_car")
private_taxi = Bool("private_taxi")
ola_taxi = Bool("ola_taxi")
uber_taxi = Bool("uber_taxi")
auto_rickshaw = Bool("auto_rickshaw")
domestic_flight = Bool("domestic_flight")
international_flight = Bool("international_flight")

# ==== Shops
grocery = Bool("grocery")
pharmacy = Bool("pharmacy")
restaurants = Bool("restaurants")
apparel = Bool("apparel")
milk_booth = Bool("milk_booth")

# ==== Financial Services
banks = Bool("banks")
atms = Bool("atms")

# ==== E-commerce platforms
amazon = Bool("amazon")
amazon_fresh = Bool("amazon_fresh")
bigbasket = Bool("bigbasket")
medlife_express = Bool("medlife_express")
grofers = Bool("grofers")

# ==== Petrol Pumps
petrol_pumps = Bool("petrol_pumps")

# ==== Educational institutes
schools = Bool("schools")
colleges = Bool("colleges")
universities = Bool("universities")

# ==== Religious institutes
temples = Bool("temples")
mosques = Bool("mosques")
churches = Bool("churches")

# Define what are essential services
def encode_essential_services () :
    constraints = []
    constraints.append(Implies(essential_services, fire_service))
    constraints.append(Implies(essential_services, electricity_service))
    constraints.append(Implies(essential_services, hospital_service))
    constraints.append(Implies(essential_services, sanitation_service))
    constraints.append(Implies(essential_services, water_service))
    constraints.append(Implies(essential_services, grocery))
    constraints.append(Implies(essential_services, pharmacy))

    return constraints


# Encode MHA Lockdown Guidelines
# constraints based on https://mha.gov.in/sites/default/files/PR_ConsolidatedGuidelinesofMHA_28032020.pdf
def encode_MHALockdownGuidelines () :
    constraints = []
    
    constraints.append(essential_services == True)

    # point 1
    constraints.append(defense == True)
    constraints.append(crpf == True)

    # point 2
    constraints.append(electricity_service == True)
    constraints.append(water_service == True)
    constraints.append(sanitation_service == True)

    # point 3
    constraints.append(hospital_service == True)
    constraints.append(pharmacy == True)

    # point 4
    constraints.append(restaurants == False)
    constraints.append(apparel == False)
    constraints.append(grocery == True)
    constraints.append(milk_booth == True)
    constraints.append(banks == True)
    constraints.append(atms == True)
    constraints.append(amazon == False)
    constraints.append(amazon_fresh == True)
    constraints.append(bigbasket == True)
    constraints.append(medlife_express == True)
    constraints.append(grofers == True)
    constraints.append(petrol_pumps == True)

    # point 6
    constraints.append(local_bus_public == False)
    constraints.append(local_bus_private == False)
    constraints.append(express_train == False)
    constraints.append(private_car == False)
    constraints.append(private_taxi == False)
    constraints.append(ola_taxi == False)
    constraints.append(uber_taxi == False)
    constraints.append(auto_rickshaw == False)
    constraints.append(domestic_flight == False)
    constraints.append(international_flight == False)
    constraints.append(freight_train == True)
    constraints.append(truck == True)

    # point 8
    constraints.append(schools == False)
    constraints.append(colleges == False)
    constraints.append(universities == False)

    # point 9
    constraints.append(temples == False)
    constraints.append(mosques == False)
    constraints.append(churches == False)

    return constraints

# Encode WB Government guidelines
# contraints based on: https://static.mygov.in/rest/s3fs-public/mygov_158511551351307401.pdf
def encode_WBGovtOrder ():
    constraints = []

    constraints.append(essential_services == True)

    # point 1
    constraints.append(local_bus_public == False)
    constraints.append(local_bus_private == False)
    constraints.append(private_taxi == False)
    constraints.append(ola_taxi == False)
    constraints.append(uber_taxi == False)
    constraints.append(auto_rickshaw == False)

    # point 2
    constraints.append(restaurants == False)
    constraints.append(apparel == False)

    # point 5
    constraints.append(hospital_service == True)
    constraints.append(police == True)
    constraints.append(crpf == True)
    constraints.append(defense == True)
    constraints.append(electricity_service == True)
    constraints.append(fire_service == True)
    constraints.append(banks == True)
    constraints.append(atms == True)
    constraints.append(grocery == True)
    constraints.append(milk_booth == True)
    constraints.append(petrol_pumps == True)
    constraints.append(pharmacy == True)
    constraints.append(newspaper_service == True)

    return constraints

# Encode Andaman and Nicobar Guidelines
# constraints based on: "https://static.mygov.in/rest/s3fs-public/mygov_158513429651307401.pdf
def encode_SouthAndamanGovtOrder() :
    constraints = []

    # point 1
    constraints.append(restaurants == False)
    constraints.append(apparel == False)
    constraints.append(pharmacy == True)
    constraints.append(grocery == True)
    constraints.append(milk_booth == True)
    constraints.append(petrol_pumps == True)

    # point 3
    constraints.append(temples == False)
    constraints.append(mosques == False)
    constraints.append(churches == False)

    # point 5
    constraints.append(banks == True)
    constraints.append(atms == True)

    return constraints

def encode_KarnatakaGovtOrder() :
    # constraints based on: https://static.mygov.in/rest/s3fs-public/mygov_158505684451307401.pdf
    constraints = []
    
    # point 3
    constraints.append(restaurants == False)
    constraints.append(apparel == False)
    constraints.append(local_bus_public == False)
    constraints.append(local_bus_private == False)
    constraints.append(private_taxi == False)
    constraints.append(ola_taxi == False)
    constraints.append(uber_taxi == False)
    constraints.append(auto_rickshaw == False)

    # point 4
    constraints.append(grocery == True)
    constraints.append(milk_booth == True)
    constraints.append(pharmacy == True)
    constraints.append(truck == True)
    constraints.append(freight_train == True)
    constraints.append(police == True)
    constraints.append(fire_service == True)
    constraints.append(electricity_service == True)
    constraints.append(water_service == True)
    constraints.append(sanitation_service == True)
    constraints.append(banks == True)
    constraints.append(atms == True)
    constraints.append(amazon_fresh == True)
    constraints.append(bigbasket == True)
    constraints.append(medlife_express == True)

    return constraints

def add_constraints_and_solve () :
    mha_contraints = encode_MHALockdownGuidelines()
    wbgovt_constraints = encode_WBGovtOrder()
    andaman_constraints = encode_SouthAndamanGovtOrder()
    karnataka_constraints = encode_KarnatakaGovtOrder()
    solver = Solver()
    solver.add(mha_contraints)
    solver.add(wbgovt_constraints)
    return (solver.check(), solver.model())

if __name__ == '__main__':
    print(". COVID-19 Regulations Checker")
    (is_sat, model) = add_constraints_and_solve()
    
    if (is_sat == sat):
        solution = {}
        for d in model.decls():
            solution[d.name()] = model[d]

        print(".. All regulations are consistent.")

        option = input(".. Search status of service [list to enumerate, exit to quit]: ")
        while (str(option) != "exit"):
            if (str(option) == "list"):
                print("\n=============== Available Services to query ===============")
                for k in solution:
                    print("%s, " % k, end="")
                print("\n==============================", end="\n")
            elif option in solution:
                print("... Status of %s = %s" % (option, solution[option]))
            else:
                print("... You are querying an unsupported service. Please retry.")
            option = input(".. Search another? [list to enumerate, exit to quit]: ")
        print(". Thanks for using the COVID-19 Regulations Checker!")
    else:
        print(".. Rule inconsistencies detected!")



