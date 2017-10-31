"""
Cannot catch cases:
1) not direct import: 
    import sklearn
    a = sklearn.svm.SVC()

2) multiple lines: from sklearn.foo import bar,
    bas
"""
class SklearnImportBucket():
    def __init__(self):
        self.outliers = []
        self.subModule = set(['neighbors', 'neural_network', 'kernel_ridge', 'manifold', 'text', 'image', 'feature_extraction', 'cluster', 'partial_dependence', 'naive_bayes', 'estimator_checks', 'gaussian_process', 'utils', 'kernel_approximation', 'datasets', 'calibration', 'multiclass', 'decomposition', 'sparsefuncs', 'class_weight', 'discriminant_analysis', 'isotonic', 'mixture', 'linear_model', 'cross_decomposition', 'semi_supervised', 'covariance', 'libsvm', 'metrics', 'extmath', 'base', 'feature_selection', 'dummy', 'pipeline', 'svm', 'random_projection', 'multioutput', 'tree', 'ensemble', 'preprocessing', 'pairwise', 'validation', 'model_selection'])
        self.model = set([val[0] for val in all_estimators(True,True,None,True) if not val[0].startswith("_")])
        self.function = set(['partial_dependence', 'make_friedman3', 'make_friedman2', 'make_friedman1', 'clear_data_home', 'safe_sparse_dot', 'distance_metrics', 'dict_learning', 'label_ranking_average_precision_score', 'lars_path', 'fetch_species_distributions', 'img_to_graph', 'inplace_row_scale', 'make_sparse_coded_signal', 'paired_manhattan_distances', 'pairwise_kernels', 'precision_recall_fscore_support', 'fbeta_score', 'explained_variance_score', 'confusion_matrix', 'auc', 'fit', 'ward_tree', 'polynomial_kernel', 'fetch_kddcup99', 'load_svmlight_file', 'orthogonal_mp', 'validation_curve', 'cross_val_score', 'make_regression', 'permutation_test_score', 'make_moons', 'f1_score', 'lasso_path', 'resample', 'median_absolute_error', 'load_linnerud', 'rbf_kernel', 'assert_all_finite', 'k_means', 'fastica', 'load_wine', 'homogeneity_score', 'reconstruct_from_patches_2d', 'r2_score', 'make_sparse_uncorrelated', 'zero_one_loss', 'label_binarize', 'orthogonal_mp_gram', 'accuracy_score', 'mean_shift', 'locally_linear_embedding', 'laplacian_kernel', 'dict_learning_online', 'make_pipeline', 'load_mlcomp', 'mutual_info_regression', 'johnson_lindenstrauss_min_dim', 'grid_to_graph', 'make_swiss_roll', 'hamming_loss', 'precision_score', 'calinski_harabaz_score', 'manhattan_distances', 'cross_validate', 'inplace_column_scale', 'label_ranking_loss', 'empirical_covariance', 'homogeneity_completeness_v_measure', 'load_digits', 'learning_curve', 'fetch_lfw_pairs', 'check_is_fitted', 'export_graphviz', 'check_random_state', 'cross_val_predict', 'make_multilabel_classification', 'compute_sample_weight', 'dbscan', 'average_precision_score', 'completeness_score', 'make_low_rank_matrix', 'kernel_metrics', 'load_sample_image', 'hinge_loss', 'pairwise_distances_argmin_min', 'shuffle', 'train_test_split', 'adjusted_mutual_info_score', 'roc_auc_score', 'sigmoid_kernel', 'safe_indexing', 'radius_neighbors_graph', 'check_increasing', 'indexable', 'column_or_1d', 'sparse_encode', 'brier_score_loss', 'fit_grid_point', 'normalized_mutual_info_score', 'linear_kernel', 'roc_curve', 'fetch_20newsgroups', 'maxabs_scale', 'dcg_score', 'load_breast_cancer', 'fetch_olivetti_faces', 'fetch_mldata', 'log_loss', 'mldata_filename', 'v_measure_score', 'make_blobs', 'cohen_kappa_score', 'consensus_score', 'l1_min_c', 'estimate_bandwidth', 'make_s_curve', 'make_hastie_10_2', 'pairwise_distances', 'spectral_embedding', 'check_array', 'lasso_stability_path', 'jaccard_similarity_score', 'f_classif', 'pairwise_distances_argmin', 'spectral_clustering', 'get_scorer', 'cosine_similarity', 'predict_proba', 'euclidean_distances', 'load_files', 'make_union', 'enet_path', 'make_sparse_spd_matrix', 'ledoit_wolf', 'isotonic_regression', 'make_spd_matrix', 'logistic_regression_path', 'check_consistent_length', 'make_biclusters', 'fetch_covtype', 'silhouette_score', 'fowlkes_mallows_score', 'check_cv', 'kneighbors_graph', 'load_sample_images', 'coverage_error', 'make_scorer', 'silhouette_samples', 'get_data_home', 'fetch_california_housing', 'dump_svmlight_file', 'check_X_y', 'inplace_swap_row', 'fetch_rcv1', 'check_symmetric', 'has_fit_parameter', 'calibration_curve', 'graph_lasso', 'paired_distances', 'make_classification', 'predict', 'f_regression', 'cosine_distances', 'robust_scale', 'mutual_info_classif', 'inplace_swap_column', 'cross_validation', 'adjusted_rand_score', 'paired_euclidean_distances', 'incr_mean_variance_axis', 'mean_absolute_error', 'classification_report', 'as_float_array', 'fetch_lfw_people', 'oas', 'plot_partial_dependence', 'check_estimator', 'extract_patches_2d', 'quantile_transform', 'normalize', 'load_boston', 'mean_variance_axis', 'binarize', 'paired_cosine_distances', 'chi2', 'fetch_20newsgroups_vectorized', 'clone', 'affinity_propagation', 'shrunk_covariance', 'load_diabetes', 'scale', 'load_svmlight_files', 'minmax_scale', 'matthews_corrcoef', 'smacof', 'add_dummy_feature', 'compute_class_weight', 'make_gaussian_quantiles', 'additive_chi2_kernel', 'decision_function', 'chi2_kernel', 'make_circles', 'ndcg_score', 'make_checkerboard', 'recall_score', 'mutual_info_score', 'mean_squared_log_error', 'load_iris', 'mean_squared_error', 'precision_recall_curve'])
        self.modelCount={key: 0 for key in self.model}
        self.subModuleCount={key: 0 for key in self.subModule}
        self.functionCount={key: 0 for key in self.function}

    def putInBucket(self, key, val, context):
        if key in self.subModule:
            self.subModuleCount[key] += val
        elif key in self.model:
            self.modelCount[key] += val
        elif key in self.function:
            self.functionCount[key] += val
        else:
            self.addOutlier(key,val,context)
    
    def addOutlier(self,key,val,context):
        self.outliers.append((key,val,context))

