import numpy as np
np.seterr(divide='ignore', invalid='ignore')

from ._evaluate_rewards import _evaluate_rewards

from ._encode_age import _encode_age
from ._encode_conditions import _encode_conditions
from ._encode_steps import _encode_steps
from ._encode_deviation import _encode_deviation

def _encode_raw_SARS_NL_detailed(s_a_rs, valid_A = None, enough_budget = True, n_elements = 3):
		'''encoding the features, actions, and rewards
	
		valid_A: [True,True,True]
		enough_budget: Boolean
		'''
		if valid_A is None:
			valid_A = [True, True, True]

		s = {} # States
		r = {} # rewards
		uc = {} # user costs
		ac = {} # agency costs

		s_temp = []
		first = True
		for id_ in s_a_rs:

			if first:
				s_temp.append(s_a_rs[id_]['remaining_budget'])
				s_temp.append(_encode_steps(s_a_rs[id_]['step']))
				first = False

			s_temp += _encode_age(s_a_rs[id_]['elements_age'])
			s_temp += _encode_conditions(s_a_rs[id_]['elements_conds'])
			s_temp.append(_encode_deviation(s_a_rs[id_]['deviation']))

			r[id_] = _evaluate_rewards(s_a_rs, id_, n_elements, valid_A, enough_budget)
			ac[id_] = np.sum(s_a_rs[id_]['elements_costs'])
			uc[id_] = s_a_rs[id_]['user_costs']

		for id_ in s_a_rs:
			s[id_] = [s_temp, s_temp, s_temp]

		return s, r, ac, uc