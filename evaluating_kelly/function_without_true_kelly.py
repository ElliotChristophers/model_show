import random
import numpy
import scipy.stats
from cmath import sqrt
import warnings
warnings.filterwarnings('ignore')

def function_without_true_kelly(case, distort_by_factor, p2_factor, initial_capital, number_external_simulations, number_internal_simulations, volatility_by_factor, volatility, bad_bet_proportion, resilience_factor, p1_factor, list_distort, list_min_max):
    upper_distorter, lower_distorter, upper_distortion, lower_distortion = list_distort[0], list_distort[1], list_distort[2], list_distort[3]
    min_random_prob, max_random_prob, min_random_ev, max_random_ev, min_random_bad_ev, max_random_bad_ev, min_random_kelly, max_random_kelly, min_random_bad_kelly, max_random_bad_kelly = list_min_max[0], list_min_max[1], list_min_max[2], list_min_max[3], list_min_max[4], list_min_max[5], list_min_max[6], list_min_max[7], list_min_max[8], list_min_max[9]

    list_profit_1 = []
    list_profit_2 = []
    list_profit_3 = []
    list_final_ec_1 = []
    list_final_ec_2 = []
    list_final_ec_3 = []

    list_capital_value_1 = []
    list_capital_value_2 = []
    list_capital_value_3 = []
    list_expected_capital_1 = []
    list_expected_capital_2 = []
    list_expected_capital_3 = []
    for i in range(number_internal_simulations):
        list_capital_value_1.append(0)
        list_capital_value_2.append(0)
        list_capital_value_3.append(0)
        list_expected_capital_1.append(0)
        list_expected_capital_2.append(0)
        list_expected_capital_3.append(0)

    list_bad_bets = []
    for i in range(round(bad_bet_proportion * 1000)):
        list_bad_bets.append('h')
    for i in range(round((1-bad_bet_proportion)*1000)):
        list_bad_bets.append('t')

    for num in range(number_external_simulations):
        capital_1 = initial_capital * resilience_factor
        capital_2 = initial_capital * resilience_factor
        capital_3 = initial_capital * resilience_factor
        expected_capital_1 = initial_capital * resilience_factor
        expected_capital_2 = initial_capital * resilience_factor
        expected_capital_3 = initial_capital * resilience_factor
        count = 0
        for iter in range(number_internal_simulations):
            if case == 1:
                prob_g = numpy.random.uniform(min_random_prob, max_random_prob)
                ev = numpy.random.uniform(min_random_ev, max_random_ev)
                odds = (1 + ev) / prob_g - 1
                kelly_g = prob_g - (1 - prob_g) / odds
            elif case == 2:
                for i in range(100000):
                    prob_g = numpy.random.uniform(min_random_prob, max_random_prob)
                    kelly_g = numpy.random.uniform(min_random_kelly, max_random_kelly)
                    if prob_g > kelly_g:
                        break                
                odds = (1 - prob_g) / (prob_g - kelly_g)
            else:
                ev = numpy.random.uniform(min_random_ev, max_random_ev)
                kelly_g = numpy.random.uniform(min_random_kelly, max_random_kelly)
                odds = ev / kelly_g
                prob_g = kelly_g * (1 + ev) / (ev + kelly_g)
            
            if distort_by_factor:
                bet_1 = capital_1 * kelly_g * upper_distorter
                bet_2 = capital_2 * kelly_g
                bet_3 = capital_3 * kelly_g * lower_distorter
            else:
                bet_1 = initial_capital * upper_distortion
                bet_2 = capital_2 * kelly_g
                bet_3 = initial_capital * lower_distortion

            expected_capital_1 += bet_1 * prob_g * (1 + odds) - bet_1
            expected_capital_2 += bet_2 * prob_g * (1 + odds) - bet_2
            expected_capital_3 += bet_3 * prob_g * (1 + odds) - bet_3

            if bad_bet_proportion > 0:
                if random.choice(list_bad_bets) == 'h':
                    if case == 2:
                        for i in range(10000):
                            bad_ev = numpy.random.uniform(min_random_bad_kelly * (1 - prob_g) / (prob_g - min_random_bad_kelly), max_random_bad_kelly * (1 - prob_g) / (prob_g - max_random_bad_kelly))
                            if bad_ev < 1:
                                break
                    if case in [1,3]:
                        bad_ev = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                    prob_g = (1 - bad_ev) / (odds + 1)     
            elif volatility > 0 and volatility_by_factor == True:
                for i in range(100000):
                    prob_g *= (1 + numpy.random.uniform(-volatility, volatility))
                    if prob_g < 1:
                        break
            elif volatility > 0 and volatility_by_factor == False:
                for i in range(100000):
                    prob_g += numpy.random.uniform(-volatility, volatility)
                    if prob_g < 1:
                        break
            else:
                pass               

            list_outcomes = []
            for i in range(round(prob_g * 1000)):
                list_outcomes.append('h')
            for i in range(round((1-prob_g)*1000)):
                list_outcomes.append('t')
            result = random.choice(list_outcomes)

            capital_1 -= bet_1
            capital_2 -= bet_2
            capital_3 -= bet_3
            if result == 'h':
                capital_1 += bet_1 * (odds + 1)
                capital_2 += bet_2 * (odds + 1)
                capital_3 += bet_3 * (odds + 1)

            count += 1
            list_capital_value_1[iter] += capital_1
            list_capital_value_2[iter] += capital_2
            list_capital_value_3[iter] += capital_3
            list_expected_capital_1[iter] += expected_capital_1
            list_expected_capital_2[iter] += expected_capital_2
            list_expected_capital_3[iter] += expected_capital_3

        list_profit_1.append(capital_1 - initial_capital)
        list_profit_2.append(capital_2 - initial_capital)
        list_profit_3.append(capital_3 - initial_capital)
        list_final_ec_1.append(expected_capital_1)
        list_final_ec_2.append(expected_capital_2)
        list_final_ec_3.append(expected_capital_3)    

    for i in range(number_internal_simulations):
        list_capital_value_1[i] /= number_external_simulations
        list_capital_value_2[i] /= number_external_simulations
        list_capital_value_3[i] /= number_external_simulations
        list_expected_capital_1[i] /= number_external_simulations
        list_expected_capital_2[i] /= number_external_simulations
        list_expected_capital_3[i] /= number_external_simulations

    profit_1 = numpy.mean(list_profit_1)
    profit_2 = numpy.mean(list_profit_2)
    profit_3 = numpy.mean(list_profit_3)
    growth_1 = profit_1 / initial_capital
    growth_2 = profit_2 / initial_capital
    growth_3 = profit_3 / initial_capital
    message_1 = f'Growth Rate: {round(100*growth_1, 2)}%, Profit: {round(profit_1, 2)}'
    message_2 = f'Growth Rate: {round(100*growth_2, 2)}%, Profit: {round(profit_2, 2)}'
    message_3 = f'Growth Rate: {round(100*growth_3, 2)}%, Profit: {round(profit_3, 2)}'
    if number_external_simulations > 1:
        std_profit_1 = numpy.std(list_profit_1)
        std_profit_2 = numpy.std(list_profit_2)
        std_profit_3 = numpy.std(list_profit_3)
        message_1 += f', Profit STD: {round(std_profit_1, 2)}'
        message_2 += f', Profit STD: {round(std_profit_2, 2)}'
        message_3 += f', Profit STD: {round(std_profit_3, 2)}'
    if number_external_simulations >= 30:
        observed_1 = float((profit_1 - p1_factor * initial_capital) / (std_profit_1 / sqrt(number_external_simulations)))
        p1_value_1 = round(1 - scipy.stats.norm(0, 1).cdf(observed_1), 3)
        message_1 += f', p1: {p1_value_1}'
        observed_2 = float((profit_2 - p1_factor * initial_capital) / (std_profit_2 / sqrt(number_external_simulations)))
        p1_value_2 = round(1 - scipy.stats.norm(0, 1).cdf(observed_2), 3)
        message_2 += f', p1: {p1_value_2}'
        observed_3 = float((profit_3 - p1_factor * initial_capital) / (std_profit_3 / sqrt(number_external_simulations)))
        p1_value_3 = round(1 - scipy.stats.norm(0, 1).cdf(observed_3), 3)
        message_3 += f', p1: {p1_value_3}'

        final_ec_1 = list_expected_capital_1[-1]
        final_ec_2 = list_expected_capital_2[-1]
        final_ec_3 = list_expected_capital_3[-1]
        std_final_ec_1 = numpy.std(list_final_ec_1)
        std_final_ec_2 = numpy.std(list_final_ec_2)
        std_final_ec_3 = numpy.std(list_final_ec_3)
        std_1 = sqrt((std_profit_1**2 + std_final_ec_1**2) / number_external_simulations)
        std_2 = sqrt((std_profit_2**2 + std_final_ec_2**2) / number_external_simulations)
        std_3 = sqrt((std_profit_3**2 + std_final_ec_3**2) / number_external_simulations)

        p2_u_1 = round(scipy.stats.norm(0, 1).cdf(float((profit_1 + initial_capital - final_ec_1 - p2_factor * initial_capital) / std_1)), 3)
        p2_l_1 = round(1 - scipy.stats.norm(0, 1).cdf(float((profit_1 + initial_capital - final_ec_1 + p2_factor * initial_capital) / std_1)), 3)
        message_1 += f', p2l: {p2_l_1}, p2u: {p2_u_1}'
        p2_u_2 = round(scipy.stats.norm(0, 1).cdf(float((profit_2 + initial_capital - final_ec_2 - p2_factor * initial_capital) / std_2)), 3)
        p2_l_2 = round(1 - scipy.stats.norm(0, 1).cdf(float((profit_2 + initial_capital - final_ec_2 + p2_factor * initial_capital) / std_2)), 3)
        message_2 += f', p2l: {p2_l_2}, p2u: {p2_u_2}'
        p2_u_3 = round(scipy.stats.norm(0, 1).cdf(float((profit_3 + initial_capital - final_ec_3 - p2_factor * initial_capital) / std_3)), 3)
        p2_l_3 = round(1 - scipy.stats.norm(0, 1).cdf(float((profit_3 + initial_capital - final_ec_3 + p2_factor * initial_capital) / std_3)), 3)
        message_3 += f', p2l: {p2_l_3}, p2u: {p2_u_3}'

    if distort_by_factor:
        legend_1 = f'Bets at Kelly * {upper_distorter}\n{message_1}'
        legend_2 = f'Bets at Kelly\n{message_2}'
        legend_3 = f'Bets at Kelly * {lower_distorter}\n{message_3}'
        location = 'best'
    else:
        legend_1 = f'Fixed bets at {initial_capital * upper_distortion}\n{message_1}'
        legend_2 = f'Bets at Kelly\n{message_2}'
        legend_3 = f'Fixed bets at {initial_capital * lower_distortion}\n{message_3}'
        location = 'best'
    list_graph = [legend_1, legend_2, legend_3, location]
    return [list_capital_value_1, list_capital_value_2, list_capital_value_3, list_expected_capital_1, list_expected_capital_2, list_expected_capital_3, list_graph]


