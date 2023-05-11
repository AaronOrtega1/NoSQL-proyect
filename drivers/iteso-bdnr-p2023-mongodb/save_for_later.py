"""     parser = argparse.ArgumentParser()

    list_of_actions = ["search", "get", "update", "delete"]
    parser.add_argument("action", choices=list_of_actions,
                        help="Action to be user for the flights library")
    parser.add_argument("-f", "--frequency",
                        nargs='?', const=None, help="Provide a flight ID which related to the flight action")
    parser.add_argument("-t", "--to",
                        help="Search parameter to look for flights with certain destination", default=None)
    parser.add_argument("-s", "--skip",
                        help="Search parameter to skip results oveer the operation", default=None)

    args = parser.parse_args()

    if args.id and not args.action in ["get", "update", "delete"]:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)

    if args.to and args.action != "search":
        log.error(f"to arg can only be used with search action")
        exit(1)

    if args.day and args.action != "search":
        log.error(f"day arg can only be used with search action")

    if args.month and args.action != "search":
        log.error(f"month arg can only be used with search action")

    if args.year and args.action != "search":
        log.error(f"year arg can only be used with search action")

    if args.skip and args.action != "search":
        log.error(f"Skip arg can only be used with search action")

    if args.limit and args.action != "search":
        log.error(f"Limit arg can only be used with search action")
        
    if args.action == "search" and args.frequency is not None:
            get_month_count()



    if args.action == "search":
        get_month_count(args.rating)
    elif args.action == "get" and args.id:
        get_flight_by_id(args.id)
    elif args.action == "update":
        update_flight(args.id)
    elif args.action == "delete":
        delete_flight(args.id) """
        

""" def print_flight(flight):
    print(f"Matched flights: {len(flight.keys())}")
    for k in flight.keys():
        print(f"{k}: {flight[k]}")
    print("="*50) """
    
    
"""     
def list_flights(to, day, month, year):
    suffix = "/flight"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "to": to,
        "day": day,
        "month": month,
        "year": year
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        print(f"Resultados: {len(json_resp)}")
    else:
        print(f"Error: {response}") """
        
""" def get_flight_by_id(id):
    suffix = f"/flight/{id}"
    endpoint = FLIGHTS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_flight(json_resp)
    else:
        print(f"Error: {response}") """
        
""" def update_flight(id):
    suffix = f"/flight/{id}"
    endpoint = FLIGHTS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_flight(json_resp)
        print("Provide the new flight data:")
        data = {}
        for key in json_resp:
            updated_values = input(f"{key} ({json_resp[key]}):")
            if updated_values:
                data[key] = updated_values
            else:
                data[key] = json_resp[key]
        response = requests.put(endpoint, json=data)
        if response.ok:
            print("Flight has been updated")
        else:
            print("Flight was not updated")
            print(response.json)
    else:
        print(f"Error: {response}")


def delete_flight(id):
    suffix = f"/flight/{id}"
    endpoint = FLIGHTS_API_URL + suffix
    response = requests.delete(endpoint)
    if response.ok:
        json_resp = response.json()
        print_flight(json_resp)
    else:
        print(f"Error: {response}")
 """