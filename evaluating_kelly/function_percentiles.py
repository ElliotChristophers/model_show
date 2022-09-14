import random
import numpy
import warnings
warnings.filterwarnings('ignore')

def function_percentiles(with_true_kellys, distort_by_factor, case, random_probs_evs_kellys, initial_capital, number_external_simulations, number_internal_simulations, volatility_by_factor, volatility, bad_bet_proportion, resilience_factor, view_percentile, percentile_range, list_desired, list_min_max, list_distort):
    desired_prob, desired_ev, desired_bad_ev, desired_kelly = list_desired[0], list_desired[3], list_desired[4], list_desired[5]
    min_random_prob, max_random_prob, min_random_ev, max_random_ev, min_random_bad_ev, max_random_bad_ev, min_random_kelly, max_random_kelly, min_random_bad_kelly, max_random_bad_kelly = list_min_max[0], list_min_max[1], list_min_max[2], list_min_max[3], list_min_max[4], list_min_max[5], list_min_max[6], list_min_max[7], list_min_max[8], list_min_max[9]
    distorter, distortion = list_distort[0], list_distort[2]

    if not random_probs_evs_kellys and case != 2:
        if desired_prob <= desired_kelly:
            print(f'desired_kelly cannot be lower than probability, see assignment to desired_kelly and probs\n')
            exit()
        elif 1 < desired_kelly * (1 - desired_prob) / (desired_prob - desired_kelly):
            print(f"desired_kelly and desired_prob_1 must fulfil the following: 1 < desired_kelly * (1 - desired_prob_1) / (desired_prob_1 - desired_kelly), see assignment to desired_kelly, desired_bad_kelly, and probs\n")
            exit()
        else:
            pass
    if number_external_simulations < 100:
        print(f'number_external_simulations = {number_external_simulations}; percentiles requires a larger sample size, 500+ is advisible')
        exit()

    list_lists_capital = []
    list_lists_expected_capital = []

    if bad_bet_proportion > 0:
        list_bad_bets = []
        for i in range(round(bad_bet_proportion * 1000)):
            list_bad_bets.append('h')
        for i in range(round((1-bad_bet_proportion)*1000)):
            list_bad_bets.append('t')


    for num in range(1, number_external_simulations + 1):
        list_capital_value = []
        list_expected_capital_value = []
        capital = initial_capital * resilience_factor
        expected_capital = initial_capital * resilience_factor
        for iter in range(number_internal_simulations):
            if with_true_kellys:
                if random_probs_evs_kellys:
                    if case == 1:
                        prob = numpy.random.uniform(min_random_prob, max_random_prob)
                        ev = numpy.random.uniform(min_random_ev, max_random_ev)
                        bad_ev = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                    elif case == 2:
                        for i in range(100000):
                            prob = numpy.random.uniform(min_random_prob, max_random_prob)
                            kelly = numpy.random.uniform(min_random_kelly, max_random_kelly)
                            if prob > kelly:
                                bad_ev = numpy.random.uniform(min_random_bad_kelly * (1 - prob) / (prob - min_random_bad_kelly), max_random_bad_kelly * (1 - prob) / (prob - max_random_bad_kelly))
                                if bad_ev < 1:
                                    break
                    else:
                        ev = numpy.random.uniform(min_random_ev, max_random_ev)
                        bad_ev = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
                        kelly = numpy.random.uniform(min_random_kelly, max_random_kelly)
                else:
                    prob = desired_prob
                    ev = desired_ev
                    bad_ev = desired_bad_ev
                    kelly = desired_kelly
                    if case == 2:
                        bad_ev = kelly * (1 - prob) / (prob - kelly)
                if case == 1:
                    odds = (1 + ev) / prob - 1
                    kelly = prob - (1 - prob) / odds
                elif case == 2:                
                    odds = (1 - prob) / (prob - kelly)
                else:
                    odds = ev / kelly
                    prob = kelly * (1 + ev) / (ev + kelly)
                bet = capital * kelly
            else:
                if case == 1:
                    prob = numpy.random.uniform(min_random_prob, max_random_prob)
                    ev = numpy.random.uniform(min_random_ev, max_random_ev)
                    odds = (1 + ev) / prob - 1
                    kelly = prob - (1 - prob) / odds
                elif case == 2:
                    for i in range(100000):
                        prob = numpy.random.uniform(min_random_prob, max_random_prob)
                        kelly = numpy.random.uniform(min_random_kelly, max_random_kelly)
                        if prob > kelly:
                            break                
                    odds = (1 - prob) / (prob - kelly)
                else:
                    ev = numpy.random.uniform(min_random_ev, max_random_ev)
                    kelly = numpy.random.uniform(min_random_kelly, max_random_kelly)
                    odds = ev / kelly
                    prob = kelly * (1 + ev) / (ev + kelly)
                if distort_by_factor:
                    bet = capital * kelly * distorter
                else:
                    bet = initial_capital * distortion
            
            expected_capital += bet * prob * (1 + odds) - bet

            if bad_bet_proportion > 0:
                if random.choice(list_bad_bets) == 'h':
                    prob = (1 - bad_ev) / (odds + 1)
            elif volatility > 0 and volatility_by_factor == True:
                for i in range(100000):
                    prob *= (1 + numpy.random.uniform(-volatility, volatility))
                    if prob < 1:
                        break
            elif volatility > 0 and volatility_by_factor == False:
                for i in range(100000):
                    prob += numpy.random.uniform(-volatility, volatility)
                    if prob < 1:
                        break
            else:
                pass
            
            list_outcomes = []
            for i in range(round(prob * 1000)):
                list_outcomes.append('h')
            for i in range(round((1 - prob) * 1000)):
                list_outcomes.append('t')
            
            result = random.choice(list_outcomes)
            capital -= bet
            if result == 'h':
                capital += bet * (odds + 1)
            
            list_capital_value.append(capital)
            list_expected_capital_value.append(expected_capital)

        list_lists_capital.append(list_capital_value)
        list_lists_expected_capital.append(list_expected_capital_value)

    
    list_capital_progression = []
    list_expected_capital_progression = []
    for i in range(number_internal_simulations):
        list_capital_progression.append(0)
        list_expected_capital_progression.append(0)
    for i in range(number_external_simulations):
        capital_list = list_lists_capital[i]
        expected_capital_list = list_lists_expected_capital[i]
        for j in range(number_internal_simulations):
            list_capital_progression[j] += capital_list[j]
            list_expected_capital_progression[j] += expected_capital_list[j]
    for i in range(number_internal_simulations):
        list_capital_progression[i] /= number_external_simulations
        list_expected_capital_progression[i] /= number_external_simulations
    
    list_lists_capital = sorted(list_lists_capital, key=lambda x: x[-1])    
    
    if percentile_range == 0:
        list_lower = list_lists_capital[round(view_percentile * number_external_simulations)]
        list_upper = list_lists_capital[round((1 - view_percentile) * number_external_simulations)]
        break_even = False
        for list_break_even in list_lists_capital:
            if list_break_even[-1] > initial_capital:
                percentile_break_even = (1 + list_lists_capital.index(list_break_even)) / number_external_simulations
                break_even = True
                break
            percentile_break_even = 0
    else:
        lower_lower = round((view_percentile - percentile_range) * number_external_simulations)
        lower_upper = round((view_percentile + percentile_range) * number_external_simulations)
        upper_lower = round((1 - view_percentile - percentile_range) * number_external_simulations)
        upper_upper = round((1 - view_percentile + percentile_range) * number_external_simulations)
        list_lower = []
        list_upper = []
        for i in range(number_internal_simulations):
            list_lower.append(0)
            list_upper.append(0)
        for i in range(lower_lower, lower_upper):
            capital_list = list_lists_capital[i]
            for j in range(number_internal_simulations):
                list_lower[j] += capital_list[j]
        for i in range(upper_lower, upper_upper):
            capital_list = list_lists_capital[i]
            for j in range(number_internal_simulations):
                list_upper[j] += capital_list[j]
        for i in range(number_internal_simulations):
            list_lower[i] /= round(2 * percentile_range * number_external_simulations)
            list_upper[i] /= round(2 * percentile_range * number_external_simulations)
        
        break_even = False
        for i in range(number_external_simulations):
            if list_lists_capital[i][-1] > initial_capital:
                percentile_break_even = (1 + i) / number_external_simulations
                break_even_lower = round((percentile_break_even - percentile_range) * number_external_simulations)
                break_even_upper = round((percentile_break_even + percentile_range) * number_external_simulations)
                list_break_even = []
                for i in range(number_internal_simulations):
                    list_break_even.append(0)
                for i in range(break_even_lower, break_even_upper):
                    capital_list = list_lists_capital[i]
                    for j in range(number_internal_simulations):
                        list_break_even[j] += capital_list[j]    
                for i in range(number_internal_simulations):
                    list_break_even[i] /= round(2 * percentile_range * number_external_simulations)
                break_even = True
                break
            percentile_break_even = 0

    return [list_capital_progression, list_expected_capital_progression, list_lower, list_upper, list_break_even, break_even, percentile_break_even]