def parseDict(mostImportedSubmoduleDict):
    b = sklearnImportBucket()
    for key, val in mostImportedSubmoduleDict.items():
        """
        There are three cases:
        a) from sklearn.x import y as z
        b) from sklearn import x
        c) import sklearn.x.y.z
        """
        if key.startswith("from sklearn."):
            s1, s2 = key.split("from sklearn.")[1].split(" import")
            for s in s1.split(","):
                # import sklearn.foo.bar.baz
                for k in s.split("."):
                    b.putInBucket(k.strip(" ()#\n\r\t\""), val, key)
            for s in s2.split(","):
                # import sklearn.foo.bar.baz
                for k in s.split("."):
                    b.putInBucket(k.split(" as ")[0].strip(" ()#\n\r\t\""), val, key)
        elif key.startswith("from sklearn import"):
            ss = key.split("from sklearn import")[1].strip().split(" as ")
            if len(ss) >= 3:
                # weird string, put it in outlier
                b.addOutlier(key,val,key)
            else:
                # from sklearn import foo,bar,baz
                for k in ss[0].split(","):
                    b.putInBucket(k.split(" as ")[0].strip(" ()#\n\r\t"), val, key)

        elif key.startswith("import sklearn."):
            ss = key.split("import sklearn.")[1].strip()
            # import sklearn.this, sklearn.that,
            for s in ss.split(","):
                # import sklearn.foo.bar.baz
                for k in s.split("."):
                    b.putInBucket(k.split(" as ")[0].strip(" ()#\n\r\t\""), val, key)
        else:
            b.addOutlier(key, val, key)
    return b