from function_with_true_kelly import function_with_true_kelly
from function_without_true_kelly import function_without_true_kelly
from function_percentiles import function_percentiles
from function_threshold_analysis import function_threshold_analysis
import matplotlib.pyplot as plt
import numpy as np
import os

file_parameters = open(os.path.realpath(r'evaluating_kelly\arguments.txt'), 'r')
list_split = file_parameters.readlines()
file_parameters.close()
list_parameters = []
for item in list_split:
    item = item.strip('\n')
    if len(item) > 0 and len(item) < 7:
        list_parameters.append(item)
for i in range(7):
    if list_parameters[i] == 'True':
        list_parameters[i] = True
    elif list_parameters[i] == 'False':
        list_parameters[i] = False
    else:
        print('Invalid value for boolean: True or False only')
        quit()
for i in range(7, 11):
    list_parameters[i] = int(list_parameters[i])
for i in range(11, len(list_parameters)):
    list_parameters[i] = float(list_parameters[i])

with_true_kellys, distort_by_factor, random_probs_evs_kellys, volatility_by_factor, percentiles, threshold_analysis, ev_by_uniform, case, initial_capital, number_external_simulations, number_internal_simulations, volatility, bad_bet_proportion, resilience_factor, view_percentile, percentile_range, p1_factor, p2_factor, min_random_prob, max_random_prob, min_random_ev, max_random_ev, min_random_bad_ev, max_random_bad_ev, min_random_kelly, max_random_kelly, min_random_bad_kelly, max_random_bad_kelly, desired_prob_1, desired_prob_2, desired_prob_3, desired_ev, desired_bad_ev, desired_kelly, upper_distorter, lower_distorter, upper_distortion, lower_distortion, threshold_1, threshold_2, threshold_3 = list_parameters[0], list_parameters[1], list_parameters[2], list_parameters[3], list_parameters[4], list_parameters[5], list_parameters[6], list_parameters[7], list_parameters[8], list_parameters[9], list_parameters[10], list_parameters[11], list_parameters[12], list_parameters[13], list_parameters[14], list_parameters[15], list_parameters[16], list_parameters[17], list_parameters[18], list_parameters[19], list_parameters[20], list_parameters[21], list_parameters[22], list_parameters[23], list_parameters[24], list_parameters[25], list_parameters[26], list_parameters[27], list_parameters[28], list_parameters[29], list_parameters[30], list_parameters[31], list_parameters[32], list_parameters[33], list_parameters[34], list_parameters[35], list_parameters[36], list_parameters[37], list_parameters[38], list_parameters[39], list_parameters[40]

list_desired = [desired_prob_1, desired_prob_2, desired_prob_3, desired_ev, desired_bad_ev, desired_kelly]
list_min_max = [min_random_prob, max_random_prob, min_random_ev, max_random_ev, min_random_bad_ev, max_random_bad_ev, min_random_kelly, max_random_kelly, min_random_bad_kelly, max_random_bad_kelly]
list_distort = [upper_distorter, lower_distorter, upper_distortion, lower_distortion]
list_threshold = [threshold_1, threshold_2, threshold_3]

if volatility > 0 and bad_bet_proportion > 0:
    print(f'Both volatility and bad_bet_proportion cannot be greater than 0')
    quit()
if case not in [1,2,3]:
    print(f'The variable "case" must be assigned as the integer 1, 2, or 3')
    quit()
if case == 3 and with_true_kellys and not random_probs_evs_kellys:
    print(f'This function is not supported (trying different expected values at a certain kelly fraction, or vice versa, does not seem very interesting)')
    quit()
if threshold_analysis and percentiles:
    print('Cannot have both threshold_analysis and percentiles as True')
    quit()

