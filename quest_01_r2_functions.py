def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game(game_state, object_relations):
    print("Suddenly, you find yourself waking up on an unfamiliar couch, in an eerie house devoid of windows. Your memory fails to provide any explanation about how you ended up here, or what transpired previously. You can sense an imminent threat lurking somewhere - your gut tells you to escape the house immediately!")
    play_room(game_state["current_room"], game_state, object_relations)

def play_room(room, game_state, object_relations):
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"] + ".")
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        if intended_action == "explore":
            explore_room(room, game_state, object_relations)
            play_room(room, game_state, object_relations)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip(), game_state, object_relations)
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room, game_state, object_relations)
        linebreak()

def explore_room(room, game_state, object_relations):
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You decide to explore the room,. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room, object_relations):
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name, game_state, object_relations):
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room, object_relations)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    if(next_room and input("Will you step into the unknown through " + item_name + "?").strip() == 'yes'):
        play_room(next_room, game_state, object_relations)
    else:
        play_room(current_room, game_state, object_relations)