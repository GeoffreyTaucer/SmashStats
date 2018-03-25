import json

meleeStages = ["Yoshi's Story", "Fountain of Dreams", "Final Destination", "Battlefield", "Dream Land",
               "Pokemon Stadium"]
meleeCharacters = ["doc", "mario", "luigi", "bowser", "peach", "yoshi", "dk", "falcon", "ganon", "falco", "fox", "ness",
                   "ic", "kirby", "samus", "zelda", "sheik", "link", "young link", "pichu", "pikachu", "puff", "mewtwo",
                   "game and watch", "marth", "roy"]


"""
matchup data format:
    {
        'Players': [player_one, player_two],
        'Stage' : stage,
        'P 1 char' : player_one_char,
        'P 2 char' : player_two_char,
        'P 1 wins' : player_one_wins,
        'P 2 wins' : player_two_wins
    }
"""


def read_data():
    try:
        with open("data.txt", "r") as json_file:
            data = json.load(json_file)

    except OSError:
        print("No data recorded. Creating data file...")
        data = {'Tracked players': [], 'Recorded matchups': []}
        with open("data.txt", "w") as json_file:
            json.dump(data, json_file)

    return data


def write_data(data):
    try:
        with open("data.txt", "w") as json_file:
            json.dump(data, json_file)

    except OSError:
        print("Unable to write data to file.")


def create_matchup(strict):
    print("Player 1")
    player_one = get_player(strict)
    print("Player 2")
    player_two = get_player(strict)
    if not player_one + player_two:
        print("You must input at least one player")
        return
    player_one, player_two = sorted([player_one, player_two])
    player_one_char = get_char(player_one, strict)
    player_two_char = get_char(player_two, strict)
    stage = get_stage(strict)
    matchup = {
        'Players': [player_one, player_two],
        'Stage': stage,
        'P 1 char': player_one_char,
        'P 2 char': player_two_char,
    }

    return matchup


def record_match():
    ref_match = create_matchup(True)
    this_match = {}
    data = read_data()
    matches = data["Recorded matchups"]
    for i in range(len(matches)):
        if (
                ref_match["Players"][0] in matches[i]["Players"] and
                ref_match["Players"][1] in matches[i]["Players"] and
                ref_match["Stage"] == matches[i]["Stage"] and
                ref_match["P 1 char"] == matches[i]["P 1 char"] and
                ref_match["P 2 char"] == matches[i]["P 2 char"]
        ):
            print("Match found. Pulling matchup from database...")
            this_match = matches.pop(i)

    if not this_match:
        print("Match not found. Creating matchup in database...")
        this_match = ref_match
        this_match["P 1 wins"], this_match["P 2 wins"] = 0, 0

    while True:
        print("Who won?")
        print("1. " + this_match["Players"][0])
        print("2. " + this_match["Players"][1])
        print("3. (cancel)")
        try:
            winner = int(input())
            if winner == 1:
                this_match["P 1 wins"] += 1
                break

            elif winner == 2:
                this_match["P 2 wins"] += 1
                break

            elif winner == 3:
                return

            else:
                print("Invalid input")

        except TypeError:
            print("Invalid input")

    matches.append(this_match)
    data["Recorded matchups"] = matches
    write_data(data)