if percentiles:
    list_returned = function_percentiles(with_true_kellys, distort_by_factor, case, random_probs_evs_kellys, initial_capital, number_external_simulations, number_internal_simulations, volatility_by_factor, volatility, bad_bet_proportion, resilience_factor, view_percentile, percentile_range, list_desired, list_min_max, list_distort)
    list_capital_progression, list_expected_capital_progression, list_lower, list_upper, list_break_even, break_even, percentile_break_even = list_returned[0], list_returned[1], list_returned[2], list_returned[3], list_returned[4], list_returned[5], list_returned[6]

    list_capital_progression.insert(0, initial_capital * resilience_factor)
    list_expected_capital_progression.insert(0, initial_capital * resilience_factor)
    list_lower.insert(0, initial_capital * resilience_factor)
    list_upper.insert(0, initial_capital * resilience_factor)
    list_break_even.insert(0, initial_capital * resilience_factor)

    x_points = np.array(range(number_internal_simulations + 1))
    y_points_capital = np.array(list_capital_progression)
    y_points_expected_capital = np.array(list_expected_capital_progression)
    y_points_lower = np.array(list_lower)
    y_points_upper = np.array(list_upper)
    label_lower = f'Percentile {view_percentile * 100}'
    label_upper = f'Percentile {(1 - view_percentile) * 100}'
    if break_even:
        y_points_break_even = np.array(list_break_even)
        label_break_even = 'Break-Even Percentile: ' + f'{100 * round(percentile_break_even, 3)}'[:4]
    if percentile_range > 0:
        interval = f' +- {100 * round(percentile_range, 3)}'[:8]
        label_lower += interval
        label_upper += interval
        if break_even:
            label_break_even += interval
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title = "Capital Development", xlabel = "Number of Bets", ylabel = "Capital")
    points_1 = ax.scatter(x_points, y_points_capital, color = 'yellow', label = 'Average Capital' + f', Profit: {round(list_capital_progression[-1] - initial_capital, 3)}')
    points_2 = ax.plot(x_points, y_points_expected_capital, color = 'yellow', linestyle='dashed', label = 'Average Expected Capital')
    points_3 = ax.scatter(x_points, y_points_lower, color = 'red', label = label_lower + f', Profit: {round(list_lower[-1] - initial_capital, 3)}')
    points_ec_1 = ax.scatter(x_points, y_points_upper, color = 'green', label = label_upper + f', Profit: {round(list_upper[-1] - initial_capital, 3)}')
    if break_even:
        points_ec_2 = ax.scatter(x_points, y_points_break_even, color = 'black', label = label_break_even)
    points_ic = ax.plot([0,number_internal_simulations], [initial_capital, initial_capital], color="black")
    plt.legend(loc = 'best')
    ax.set_xlim(0, )
    if not (not with_true_kellys and not distort_by_factor):
        ax.set_ylim(0, )
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.show()

elif threshold_analysis:
    list_returned = function_threshold_analysis(ev_by_uniform, initial_capital, number_external_simulations, number_internal_simulations, volatility_by_factor, volatility, list_min_max, list_threshold, bad_bet_proportion, resilience_factor)
    list_capital_value_1, list_capital_value_2, list_capital_value_3, list_expected_capital_1, list_expected_capital_2, list_expected_capital_3, bet_count_1, bet_count_2, bet_count_3 = list_returned[0], list_returned[1], list_returned[2], list_returned[3], list_returned[4], list_returned[5], list_returned[6], list_returned[7], list_returned[8]

    x_points_1 = np.array(range(len(list_capital_value_1) + 1))
    x_points_2 = np.array(range(len(list_capital_value_2) + 1))
    x_points_3 = np.array(range(len(list_capital_value_3) + 1))
    x_points_ec_1 = np.array(range(len(list_expected_capital_1) + 1))
    x_points_ec_2 = np.array(range(len(list_expected_capital_2) + 1))
    x_points_ec_3 = np.array(range(len(list_expected_capital_3) + 1))
    list_capital_value_1.insert(0, initial_capital * resilience_factor)
    list_capital_value_2.insert(0, initial_capital * resilience_factor)
    list_capital_value_3.insert(0, initial_capital * resilience_factor)
    list_expected_capital_1.insert(0, initial_capital * resilience_factor)
    list_expected_capital_2.insert(0, initial_capital * resilience_factor)
    list_expected_capital_3.insert(0, initial_capital * resilience_factor)
    y_points_1 = np.array(list_capital_value_1)
    y_points_2 = np.array(list_capital_value_2)
    y_points_3 = np.array(list_capital_value_3)
    y_points_ec_1 = np.array(list_expected_capital_1)
    y_points_ec_2 = np.array(list_expected_capital_2)
    y_points_ec_3 = np.array(list_expected_capital_3)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title = "Capital Development", xlabel = "Number of Bets", ylabel = "Capital")
    points_1 = ax.scatter(x_points_1, y_points_1, color = 'red', label = f'Threshold: {threshold_1}, Profit: {round(list_capital_value_1[-1] - initial_capital, 3)}, Bet Proportion: {round(bet_count_1 / number_internal_simulations, 3)}')
    points_2 = ax.scatter(x_points_2, y_points_2, color = 'purple', label = f'Threshold: {threshold_2}, Profit: {round(list_capital_value_2[-1] - initial_capital, 3)}, Bet Proportion: {round(bet_count_2 / number_internal_simulations, 3)}')
    points_3 = ax.scatter(x_points_3, y_points_3, color = 'green', label = f'Threshold: {threshold_3}, Profit: {round(list_capital_value_3[-1] - initial_capital, 3)}, Bet Proportion: {round(bet_count_3 / number_internal_simulations, 3)}')
    points_ec_1 = ax.plot(x_points_ec_1, y_points_ec_1, color = 'red', linestyle='dashed')
    points_ec_2 = ax.plot(x_points_ec_2, y_points_ec_2, color = 'purple', linestyle='dashed')
    points_ec_3 = ax.plot(x_points_ec_3, y_points_ec_3, color = 'green', linestyle='dashed')
    points_ic = ax.plot([0,max([bet_count_1, bet_count_2, bet_count_3])], [initial_capital, initial_capital], color="black")
    points_label_ec = ax.plot([0,max([bet_count_1, bet_count_2, bet_count_3])], [initial_capital, initial_capital], 'k--', label = 'Expected Capital')
    plt.legend(loc = 'best')
    ax.set_xlim(0, )
    ax.set_ylim(0, )
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.show()

