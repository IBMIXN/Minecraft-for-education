import time, pickle, os
from datetime import datetime
import signal
import random, math, time
import mcpi.block as block
import mcpi.minecraft as minecraft


catastrophising = ["will", "fail", "will go wrong", "will end", "will be impossible", "will not happen", "will be terrible", "will be horrible", "will be a catastrophe", "will be a disaster", "will never", "nvr end", "will not end", "lose", "loser", "tbh u fail", "not ez", "u never", "u nvr", "nvr IRL"]

dichotomous_reasoning = ["only", "every", "everyone", "everybody", "everything", "everywhere", "always", "perfect", "the best", "all", "not a single", "no one", "nobody", "nothing", "nowhere", "never", "worthless", "the worst", "neither", "nor", "either or", "black or white", "ever", "no1", "blk", "wyt"]

disqualifying_the_positive = ["great", "but", "good but", "OK but", "not that great", "not that good", "it was not", "not all that", "fine but", "acceptable but", "great yet", "good yet", "OK yet", "fine yet", "acceptable yet", "idiot", "stupid", "dum", "annoying", "idot", "u nvr", "not IRL", "nvm", "noob", "smh", "jk"]

emotional_reasoning = ["but I feel", "since I feel", "because I feel", "but it feels", "since it feels", "because it feels", "still feels", "idc", ":)", ":("]

fortune_telling = ["I will not", "we will not", "you will not", "they will not", "it will not", "that will not", "he will not", "she will not", "ill", "u wont", "u always", "IRL", "you probs", "probs"]

labeling_and_mislabeling = ["I am a", "he is a", "she is a", "they are a", "it is a", "that is a", "sucks at", "suck at", "I never", "he never", "she never", "you never", "we never", "they never", "I am an", "he is an", "she is an", "they are an", "it is an", "that is an", "a burden", "a complete", "a completely", "a huge", "a loser", "a major", "a total", "a totally", "a weak", "an absolute", "an utter", "a bad", "a broken", "a damaged", "a helpless", "a hopeless", "an incompetent", "a toxic", "an ugly", "an undesirable", "an unlovable", "a worthless", "a horrible", "a terrible", "unvr", "u suck", "u never", "they r", "all", "ur trash", "ur crappy", "ur iot", "u useless", "u idot", "u fool", "u noob", "smh", "i smh"]

magnification_and_minimisation = ["worst", "best", "not important", "not count", "not matter", "no matter", "the only thing", "the one thing", "wrst", "not gr8", "always gr8"]

mental_filtering = ["I see only", "all I see", "all I can see", "can only think", "nothing good", "nothing right", "completely bad", "completely wrong", "only the bad", "only the worst", "if I just", "if I only", "if it just", "if it only", "I c"]

mindreading = ["everyone believes", "everyone knows", "everyone thinks", "everyone will believe", "everyone will know", "everyone will think", "nobody believes", "nobody knows", "nobody thinks", "nobody will believe", "nobody will know", "nobody will think", "he believes", "he knows", "he thinks", "he does not believe", "he does not know", "he does not think", "he will believe", "he will know", "he will think", "he will not believe", "he will not know", "he will not think", "she believes", "she knows", "she thinks", "she does not believe", "she does not know", "she does not think", "she will believe", "she will know", "she will think", "she will not believe", "she will not know", "she will not think", "they believe", "they know", "they think", "they do not believe", "they do not know", "they do not think", "they will believe", "they will know", "they will think", "they will not believe", "they will not know", "they will not think", "we believe", "we know", "we think", "we do not believe", "we do not know", "we do not think", "we will believe", "we will know", "we will think", "we will not believe", "we will not know", "we will not think", "you believe", "you know", "you think", "you do not believe", "you do not know", "you do not think", "you will believe", "you will know", "you will think", "you will not believe", "you will not know", "you will not think", "u believe", "u know", "u think", "u do not believe", "u do not know", "u do not think", "u will believe", "u will know", "u will think", "u will not believe", "u will not know", "u will not think", "irl nvr"]

overgeneralising = ["all of the time", "all of them", "all the time", "always happens", "always like", "happens every time", "completely", "no one ever", "nobody ever", "every single one of them", "every single one of you", "I always", "you always", "he always", "she always", "they always", "I am always", "you are always", "he is always", "she is always", "they are always", "u always", "irl nvr", "irl always", "always gr8", "udc"]

personalising = ["all me", "all my", "because I", "because my", "because of my", "because of me", "I am responsible", "blame me", "I caused", "I feel responsible", "all my doing", "all my fault", "my bad", "my responsibility", "becuz I", "cuz", "cuz I", "cuz my", "idc"]

should_statements = ["should", "ought", "must", "have to", "has to", "hav2"]


