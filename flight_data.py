#!/usr/bin/env python

"""
Generador de datos para proyecto de Bases de Datos No Relacionales
ITESO 
"""
import argparse
import csv
import datetime

from random import choice, randint, randrange, sample

usernames = ['Juan Hernandez', 'Cristina Flores', 'Ricardo Castro', 'Gabriela Ramos', 'Fernando Guzman', 'Andrea Mendez', 'Miguel Jimenez', 'Sara Vazquez', 'Alejandro Reyes', 'Ana Martinez', 'Manuel Chavez', 'Sofia Cortes', 'Carlos Moreno', 'Paulina Acosta', 'Jorge Solis', 'Natalia Villanueva', 'Raul Mendoza', 'Lucia Fernandez', 'Emilio Gutierrez', 'Estefania Garcia', 'Pablo Contreras', 'Valeria Leon', 'Roberto Pena', 'Mariana Ortiz', 'Pedro Suarez', 'Carla Aguilar', 'Mario Fuentes', 'Karen Valdez', 'Luisa Rios', 'Javier Vega', 'Isabella Rosas', 'Ramon Rubio', 'Maria Delgado', 'Rodrigo Camacho', 'Elena Zuniga', 'Adrian Soto', 'Julia Perez', 'Juan Carlos Ortega', 'Aurora Morales', 'David Duran', 'Valentina Espinoza', 'Federico Hernandez', 'Luciana Mercado', 'Ricardo Escobar', 'Nadia Nunez', 'Joaquin Fernandez', 'Ana Karen Garcia', 'Oscar Cruz', 'Carmen Reyes', 'Maximiliano Aguilar', 'Gabriela Medina', 'Emiliano Torres', 'Cecilia Pineda', 'Eduardo Marin', 'Angela Hernandez', 'Alfredo Gallegos', 'Gloria Torres', 'Joaquin Alvarez', 'Valeria Chavez', 'Carlos Fuentes', 'Maria Contreras', 'Juan Pablo Maldonado', 'Montserrat Ibarra', 'Javier Jimenez', 'Ximena Valencia', 'Hector Flores', 'Fernanda Pacheco', 'Roberto Roman', 'Elena Vargas', 'Jorge Flores', 'Daniela Guzman', 'Rafael Vega', 'Alicia Ponce', 'Miguel Angel Aguilar', 'Lorena Hernandez', 'Mauricio Avila', 'Alejandra Roman', 'Rodrigo Perez', 'Mariana Aguilar', 'Juan Jose Rios', 'Bianca Vazquez', 'Adrian Torres', 'Paola Velazquez', 'Eduardo Marquez', 'Fernanda Barrera', 'Arturo Sosa', 'Mariana Gallegos', 'Carlos Fernandez', 'Evelyn Alvarez', 'Daniel Castillo', 'Sofia Diaz', 'Gustavo Ibarra', 'Ana Sofia Montes', 'Luisa Perez', 'Jose Luis Rosales', 'Laura Torres', 'Luis Hernandez', 'Marcela Zavala', 'Javier Mendoza', 'Camila Ortiz', 'Fernando Reyes', 'Mariana Sandoval', 'Alberto Montes', 'Margarita Acosta', 'Juan Carlos Juarez', 'Paula Ponce', 'Mauricio Ortiz', 'Alicia Hernandez', 'Pedro Rodriguez', 'Daniela Navarro', 'Jorge Acosta', 'Regina Aguilar', 'Ismael Mendoza', 'Samantha Rios', 'Cesar Castro', 'Rebeca Morales', 'Miguel Vazquez', 'Ana Karen Morales', 'Cristian Valenzuela', 'Patricia Reyes', 'Hector Garcia', 'Jessica Velasco', 'Jose Antonio Marin', 'Karla Diaz',]
airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris"]
airports = ["PDX", "GDL", "SJC", "LAX", "JFK"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date


def generate_dataset(output_file, rows):
    with open(output_file, "w") as fd:
        fieldnames = ["id","airline","username", "from" ,"to", "day", "month", "year","age", "gender", "reason", "stay", "transit"]
        fp_dict = csv.DictWriter(fd, fieldnames=fieldnames)
        fp_dict.writeheader()
        for i in range(rows):
            from_airport = choice(airports)
            to_airport = choice(airports)
            while from_airport == to_airport:
                to_airport = choice(airports)
            date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
            reason = choice(reasons)
            stay = choice(stays)
            transit = choice(transits)
            if reason == "Back Home":
                stay = "Home"
            limite_inferior = 1
            limite_superior = 200


            numeros = list(range(limite_inferior, limite_superior + 1))


            line = {
                "id":sample(numeros, 1)[0],
                "airline": choice(airlines),
                "username": sample(usernames, 1)[0],
                "from":  from_airport,
                "to":  to_airport,
                "day": date.day,
                "month": date.month,
                "year": date.year,
                "age": randint(1,90),
                "gender": choice(genders),
                "reason": reason,
                "stay": stay,
                "transit": transit,
            }
            fp_dict.writerow(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output",
            help="Specify the output filename of your csv, defaults to: flight_passengers.csv", default="flight_passengers.csv")
    parser.add_argument("-r", "--rows",
            help="Amount of random generated entries for the dataset, defaults to: 100", type=int, default=100)

    args = parser.parse_args()
    
    print(f"Generating {args.rows} for flight passenger dataset")
    generate_dataset(args.output, args.rows)
    print(f"Completed generating dataset in {args.output}")


