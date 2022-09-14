import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy
import scipy.stats as stats 
import warnings
warnings.filterwarnings('ignore')

def function_threshold_analysis(ev_by_uniform, initial_capital, number_external_simulations, number_internal_simulations, volatility_by_factor, volatility, list_min_max, list_threshold, bad_bet_proportion, resilience_factor):
    min_random_prob, max_random_prob, min_random_bad_ev, max_random_bad_ev = list_min_max[0], list_min_max[1], list_min_max[4], list_min_max[5]
    threshold_1, threshold_2, threshold_3 = list_threshold[0], list_threshold[1], list_threshold[2]

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.30)
    ax.set_xlim(-0.15, 0.15)
    ax.set(title = "Expected Value Probability Density Function", xlabel = "Expected Value", ylabel = "Probability Density")
    ax_color = 'lightgoldenrodyellow'

    if ev_by_uniform:
        lower0 = -0.1
        upper0 = 0.1
        height0 = 1 / (upper0 - lower0)
        lower_value = lower0
        upper_value = upper0
        ax.set_ylim(0, 100)
        x = numpy.array([lower0, upper0])
        y = numpy.array([height0, height0])
        area = ax.fill_between(x, y, color='cadetblue', alpha=0.7)
        l, = plt.plot(x, y, color='navy')
        ax_lower = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=ax_color)
        ax_upper = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=ax_color)

        s_lower = Slider(ax_lower, 'Lower Bound', -0.15, 0.15, valinit=lower0)
        s_upper = Slider(ax_upper, 'Upper Bound', -0.15, 0.15, valinit=upper0)

        def uniform_update(val):
            if s_lower.val < s_upper.val:
                lower = s_lower.val
                upper = s_upper.val
                height = 1 / (upper - lower)
                l.set_xdata(numpy.array([lower, upper]))
                l.set_ydata(numpy.array([height, height]))
                nonlocal area
                area.remove()
                area = ax.fill_between(numpy.array([lower, upper]), numpy.array([height, height]), color='cadetblue', alpha=0.7)
                fig.canvas.draw_idle()


        s_lower.on_changed(uniform_update)
        s_upper.on_changed(uniform_update)

        resetax = plt.axes([0.02, 0.275, 0.175, 0.04])
        uniform_button_reset = Button(resetax, 'Reset Values', color=ax_color, hovercolor='0.975')
        def uniform_reset(event):
            s_lower.reset()
            s_upper.reset()
        uniform_button_reset.on_clicked(uniform_reset)


        savevalues = plt.axes([0.02, 0.225, 0.175, 0.04])
        uniform_button_save = Button(savevalues, 'Save and Close', color=ax_color, hovercolor='0.975')
        def uniform_save_and_close(event):
            global lower_value
            global upper_value
            lower_value = s_lower.val
            upper_value = s_upper.val
            plt.close()
        uniform_button_save.on_clicked(uniform_save_and_close)

        max_bet_count_1 = round(number_internal_simulations * (upper_value - threshold_1) / (upper_value - lower_value)) - 1
        max_bet_count_2 = round(number_internal_simulations * (upper_value - threshold_2) / (upper_value - lower_value)) - 1
        max_bet_count_3 = round(number_internal_simulations * (upper_value - threshold_3) / (upper_value - lower_value)) - 1

    else:
        shape0 = 2.5
        scale0 = 0.02
        threshold0 = -0.05
        shape_value = shape0
        scale_value = scale0
        threshold_value = threshold0
        x = numpy.linspace (-.15, .15, 100)
        y = stats.gamma.pdf(x, shape0, threshold0, scale0)    
        ax.set_ylim(0, max(y) * 3)
        area = ax.fill_between(x, y, color='cadetblue', alpha=0.7)
        l, = plt.plot(x, y, color='navy')

        ax_shape = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=ax_color)
        ax_scale = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=ax_color)
        ax_threshold = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=ax_color)

        s_shape = Slider(ax_shape, 'Shape', 0, 10, valinit=shape0)
        s_scale = Slider(ax_scale, 'Scale', 0, 0.1, valinit=scale0)
        s_threshold = Slider(ax_threshold, 'Threshold', -0.15, 0.15, valinit=threshold0)

        def gamma_update(val):
            shape = s_shape.val
            scale = s_scale.val
            threshold = s_threshold.val
            l.set_ydata(stats.gamma.pdf(x, shape, threshold, scale))
            nonlocal area
            area.remove()
            area = ax.fill_between(x, stats.gamma.pdf(x, shape, threshold, scale), color='cadetblue', alpha=0.7)
            fig.canvas.draw_idle()


        s_shape.on_changed(gamma_update)
        s_scale.on_changed(gamma_update)
        s_threshold.on_changed(gamma_update)

        resetax = plt.axes([0.02, 0.275, 0.175, 0.04])
        gamma_button_reset = Button(resetax, 'Reset Values', color=ax_color, hovercolor='0.975')
        def gamma_reset(event):
            s_shape.reset()
            s_scale.reset()
            s_threshold.reset()
        gamma_button_reset.on_clicked(gamma_reset)


        savevalues = plt.axes([0.02, 0.225, 0.175, 0.04])
        gamma_button_save = Button(savevalues, 'Save and Close', color=ax_color, hovercolor='0.975')
        def gamma_save_and_close(event):
            global shape_value
            global scale_value
            global threshold_value
            shape_value = s_shape.val
            scale_value = s_scale.val
            threshold_value = s_threshold.val
            plt.close()
        gamma_button_save.on_clicked(gamma_save_and_close)

        max_bet_count_1 = round(number_internal_simulations * (1 - stats.gamma.cdf(threshold_1, shape0, threshold0, scale0))) - 1
        max_bet_count_2 = round(number_internal_simulations * (1 - stats.gamma.cdf(threshold_2, shape0, threshold0, scale0))) - 1
        max_bet_count_3 = round(number_internal_simulations * (1 - stats.gamma.cdf(threshold_3, shape0, threshold0, scale0))) - 1

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()
    
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
        capital_1 = initial_capital  * resilience_factor
        capital_2 = initial_capital * resilience_factor
        capital_3 = initial_capital * resilience_factor
        expected_capital_1 = initial_capital * resilience_factor
        expected_capital_2 = initial_capital * resilience_factor
        expected_capital_3 = initial_capital * resilience_factor
        bet_count_1 = 0
        bet_count_2 = 0
        bet_count_3 = 0
        while bet_count_1 < max_bet_count_1 or bet_count_2 < max_bet_count_2 or bet_count_3 < max_bet_count_3:
            prob = numpy.random.uniform(min_random_prob, max_random_prob)
            prob_off = prob
            
            if ev_by_uniform:
                ev = numpy.random.uniform(lower_value, upper_value)
            else:
                ev = stats.gamma.rvs(a= shape_value, loc= threshold_value, scale= scale_value)

            bad_ev = numpy.random.uniform(min_random_bad_ev, max_random_bad_ev)
            
            odds = (1 + ev) / prob - 1
            kelly = prob - (1 - prob) / odds

            if bad_bet_proportion > 0:
                if random.choice(list_bad_bets) == 'h':
                    prob_off = (1 - bad_ev) / (odds + 1)
            elif volatility > 0 and volatility_by_factor == True:
                for i in range(100000):
                    prob_off *= (1 + numpy.random.uniform(-volatility, volatility))
                    if prob_off < 1:
                        break
            elif volatility > 0 and volatility_by_factor == False:
                for i in range(100000):
                    prob_off += numpy.random.uniform(-volatility, volatility)
                    if prob_off < 1:
                        break
            else:
                pass
            
            list_outcomes = []
            for i in range(round(prob_off * 1000)):
                list_outcomes.append('h')
            for i in range(round((1 - prob_off) * 1000)):
                list_outcomes.append('t')
            result = random.choice(list_outcomes)          

            if threshold_1 < ev and bet_count_1 < max_bet_count_1:             
                bet_1 = capital_1 * kelly
                expected_capital_1 += bet_1 * prob * (1 + odds) - bet_1
                capital_1 -= bet_1
                if result == 'h':
                    capital_1 += bet_1 * (odds + 1)
                list_capital_value_1[bet_count_1] += capital_1
                list_expected_capital_1[bet_count_1] += expected_capital_1
                bet_count_1 += 1
            
            if threshold_2 < ev and bet_count_2 < max_bet_count_2:
                bet_2 = capital_2 * kelly
                expected_capital_2 += bet_2 * prob * (1 + odds) - bet_2
                capital_2 -= bet_2
                if result == 'h':
                    capital_2 += bet_2 * (odds + 1)
                list_capital_value_2[bet_count_2] += capital_2
                list_expected_capital_2[bet_count_2] += expected_capital_2
                bet_count_2 += 1
            
            if threshold_3 < ev and bet_count_3 < max_bet_count_3:
                bet_3 = capital_3 * kelly
                expected_capital_3 += bet_3 * prob * (1 + odds) - bet_3
                capital_3 -= bet_3
                if result == 'h':
                    capital_3 += bet_3 * (odds + 1)
                list_capital_value_3[bet_count_3] += capital_3
                list_expected_capital_3[bet_count_3] += expected_capital_3
                bet_count_3 += 1

    for i in range(number_internal_simulations):
        list_capital_value_1[i] /= number_external_simulations
        list_capital_value_2[i] /= number_external_simulations
        list_capital_value_3[i] /= number_external_simulations
        list_expected_capital_1[i] /= number_external_simulations
        list_expected_capital_2[i] /= number_external_simulations
        list_expected_capital_3[i] /= number_external_simulations
    
    def remove_zero(input_list):
        output_list = [i for i in input_list if i != 0]
        return output_list

    
    list_capital_value_1 = remove_zero(list_capital_value_1)
    list_capital_value_2 = remove_zero(list_capital_value_2)
    list_capital_value_3 = remove_zero(list_capital_value_3)
    list_expected_capital_1 = remove_zero(list_expected_capital_1)
    list_expected_capital_2 = remove_zero(list_expected_capital_2)
    list_expected_capital_3 = remove_zero(list_expected_capital_3)

    return [list_capital_value_1, list_capital_value_2, list_capital_value_3, list_expected_capital_1, list_expected_capital_2, list_expected_capital_3, max_bet_count_1, max_bet_count_2, max_bet_count_3]