def check_match():
    this_match = False
    while not this_match:
        this_match = create_matchup(False)
    data = read_data()
    matches = data["Recorded matchups"]
    if this_match["Players"][0]:
        matches = [x for x in matches if this_match["Players"][0] in x["Players"]]
    if this_match["Players"][1]:
        matches = [x for x in matches if this_match["Players"][1] in x["Players"]]
    if this_match["P 1 char"]:
        matches = [x for x in matches if this_match["P 1 char"] == x["P 1 char"]]
    if this_match["P 2 char"]:
        matches = [x for x in matches if this_match["P 2 char"] == x["P 2 char"]]
    if this_match["Stage"]:
        matches = [x for x in matches if this_match["Stage"] == x["Stage"]]

    if not matches:
        print("No record of this matchup in database")
        return

    total_games = 0
    for matchup in matches:
        total_games += matchup["P 1 wins"] + matchup["P 2 wins"]

    if this_match["Players"]:

        player_one_wins = 0
        player_two_wins = 0

        for matchup in matches:
            if this_match["Players"][0] == matchup["Players"][0]:
                player_one_wins += matchup["P 1 wins"]

            elif this_match["Players"][0] == matchup["Players"][1]:
                player_one_wins += matchup["P 2 wins"]

            if this_match["Players"][1] == matchup["Players"][0]:
                player_two_wins += matchup["P 1 wins"]

            elif this_match["Players"][1] == matchup["Players"][1]:
                player_two_wins += matchup["P 2 wins"]

        if this_match["Players"][0] and not this_match["P 1 char"]:
            print(this_match["Players"][0] + "'s win rate is " + str(player_one_wins/total_games))

        elif this_match["Players"][0] and this_match["P 1 char"]:
            print(this_match["Players]"][0] + "'s win rate with " + this_match["P 1 char"] + " is " +
                  str(player_one_wins/total_games))

        if this_match["Players"][1] and not this_match["P 2 char"]:
            print(this_match["Players"][1] + "'s win rate is " + str(player_two_wins/total_games))

        elif this_match["Players"][1] and this_match["P 2 char"]:
            print(this_match["Players]"][1] + "'s win rate with " + this_match["P 2 char"] + " is " +
                  str(player_two_wins / total_games))

    """Need to figure out why this block isn't working, but for now its disabled
    elif this_match["P 1 char"] or this_match["P 2 char"]:
        char_one_wins = 0
        char_two_wins = 0
        for matchup in matches:
            if this_match["P 1 char"] == matchup["P 1 char"]:
                char_one_wins += matchup["P 1 wins"]

            elif this_match["P 1 char"] == matchup["P 2 char"]:
                char_one_wins += matchup["P 2 wins"]

            if this_match["P 2 char"] == matchup["P 1 char"]:
                char_two_wins += matchup["P 1 wins"]

            elif this_match["P 2 char"] == matchup["P 2 char"]:
                char_two_wins += matchup["P 2 wins"]

        if this_match["P 1 char"]:
            print(this_match["P 1 char"] + "'s win rate is " + str(char_one_wins/total_games))

        if this_match["P 2 char"]:
            print(this_match["P 2 char"] + "'s win rate is " + str(char_two_wins/total_games))"""


def get_player(strict):
    player = ""
    data = read_data()
    while player not in data["Tracked players"]:
        print("Input player tag")
        if not strict:
            print("You may leave this blank")

        player = input()

        if player in data["Tracked players"] or (not player and not strict):
            break

        elif strict and not player:
            print("Player tag cannot be blank")
            continue

        elif strict and player not in data["Tracked players"]:
            new_player = input("Player not recognized. Add new player? ")
            if new_player.lower() in ["y", "yes"]:
                data["Tracked players"].append(player)
                break

            else:
                continue

    write_data(data)
    return player


def get_char(player, strict):
    character = ""
    while character not in meleeCharacters:
        print("Input character selection for %s" % player)
        if not strict:
            print("You may leave this blank")

        character = char_translate(input())

        if character in meleeCharacters or (not character and not strict):
            break

        else:
            print("Invalid character choice")
            continue

    return character


def get_stage(strict):
    stage = ""
    while stage not in meleeStages:
        for i in range(len(meleeStages)):
            print(str(i + 1) + ". " + meleeStages[i])
        if not strict:
            print("You may leave this blank")

        stage = input()

        if not stage and not strict:
            break

        try:
            stage = meleeStages[int(stage) - 1]

        except TypeError:
            print("Invalid input")
            continue

        if stage in meleeStages:
            break

        else:
            print("Invalid selection")

    return stage


def char_translate(char):
    if char.lower() in ["dr. mario", "doctor mario"]:
        return "doc"
    elif char.lower() in ["captain falcon", "c. falcon", "c falcon"]:
        return "falcon"
    elif char.lower() == "ganondorf":
        return "ganon"
    elif char.lower() in ["game & watch", "g & w", "g&w"]:
        return "game and watch"
    elif char.lower() == "shiek":
        return "sheik"
    elif char.lower() in ["jigglypuff", "jiggly puff"]:
        return "puff"
    elif char.lower() in ["ice climbers", "ics", "iceclimbers"]:
        return "ic"
    elif char.lower() == "yl":
        return "young link"
    elif char.lower() == "donkey kong":
        return "dk"
    elif char.lower() == "marf":
        return "marth"
    else:
        return char.lower()


def select_task():
    selection = ""
    while selection not in [1, 2, 3]:
        print("Select option:")
        print("1. Report match")
        print("2. Check matchup stats")
        print("3. Exit program")
        try:
            selection = int(input())

        except TypeError:
            print("Invalid selection")
            continue

        if selection not in [1, 2, 3]:
            print("Invalid selection")

    return selection


def main():
    print("Welcome to Smash Stats Version 3.2")
    print("By Geoffrey Taucer")
    while True:
        task_selection = select_task()
        if task_selection == 1:
            record_match()

        elif task_selection == 2:
            check_match()

        elif task_selection == 3:
            print("Thank you for using Smash Stats V3.2")
            break

        else:
            print("Error: select_task() returned an incorrect value")
            break


if __name__ == "__main__":
    main()
