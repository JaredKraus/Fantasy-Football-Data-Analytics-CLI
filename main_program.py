# main routine to call program
# authors: Graydon Hall and Jared Kraus Group 2

# obtain user input for study, then present statistical data based on league type, position, chosen
# ranking system, and count of players to study
from individual_pos_stats import ind_player_stats
from genereal_stats import run_general_stats
from player_comparison import player_compare
ind_player_stats()  # terminal program that gets user input, gives data specific to speicified position
run_general_stats()  # terminal application that shows tables for all positions, and prints plots comparint the positions
player_compare("QB")  # gives graph comparing how QBs got their points (passing, rushing, other)
player_compare("RB")  # gives graph comparing how RBs got their points (receiving, rushing, other)
