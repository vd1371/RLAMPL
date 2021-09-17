

def checkpoint(experience,
				LrnObjs,
				models_holder,
				target_models_holder,
				for_= None,
				checkpoint_freq = 100):


	if experience % checkpoint_freq == 0:
		n_trained = models_holder.save_all()
		LrnObjs.save_and_update_hyperparameters(experience, n_trained)

		if not for_ == 'A2C':
			target_models_holder.update(by_other_models_holder = models_holder)