# main routine to call program

# obtain user input for study, then present statistical data based on league type, position, chosen
# ranking system, and count of players to study
from individual_pos_stats import ind_player_stats
from genereal_stats import run_general_stats
from player_comparison import player_compare
ind_player_stats()
run_general_stats()
player_compare("QB")
player_compare("RB")
# stats for all positions
