from adventurelib import *

class Help:
    def __init__(self, lang) -> None:
        self.lang = lang

    def help(self, context) -> None:
        match context:
            case "forest":
                say(self.lang["help_forest_1"])
                say(self.lang["action_goto_direction"] + " -> " + self.lang["help_forest_2"])
            case "battle":
                say(self.lang["action_battle_attack"] + " -> " + self.lang["help_battle_1"])
                say(self.lang["action_battle_defend"] + " -> " + self.lang["help_battle_2"])
                say(self.lang["action_battle_escape"] + " -> " + self.lang["help_battle_3"])
            case "cavern.entrance":
                say(self.lang["action_cavern_left"] + " -> " + self.lang["help_cavern_entrance_1"])
                say(self.lang["action_cavern_right"] + " -> " + self.lang["help_cavern_entrance_2"])
            case "cavern.warehouse":
                say(self.lang["action_cavern_search"] + " -> " + self.lang["help_cavern_warehouse_1"])
                say(self.lang["action_cavern_continue"] + " -> " + self.lang["help_cavern_warehouse_2"])
            case "cavern.decision":
                say(self.lang["action_enter_portal"] + " -> " + self.lang["help_cavern_decision_1"])
                say(self.lang["action_break_portal"] + " -> " + self.lang["help_cavern_decision_2"])
        say(self.lang["action_where_i_am"] + " -> " + self.lang["help_where"])
        say(self.lang["action_help"] + " -> " + self.lang["help_help"])
        say(self.lang["action_exit"] + " -> " + self.lang["help_exit"])
