rm lang_correlations
python3 diststruct_experiments.py --correlation --learningdata cmuwordlist >>lang_correlations
python3 diststruct_experiments.py --correlation --learningdata shona/ShonaLearningData.txt --featuredata shona/ShonaFeatures.txt >>lang_correlations
python3 diststruct_experiments.py --correlation --learningdata wargamay/WargamayLearningData.txt --featuredata wargamay/WargamayFeatures.txt >>lang_correlations
python3 diststruct_experiments.py --correlation --learningdata indian/telugu-brown.dict --featuredata indian/brahmifeatures.txt >>lang_correlations
python3 diststruct_experiments.py --correlation --learningdata indian/rvfull-learning.txt --featuredata indian/brahmifeatures.txt >>lang_correlations