key_word = {
    "catastrophising": catastrophising,
    "dichotomous_reasoning": dichotomous_reasoning,
    "disqualifying_the_positive": disqualifying_the_positive,
    "emotional_reasoning": emotional_reasoning,
    "fortune_telling": fortune_telling,
    "labeling_and_mislabeling": labeling_and_mislabeling,
    "magnification_and_minimisation": magnification_and_minimisation,
    "mental_filtering": mental_filtering,
    "mindreading": mindreading,
    "overgeneralising": overgeneralising,
    "personalising": personalising,
    "should_statements": should_statements
}

# Purpose: Reading the log files.
# Input: None
# Output: Gives messages from log files.
def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


# Purpose: First function of the code that gets called. Only selects messages that were written by users in the logile.
# Input: user_name, user_text
# Output: none (calls start_interaction function)
def start():
    done = False
    while True:
        logfile = open("latest.log", "r")
        loglines = follow(logfile)
        for line in loglines:
            if "Chat Thread" in line:
                user_text = line.split('> ')[1]
                user_text = user_text.split('[m')[0]
                user_name = line.split('<')[1].split('>')[0]
                for (key, values) in key_word.items():
                    for value in values:
                        if value in user_text and not done:
                            done = True
                            start_interaction(user_name, user_text)

# Purpose: We start the first interaction with users.
# Input: user_name, user_text, response
# Output: none (calls start function or treasure function)
def start_interaction(user_name, user_text):
    # user_text = user_text.split('[m')[0]
    mc.postToChat(f"You appear to be struggling with thoughts associated to '{user_text}'")
    mc.postToChat("Is this true? yes/no")
    response = user_input(user_name)
    counter = 0
    while "yes" not in response and "no" not in response and counter < 4:
        mc.postToChat("Answer yes/no")
        counter += 1
        response = user_input(user_name)
    if "yes" in response:
        pickle_yes_dict(user_name, user_text)
        treasure(user_name)
    elif "no" in response:
        mc.postToChat("Have a great day")
        pickle_no_dict(user_name, user_text)
        start()
    else:
        mc.postToChat("Have a great day and we will await your messages again.")
        start()

# Purpose: Handle the waiting time of the server.
# Input: none
# Output: none (calls start function)
def handle(s, f):
    mc.postToChat("Have a great day and we will await your messages again.")
    start()

# Purpose: This function gets user input from users.
# Input: user_name, user_text
# Output: none (calls start function or treasure function)
def user_input(user_name):
    signal.signal(signal.SIGALRM, handle)
    # Change signal time to how long we want before server
    # restarts listening to what users say
    signal.setitimer(signal.ITIMER_REAL, 30)
    while True:
        logfile = open("latest.log", "r")
        loglines = follow(logfile)
        for line in loglines:
            if "Chat Thread" in line:
                user_text = line.split('> ')[1].split('<')[0]
                user = line.split('<')[1].split('>')[0]
                if user == user_name:
                    signal.alarm(0)
                    return user_text.strip().lower()

# Purpose: Asking users whether they want to play a game which can lead to a treasure hunt.
# Input: response
# Output: none (calls start function or word_describe function)
def treasure(user_name):
    mc.postToChat("You can get a treasure hunt by playing a game, are you interested? yes/no")
    response = user_input(user_name)
    counter = 0
    while "yes" not in response and "no" not in response and counter < 4:
        mc.postToChat("Answer yes/no")
        counter += 1
        response = user_input(user_name)
    if "yes" in response:
        word_describe(user_name)
    elif "no" in response:
        mc.postToChat("Have a great day")
        start()
    else:
        mc.postToChat("Have a great day and we will await your messages again.")
        start()


# Purpose: Function that gets the word that users are most uncomfortable with.
# Input: new_response, user_input
# Output: none (calls accept_game function)
def word_describe(user_name):
    mc.postToChat("What 1 word best describes the thoughts you are uncomfortable with?")
    new_response = user_input(user_name)
    pickle_uncomf_dict(user_name, new_response)
    mc.postToChat("Ok, great")
    accept_game(user_name, new_response)

# Purpose: Users can decide to start the game.
# Input: response
# Output: none (calls start function or in_game function)
def accept_game(user_name, new_response):
    new_response = new_response.split('[m')[0]
    mc.postToChat(f"if you accept {new_response} by typing it 20 times. Then show you do not need to hold on to thoughts associated to {new_response} by typing ‘Drop the rope’")
    mc.postToChat("you will get additional in game features.")
    response = user_input(user_name)
    if "drop the rope" in response:
        in_game(user_name, new_response)
    else:
        mc.postToChat("Have a great day and do not forget to talk about your thoughts with people around you.")
        start()

# Purpose: Users are playing the game.
# Input: none
# Output: none (calls after_game function)
def in_game(user_name, new_response):
    mc.postToChat(f"Start typing {new_response} for 45 seconds: ")
    time.sleep(45)
    mc.postToChat("Well done")
    after_game(user_name, new_response)