else:
    if with_true_kellys:
        list_returned = function_with_true_kelly(case, random_probs_evs_kellys, p2_factor, initial_capital, number_external_simulations, number_internal_simulations, volatility_by_factor, volatility, bad_bet_proportion, resilience_factor, p1_factor, list_desired, list_min_max)
    else:
        list_returned = function_without_true_kelly(case, distort_by_factor, p2_factor, initial_capital, number_external_simulations, number_internal_simulations, volatility_by_factor, volatility, bad_bet_proportion, resilience_factor, p1_factor, list_distort, list_min_max)

    list_capital_value_1, list_capital_value_2, list_capital_value_3, list_expected_capital_1, list_expected_capital_2, list_expected_capital_3, list_graph = list_returned[0], list_returned[1], list_returned[2], list_returned[3], list_returned[4], list_returned[5], list_returned[6]
    legend_1, legend_2, legend_3, location = list_graph[0], list_graph[1], list_graph[2], list_graph[3]

    list_capital_value_1.insert(0, initial_capital * resilience_factor)
    list_capital_value_2.insert(0, initial_capital * resilience_factor)
    list_capital_value_3.insert(0, initial_capital * resilience_factor)
    list_expected_capital_1.insert(0, initial_capital * resilience_factor)
    list_expected_capital_2.insert(0, initial_capital * resilience_factor)
    list_expected_capital_3.insert(0, initial_capital * resilience_factor)

    x_points = np.array(range(number_internal_simulations + 1))
    y_points_1 = np.array(list_capital_value_1)
    y_points_2 = np.array(list_capital_value_2)
    y_points_3 = np.array(list_capital_value_3)
    y_points_ec_1 = np.array(list_expected_capital_1)
    y_points_ec_2 = np.array(list_expected_capital_2)
    y_points_ec_3 = np.array(list_expected_capital_3)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title = "Capital Development", xlabel = "Number of Bets", ylabel = "Capital")
    points_1 = ax.scatter(x_points, y_points_1, color = 'red', label = legend_1)
    points_2 = ax.scatter(x_points, y_points_2, color = 'purple', label = legend_2)
    points_3 = ax.scatter(x_points, y_points_3, color = 'green', label = legend_3)
    points_ec_1 = ax.plot(x_points, y_points_ec_1, color = 'red', linestyle='dashed')
    points_ec_2 = ax.plot(x_points, y_points_ec_2, color = 'purple', linestyle='dashed')
    points_ec_3 = ax.plot(x_points, y_points_ec_3, color = 'green', linestyle='dashed')
    points_ic = ax.plot([0,number_internal_simulations], [initial_capital, initial_capital], color="black")
    points_label_ec = ax.plot([0,number_internal_simulations], [initial_capital, initial_capital], 'k--', label = 'Expected Capital')
    plt.legend(loc = location)
    ax.set_xlim(0, )
    if not (not with_true_kellys and not distort_by_factor):
        ax.set_ylim(0, )
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.show()
