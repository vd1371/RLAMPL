#Loading dependenvies
import os
import sys
import time
import numpy as np

sys.path.append('../GIAMS/')

from RLUtils import *
from ModelsAndLearning import *
from FindBaseLines import *
from LifeCycleRun import Run
from LearningObjects import *

def exec(warm_up = False,
		learning_model = DQN,
		should_find_baselines = True,
		is_double = False,
		n_assets = 1,
		with_detailed_features = False):
	
	print ("Learning started")
	base_direc, report_direc = create_path(__file__, learning_model.name)
	LrnObjs = LearningObjects(base_direc,
						n_assets,
						learning_model = learning_model,
						Exp = 0,
						max_Exp = 10000,
						GAMMA = 0.97,
						lr = 0.0001,
						batch_size = 1000,
						epochs = 10,
						t = 1,
						eps_decay = 0.001,
						eps = 0.5,
						bucket_size = 10000,
						n_sim = 10,
						# n_states = 7*n_assets + 2, # 7*n+2 for detailed,
						# 51 features from network + 6 for conds and ages 
						n_states = 49 + 7,
						warm_up = warm_up,
						is_double = is_double,
						with_detailed_features = with_detailed_features,
						n_jobs = 10)

	R_opt, ac_opt, uc_opt = show_baseline("GAbyRF", should_find_baselines, LrnObjs, Run)

	start, previous_time = time.time(), time.time()
	for i in range(int(LrnObjs.Exp), int(LrnObjs.max_Exp)):

		Run(LrnObjs, for_ = learning_model.name)
		
		LrnObjs.memory_replay(LrnObjs, for_ = learning_model.name)

		LrnObjs.save_models_and_hyperparameters(i, after_each = 100)

		LrnObjs.update_target_models(i,
									after_each = 100,
									for_ = learning_model.name)

		LrnObjs.update_eps(i, after_each = 5)

		previous_time = monitor_learning(i, LrnObjs, Run,
										R_opt, ac_opt, uc_opt,
										start, previous_time)

		print (f"Experience {i} is analyzed in {time.time()-previous_time:.2f}")

	print ("Done")



if __name__ == "__main__":

	os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

	exec(warm_up = False,
		should_find_baselines = True,
		learning_model = A2C,
		is_double = False,
		n_assets = 10,
		with_detailed_features = False)