# Purpose: We are after the game, users can continue to answer questions in order to get to the reward (treasure hunt).
# Input: response, user_name, user_input
# Output: none (calls start function or pre_reward function)
def after_game(user_name, new_response):
    mc.postToChat(f"Now imagine the word {new_response} is pulling you on a rope towards uncomfortable thoughts. You have control of the rope if you type 'Drop the rope'")
    mc.postToChat("Do you want to type 'drop the rope', yes/no?")
    response = user_input(user_name)
    counter = 0
    while "yes" not in response and "no" not in response and counter < 4:
        mc.postToChat("Answer yes/no")
        counter += 1
        response = user_input(user_name)
    if "yes" in response:
        pre_reward(user_name, response)
    elif "no" in response:
        mc.postToChat("Have a great day and do not forget to talk about your thoughts with people around you.")
        start()
    else:
        mc.postToChat("Have a great day and we will await your messages again.")
        start()

# Purpose: users are just before the reward and can type the last thing before getting acces to the reward.
# Input: response, user_input, user_name
# Output: none (calls start function or reward function)
def pre_reward(user_name, response):
    mc.postToChat("Type: 'Drop The Rope'")
    response = user_input(user_name)
    if "drop the rope" in response:
        mc.postToChat("Well done")
        mc.postToChat("Do not forget to speak about your thoughts with people around you.")
        mc.postToChat("Have a great day!")
        mc.postToChat("Start your treasure hunt")
        reward()
    else:
        mc.postToChat("Have a great day and do not forget to talk about your thoughts with people around you.")
        start()


# The reward function was taken from online and can be found at:
# https://www.raspberry-pi-geek.com/Archive/2014/03/Learning-to-program-with-Minecraft/(offset)/2

# Purpose: Users got access to the reward i.e. the treasure hunt
# Input: none
# Output: none
def reward():
    v_height=0
    while v_height <= 0:
        (tx, tz)=(random.randint(-100,100), random.randint(-100,100))
        v_height=mc.getHeight(tx, tz)
    mc.setBlock(tx, v_height-2, tz, block.DIAMOND_BLOCK)
    vdistance = math.sqrt(math.pow(mc.player.getTilePos().x-tx, 2) + math.pow(mc.player.getTilePos().z-tz, 2))
    while mc.getBlock(tx, v_height-2, tz)!=0:
        vnewdistance=math.sqrt(math.pow(mc.player.getTilePos().x-tx,2)+ math.pow(mc.player.getTilePos().z-tz, 2))
        if vnewdistance == 0: mc.postToChat("Dig!")
        elif vdistance > vnewdistance: mc.postToChat("Warmer!")
        elif vdistance < vnewdistance: mc.postToChat("Colder!")
        else: mc.postToChat("Move!")
        vdistance=vnewdistance
        time.sleep(2)
    mc.postToChat("Treasure found... And destroyed!")
    mc.postToChat("Congratulations!")
    start()


# Purpose: The next four functions pickle answers (i.e. store answers).
# Input: user_name, user_text, new_response
# Output: none
def pickle_yes_dict(user_name, user_text):
    if user_name not in yes_dict.keys():
        yes_dict[user_name] = [user_text]
    else:
        yes_dict[user_name].append(user_text)
    save_data()

def pickle_uncomf_dict(user_name, new_response):
    if user_name not in uncomf_word.keys():
        uncomf_word[user_name] = [new_response]
    else:
        uncomf_word[user_name].append(new_response)
    save_data()

def pickle_no_dict(user_name, user_text):
    if user_name not in no_dict.keys():
        no_dict[user_name] = [user_text]
    else:
        no_dict[user_name].append(user_text)
    save_data()

def save_data():
    pickling_on = open("all_dicts.pickle", "wb")
    pickle.dump(all_dicts, pickling_on)


# Purpose: starts the file with either the try or except function and initialises all the dictionaries or checks whether they exist.
# Input: none
# Output: none (calls start function)
if __name__ == "__main__":
    try:
        pickle_off = open("all_dicts.pickle", "rb")
        all_dicts = pickle.load(pickle_off)
        yes_dict = all_dicts["yes_dict"]
        no_dict = all_dicts["no_dict"]
        uncomf_word = all_dicts["uncomf_word"]
        print("Try (start)")
        mc = minecraft.Minecraft.create()
        start()
    except:
        yes_dict = {}
        no_dict = {}
        uncomf_word = {}
        all_dicts = {
        "yes_dict": yes_dict,
        "no_dict": no_dict,
        "uncomf_word": uncomf_word
        }
        print("Except (start)")
        mc = minecraft.Minecraft.create()
        start()



# Purpose: Code to unpickle 'all_dicts.pickle' file when one wants to check all the saved answers:

# pickle_off = open("all_dicts.pickle", "rb")
# all_dicts = pickle.load(pickle_off)
# yes_dict = all_dicts["yes_dict"]
# no_dict = all_dicts["no_dict"]
# uncomf_word = all_dicts["uncomf_word"]

# for (k,v) in all_dicts.items():
#     print(k, v)




