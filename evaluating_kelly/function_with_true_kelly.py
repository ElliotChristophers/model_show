import random
import numpy
import scipy.stats
from cmath import sqrt
import warnings
warnings.filterwarnings('ignore')

def function_with_true_kelly(case, random_probs_evs_kellys, p2_factor, initial_capital, number_external_simulations, number_internal_simulations, volatility_by_factor, volatility, bad_bet_proportion, resilience_factor, p1_factor, list_desired, list_min_max):
    desired_prob_1, desired_prob_2, desired_prob_3, desired_ev, desired_bad_ev, desired_kelly = list_desired[0], list_desired[1], list_desired[2], list_desired[3], list_desired[4], list_desired[5]
    min_random_prob, max_random_prob, min_random_ev, max_random_ev, min_random_bad_ev, max_random_bad_ev, min_random_kelly, max_random_kelly, min_random_bad_kelly, max_random_bad_kelly = list_min_max[0], list_min_max[1], list_min_max[2], list_min_max[3], list_min_max[4], list_min_max[5], list_min_max[6], list_min_max[7], list_min_max[8], list_min_max[9]

    if not random_probs_evs_kellys and case != 2:
        exit_condition = False
        if desired_prob_1 <= desired_kelly or desired_prob_2 <= desired_kelly or desired_prob_3 <= desired_kelly:
            print(f'desired_kelly cannot be lower than probability, see assignment to desired_kelly and probs\n')
            exit_condition = True
        if 1 < desired_kelly * (1 - desired_prob_1) / (desired_prob_1 - desired_kelly):
            print(f"desired_kelly and desired_prob_1 must fulfil the following: 1 < desired_kelly * (1 - desired_prob_1) / (desired_prob_1 - desired_kelly), see assignment to desired_kelly, desired_bad_kelly, and probs\n")
            exit_condition = True
        if 1 < desired_kelly * (1 - desired_prob_2) / (desired_prob_2 - desired_kelly):
            print(f"desired_kelly and desired_prob_2 must fulfil the following: 1 < desired_kelly * (1 - desired_prob_2) / (desired_prob_2 - desired_kelly), see assignment to desired_kelly, desired_bad_kelly, and probs\n")
            exit_condition = True
        if 1 < desired_kelly * (1 - desired_prob_3) / (desired_prob_3 - desired_kelly):
            print(f"desired_kelly and desired_prob_3 must fulfil the following: 1 < desired_kelly * (1 - desired_prob_3) / (desired_prob_3 - desired_kelly), see assignment to desired_kelly, desired_bad_kelly, and probs\n")
            exit_condition = True
        if exit_condition:
            exit()

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


    for num in range(1, number_external_simulations + 1):
        capital_1 = initial_capital * resilience_factor
        capital_2 = initial_capital * resilience_factor
        capital_3 = initial_capital * resilience_factor
        expected_capital_1 = initial_capital * resilience_factor
        expected_capital_2 = initial_capital * resilience_factor
        expected_capital_3 = initial_capital * resilience_factor
        for iter in range(number_internal_simulations):
            if random_probs_evs_kellys:
                if case == 1:
                    p_1 = numpy.random.uniform(min_random_prob, max_random_prob)
                    p_2 = numpy.random.uniform(min_random_prob, max_random_prob)
                    p_3 = numpy.random.uniform(min_random_prob, max_random_prob)
                    ev_1 = numpy.random.uniform(min_random_ev, max_random_ev)
                    ev_2 = numpy.random.uniform(min_random_ev, max_random_ev)
                    ev_3 = numpy.random.uniform(min_random_ev, max_random_ev)
                    bad_ev_1 = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                    bad_ev_2 = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                    bad_ev_3 = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                elif case == 2:
                    for i in range(100000):
                        p_1 = numpy.random.uniform(min_random_prob, max_random_prob)
                        p_2 = numpy.random.uniform(min_random_prob, max_random_prob)
                        p_3 = numpy.random.uniform(min_random_prob, max_random_prob)
                        kelly_1 = numpy.random.uniform(min_random_kelly, max_random_kelly)
                        kelly_2 = numpy.random.uniform(min_random_kelly, max_random_kelly)
                        kelly_3 = numpy.random.uniform(min_random_kelly, max_random_kelly)
                        if p_1 > kelly_1 and p_2 > kelly_2 and p_3 > kelly_3:
                            bad_ev_1 = numpy.random.uniform(min_random_bad_kelly * (1 - p_1) / (p_1 - min_random_bad_kelly), max_random_bad_kelly * (1 - p_1) / (p_1 - max_random_bad_kelly))
                            bad_ev_2 = numpy.random.uniform(min_random_bad_kelly * (1 - p_2) / (p_2 - min_random_bad_kelly), max_random_bad_kelly * (1 - p_2) / (p_2 - max_random_bad_kelly))
                            bad_ev_3 = numpy.random.uniform(min_random_bad_kelly * (1 - p_3) / (p_3 - min_random_bad_kelly), max_random_bad_kelly * (1 - p_3) / (p_3 - max_random_bad_kelly))
                            if bad_ev_1 < 1 and bad_ev_2 < 1 and bad_ev_3 < 1:
                                break
                else:
                    ev_1 = numpy.random.uniform(min_random_ev, max_random_ev)
                    ev_2 = numpy.random.uniform(min_random_ev, max_random_ev)
                    ev_3 = numpy.random.uniform(min_random_ev, max_random_ev)
                    bad_ev_1 = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                    bad_ev_2 = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                    bad_ev_3 = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                    kelly_1 = numpy.random.uniform(min_random_kelly, max_random_kelly)
                    kelly_2 = numpy.random.uniform(min_random_kelly, max_random_kelly)
                    kelly_3 = numpy.random.uniform(min_random_kelly, max_random_kelly)
            else:
                p_1 = desired_prob_1
                p_2 = desired_prob_2
                p_3 = desired_prob_3
                ev_1 = desired_ev
                ev_2 = desired_ev
                ev_3 = desired_ev
                bad_ev_1 = desired_bad_ev
                bad_ev_2 = desired_bad_ev
                bad_ev_3 = desired_bad_ev
                kelly_1 = desired_kelly
                kelly_2 = desired_kelly
                kelly_3 = desired_kelly
                if case == 2:
                    bad_ev_1 = kelly_1 * (1 - p_1) / (p_1 - kelly_1)
                    bad_ev_2 = kelly_2 * (1 - p_2) / (p_2 - kelly_2)
                    bad_ev_3 = kelly_3 * (1 - p_3) / (p_3 - kelly_3)
            
            if case == 1:
                odds_1 = (1 + ev_1) / p_1 - 1
                odds_2 = (1 + ev_2) / p_2 - 1
                odds_3 = (1 + ev_3) / p_3 - 1

                kelly_1 = p_1 - (1 - p_1) / odds_1
                kelly_2 = p_2 - (1 - p_2) / odds_2
                kelly_3 = p_3 - (1 - p_3) / odds_3
            elif case == 2:                
                odds_1 = (1 - p_1) / (p_1 - kelly_1)
                odds_2 = (1 - p_2) / (p_2 - kelly_2)
                odds_3 = (1 - p_3) / (p_3 - kelly_3)
            else:
                odds_1 = ev_1 / kelly_1
                odds_2 = ev_2 / kelly_2
                odds_3 = ev_3 / kelly_3
                p_1 = kelly_1 * (1 + ev_1) / (ev_1 + kelly_1)
                p_2 = kelly_2 * (1 + ev_2) / (ev_2 + kelly_2)
                p_3 = kelly_3 * (1 + ev_3) / (ev_3 + kelly_3)

            bet_1 = capital_1 * kelly_1
            bet_2 = capital_2 * kelly_2
            bet_3 = capital_3 * kelly_3
            
            expected_capital_1 += bet_1 * p_1 * (1 + odds_1) - bet_1
            expected_capital_2 += bet_2 * p_2 * (1 + odds_2) - bet_2
            expected_capital_3 += bet_3 * p_3 * (1 + odds_3) - bet_3

            if bad_bet_proportion > 0:
                if random.choice(list_bad_bets) == 'h':
                    p_1 = (1 - bad_ev_1) / (odds_1 + 1)
                if random.choice(list_bad_bets) == 'h':
                    p_2 = (1 - bad_ev_2) / (odds_2 + 1)
                if random.choice(list_bad_bets) == 'h':
                    p_3 = (1 - bad_ev_3) / (odds_3 + 1)
            elif volatility > 0 and volatility_by_factor == True:
                for i in range(100000):
                    p_1 *= (1 + numpy.random.uniform(-volatility, volatility))
                    p_2 *= (1 + numpy.random.uniform(-volatility, volatility))
                    p_3 *= (1 + numpy.random.uniform(-volatility, volatility))
                    if max([p_1, p_2, p_3]) < 1:
                        break
            elif volatility > 0 and volatility_by_factor == False:
                for i in range(100000):
                    p_1 += numpy.random.uniform(-volatility, volatility)
                    p_2 += numpy.random.uniform(-volatility, volatility)
                    p_3 += numpy.random.uniform(-volatility, volatility)
                    if max([p_1, p_2, p_3]) < 1:
                        break
            else:
                pass
            
            list_outcomes_1 = []
            list_outcomes_2 = []
            list_outcomes_3 = []
            for i in range(round(p_1 * 1000)):
                list_outcomes_1.append('h')
            for i in range(round((1 - p_1) * 1000)):
                list_outcomes_1.append('t')
            for i in range(round(p_2 * 1000)):
                list_outcomes_2.append('h')
            for i in range(round((1 - p_2) * 1000)):
                list_outcomes_2.append('t')
            for i in range(round(p_3 * 1000)):
                list_outcomes_3.append('h')
            for i in range(round((1 - p_3) * 1000)):
                list_outcomes_3.append('t')
            
            result_1 = random.choice(list_outcomes_1)
            result_2 = random.choice(list_outcomes_2)
            result_3 = random.choice(list_outcomes_3)
            capital_1 -= bet_1
            capital_2 -= bet_2
            capital_3 -= bet_3
            if result_1 == 'h':
                capital_1 += bet_1 * (odds_1 + 1)
            if result_2 == 'h':
                capital_2 += bet_2 * (odds_2 + 1)
            if result_3 == 'h':
                capital_3 += bet_3 * (odds_3 + 1)
            
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

    if random_probs_evs_kellys:
        legend_1 = f'One Possible Permutation\n{message_1}'
        legend_2 = f'One Possible Permutation\n{message_2}'
        legend_3 = f'One Possible Permutation\n{message_3}'
        location = 'best'
    else:
        legend_1 = f'Probability: {desired_prob_1}\n{message_1}'
        legend_2 = f'Probability: {desired_prob_2}\n{message_2}'
        legend_3 = f'Probability: {desired_prob_3}\n{message_3}'
        location = 'best'
    list_graph = [legend_1, legend_2, legend_3, location]
    return [list_capital_value_1, list_capital_value_2, list_capital_value_3, list_expected_capital_1, list_expected_capital_2, list_expected_capital_3, list_graph]